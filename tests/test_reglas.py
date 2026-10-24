
import csv

import pytest

from ventas.reglas import (
    UMBRAL_RECHAZO,
    leer_csv,
    revisar_calidad,
    separar_ventas,
    validar_fila,
)

FECHA = "2026-10-05"
ENCABEZADO = "id_venta,fecha,region,producto,cantidad,precio_unitario\n"


def fila(**cambios):
    """Construye una fila válida y permite sobrescribir campos para las pruebas."""
    base = {
        "id_venta": "70001",
        "fecha": FECHA,
        "region": "norte",
        "producto": "Mouse",
        "cantidad": "3",
        "precio_unitario": "45.50",
    }
    base.update(cambios)
    return base


# --- validar_fila -------------------------------------------------------


def test_fila_valida_calcula_el_total():
    registro, motivo = validar_fila(fila(), FECHA)

    assert motivo is None
    assert registro is not None
    assert registro["id_venta"] == 70001
    assert registro["cantidad"] == 3
    assert registro["precio_unitario"] == 45.50
    assert registro["total"] == pytest.approx(136.50)


def test_normaliza_region_y_producto():
    registro, motivo = validar_fila(
        fila(region="  SUR ", producto=" AURICULARES"),
        FECHA,
    )

    assert motivo is None
    assert registro is not None
    assert registro["region"] == "Sur"
    assert registro["producto"] == "Auriculares"


@pytest.mark.parametrize(
    "cambios, motivo_esperado",
    [
        ({"id_venta": ""}, "id_invalido"),
        ({"id_venta": "abc"}, "id_invalido"),
        ({"id_venta": "-5"}, "id_invalido"),
        ({"id_venta": "+5"}, "id_invalido"),
        ({"id_venta": "1_000"}, "id_invalido"),
        ({"id_venta": "0"}, "id_invalido"),
        ({"fecha": "2026-10-04"}, "fecha_distinta"),
        ({"region": "Lima"}, "region_invalida"),
        ({"region": ""}, "region_invalida"),
        ({"producto": "   "}, "producto_vacio"),
        ({"cantidad": ""}, "cantidad_invalida"),
        ({"cantidad": "0"}, "cantidad_invalida"),
        ({"cantidad": "-2"}, "cantidad_invalida"),
        ({"cantidad": "dos"}, "cantidad_invalida"),
        ({"cantidad": "1.5"}, "cantidad_invalida"),
        ({"cantidad": "+3"}, "cantidad_invalida"),
        ({"cantidad": "1_000"}, "cantidad_invalida"),
        ({"precio_unitario": ""}, "precio_invalido"),
        ({"precio_unitario": "0"}, "precio_invalido"),
        ({"precio_unitario": "0.00"}, "precio_invalido"),
        ({"precio_unitario": "0.004"}, "precio_invalido"),
        ({"precio_unitario": "45,50"}, "precio_invalido"),
        ({"precio_unitario": "nan"}, "precio_invalido"),
        ({"precio_unitario": "inf"}, "precio_invalido"),
        ({"precio_unitario": "1e3"}, "precio_invalido"),
        ({"precio_unitario": "-45.50"}, "precio_invalido"),
    ],
)
def test_motivos_de_rechazo(cambios, motivo_esperado):
    registro, motivo = validar_fila(fila(**cambios), FECHA)

    assert registro is None
    assert motivo == motivo_esperado


@pytest.mark.parametrize(
    "columna",
    ["id_venta", "fecha", "region", "producto", "cantidad", "precio_unitario"],
)
def test_fila_con_columna_ausente(columna):
    datos = fila()
    datos[columna] = None

    registro, motivo = validar_fila(datos, FECHA)

    assert registro is None
    assert motivo == "columnas_incorrectas"


def test_fila_con_sobrantes():
    datos = fila()
    datos["_sobrantes"] = ["dato_extra"]

    registro, motivo = validar_fila(datos, FECHA)

    assert registro is None
    assert motivo == "columnas_incorrectas"


def test_precio_sin_decimales_es_valido():
    registro, motivo = validar_fila(
        fila(precio_unitario="699"),
        FECHA,
    )

    assert motivo is None
    assert registro is not None
    assert registro["precio_unitario"] == 699.0


def test_precio_redondeado_a_dos_decimales():
    registro, motivo = validar_fila(
        fila(precio_unitario="45.567"),
        FECHA,
    )

    assert motivo is None
    assert registro is not None
    assert registro["precio_unitario"] == 45.57


def test_se_reporta_el_primer_problema():
    # La región se valida antes que el producto y la cantidad.
    _, motivo = validar_fila(
        fila(region="Oeste", cantidad="dos"),
        FECHA,
    )

    assert motivo == "region_invalida"


