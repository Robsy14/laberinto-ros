"""Mapa lógico del laberinto 7x7 para la Etapa 0.

Valores de cada celda:
    0 = libre
    1 = pared
    2 = inicio (S)
    3 = salida (G)
"""

import numpy as np

MAZE = np.array([
    [2, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 3],
])

START = tuple(int(v) for v in np.argwhere(MAZE == 2)[0])
GOAL = tuple(int(v) for v in np.argwhere(MAZE == 3)[0])


def is_free(cell):
    """Indica si una celda (fila, columna) es transitable."""
    r, c = cell
    if not (0 <= r < MAZE.shape[0] and 0 <= c < MAZE.shape[1]):
        return False
    return bool(MAZE[r, c] != 1)


def neighbors(cell):
    """Vecinos transitables en 4 direcciones."""
    r, c = cell
    candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    return [n for n in candidates if is_free(n)]


def print_maze():
    """Imprime el laberinto en texto, con S, G, paredes y libres."""
    symbols = {0: " . ", 1: " # ", 2: " S ", 3: " G "}
    for row in MAZE:
        print("".join(symbols[int(v)] for v in row))


if __name__ == "__main__":
    print(f"Inicio: {START}  |  Salida: {GOAL}")
    print_maze()
