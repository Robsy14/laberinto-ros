"""Comparación de A* y Dijkstra en el laberinto y en mapas de prueba (Etapa 0).

Mide para cada caso: longitud de la ruta, nodos expandidos y tiempo de cálculo.
Genera el registro en datos/comparacion_planificadores.csv y dos gráficas.
"""

import csv
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import dijkstra
import maze
import planner

RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "capturas"
DATOS = RAIZ / "datos"
CAPTURAS.mkdir(exist_ok=True)
DATOS.mkdir(exist_ok=True)

TAM_ALEATORIO = 15
N_ALEATORIOS = 30
P_PARED = 0.30
REPETICIONES = 3


@contextmanager
def mapa(grid):
    original = maze.MAZE
    maze.MAZE = grid
    try:
        yield
    finally:
        maze.MAZE = original


def resolver(algoritmo, grid, inicio, meta):
    """Ejecuta un algoritmo sobre una cuadrícula y devuelve (ruta, expandidos)."""
    with mapa(grid):
        if algoritmo == "A*":
            return planner.astar_detalle(inicio, meta, "menor_h")
        return dijkstra.dijkstra_detalle(inicio, meta)


def tiempo_ms(algoritmo, grid, inicio, meta):
    """Tiempo mínimo de varias repeticiones, en milisegundos."""
    mejores = []
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        resolver(algoritmo, grid, inicio, meta)
        mejores.append(time.perf_counter() - t0)
    return min(mejores) * 1000


def abierto(n):
    g = np.zeros((n, n), dtype=int)
    g[0, 0] = 2
    g[n - 1, n - 1] = 3
    return g


def casos_fijos():
    return [
        ("Laberinto 7x7", maze.MAZE.copy(), maze.START, maze.GOAL),
        ("Abierto 7x7", abierto(7), (0, 0), (6, 6)),
        ("Abierto 11x11", abierto(11), (0, 0), (10, 10)),
    ]


def mapas_aleatorios():
    """Genera mapas aleatorios de TAM_ALEATORIO celdas que sí tienen solución."""
    instancias = []
    semilla = 0
    meta = (TAM_ALEATORIO - 1, TAM_ALEATORIO - 1)
    while len(instancias) < N_ALEATORIOS:
        rng = np.random.default_rng(semilla)
        g = (rng.random((TAM_ALEATORIO, TAM_ALEATORIO)) < P_PARED).astype(int)
        g[0, 0] = 2
        g[-1, -1] = 3
        ruta, _ = resolver("Dijkstra", g, (0, 0), meta)
        if ruta is not None:
            instancias.append((f"Aleatorio {semilla}", g, (0, 0), meta))
        semilla += 1
    return instancias


def comparar(nombre, grid, inicio, meta):
    ruta_a, exp_a = resolver("A*", grid, inicio, meta)
    ruta_d, exp_d = resolver("Dijkstra", grid, inicio, meta)
    return {
        "caso": nombre,
        "pasos_astar": len(ruta_a) - 1,
        "pasos_dijkstra": len(ruta_d) - 1,
        "expandidos_astar": exp_a,
        "expandidos_dijkstra": exp_d,
        "tiempo_astar_ms": tiempo_ms("A*", grid, inicio, meta),
        "tiempo_dijkstra_ms": tiempo_ms("Dijkstra", grid, inicio, meta),
    }


def guardar_csv(filas):
    archivo = DATOS / "comparacion_planificadores.csv"
    with open(archivo, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print("Datos guardados en:", archivo)


def graficar(filas):
    fijos = [f for f in filas if not f["caso"].startswith("Aleatorio")]
    aleat = [f for f in filas if f["caso"].startswith("Aleatorio")]
    etiquetas = [f["caso"] for f in fijos] + ["Promedio aleatorios"]
    n_fijos = len(fijos)

    metricas = [
        ("expandidos_astar", "expandidos_dijkstra", "Nodos expandidos",
         "Nodos expandidos: A* contra Dijkstra", "%.0f",
         "etapa0_20_comparacion_expandidos.png"),
        ("tiempo_astar_ms", "tiempo_dijkstra_ms", "Tiempo de cálculo [ms]",
         "Tiempo de cálculo: A* contra Dijkstra", "%.3f",
         "etapa0_21_comparacion_tiempo.png"),
    ]

    for clave_a, clave_d, ylabel, titulo, formato, nombre in metricas:
        va = [f[clave_a] for f in fijos] + [np.mean([f[clave_a] for f in aleat])]
        vd = [f[clave_d] for f in fijos] + [np.mean([f[clave_d] for f in aleat])]
        ea = [0.0] * n_fijos + [np.std([f[clave_a] for f in aleat])]
        ed = [0.0] * n_fijos + [np.std([f[clave_d] for f in aleat])]

        x = np.arange(len(etiquetas))
        ancho = 0.38
        fig, ax = plt.subplots(figsize=(9, 5))
        barras_a = ax.bar(x - ancho / 2, va, ancho, yerr=ea, capsize=4, label="A*")
        barras_d = ax.bar(x + ancho / 2, vd, ancho, yerr=ed, capsize=4, label="Dijkstra")
        ax.bar_label(barras_a, fmt=formato, padding=2, fontsize=8)
        ax.bar_label(barras_d, fmt=formato, padding=2, fontsize=8)
        ax.set_xticks(x)
        ax.set_xticklabels(etiquetas)
        ax.set_ylabel(ylabel)
        ax.set_title(titulo)
        ax.legend(title="Algoritmo")
        ax.grid(axis="y", alpha=0.3)

        archivo = CAPTURAS / nombre
        fig.savefig(archivo, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print("Figura guardada en:", archivo)


def resumen(filas):
    aleat = [f for f in filas if f["caso"].startswith("Aleatorio")]
    longitudes_iguales = all(f["pasos_astar"] == f["pasos_dijkstra"] for f in filas)
    menos_nodos = sum(f["expandidos_astar"] < f["expandidos_dijkstra"] for f in aleat)

    print("\nResumen")
    print(f"Longitud de ruta igual en todos los casos: {longitudes_iguales}")
    print(f"Mapas aleatorios: {len(aleat)}")
    print(f"  A* expande menos nodos en {menos_nodos} de {len(aleat)}")
    print(f"  Expandidos promedio: A* {np.mean([f['expandidos_astar'] for f in aleat]):.1f}"
          f" | Dijkstra {np.mean([f['expandidos_dijkstra'] for f in aleat]):.1f}")
    print(f"  Tiempo promedio [ms]: A* {np.mean([f['tiempo_astar_ms'] for f in aleat]):.3f}"
          f" | Dijkstra {np.mean([f['tiempo_dijkstra_ms'] for f in aleat]):.3f}")


def main():
    filas = []

    for nombre, grid, inicio, meta in casos_fijos():
        fila = comparar(nombre, grid, inicio, meta)
        filas.append(fila)
        print(f"{nombre:>15} | pasos A* {fila['pasos_astar']} Dijkstra {fila['pasos_dijkstra']}"
              f" | expandidos A* {fila['expandidos_astar']} Dijkstra {fila['expandidos_dijkstra']}"
              f" | tiempo A* {fila['tiempo_astar_ms']:.3f} ms Dijkstra {fila['tiempo_dijkstra_ms']:.3f} ms")

    for nombre, grid, inicio, meta in mapas_aleatorios():
        filas.append(comparar(nombre, grid, inicio, meta))

    guardar_csv(filas)
    graficar(filas)
    resumen(filas)


if __name__ == "__main__":
    main()