def test_id_invalido_tiene_prioridad_sobre_fecha():
    _, motivo = validar_fila(
        fila(id_venta="-1", fecha="2026-10-04"),
        FECHA,
    )

    assert motivo == "id_invalido"


def test_fecha_distinta_tiene_prioridad_sobre_region():
    _, motivo = validar_fila(
        fila(fecha="2026-10-04", region="Oeste"),
        FECHA,
    )

    assert motivo == "fecha_distinta"


def test_cantidad_invalida_tiene_prioridad_sobre_precio():
    _, motivo = validar_fila(
        fila(cantidad="0", precio_unitario="abc"),
        FECHA,
    )

    assert motivo == "cantidad_invalida"


def test_total_extremo_no_genera_registro_no_finito():
    # Este caso verifica el manejo defensivo de cantidades extremas.
    datos = fila(cantidad="9" * 1000)

    registro, motivo = validar_fila(datos, FECHA)

    assert registro is None
    assert motivo == "precio_invalido"


# --- separar_ventas -----------------------------------------------------


def test_duplicado_conserva_la_primera_aparicion():
    filas = [
        fila(),
        fila(cantidad="9"),
        fila(id_venta="70002"),
    ]

    limpias, rechazadas = separar_ventas(filas, FECHA)

    assert [v["id_venta"] for v in limpias] == [70001, 70002]
    assert limpias[0]["cantidad"] == 3
    assert len(rechazadas) == 1
    assert rechazadas[0]["motivo"] == "id_duplicado"


def test_duplicado_aunque_la_primera_aparicion_se_rechace():
    _, rechazadas = separar_ventas(
        [fila(cantidad=""), fila()],
        FECHA,
    )

    assert [r["motivo"] for r in rechazadas] == [
        "cantidad_invalida",
        "id_duplicado",
    ]


def test_duplicado_se_revisa_antes_que_otros_errores():
    _, rechazadas = separar_ventas(
        [fila(), fila(region="Lima")],
        FECHA,
    )

    assert rechazadas[0]["motivo"] == "id_duplicado"


def test_ids_se_comparan_como_numero():
    _, rechazadas = separar_ventas(
        [fila(id_venta="70001"), fila(id_venta="070001")],
        FECHA,
    )

    assert rechazadas[0]["motivo"] == "id_duplicado"


def test_columnas_incorrectas_le_gana_al_duplicado():
    _, rechazadas = separar_ventas(
        [fila(), fila(precio_unitario=None)],
        FECHA,
    )

    assert rechazadas[0]["motivo"] == "columnas_incorrectas"


def test_id_invalido_no_se_considera_duplicado():
    _, rechazadas = separar_ventas(
        [fila(id_venta="abc"), fila(id_venta="abc")],
        FECHA,
    )

    assert [r["motivo"] for r in rechazadas] == [
        "id_invalido",
        "id_invalido",
    ]


def test_rechazadas_guardan_linea_y_fila_original():
    filas = [
        fila(),
        fila(id_venta="70002", region="Lima"),
    ]

    _, rechazadas = separar_ventas(filas, FECHA)

    assert rechazadas[0]["linea"] == 3
    assert rechazadas[0]["id_venta"] == "70002"
    assert "Lima" in rechazadas[0]["fila_original"]


def test_rechazadas_guardan_fila_original_completa():
    datos = fila(id_venta="70002", region="Lima")

    _, rechazadas = separar_ventas([datos], FECHA)

    assert len(rechazadas) == 1
    assert rechazadas[0]["fila_original"] == (
        '{"id_venta": "70002", "fecha": "2026-10-05", '
        '"region": "Lima", "producto": "Mouse", '
        '"cantidad": "3", "precio_unitario": "45.50"}'
    )


def test_ningun_registro_se_pierde():
    filas = [
        fila(),
        fila(id_venta=""),
        fila(id_venta="70003", cantidad="0"),
        fila(),
    ]

    limpias, rechazadas = separar_ventas(filas, FECHA)

    assert len(limpias) + len(rechazadas) == len(filas)


def test_listas_vacias_separan_sin_error():
    limpias, rechazadas = separar_ventas([], FECHA)

    assert limpias == []
    assert rechazadas == []


# --- revisar_calidad ----------------------------------------------------


def test_calidad_acepta_hasta_el_umbral():
    assert revisar_calidad(10, 2) == pytest.approx(0.20)
    assert revisar_calidad(100, 20) == pytest.approx(UMBRAL_RECHAZO)
    assert revisar_calidad(46, 5) < UMBRAL_RECHAZO


def test_calidad_rechaza_justo_sobre_el_umbral():
    with pytest.raises(ValueError, match="No se carga nada"):
        revisar_calidad(100, 21)


