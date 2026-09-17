# ❌⭕ MinimaxXO

> Tres en Raya clásico con una IA que juega perfecto: implementa Minimax con poda alfa-beta sobre el árbol de juego completo, y su optimalidad está verificada de forma exhaustiva (no con partidas de muestra) contra las 642 partidas legales posibles. Ideal para quien quiera un ejemplo de referencia, correcto y con tests, de un juego "resuelto" jugado por una IA sin fisuras.

## Características

- **IA invencible y verificada, no solo prometida**: Minimax + poda alfa-beta explorando el árbol de juego completo (`logica/inteligencia_artificial.py`). Se probó exhaustivamente jugando contra TODAS las secuencias de movimientos legales del oponente, tanto con la IA como primer jugador como segundo: 0 derrotas en las 642 partidas posibles (569 jugando de segunda + 73 jugando de primera).
- **Interfaz gráfica con Pygame**: tablero interactivo, animaciones al colocar fichas y resaltado de la línea ganadora.
- **Menú completo**: jugar, tutorial interactivo paso a paso, estadísticas de partidas y salir.
- **Sistema de estadísticas persistente**: partidas jugadas, victorias/derrotas/empates, rachas y tiempo de juego, guardado en `datos_juego.json`.
- **Controles de teclado**: `ESC` pausa, `R` reinicia la partida, `M` vuelve al menú, `F11` pantalla completa, `F3` contador de FPS.
- **Arquitectura en capas**: `logica/` (reglas del tablero y Minimax, sin dependencias gráficas, 100% testeable) separada de `presentacion/` (todo lo relacionado con Pygame).

## Cómo usar

1. Ejecuta `python main.py`.
2. Elige **JUGAR** en el menú. Tú siempre juegas con `X` y mueves primero; la IA (`O`) responde automáticamente.
3. Haz clic en cualquier casilla vacía para colocar tu ficha. Gana quien consiga tres en línea (fila, columna o diagonal); si se llena el tablero sin ganador, es empate.
4. Contra un Minimax perfecto la única forma de no perder es jugar tú también de forma óptima — y aun así el resultado teórico es empate.

## Instalación y uso local

```bash
git clone https://github.com/Luiss2080/MinimaxXO.git
cd MinimaxXO
pip install -r requirements.txt
python main.py
```

Requiere Python 3.8+.

## Tecnologías

- **Python 3**
- **Pygame** — motor gráfico y de eventos
- **NumPy** — utilizado por la capa de presentación
- **pytest** — suite de tests de la capa de lógica

## Tests

La lógica del juego (tablero e IA) está completamente desacoplada de Pygame, así que se puede probar sin abrir ninguna ventana:

```bash
pip install pytest
pytest -v
```

La suite (17 tests) cubre:
- Detección de victoria en las 8 líneas posibles (filas, columnas, diagonales) y de empate con tablero lleno.
- Manejo correcto de estados terminales (la IA no calcula un movimiento sobre un tablero ya decidido).
- **Verificación exhaustiva de invencibilidad**: la IA se enfrenta a *todas* las secuencias de movimientos legales del oponente —no una muestra— tanto jugando de primera como de segunda, y en ningún caso pierde.

Se ejecuta automáticamente en cada push/PR vía GitHub Actions (`.github/workflows/tests.yml`).

## Licencia

MIT — ver [`LICENSE`](LICENSE).
