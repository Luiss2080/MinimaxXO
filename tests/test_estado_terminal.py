"""Verifica que la IA maneje correctamente los estados terminales del
tablero: no debe intentar calcular un movimiento cuando la partida ya
está decidida (alguien ganó) o cuando el tablero está lleno (empate).
"""
from logica.inteligencia_artificial import AlgoritmoMinimax
from logica.logica_tablero import TableroJuego


def _tablero_desde_filas(filas):
    tablero = TableroJuego()
    tablero.matriz_tablero = [fila[:] for fila in filas]
    return tablero


def test_ia_no_juega_sobre_tablero_ya_ganado_por_humano():
    tablero = _tablero_desde_filas([
        ['X', 'X', 'X'],
        ['O', 'O', ' '],
        [' ', ' ', ' '],
    ])
    assert tablero.verificar_ganador() == 'X'

    ia = AlgoritmoMinimax(tablero)
    assert ia.obtener_mejor_movimiento_ia() is None


def test_ia_no_juega_sobre_tablero_ya_ganado_por_ella_misma():
    tablero = _tablero_desde_filas([
        ['O', 'O', 'O'],
        ['X', 'X', ' '],
        [' ', ' ', ' '],
    ])
    assert tablero.verificar_ganador() == 'O'

    ia = AlgoritmoMinimax(tablero)
    assert ia.obtener_mejor_movimiento_ia() is None


def test_ia_no_juega_sobre_tablero_lleno_en_empate():
    tablero = _tablero_desde_filas([
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X'],
    ])
    assert tablero.verificar_ganador() is None
    assert tablero.es_tablero_lleno() is True

    ia = AlgoritmoMinimax(tablero)
    assert ia.obtener_mejor_movimiento_ia() is None
