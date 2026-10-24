
"""ETL diario de ventas: CSV de las tiendas -> validación -> PostgreSQL.

Se dispara a mano con el parámetro `fecha` (AAAA-MM-DD). Cada corrida reemplaza
solo los datos de esa fecha, así que repetirla no duplica filas.
"""

import logging
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import Param, dag, get_current_context, task

from ventas.reglas import leer_csv, revisar_calidad, separar_ventas


logger = logging.getLogger(__name__)

CARPETA_ENTRADA = Path(
    os.environ.get("VENTAS_CARPETA_ENTRADA", "/opt/airflow/data/entrada")
)
CONEXION = "postgres_datapath"

CREAR_TABLAS = """
CREATE TABLE IF NOT EXISTS ventas_limpias (
    id_venta        INTEGER PRIMARY KEY,
    fecha           DATE NOT NULL,
    region          TEXT NOT NULL,
    producto        TEXT NOT NULL,
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL CHECK (precio_unitario > 0),
    total           NUMERIC(12, 2) NOT NULL,
    cargado_en      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ventas_rechazadas (
    fecha_archivo DATE NOT NULL,
    linea         INTEGER NOT NULL,
    id_venta      TEXT,
    motivo        TEXT NOT NULL,
    fila_original TEXT NOT NULL,
    PRIMARY KEY (fecha_archivo, linea)
);

CREATE TABLE IF NOT EXISTS resumen_ventas_diario (
    fecha       DATE NOT NULL,
    region      TEXT NOT NULL,
    num_ventas  INTEGER NOT NULL,
    unidades    INTEGER NOT NULL,
    monto_total NUMERIC(14, 2) NOT NULL,
    PRIMARY KEY (fecha, region)
);
"""


