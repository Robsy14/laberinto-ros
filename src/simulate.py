"""Recorrido completo S -> G con planificador y controlador (Etapa 0).

Genera el registro en CSV y la animación GIF del recorrido.
"""

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle

sys.path.append(str(Path(__file__).resolve().parent))
import controller
import maze
import planner
from plot_planner import dibujar_mapa

RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "capturas"
DATOS = RAIZ / "datos"
CAPTURAS.mkdir(exist_ok=True)
DATOS.mkdir(exist_ok=True)

TAM = controller.TAMANO_CELDA
PASO_ANIM = 20  # un cuadro cada 20 pasos de simulación (20 ms)


def ejecutar():
    celdas = planner.astar(maze.START, maze.GOAL, "menor_h")
    ruta = [controller.cell_a_xy(c) for c in celdas]
    res = controller.seguir(ruta, t_max=20.0)
    return celdas, res


def guardar_csv(res, archivo):
    h = res["hist"]
    with open(archivo, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_s", "x_m", "y_m", "theta_x_rad", "theta_y_rad",
                    "error_x_m", "error_y_m"])
        for i in range(len(h["t"])):
            w.writerow([h["t"][i], h["x"][i], h["y"][i], h["thx"][i],
                        h["thy"][i], h["ex"][i], h["ey"][i]])
    print("Datos guardados en:", archivo)


def animar(celdas, res, archivo):
    h = res["hist"]
    xs = np.array(h["x"]) / TAM
    ys = np.array(h["y"]) / TAM
    tiempos = h["t"]

    fig, ax = plt.subplots(figsize=(6, 6))
    dibujar_mapa(ax, maze.MAZE, celdas, "Recorrido S → G con planificador y controlador")
    esfera = Circle((xs[0], ys[0]), controller.RADIO_ESFERA / TAM,
                    color="#8e44ad", zorder=5)
    ax.add_patch(esfera)
    texto = ax.text(0.1, 6.85, "", fontsize=10, color="black")

    cuadros = list(range(0, len(xs), PASO_ANIM))
    if cuadros[-1] != len(xs) - 1:
        cuadros.append(len(xs) - 1)

    def actualizar(i):
        esfera.center = (xs[i], ys[i])
        texto.set_text(f"t = {tiempos[i]:.2f} s")
        return esfera, texto

    anim = FuncAnimation(fig, actualizar, frames=cuadros, interval=20)
    anim.save(archivo, writer=PillowWriter(fps=50))
    plt.close(fig)
    print("Animación guardada en:", archivo)


def main():
    celdas, res = ejecutar()
    print(f"Llegó: {res['llego']} | Colisión: {res['colision']} | "
          f"Tiempo: {res['tiempo']:.2f} s | Pasos: {len(res['hist']['t'])}")
    guardar_csv(res, DATOS / "etapa0_recorrido_nominal.csv")
    animar(celdas, res, CAPTURAS / "etapa0_17_recorrido.gif")


if __name__ == "__main__":
    main()
