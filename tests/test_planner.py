import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import maze
import planner


def pasos(ruta):
    return len(ruta) - 1


def test_encuentra_ruta_de_inicio_a_salida():
    ruta = planner.astar(maze.START, maze.GOAL)
    assert ruta[0] == maze.START
    assert ruta[-1] == maze.GOAL


def test_ruta_mas_corta_tiene_12_pasos_con_ambos_criterios():
    for criterio in planner.CRITERIOS:
        assert pasos(planner.astar(maze.START, maze.GOAL, criterio)) == 12


def test_ruta_pasa_por_el_centro():
    ruta = planner.astar(maze.START, maze.GOAL)
    assert (2, 4) in ruta
    assert (3, 4) in ruta


def test_ruta_no_atraviesa_paredes():
    for celda in planner.astar(maze.START, maze.GOAL):
        assert maze.is_free(celda)


def test_sin_ruta_cuando_se_bloquea_la_salida(monkeypatch):
    bloqueado = maze.MAZE.copy()
    bloqueado[5, 6] = 1
    bloqueado[6, 5] = 1
    monkeypatch.setattr(maze, "MAZE", bloqueado)
    assert planner.astar(maze.START, maze.GOAL) is None


def test_empate_en_mapa_abierto(monkeypatch):
    # Mapa 3x3 sin paredes: hay dos rutas de igual longitud de (0,0) a (2,2)
    monkeypatch.setattr(maze, "MAZE", np.zeros((3, 3), dtype=int))
    for criterio in planner.CRITERIOS:
        ruta = planner.astar((0, 0), (2, 2), criterio)
        assert pasos(ruta) == 4
        assert ruta[0] == (0, 0) and ruta[-1] == (2, 2)


def test_criterio_invalido():
    try:
        planner.astar(maze.START, maze.GOAL, "otro")
        assert False, "debió lanzar ValueError"
    except ValueError:
        pass


def test_menor_h_expande_menos_nodos_en_mapa_abierto(monkeypatch):
    monkeypatch.setattr(maze, "MAZE", np.zeros((7, 7), dtype=int))
    _, exp_primera = planner.astar_detalle((0, 0), (6, 6), "primera")
    _, exp_h = planner.astar_detalle((0, 0), (6, 6), "menor_h")
    assert exp_h < exp_primera
