"""Pruebas unitarias de la lógica de tablero: detección de victoria en
las 8 líneas posibles, empate y estados de tablero lleno/vacío."""
import pytest

from logica.logica_tablero import TableroJuego


def _tablero_desde_filas(filas):
    tablero = TableroJuego()
    tablero.matriz_tablero = [fila[:] for fila in filas]
    return tablero


@pytest.mark.parametrize("filas, ganador_esperado", [
    # Filas
    ([['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']], 'X'),
    ([[' ', ' ', ' '], ['O', 'O', 'O'], [' ', ' ', ' ']], 'O'),
    ([[' ', ' ', ' '], [' ', ' ', ' '], ['X', 'X', 'X']], 'X'),
    # Columnas
    ([['O', ' ', ' '], ['O', ' ', ' '], ['O', ' ', ' ']], 'O'),
    ([[' ', 'X', ' '], [' ', 'X', ' '], [' ', 'X', ' ']], 'X'),
    ([[' ', ' ', 'O'], [' ', ' ', 'O'], [' ', ' ', 'O']], 'O'),
    # Diagonales
    ([['X', ' ', ' '], [' ', 'X', ' '], [' ', ' ', 'X']], 'X'),
    ([[' ', ' ', 'O'], [' ', 'O', ' '], ['O', ' ', ' ']], 'O'),
])
def test_detecta_victoria_en_cada_una_de_las_8_lineas(filas, ganador_esperado):
    tablero = _tablero_desde_filas(filas)
    assert tablero.verificar_ganador() == ganador_esperado


def test_tablero_vacio_no_tiene_ganador():
    tablero = TableroJuego()
    assert tablero.verificar_ganador() is None
    assert tablero.es_tablero_lleno() is False
    assert tablero.es_empate() is False
    assert len(tablero.obtener_movimientos_disponibles()) == 9


def test_tablero_lleno_sin_ganador_es_empate():
    tablero = _tablero_desde_filas([
        ['X', 'O', 'X'],
        ['X', 'O', 'O'],
        ['O', 'X', 'X'],
    ])
    assert tablero.verificar_ganador() is None
    assert tablero.es_tablero_lleno() is True
    assert tablero.es_empate() is True
    assert tablero.obtener_movimientos_disponibles() == []


def test_tablero_lleno_con_ganador_no_es_empate():
    """Un tablero puede llenarse completamente y aun así tener un
    ganador (la última ficha colocada puede completar la línea)."""
    tablero = _tablero_desde_filas([
        ['X', 'X', 'X'],
        ['O', 'O', 'X'],
        ['X', 'O', 'O'],
    ])
    assert tablero.verificar_ganador() == 'X'
    assert tablero.es_tablero_lleno() is True
    assert tablero.es_empate() is False


def test_realizar_movimiento_en_celda_ocupada_falla():
    tablero = TableroJuego()
    assert tablero.realizar_movimiento(1, 1, 'X') is True
    assert tablero.realizar_movimiento(1, 1, 'O') is False
    # La celda conserva el símbolo original
    assert tablero.matriz_tablero[1][1] == 'X'


def test_deshacer_movimiento_libera_la_celda():
    tablero = TableroJuego()
    tablero.realizar_movimiento(0, 0, 'X')
    tablero.deshacer_movimiento(0, 0)
    assert tablero.matriz_tablero[0][0] == ' '
    assert tablero.es_posicion_valida(0, 0) is True


def test_reiniciar_tablero_restaura_estado_inicial():
    tablero = TableroJuego()
    tablero.realizar_movimiento(0, 0, 'X')
    tablero.realizar_movimiento(1, 1, 'O')
    tablero.reiniciar_tablero()
    assert tablero.verificar_ganador() is None
    assert len(tablero.obtener_movimientos_disponibles()) == 9
    assert tablero.jugador_actual == tablero.simbolo_jugador_humano
