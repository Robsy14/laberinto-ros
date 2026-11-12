import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import maze


def test_inicio_y_salida():
    assert maze.START == (0, 0)
    assert maze.GOAL == (6, 6)


def test_pared_no_es_libre():
    assert maze.is_free((1, 0)) is False


def test_celda_libre():
    assert maze.is_free((0, 1)) is True


def test_fuera_del_mapa_no_es_libre():
    assert maze.is_free((-1, 0)) is False
    assert maze.is_free((7, 0)) is False


def test_vecinos_de_inicio():
    # (1,0) es pared, así que la única salida desde S es (0,1)
    assert set(maze.neighbors((0, 0))) == {(0, 1)}


def test_vecinos_de_salida():
    # En el mapa base, G tiene dos vecinos libres: (5,6) y (6,5)
    assert set(maze.neighbors((6, 6))) == {(5, 6), (6, 5)}
