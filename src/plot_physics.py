"""Gráficas del modelo físico de la esfera para el informe (Etapa 0)."""

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import physics

CAPTURAS = Path(__file__).resolve().parents[1] / "capturas"
CAPTURAS.mkdir(exist_ok=True)


def grafica_aceleracion():
    angulos = np.linspace(0, 8, 200)
    a_teorica = [physics.aceleracion(math.radians(g)) for g in angulos]

    prueba = [0.5, 1, 2, 3, 4, 5, 6, 7, 8]
    a_simulada = []
    for g in prueba:
        res = physics.simular(math.radians(g), 0.0, t_total=0.1)
        a_simulada.append(res["vx"][-1] / 0.1)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(angulos, a_teorica, label="Modelo (5/7) g sen(θ)")
    ax.plot(prueba, a_simulada, "o", label="Simulación numérica")
    ax.axvline(5, color="gray", linestyle="--", alpha=0.6)
    ax.axvline(8, color="gray", linestyle="--", alpha=0.6)
    ax.annotate("5°: 0,61 m/s²", (5, 0.611), textcoords="offset points",
                xytext=(8, -14))
    ax.annotate("8°: 0,98 m/s²", (8, physics.aceleracion(math.radians(8))),
                textcoords="offset points", xytext=(-70, 6))
    ax.set_xlabel("Ángulo de inclinación θ [°]")
    ax.set_ylabel("Aceleración a lo largo del eje [m/s²]")
    ax.set_title("Aceleración de la esfera según la inclinación")
    ax.legend()
    ax.grid(alpha=0.3)

    archivo = CAPTURAS / "etapa0_10_physics_aceleracion.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


def grafica_caida():
    fig, ax = plt.subplots(figsize=(7, 5))
    for g in [5, 8]:
        res = physics.simular(math.radians(g), 0.0, t_total=0.45)
        ax.plot(res["t"], np.array(res["x"]) * 1000, label=f"θ = {g}°")
        t_teorico = math.sqrt(2 * 0.040 / physics.aceleracion(math.radians(g)))
        ax.plot(t_teorico, 40, "k^")
        ax.annotate(f"{t_teorico:.3f} s", (t_teorico, 40),
                    textcoords="offset points", xytext=(6, 6))

    ax.axhline(40, color="gray", linestyle="--", alpha=0.6)
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Posición en x [mm]")
    ax.set_title("Recorrido de una celda de 40 mm desde el reposo")
    ax.legend()
    ax.grid(alpha=0.3)

    archivo = CAPTURAS / "etapa0_11_physics_caida.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


if __name__ == "__main__":
    grafica_aceleracion()
    grafica_caida()