def test_calidad_rechaza_sobre_el_umbral():
    with pytest.raises(ValueError):
        revisar_calidad(41, 24)


def test_calidad_rechaza_archivo_vacio():
    with pytest.raises(ValueError, match="no trae ninguna venta"):
        revisar_calidad(0, 0)


@pytest.mark.parametrize(
    "total_leidas,total_rechazadas,umbral",
    [
        (-1, 0, 0.20),
        (10, -1, 0.20),
        (10, 11, 0.20),
        (10, 2, -0.10),
        (10, 2, 1.10),
        (10, 2, float("nan")),
        (10, 2, float("inf")),
        (10, 2, True),
        (True, 0, 0.20),
        (10, False, 0.20),
        (10.5, 2, 0.20),
    ],
)
def test_calidad_rechaza_parametros_invalidos(
    total_leidas,
    total_rechazadas,
    umbral,
):
    with pytest.raises(ValueError):
        revisar_calidad(total_leidas, total_rechazadas, umbral)


def test_calidad_acepta_cero_rechazos():
    assert revisar_calidad(100, 0) == 0.0


def test_calidad_acepta_umbral_cero_sin_rechazos():
    assert revisar_calidad(10, 0, umbral=0) == 0.0


def test_calidad_rechaza_con_umbral_cero_y_un_rechazo():
    with pytest.raises(ValueError):
        revisar_calidad(10, 1, umbral=0)


def test_calidad_acepta_umbral_uno():
    assert revisar_calidad(10, 10, umbral=1) == 1.0


# --- leer_csv -----------------------------------------------------------


def test_leer_csv_exige_las_columnas(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        "id_venta,fecha,region,producto,cantidad\n"
        "1,2026-10-05,norte,Mouse,2\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="precio_unitario"):
        leer_csv(ruta)


def test_leer_csv_respeta_valores_entre_comillas(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        ENCABEZADO + '1,2026-10-05,sur,Mouse,2,"45,50"\n',
        encoding="utf-8",
    )

    filas = leer_csv(ruta)

    assert len(filas) == 1
    assert filas[0]["precio_unitario"] == "45,50"


def test_coma_sin_comillas_no_pasa_con_otro_precio(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        ENCABEZADO + "1,2026-10-05,sur,Mouse,2,45,50\n",
        encoding="utf-8",
    )

    limpias, rechazadas = separar_ventas(leer_csv(ruta), FECHA)

    assert limpias == []
    assert rechazadas[0]["motivo"] == "columnas_incorrectas"


def test_leer_csv_tolera_el_bom_de_excel(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        ENCABEZADO + "1,2026-10-05,sur,Mouse,2,45.50\n",
        encoding="utf-8-sig",
    )

    assert leer_csv(ruta)[0]["id_venta"] == "1"


def test_leer_csv_rechaza_columnas_de_mas_en_el_encabezado(tmp_path):
    ruta = tmp_path / "ventas.csv"

    contenido = (
        ENCABEZADO.strip()
        + ",obs\n"
        + "1,2026-10-05,sur,Mouse,2,45,50\n"
    )
    ruta.write_text(contenido, encoding="utf-8")

    with pytest.raises(ValueError, match="obs"):
        leer_csv(ruta)


def test_leer_csv_rechaza_encabezados_duplicados(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        "id_venta,fecha,region,producto,cantidad,precio_unitario,region\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicadas"):
        leer_csv(ruta)


def test_leer_csv_falla_con_una_comilla_sin_cerrar(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        ENCABEZADO
        + '1,2026-10-05,sur,"Mouse,2,45.50\n'
        + "2,2026-10-05,sur,Mouse,1,45.50\n",
        encoding="utf-8",
    )

    with pytest.raises(csv.Error):
        leer_csv(ruta)


def test_leer_csv_devuelve_lista_vacia_si_solo_hay_encabezado(tmp_path):
    ruta = tmp_path / "ventas.csv"
    ruta.write_text(ENCABEZADO, encoding="utf-8")

    assert leer_csv(ruta) == []


def test_leer_csv_conserva_columnas_faltantes_como_none(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        ENCABEZADO + "1,2026-10-05,sur,Mouse,2\n",
        encoding="utf-8",
    )

    filas = leer_csv(ruta)

    assert filas[0]["precio_unitario"] is None


def test_leer_csv_conserva_columnas_sobrantes_en_restkey(tmp_path):
    ruta = tmp_path / "ventas.csv"

    ruta.write_text(
        ENCABEZADO + "1,2026-10-05,sur,Mouse,2,45.50,extra\n",
        encoding="utf-8",
    )

    filas = leer_csv(ruta)

    assert filas[0]["_sobrantes"] == ["extra"]
