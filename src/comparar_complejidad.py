"""Comparación de A* y Dijkstra en laberintos de 15x15 y 31x31 (Etapa 0).

Usa 20 laberintos generados por tamaño, con bucles, así que hay caminos
alternativos y también se verifica que ambos algoritmos encuentren la
ruta de igual longitud.
"""

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import comparar_planificadores as cp
import generador_laberintos as gen
import planner
from plot_planner import dibujar_mapa

RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "capturas"
DATOS = RAIZ / "datos"
CAPTURAS.mkdir(exist_ok=True)
DATOS.mkdir(exist_ok=True)

TAMANOS = [(7, "15x15"), (15, "31x31")]  # (celdas por lado, etiqueta)
N_INSTANCIAS = 20
P_BUCLE = 0.10


def casos():
    for n, etiqueta in TAMANOS:
        for semilla in range(N_INSTANCIAS):
            grid = gen.generar(n, semilla, P_BUCLE)
            size = grid.shape[0]
            fila = cp.comparar(f"Laberinto {etiqueta}", grid, (1, 1), (size - 2, size - 2))
            fila["tamano"] = etiqueta
            fila["semilla"] = semilla
            yield fila


def guardar_csv(filas):
    archivo = DATOS / "comparacion_complejidad.csv"
    with open(archivo, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print("Datos guardados en:", archivo)


def graficar(filas):
    etiquetas = [e for _, e in TAMANOS]
    x = np.arange(len(etiquetas))
    ancho = 0.38

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5))
    configuraciones = [
        (a1, "expandidos_astar", "expandidos_dijkstra",
         "Nodos expandidos", "Nodos expandidos", "%.0f"),
        (a2, "tiempo_astar_ms", "tiempo_dijkstra_ms",
         "Tiempo de cálculo", "Tiempo [ms]", "%.3f"),
    ]

    for ax, ka, kd, titulo, ylabel, formato in configuraciones:
        medias_a = [np.mean([f[ka] for f in filas if f["tamano"] == e]) for e in etiquetas]
        medias_d = [np.mean([f[kd] for f in filas if f["tamano"] == e]) for e in etiquetas]
        std_a = [np.std([f[ka] for f in filas if f["tamano"] == e]) for e in etiquetas]
        std_d = [np.std([f[kd] for f in filas if f["tamano"] == e]) for e in etiquetas]

        barras_a = ax.bar(x - ancho / 2, medias_a, ancho, yerr=std_a, capsize=4, label="A*")
        barras_d = ax.bar(x + ancho / 2, medias_d, ancho, yerr=std_d, capsize=4, label="Dijkstra")
        ax.bar_label(barras_a, fmt=formato, padding=2, fontsize=8)
        ax.bar_label(barras_d, fmt=formato, padding=2, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels([f"Laberinto {e}" for e in etiquetas])
        ax.set_ylabel(ylabel)
        ax.set_title(f"{titulo} ({N_INSTANCIAS} laberintos por tamaño)")
        ax.legend(title="Algoritmo")
        ax.grid(axis="y", alpha=0.3)

    archivo = CAPTURAS / "etapa0_23_complejidad.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


def ejemplo():
    """Dibuja un laberinto de 31x31 con la ruta de A* para el informe."""
    grid = gen.generar(15, 0, P_BUCLE)
    size = grid.shape[0]
    with cp.mapa(grid):
        ruta, _ = planner.astar_detalle((1, 1), (size - 2, size - 2), "menor_h")

    fig, ax = plt.subplots(figsize=(7, 7))
    dibujar_mapa(ax, grid, ruta, "Ejemplo: laberinto 31x31 y ruta de A*")
    archivo = CAPTURAS / "etapa0_24_ejemplo_laberinto.png"
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura guardada en:", archivo)


def resumen(filas):
    print("\nResumen por tamaño")
    for _, etiqueta in TAMANOS:
        sub = [f for f in filas if f["tamano"] == etiqueta]
        n = len(sub)
        iguales = sum(f["pasos_astar"] == f["pasos_dijkstra"] for f in sub)
        menos = sum(f["expandidos_astar"] < f["expandidos_dijkstra"] for f in sub)
        pasos = np.mean([f["pasos_astar"] for f in sub])
        exp_a = np.mean([f["expandidos_astar"] for f in sub])
        exp_d = np.mean([f["expandidos_dijkstra"] for f in sub])
        t_a = np.mean([f["tiempo_astar_ms"] for f in sub])
        t_d = np.mean([f["tiempo_dijkstra_ms"] for f in sub])

        print(f"Laberinto {etiqueta} ({n} instancias)")
        print(f"  Longitud de ruta igual: {iguales} de {n}")
        print(f"  Longitud promedio de la ruta: {pasos:.1f} pasos")
        print(f"  A* expande menos nodos en {menos} de {n}")
        print(f"  Expandidos promedio: A* {exp_a:.1f} | Dijkstra {exp_d:.1f}")
        print(f"  Tiempo promedio [ms]: A* {t_a:.3f} | Dijkstra {t_d:.3f}")


def main():
    filas = list(casos())
    guardar_csv(filas)
    graficar(filas)
    ejemplo()
    resumen(filas)


if __name__ == "__main__":
    main()
