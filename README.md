# Plataforma robótica de laberinto con control autónomo

Proyecto final de Robótica. Una esfera se guía a través de un laberinto de 7×7 celdas
inclinando una plataforma de dos ejes.

## Estado

- **Etapa 0 (completa):** simulación 2D en Python. Planificación A*, modelo físico,
  controlador PD y pruebas de robustez.
- **Etapa 1 (pendiente):** modelo en Gazebo con ROS 2 Jazzy.

## Estructura

- `src/`: módulos de la simulación (`maze`, `planner`, `physics`, `controller`, `simulate`)
  y scripts de gráficas.
- `tests/`: pruebas automáticas con pytest.
- `capturas/`: figuras y capturas de la Etapa 0, usadas en el informe.
- `datos/`: registro CSV del recorrido nominal.

## Ejecutar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v tests/
python src/simulate.py
```
