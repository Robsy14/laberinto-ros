"""Prueba de robustez del controlador ante ruido de medición (Etapa 0)."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import controller
import maze
import planner

CAPTURAS = Path(__file__).resolve().parents[1] / "capturas"
CAPTURAS.mkdir(exist_ok=True)

SIGMAS_MM = [0.0, 0.5, 1.0, 2.0, 5.0]
CORRIDAS = 30


def ruta_laberinto():
    celdas = planner.astar(maze.START, maze.GOAL, "menor_h")
    return [controller.cell_a_xy(c) for c in celdas]


def main():
    ruta = ruta_laberinto()
    tasas, t_medios, t_desv = [], [], []

    print(f"{'σ [mm]':>8} | {'éxito':>7} | {'t medio [s]':>12} | {'desv [s]':>9}")
    for s_mm in SIGMAS_MM:
        exitos, tiempos = 0, []
        for semilla in range(CORRIDAS):
            res = controller.seguir(ruta, t_max=20.0, ruido=s_mm / 1000,
                                    semilla=semilla)
            if res["llego"] and not res["colision"]:
                exitos += 1
                tiempos.append(res["tiempo"])

        tasa = 100 * exitos / CORRIDAS
        tasas.append(tasa)
        t_medios.append(np.mean(tiempos) if tiempos else np.nan)
        t_desv.append(np.std(tiempos) if tiempos else np.nan)
        print(f"{s_mm:>8.1f} | {tasa:>6.0f}% | {t_medios[-1]:>12.2f} | "
              f"{t_desv[-1]:>9.2f}")

    etiquetas = [f"{s:g}" for s in SIGMAS_MM]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4.5))

    barras = a1.bar(etiquetas, tasas, color="#3498db")
    a1.bar_label(barras, fmt="%.0f%%")
    a1.set_ylim(0, 110)
    a1.set_xlabel("Ruido de medición σ [mm]")
    a1.set_ylabel("Corridas exitosas [%]")
    a1.set_title(f"Éxito en {CORRIDAS} corridas")
    a1.grid(axis="y", alpha=0.3)

    a2.errorbar(etiquetas, t_medios, yerr=t_desv, fmt="o-", capsize=5)
    a2.set_xlabel("Ruido de medición σ [mm]")
    a2.set_ylabel("Tiempo de recorrido [s]")
    a2.set_title("Tiempo medio de las corridas exitosas")
    a2.grid(alpha=0.3)

    archivo = CAPTURAS / "etapa0_18_robustez.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


if __name__ == "__main__":
    main()