@dag(
    dag_id="etl_ventas_diarias",
    description="Carga diaria de ventas desde CSV a PostgreSQL",
    start_date=datetime(2026, 10, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    params={
        "fecha": Param(
            "2026-10-05",
            type="string",
            format="date",
            description="Fecha del archivo a procesar (AAAA-MM-DD)",
        ),
    },
    default_args={
        "owner": "equipo-datos",
        "retries": 1,
        "retry_delay": timedelta(seconds=15),
    },
    tags=["laboratorio", "ventas", "etl"],
)
def etl_ventas_diarias():

    @task
    def extraer():
        fecha = get_current_context()["params"]["fecha"]

        # Validación defensiva del parámetro.
        date.fromisoformat(fecha)

        ruta = CARPETA_ENTRADA / f"ventas_{fecha}.csv"

        if not ruta.is_file():
            raise FileNotFoundError(f"No existe el archivo {ruta}")

        filas = leer_csv(ruta)

        logger.info(
            "Se leyeron %s filas del archivo %s",
            len(filas),
            ruta.name,
        )

        return {"fecha": fecha, "filas": filas}

    @task
    def transformar(datos):
        limpias, rechazadas = separar_ventas(
            datos["filas"],
            datos["fecha"],
        )

        logger.info(
            "Fecha %s: %s válidas y %s rechazadas",
            datos["fecha"],
            len(limpias),
            len(rechazadas),
        )

        for fila in rechazadas:
            logger.warning(
                "Fecha %s, línea %s: %s",
                datos["fecha"],
                fila["linea"],
                fila["motivo"],
            )

        return {
            "fecha": datos["fecha"],
            "leidas": len(datos["filas"]),
            "limpias": limpias,
            "rechazadas": rechazadas,
        }

    # Un archivo con problemas de calidad no se arregla reintentando.
    @task(retries=0)
    def validar_calidad(resultado):
        tasa = revisar_calidad(
            resultado["leidas"],
            len(resultado["rechazadas"]),
        )

        logger.info(
            "Fecha %s: tasa de rechazo %.1f%%",
            resultado["fecha"],
            tasa * 100,
        )

        return resultado

    @task
    def cargar(resultado):
        fecha = date.fromisoformat(resultado["fecha"])
        limpias = resultado["limpias"]
        rechazadas = resultado["rechazadas"]

        filas_limpias = [
            (
                v["id_venta"],
                fecha,
                v["region"],
                v["producto"],
                v["cantidad"],
                v["precio_unitario"],
                v["total"],
            )
            for v in limpias
        ]

        filas_rechazadas = [
            (
                fecha,
                r["linea"],
                r["id_venta"],
                r["motivo"],
                r["fila_original"],
            )
            for r in rechazadas
        ]

        hook = PostgresHook(postgres_conn_id=CONEXION)
        conn = hook.get_conn()

        try:
            # La eliminación, la inserción y las verificaciones se ejecutan
            # dentro de una única transacción.
            with conn:
                with conn.cursor() as cur:
                    cur.execute(CREAR_TABLAS)

                    # Reemplaza únicamente los registros de la fecha procesada.
                    cur.execute(
                        "DELETE FROM ventas_limpias WHERE fecha = %s",
                        (fecha,),
                    )
                    cur.execute(
                        "DELETE FROM ventas_rechazadas "
                        "WHERE fecha_archivo = %s",
                        (fecha,),
                    )

                    if filas_limpias:
                        cur.executemany(
                            """
                            INSERT INTO ventas_limpias (
                                id_venta,
                                fecha,
                                region,
                                producto,
                                cantidad,
                                precio_unitario,
                                total
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            filas_limpias,
                        )

                    if filas_rechazadas:
                        cur.executemany(
                            """
                            INSERT INTO ventas_rechazadas (
                                fecha_archivo,
                                linea,
                                id_venta,
                                motivo,
                                fila_original
                            )
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            filas_rechazadas,
                        )

                    # Verifica las ventas limpias cargadas.
                    cur.execute(
                        "SELECT COUNT(*) FROM ventas_limpias WHERE fecha = %s",
                        (fecha,),
                    )
                    en_tabla = cur.fetchone()[0]

                    if en_tabla != len(limpias):
                        raise ValueError(
                            f"Se esperaban {len(limpias)} ventas limpias "
                            f"y hay {en_tabla}"
                        )

                    # Verifica también los registros rechazados.
                    cur.execute(
                        """
                        SELECT COUNT(*)
                        FROM ventas_rechazadas
                        WHERE fecha_archivo = %s
                        """,
                        (fecha,),
                    )
                    rechazadas_en_tabla = cur.fetchone()[0]

                    if rechazadas_en_tabla != len(rechazadas):
                        raise ValueError(
                            f"Se esperaban {len(rechazadas)} registros "
                            f"rechazados y hay {rechazadas_en_tabla}"
                        )

        except Exception:
            logger.exception(
                "Error al cargar las ventas de la fecha %s. "
                "La transacción se revertirá.",
                fecha,
            )
            raise

        finally:
            conn.close()

        logger.info(
            "Fecha %s: %s ventas cargadas y %s rechazadas",
            fecha,
            len(limpias),
            len(rechazadas),
        )

        return {
            "fecha": resultado["fecha"],
            "cargadas": len(limpias),
            "rechazadas": len(rechazadas),
        }

    @task
    def actualizar_resumen(carga):
        fecha = date.fromisoformat(carga["fecha"])

        hook = PostgresHook(postgres_conn_id=CONEXION)
        conn = hook.get_conn()

        try:
            # La eliminación y reconstrucción del resumen se confirman
            # conjuntamente. Si falla una sentencia, se revierte la transacción.
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        DELETE FROM resumen_ventas_diario
                        WHERE fecha = %s
                        """,
                        (fecha,),
                    )

                    cur.execute(
                        """
                        INSERT INTO resumen_ventas_diario (
                            fecha,
                            region,
                            num_ventas,
                            unidades,
                            monto_total
                        )
                        SELECT
                            fecha,
                            region,
                            COUNT(*),
                            SUM(cantidad),
                            SUM(total)
                        FROM ventas_limpias
                        WHERE fecha = %s
                        GROUP BY fecha, region
                        """,
                        (fecha,),
                    )

                    cur.execute(
                        """
                        SELECT
                            region,
                            num_ventas,
                            unidades,
                            monto_total
                        FROM resumen_ventas_diario
                        WHERE fecha = %s
                        ORDER BY region
                        """,
                        (fecha,),
                    )

                    filas = cur.fetchall()

        except Exception:
            logger.exception(
                "Error al actualizar el resumen de ventas de %s",
                fecha,
            )
            raise

        finally:
            conn.close()

        for region, num_ventas, unidades, monto in filas:
            logger.info(
                "%s | %s ventas | %s unidades | monto: %s",
                region,
                num_ventas,
                unidades,
                monto,
            )

        logger.info(
            "Resumen de la fecha %s actualizado: %s regiones",
            fecha,
            len(filas),
        )

        return len(filas)

    actualizar_resumen(cargar(validar_calidad(transformar(extraer()))))


etl_ventas_diarias()
