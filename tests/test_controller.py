import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import controller
import maze
import planner


def test_ganancias_formula():
    kp, kd = controller.ganancias(4.0, 0.7)
    assert abs(kp - 16 / controller.K_G) < 1e-9
    assert abs(kd - 2 * 0.7 * 4 / controller.K_G) < 1e-9


def test_comando_saturado_a_8_grados():
    kp, kd = controller.ganancias()
    assert controller.comando(1.0, 0.0, kp, kd) == controller.LIMITE_ANG
    assert controller.comando(-1.0, 0.0, kp, kd) == -controller.LIMITE_ANG


def test_pared_y_fuera_del_tablero_son_colision():
    assert controller.choca(*controller.cell_a_xy((1, 0))) is True
    assert controller.choca(-0.01, 0.1) is True


def test_celda_libre_no_colisiona():
    assert controller.choca(*controller.cell_a_xy((0, 1))) is False


def test_escalon_sobreimpulso_menor_al_10_por_ciento():
    res = controller.seguir(controller.ruta_escalon(), t_max=4.0)
    xs = res["hist"]["x"]
    assert max(xs) - 0.06 < 0.10 * 0.04
    assert res["llego"] is True


def test_sigue_ruta_del_laberinto_sin_colisiones():
    celdas = planner.astar(maze.START, maze.GOAL, "menor_h")
    ruta = [controller.cell_a_xy(c) for c in celdas]
    res = controller.seguir(ruta, t_max=20.0)
    assert res["colision"] is False
    assert res["llego"] is True

