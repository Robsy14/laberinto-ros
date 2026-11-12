"""Gráfica de escalabilidad de A* en mapas abiertos (Etapa 0)."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import maze
import planner

CAPTURAS = Path(__file__).resolve().parents[1] / "capturas"
CAPTURAS.mkdir(exist_ok=True)
ARCHIVO = CAPTURAS / "etapa0_09_planner_escala.png"
TAMANOS = [5, 7, 9, 11]


def expandidos_en_mapa_abierto(n, criterio):
    """Ejecuta A* de (0,0) a (n-1,n-1) en un mapa sin paredes de n x n."""
    original = maze.MAZE
    maze.MAZE = np.zeros((n, n), dtype=int)
    try:
        ruta, exp = planner.astar_detalle((0, 0), (n - 1, n - 1), criterio)
    finally:
        maze.MAZE = original
    return len(ruta) - 1, exp


def main():
    resultados = {criterio: [] for criterio in planner.CRITERIOS}

    for n in TAMANOS:
        for criterio in planner.CRITERIOS:
            pasos, exp = expandidos_en_mapa_abierto(n, criterio)
            resultados[criterio].append(exp)
            print(f"{n}x{n} | {criterio}: {pasos} pasos, {exp} expandidos")

    fig, ax = plt.subplots(figsize=(7, 5))
    for criterio, valores in resultados.items():
        ax.plot(TAMANOS, valores, marker="o", label=criterio)
        for x, y in zip(TAMANOS, valores):
            ax.annotate(str(y), (x, y), textcoords="offset points",
                        xytext=(0, 8), ha="center")

    ax.set_xlabel("Tamaño del mapa abierto (n x n)")
    ax.set_ylabel("Nodos expandidos")
    ax.set_title("Escalabilidad de A* según el criterio de desempate")
    ax.set_xticks(TAMANOS)
    ax.legend(title="Desempate")
    ax.grid(alpha=0.3)

    fig.savefig(ARCHIVO, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", ARCHIVO)


if __name__ == "__main__":
    main()
