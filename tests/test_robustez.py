import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import controller
import maze
import planner


def test_ruido_de_1_mm_completa_la_ruta():
    celdas = planner.astar(maze.START, maze.GOAL, "menor_h")
    ruta = [controller.cell_a_xy(c) for c in celdas]
    res = controller.seguir(ruta, t_max=20.0, ruido=0.001, semilla=0)
    assert res["colision"] is False
    assert res["llego"] is True
