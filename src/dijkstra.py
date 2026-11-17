"""Dijkstra sobre la cuadrícula del laberinto (Etapa 0).

En una cuadrícula con costo 1 por paso, Dijkstra equivale a A* con
heurística h = 0. Se implementa por separado para compararlos en igualdad
de condiciones: misma matriz, mismos vecinos y misma forma de contar nodos
expandidos.
"""

import heapq
import itertools
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
import maze
from planner import reconstruir


def dijkstra_detalle(inicio, meta):
    """Devuelve (ruta, nodos_expandidos). La ruta es None si no hay solución."""
    orden = itertools.count()
    abiertos = [(0, next(orden), inicio)]
    padre = {inicio: None}
    costo = {inicio: 0}
    cerrados = set()

    while abiertos:
        _, _, actual = heapq.heappop(abiertos)
        if actual in cerrados:
            continue
        if actual == meta:
            return reconstruir(padre, meta), len(cerrados)
        cerrados.add(actual)

        for vecino in maze.neighbors(actual):
            nuevo_costo = costo[actual] + 1
            if nuevo_costo < costo.get(vecino, float("inf")):
                costo[vecino] = nuevo_costo
                padre[vecino] = actual
                heapq.heappush(abiertos, (nuevo_costo, next(orden), vecino))

    return None, len(cerrados)


def dijkstra(inicio, meta):
    """Devuelve solo la ruta, o None si no hay ruta."""
    ruta, _ = dijkstra_detalle(inicio, meta)
    return ruta
