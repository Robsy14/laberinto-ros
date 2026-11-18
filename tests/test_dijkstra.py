import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import dijkstra
import maze
import planner


def test_encuentra_ruta_en_laberinto():
    ruta = dijkstra.dijkstra(maze.START, maze.GOAL)
    assert ruta[0] == maze.START
    assert ruta[-1] == maze.GOAL
    assert all(maze.is_free(c) for c in ruta)


def test_misma_longitud_optima_que_astar_en_laberinto():
    ruta_d = dijkstra.dijkstra(maze.START, maze.GOAL)
    ruta_a = planner.astar(maze.START, maze.GOAL, "menor_h")
    assert len(ruta_d) == len(ruta_a) == 13


def test_sin_ruta_cuando_se_bloquea_la_salida(monkeypatch):
    bloqueado = maze.MAZE.copy()
    bloqueado[5, 6] = 1
    bloqueado[6, 5] = 1
    monkeypatch.setattr(maze, "MAZE", bloqueado)
    assert dijkstra.dijkstra(maze.START, maze.GOAL) is None


def test_misma_longitud_que_astar_en_mapas_aleatorios(monkeypatch):
    for semilla in range(10):
        rng = np.random.default_rng(semilla)
        g = (rng.random((12, 12)) < 0.3).astype(int)
        g[0, 0] = 2
        g[-1, -1] = 3
        monkeypatch.setattr(maze, "MAZE", g)
        ruta_d = dijkstra.dijkstra((0, 0), (11, 11))
        ruta_a = planner.astar((0, 0), (11, 11), "menor_h")
        if ruta_d is None:
            assert ruta_a is None
        else:
            assert len(ruta_d) == len(ruta_a)


def test_astar_no_expande_mas_nodos_que_dijkstra_en_mapa_abierto(monkeypatch):
    monkeypatch.setattr(maze, "MAZE", np.zeros((7, 7), dtype=int))
    _, exp_d = dijkstra.dijkstra_detalle((0, 0), (6, 6))
    _, exp_a = planner.astar_detalle((0, 0), (6, 6), "menor_h")
    assert exp_a <= exp_d
