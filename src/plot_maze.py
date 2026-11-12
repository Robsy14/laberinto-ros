"""Genera la figura del laberinto para el informe (Etapa 0)."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.append(str(Path(__file__).resolve().parent))
import maze

CAPTURAS = Path(__file__).resolve().parents[1] / "capturas"
CAPTURAS.mkdir(exist_ok=True)
ARCHIVO = CAPTURAS / "etapa0_04_laberinto_grafica.png"

COLORES = {0: "white", 1: "#333333", 2: "#2ecc71", 3: "#e74c3c"}
ETIQUETAS = {2: "S", 3: "G"}


def dibujar():
    filas, cols = maze.MAZE.shape
    fig, ax = plt.subplots(figsize=(6, 6))

    for r in range(filas):
        for c in range(cols):
            valor = int(maze.MAZE[r, c])
            y = filas - 1 - r  # la fila 0 queda arriba
            ax.add_patch(Rectangle((c, y), 1, 1,
                                   facecolor=COLORES[valor],
                                   edgecolor="gray"))
            if valor in ETIQUETAS:
                ax.text(c + 0.5, y + 0.5, ETIQUETAS[valor],
                        ha="center", va="center", fontsize=16,
                        fontweight="bold", color="white")

    ax.set_xlim(0, cols)
    ax.set_ylim(0, filas)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Laberinto 7x7 (Etapa 0)")

    fig.savefig(ARCHIVO, dpi=150, bbox_inches="tight")
    print("Figura guardada en:", ARCHIVO)

if __name__ == "__main__":
    dibujar()
