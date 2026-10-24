
"""Reglas de limpieza y validación de los archivos diarios de ventas.

Este módulo no importa nada de Airflow a propósito: así las reglas se pueden
probar con pytest en segundos, sin levantar Docker ni una base de datos.
"""

import csv
import json
import math
import re
from typing import Any, Optional

COLUMNAS = ["id_venta", "fecha", "region", "producto", "cantidad", "precio_unitario"]
REGIONES = {"norte", "sur", "centro"}

# Si se rechaza más del 20 % de un archivo no se carga nada de ese día
UMBRAL_RECHAZO = 0.20

# Solo dígitos 0-9. int() y float() aceptan cosas como "+3", "1_000", "1e3" o "nan"
SOLO_DIGITOS = re.compile(r"[0-9]+")
DECIMAL_CON_PUNTO = re.compile(r"[0-9]+(\.[0-9]+)?")


def leer_csv(ruta: str) -> list[dict[str, Any]]:
    """Lee el archivo y devuelve una lista de diccionarios con valores en texto.

    Si una línea trae columnas de más, lo que sobra queda en la clave
    '_sobrantes'. Si trae de menos, las columnas faltantes quedan en None.

    Rechaza encabezados faltantes, inesperados o duplicados.
    """
    # utf-8-sig tolera el BOM que agrega Excel al guardar como CSV UTF-8.
    # strict=True hace fallar el archivo si una comilla queda sin cerrar.
    with open(ruta, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(
            archivo,
            restkey="_sobrantes",
            strict=True,
        )
        encabezado = lector.fieldnames or []

        # Un encabezado duplicado puede hacer que DictReader sobrescriba
        # valores de columnas que tienen el mismo nombre.
        duplicados = sorted({
            col for col in encabezado if encabezado.count(col) > 1
        })
        if duplicados:
            raise ValueError(
                f"Columnas duplicadas en el encabezado: {', '.join(duplicados)}"
            )

        faltantes = [col for col in COLUMNAS if col not in encabezado]
        if faltantes:
            raise ValueError(
                f"Al archivo le faltan columnas: {', '.join(faltantes)}"
            )

        sobrantes = [col for col in encabezado if col not in COLUMNAS]
        if sobrantes:
            raise ValueError(
                f"Columnas que no se esperan: {', '.join(sobrantes)}"
            )

        return [dict(fila) for fila in lector]


def _texto(fila: dict[str, Any], columna: str) -> str:
    """Obtiene un campo como texto y elimina espacios en los extremos."""
    return (fila.get(columna) or "").strip()


def _entero_positivo(valor: str) -> Optional[int]:
    """Convierte un texto de dígitos en entero positivo; None si no es válido."""
    if not SOLO_DIGITOS.fullmatch(valor):
        return None

    try:
        numero = int(valor)
    except ValueError:
        # Python puede rechazar conversiones de textos con demasiados dígitos.
        return None

    return numero if numero > 0 else None


def _precio_positivo(valor: str) -> Optional[float]:
    """Convierte un decimal positivo con punto y lo redondea a dos decimales."""
    if not DECIMAL_CON_PUNTO.fullmatch(valor):
        return None

    try:
        precio = round(float(valor), 2)
    except (ValueError, OverflowError):
        return None

    # Evita aceptar infinito, NaN o valores que redondeen a cero.
    return precio if math.isfinite(precio) and precio >= 0 else None


def validar_fila(
    fila: dict[str, Any],
    fecha: str,
) -> tuple[Optional[dict[str, Any]], Optional[str]]:
    """Valida una fila.

    Devuelve (registro, None) si es válida o (None, motivo) si no lo es.
    Se reporta solamente el primer problema, respetando el orden de las reglas.
    """
    # Un precio como 45,50 sin comillas puede dividir la fila en más columnas.
    if "_sobrantes" in fila or any(
        fila.get(col) is None for col in COLUMNAS
    ):
        return None, "columnas_incorrectas"

    id_venta = _entero_positivo(_texto(fila, "id_venta"))
    if id_venta is None:
        return None, "id_invalido"

    if _texto(fila, "fecha") != fecha:
        return None, "fecha_distinta"

    region = _texto(fila, "region").lower()
    if region not in REGIONES:
        return None, "region_invalida"

    producto = _texto(fila, "producto")
    if not producto:
        return None, "producto_vacio"

    cantidad = _entero_positivo(_texto(fila, "cantidad"))
    if cantidad is None:
        return None, "cantidad_invalida"

    precio = _precio_positivo(_texto(fila, "precio_unitario"))
    if precio is None:
        return None, "precio_invalido"

    # Evita producir totales infinitos por cantidades o productos extremos.
    try:
        total = round(cantidad * precio, 2)
    except (OverflowError, ValueError):
        return None, "precio_invalido"

    if not math.isfinite(total):
        return None, "precio_invalido"

    registro = {
        "id_venta": id_venta,
        "fecha": fecha,
        "region": region.capitalize(),
        "producto": producto.capitalize(),
        "cantidad": cantidad,
        "precio_unitario": precio,
        "total": total,
    }
    return registro, None


def separar_ventas(
    filas: list[dict[str, Any]],
    fecha: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separa las filas en (limpias, rechazadas).

    Si un id_venta se repite, las apariciones posteriores se rechazan como
    id_duplicado, incluso si la primera aparición se rechazó por otro motivo.

    La línea reportada es el número de registro CSV, contando el encabezado
    como línea 1; no necesariamente coincide con la línea física del archivo
    cuando existen campos multilínea entre comillas.
    """
    limpias = []
    rechazadas = []
    ids_vistos = set()

    for linea, fila in enumerate(filas, start=2):
        registro, motivo = validar_fila(fila, fecha)

        # El duplicado se evalúa después de las columnas y del id.
        # "070001" y "70001" se consideran el mismo identificador.
        id_venta = _entero_positivo(_texto(fila, "id_venta"))

        if (
            motivo not in ("columnas_incorrectas", "id_invalido")
            and id_venta in ids_vistos
        ):
            registro, motivo = None, "id_duplicado"

        if id_venta is not None:
            ids_vistos.add(id_venta)

        if registro is not None:
            limpias.append(registro)
        else:
            rechazadas.append({
                "linea": linea,
                "id_venta": _texto(fila, "id_venta") or None,
                "motivo": motivo,
                "fila_original": json.dumps(fila, ensure_ascii=False),
            })

    return limpias, rechazadas


def revisar_calidad(
    total_leidas: int,
    total_rechazadas: int,
    umbral: float = UMBRAL_RECHAZO,
) -> float:
    """Devuelve la tasa de rechazo o lanza ValueError si el archivo no sirve.

    Los contadores deben ser enteros no negativos, los rechazos no pueden
    superar las filas leídas y el umbral debe estar entre 0 y 1.
    """
    # bool es una subclase de int en Python, pero no es válido como contador.
    if (
        not isinstance(total_leidas, int)
        or isinstance(total_leidas, bool)
        or not isinstance(total_rechazadas, int)
        or isinstance(total_rechazadas, bool)
    ):
        raise ValueError("Los contadores deben ser enteros")

    if total_leidas < 0 or total_rechazadas < 0:
        raise ValueError("Los contadores no pueden ser negativos")

    if total_rechazadas > total_leidas:
        raise ValueError("Las filas rechazadas no pueden superar las leídas")

    if total_leidas == 0:
        raise ValueError("El archivo no trae ninguna venta")

    if (
        not isinstance(umbral, (int, float))
        or isinstance(umbral, bool)
        or not math.isfinite(umbral)
        or not 0 <= umbral <= 1
    ):
        raise ValueError("El umbral debe ser un número entre 0 y 1")

    tasa = total_rechazadas / total_leidas

    if tasa > umbral:
        raise ValueError(
            f"Se rechazó el {tasa:.1%} de las filas y el máximo es {umbral:.0%}. "
            "No se carga nada de esta fecha."
        )

    return tasa

