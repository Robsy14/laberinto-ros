"""Planificador A* sobre la cuadrícula del laberinto (Etapa 0).

desempate:
    "primera": a igual costo f, gana el nodo que se insertó primero.
    "menor_h": a igual costo f, gana el nodo más cercano a la meta.
"""

import heapq
import itertools
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
import maze

CRITERIOS = ("primera", "menor_h")


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruir(padre, meta):
    ruta = []
    nodo = meta
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre[nodo]
    return ruta[::-1]


def astar_detalle(inicio, meta, desempate="menor_h"):
    """Devuelve (ruta, nodos_expandidos).

    ruta es la lista de celdas desde inicio hasta meta, o None si no hay ruta.
    nodos_expandidos cuenta las celdas procesadas antes de llegar a la meta.
    """
    if desempate not in CRITERIOS:
        raise ValueError(f"desempate no válido: {desempate}")

    orden = itertools.count()
    abiertos = [(manhattan(inicio, meta), 0, next(orden), inicio)]
    padre = {inicio: None}
    costo = {inicio: 0}
    cerrados = set()

    while abiertos:
        _, _, _, actual = heapq.heappop(abiertos)
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
                h = manhattan(vecino, meta)
                f = nuevo_costo + h
                desp = h if desempate == "menor_h" else 0
                heapq.heappush(abiertos, (f, desp, next(orden), vecino))

    return None, len(cerrados)


def astar(inicio, meta, desempate="menor_h"):
    """Devuelve solo la ruta, o None si no hay ruta."""
    ruta, _ = astar_detalle(inicio, meta, desempate)
    return ruta


if __name__ == "__main__":
    for criterio in CRITERIOS:
        ruta, expandidos = astar_detalle(maze.START, maze.GOAL, criterio)
        print(f"{criterio}: {len(ruta) - 1} pasos, {expandidos} expandidos -> {ruta}")
