import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import physics


def test_aceleracion_con_5_grados():
    a = physics.aceleracion(math.radians(5))
    esperado = 0.611
    assert abs(a - esperado) / esperado < 0.01


def test_sin_inclinacion_no_se_mueve():
    res = physics.simular(0.0, 0.0, t_total=1.0)
    assert res["x"][-1] == 0.0
    assert res["y"][-1] == 0.0
    assert res["vx"][-1] == 0.0


def test_inclinacion_positiva_mueve_en_sentido_positivo():
    res = physics.simular(math.radians(5), 0.0, t_total=0.2)
    assert res["x"][-1] > 0


def test_inclinacion_negativa_mueve_en_sentido_negativo():
    res = physics.simular(math.radians(-5), 0.0, t_total=0.2)
    assert res["x"][-1] < 0


def test_ejes_independientes():
    res = physics.simular(math.radians(5), 0.0, t_total=0.5)
    assert res["y"][-1] == 0.0


def test_tiempo_para_recorrer_una_celda_de_40_mm():
    res = physics.simular(math.radians(5), 0.0, t_total=0.5)
    t_cruce = next(t for t, x in zip(res["t"], res["x"]) if x >= 0.040)
    esperado = math.sqrt(2 * 0.040 / physics.aceleracion(math.radians(5)))
    assert abs(t_cruce - esperado) < 0.005
