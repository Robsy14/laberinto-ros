"""Gráficas del controlador PD para el informe (Etapa 0)."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import controller
import maze
import planner
from plot_planner import dibujar_mapa

CAPTURAS = Path(__file__).resolve().parents[1] / "capturas"
CAPTURAS.mkdir(exist_ok=True)
TAM = controller.TAMANO_CELDA


def ruta_laberinto():
    celdas = planner.astar(maze.START, maze.GOAL, "menor_h")
    return celdas, [controller.cell_a_xy(c) for c in celdas]


def grafica_escalon():
    fig, ax = plt.subplots(figsize=(7, 5))
    x0 = controller.ruta_escalon()[0][0]

    for omega in [2.0, 4.0, 6.0]:
        res = controller.seguir(controller.ruta_escalon(), t_max=4.0,
                                omega_n=omega)
        t = np.array(res["hist"]["t"])
        x = (np.array(res["hist"]["x"]) - x0) * 1000
        sobre = (x.max() - 40) / 40 * 100
        print(f"ωn = {omega:g} rad/s | sobreimpulso {sobre:.1f} % | "
              f"tiempo {res['tiempo']:.2f} s")
        ax.plot(t, x, label=f"ωn = {omega:g} rad/s")

    ax.axhline(40, color="k", linestyle="--", alpha=0.6, label="Objetivo 40 mm")
    ax.set_xlabel("Tiempo [s]")
    ax.set_ylabel("Desplazamiento en x [mm]")
    ax.set_title("Respuesta a un escalón de 40 mm (ζ = 0,7)")
    ax.legend()
    ax.grid(alpha=0.3)

    archivo = CAPTURAS / "etapa0_13_controller_escalon.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


def grafica_ruta():
    celdas, ruta = ruta_laberinto()
    res = controller.seguir(ruta, t_max=20.0)
    h = res["hist"]

    fig, ax = plt.subplots(figsize=(6, 6))
    dibujar_mapa(ax, maze.MAZE, None, "Seguimiento de la ruta con el PD")
    ax.plot(np.array(h["x"]) / TAM, np.array(h["y"]) / TAM,
            color="#3498db", linewidth=2, label="Trayectoria de la esfera")
    puntos = np.array(ruta) / TAM
    ax.plot(puntos[:, 0], puntos[:, 1], "o", color="#f39c12",
            markersize=4, label="Puntos de la ruta")
    ax.legend(fontsize=8, loc="upper right")

    archivo = CAPTURAS / "etapa0_14_controller_ruta.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Ruta | llegó: {res['llego']} | colisión: {res['colision']} | "
          f"tiempo: {res['tiempo']:.2f} s")
    print("Figura guardada en:", archivo)


def grafica_comandos():
    _, ruta = ruta_laberinto()
    res = controller.seguir(ruta, t_max=20.0)
    h = res["hist"]
    t = np.array(h["t"])

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)

    a1.plot(t, np.degrees(h["thx"]), label="θx")
    a1.plot(t, np.degrees(h["thy"]), label="θy")
    a1.axhline(8, color="gray", linestyle="--", alpha=0.6)
    a1.axhline(-8, color="gray", linestyle="--", alpha=0.6)
    a1.set_ylabel("Inclinación [°]")
    a1.set_title("Comandos de inclinación y error de seguimiento")
    a1.legend()
    a1.grid(alpha=0.3)

    a2.plot(t, np.array(h["ex"]) * 1000, label="error x")
    a2.plot(t, np.array(h["ey"]) * 1000, label="error y")
    a2.set_xlabel("Tiempo [s]")
    a2.set_ylabel("Error [mm]")
    a2.legend()
    a2.grid(alpha=0.3)

    archivo = CAPTURAS / "etapa0_15_controller_comandos.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


if __name__ == "__main__":
    grafica_escalon()
    grafica_ruta()
    grafica_comandos()
