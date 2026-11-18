import sys
from collections import deque
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import dijkstra
import generador_laberintos as gen
import maze
import planner


def celdas_libres(g):
    return {(r, c) for r in range(g.shape[0]) for c in range(g.shape[1]) if g[r, c] != 1}


def test_dimensiones_y_entradas():
    g = gen.generar(7, semilla=0)
    assert g.shape == (15, 15)
    assert g[1, 1] == 2
    assert g[13, 13] == 3


def test_todas_las_celdas_libres_son_alcanzables(monkeypatch):
    for semilla in range(5):
        g = gen.generar(7, semilla)
        monkeypatch.setattr(maze, "MAZE", g)
        vistos = {(1, 1)}
        cola = deque([(1, 1)])
        while cola:
            actual = cola.popleft()
            for v in maze.neighbors(actual):
                if v not in vistos:
                    vistos.add(v)
                    cola.append(v)
        assert vistos == celdas_libres(g)


def test_astar_y_dijkstra_dan_la_misma_longitud(monkeypatch):
    for semilla in range(5):
        g = gen.generar(7, semilla, p_bucle=0.10)
        monkeypatch.setattr(maze, "MAZE", g)
        ruta_a = planner.astar((1, 1), (13, 13), "menor_h")
        ruta_d = dijkstra.dijkstra((1, 1), (13, 13))
        assert len(ruta_a) == len(ruta_d)
