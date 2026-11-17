"""Generador de laberintos con bucles para comparar planificadores (Etapa 0).

Crea un laberinto perfecto (un solo camino entre dos celdas cualesquiera) con
búsqueda en profundidad y después abre algunas paredes internas para crear
caminos alternativos.

n es el número de celdas por lado. La matriz resultante mide 2n+1 por 2n+1,
porque las paredes también ocupan una celda de la cuadrícula.
"""

import numpy as np


def generar(n, semilla, p_bucle=0.10):
    rng = np.random.default_rng(semilla)
    size = 2 * n + 1
    g = np.ones((size, size), dtype=int)

    visitado = np.zeros((n, n), dtype=bool)
    visitado[0, 0] = True
    g[1, 1] = 0
    pila = [(0, 0)]

    while pila:
        i, j = pila[-1]
        vecinos = [(a, b) for a, b in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
                   if 0 <= a < n and 0 <= b < n and not visitado[a, b]]
        if not vecinos:
            pila.pop()
            continue
        a, b = vecinos[rng.integers(len(vecinos))]
        visitado[a, b] = True
        g[i + a + 1, j + b + 1] = 0  # pared que separa ambas celdas
        g[2 * a + 1, 2 * b + 1] = 0  # celda vecina
        pila.append((a, b))

    # Abrir paredes que separan dos celdas para crear bucles
    for r in range(1, size - 1):
        for c in range(1, size - 1):
            separa_celdas = (r % 2 == 0) != (c % 2 == 0)
            if separa_celdas and g[r, c] == 1 and rng.random() < p_bucle:
                g[r, c] = 0

    g[1, 1] = 2
    g[size - 2, size - 2] = 3
    return g
