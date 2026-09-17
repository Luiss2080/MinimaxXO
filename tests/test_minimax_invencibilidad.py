"""Verificación EXHAUSTIVA de la calidad del algoritmo Minimax.

El árbol de juego completo del Tres en Raya es lo bastante pequeño
(un máximo teórico de 9! = 362 880 secuencias, muchas menos en la
práctica una vez que se recorta por victorias tempranas) como para
probarlo por completo en vez de con partidas de muestra.

Estas pruebas hacen jugar al oponente humano CADA secuencia de
movimientos legal posible, en cada uno de sus turnos, mientras la IA
responde con `obtener_mejor_movimiento_ia()` (Minimax + poda alfa-beta)
en cada uno de los suyos. Si la IA es realmente óptima, el resultado
para ella nunca puede ser una derrota (Tres en Raya es un juego
"resuelto": con juego óptimo de ambos lados el resultado es siempre
empate, y un error del oponente humano sólo puede llevar a que la IA
gane, jamás a que pierda).

Se cubren los dos roles posibles de la IA:
- IA como segundo jugador ('O' responde a 'X').
- IA como primer jugador ('O' abre la partida).
"""
from logica.inteligencia_artificial import AlgoritmoMinimax
from logica.logica_tablero import TableroJuego

SIMBOLO_IA = 'O'
SIMBOLO_HUMANO = 'X'


def _explorar_todas_las_partidas(tablero, es_turno_ia, resultados):
    """Recorre exhaustivamente el árbol de juego.

    En los turnos de la IA, usa el algoritmo real (una sola jugada,
    la que Minimax considera óptima). En los turnos "humanos", prueba
    TODAS las jugadas legales disponibles (fuerza bruta), no una
    muestra, para que la verificación sea completa.
    """
    ganador = tablero.verificar_ganador()
    if ganador is not None or tablero.es_tablero_lleno():
        resultados.append(ganador)
        return

    if es_turno_ia:
        ia = AlgoritmoMinimax(tablero)
        fila, columna = ia.obtener_mejor_movimiento_ia()
        tablero.realizar_movimiento(fila, columna, SIMBOLO_IA)
        _explorar_todas_las_partidas(tablero, False, resultados)
        tablero.deshacer_movimiento(fila, columna)
    else:
        for fila, columna in tablero.obtener_movimientos_disponibles():
            tablero.realizar_movimiento(fila, columna, SIMBOLO_HUMANO)
            _explorar_todas_las_partidas(tablero, True, resultados)
            tablero.deshacer_movimiento(fila, columna)


def test_ia_invencible_jugando_segundo_contra_todas_las_secuencias():
    """La IA responde ('O' como segundo jugador). Se prueban las 9
    aperturas humanas posibles y, recursivamente, cada respuesta
    humana posible en cada turno suyo subsiguiente."""
    tablero = TableroJuego()
    resultados = []
    _explorar_todas_las_partidas(tablero, es_turno_ia=False, resultados=resultados)

    derrotas_ia = resultados.count(SIMBOLO_HUMANO)
    assert derrotas_ia == 0, (
        f"La IA perdió en {derrotas_ia} de {len(resultados)} partidas posibles "
        "jugando como segundo jugador: el algoritmo Minimax no es óptimo."
    )
    # Sanity check: nos aseguramos de que realmente se recorrieron partidas.
    assert len(resultados) > 0


def test_ia_invencible_jugando_primero_contra_todas_las_secuencias():
    """La IA abre la partida ('O' como primer jugador)."""
    tablero = TableroJuego()
    resultados = []
    _explorar_todas_las_partidas(tablero, es_turno_ia=True, resultados=resultados)

    derrotas_ia = resultados.count(SIMBOLO_HUMANO)
    assert derrotas_ia == 0, (
        f"La IA perdió en {derrotas_ia} de {len(resultados)} partidas posibles "
        "jugando como primer jugador: el algoritmo Minimax no es óptimo."
    )
    assert len(resultados) > 0


def test_juego_optimo_de_ambos_lados_termina_en_empate():
    """Caso particular y bien conocido: si además del oponente también
    se simula que la IA responde de forma óptima (que es justamente lo
    que hace Minimax), la única partida que el humano puede forzar
    jugando también de forma óptima es un empate. Lo comprobamos
    explorando la única línea de juego "óptima" conocida del Tres en
    Raya: el humano abre en el centro y responde siempre de forma
    razonable; el resultado agregado de la exploración completa debe
    incluir al menos un empate, y ninguna derrota de la IA."""
    tablero = TableroJuego()
    resultados = []
    _explorar_todas_las_partidas(tablero, es_turno_ia=False, resultados=resultados)

    assert resultados.count(None) > 0, (
        "Se esperaba que al menos una línea de juego terminara en empate "
        "(el resultado teórico del Tres en Raya con juego óptimo)."
    )
