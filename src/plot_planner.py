"""Gráficas del planificador A* para el informe (Etapa 0)."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

sys.path.append(str(Path(__file__).resolve().parent))
import maze
import planner

CAPTURAS = Path(__file__).resolve().parents[1] / "capturas"
CAPTURAS.mkdir(exist_ok=True)

COLORES = {0: "white", 1: "#333333", 2: "#2ecc71", 3: "#e74c3c"}


def dibujar_mapa(ax, grid, ruta=None, titulo=""):
    filas, cols = grid.shape
    for r in range(filas):
        for c in range(cols):
            y = filas - 1 - r
            ax.add_patch(Rectangle((c, y), 1, 1,
                                   facecolor=COLORES[int(grid[r, c])],
                                   edgecolor="gray"))
    if ruta:
        xs = [c + 0.5 for _, c in ruta]
        ys = [filas - 1 - r + 0.5 for r, _ in ruta]
        ax.plot(xs, ys, color="#3498db", linewidth=3, marker="o", markersize=5)
    ax.set_xlim(0, cols)
    ax.set_ylim(0, filas)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(titulo)


def medir(grid, inicio, meta, criterio):
    """Ejecuta A* sobre una cuadrícula arbitraria y devuelve (ruta, expandidos)."""
    original = maze.MAZE
    maze.MAZE = grid
    try:
        return planner.astar_detalle(inicio, meta, criterio)
    finally:
        maze.MAZE = original


def grafica_ruta():
    ruta = planner.astar(maze.START, maze.GOAL, "menor_h")
    fig, ax = plt.subplots(figsize=(6, 6))
    dibujar_mapa(ax, maze.MAZE, ruta,
                 f"Ruta A* en el laberinto ({len(ruta) - 1} pasos)")
    archivo = CAPTURAS / "etapa0_07_planner_ruta.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


def grafica_expandidos():
    abierto = np.zeros((7, 7), dtype=int)
    abierto[0, 0] = 2
    abierto[6, 6] = 3

    casos = {
        "Laberinto": (maze.MAZE, maze.START, maze.GOAL),
        "Mapa abierto 7x7": (abierto, (0, 0), (6, 6)),
    }

    resultados = {}
    for nombre, (grid, inicio, meta) in casos.items():
        resultados[nombre] = {}
        for criterio in planner.CRITERIOS:
            _, exp = medir(grid, inicio, meta, criterio)
            resultados[nombre][criterio] = exp
            print(f"{nombre} | {criterio}: {exp} nodos expandidos")

    fig, ax = plt.subplots(figsize=(7, 5))
    x = np.arange(len(casos))
    ancho = 0.35
    for i, criterio in enumerate(planner.CRITERIOS):
        valores = [resultados[n][criterio] for n in casos]
        barras = ax.bar(x + (i - 0.5) * ancho, valores, ancho, label=criterio)
        ax.bar_label(barras)
    ax.set_xticks(x)
    ax.set_xticklabels(list(casos))
    ax.set_ylabel("Nodos expandidos")
    ax.set_title("Comparación de criterios de desempate en A*")
    ax.legend(title="Desempate")
    ax.grid(axis="y", alpha=0.3)

    archivo = CAPTURAS / "etapa0_08_planner_expandidos.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


if __name__ == "__main__":
    grafica_ruta()
    grafica_expandidos()
