"""Animación lado a lado de la búsqueda de A* y Dijkstra (Etapa 0).

Usa el mismo laberinto de 31x31 del ejemplo (semilla 0). Muestra los nodos
que expande cada algoritmo y, al final, la ruta encontrada. Verifica que la
búsqueda reproduzca los resultados de planner.py y dijkstra.py.
"""

import heapq
import itertools
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap

sys.path.append(str(Path(__file__).resolve().parent))
import comparar_planificadores as cp
import dijkstra
import generador_laberintos as gen
import maze
import planner

RAIZ = Path(__file__).resolve().parents[1]
CAPTURAS = RAIZ / "capturas"
CAPTURAS.mkdir(exist_ok=True)

SEMILLA = 0
N_CELDAS = 15          # genera una cuadrícula de 31x31
P_BUCLE = 0.10
PASO_EXPANSION = 3     # nodos expandidos por cuadro del GIF
PASO_RUTA = 1          # pasos de la ruta por cuadro del GIF
FPS = 10

LIBRE, PARED, INICIO, META, EXPANDIDO, RUTA = 0, 1, 2, 3, 4, 5
COLORES = ListedColormap(["white", "#333333", "#2ecc71", "#e74c3c", "#f8c471", "#3498db"])


def busqueda(inicio, meta, astar):
    """Replica A* (menor_h) o Dijkstra y devuelve (ruta, orden de expansión)."""
    orden = itertools.count()
    h = (lambda c: planner.manhattan(c, meta)) if astar else (lambda c: 0)
    abiertos = [(h(inicio), 0, next(orden), inicio)]
    padre = {inicio: None}
    costo = {inicio: 0}
    expandidos = []
    cerrados = set()

    while abiertos:
        _, _, _, actual = heapq.heappop(abiertos)
        if actual in cerrados:
            continue
        if actual == meta:
            return planner.reconstruir(padre, meta), expandidos
        cerrados.add(actual)
        expandidos.append(actual)

        for vecino in maze.neighbors(actual):
            nuevo = costo[actual] + 1
            if nuevo < costo.get(vecino, float("inf")):
                costo[vecino] = nuevo
                padre[vecino] = actual
                hv = h(vecino)
                heapq.heappush(abiertos, (nuevo + hv, hv, next(orden), vecino))

    return None, expandidos


def construir_cuadros(grid, inicio, meta, ruta, expandidos):
    """Lista de (matriz de colores, texto) con los cuadros de una búsqueda."""
    cuadros = []
    total_exp = len(expandidos)
    ks = list(range(0, total_exp, PASO_EXPANSION)) + [total_exp]

    for k in ks:
        m = grid.copy()
        for nodo in expandidos[:k]:
            m[nodo] = EXPANDIDO
        m[inicio] = INICIO
        m[meta] = META
        cuadros.append((m, f"Nodos expandidos: {k}"))

    mapa_final = cuadros[-1][0].copy()
    total_ruta = len(ruta) - 1
    ks_ruta = list(range(0, total_ruta, PASO_RUTA)) + [total_ruta]

    for k in ks_ruta:
        m = mapa_final.copy()
        for nodo in ruta[1:k + 1]:
            m[nodo] = RUTA
        m[inicio] = INICIO
        m[meta] = META
        cuadros.append((m, f"Ruta: {k} de {total_ruta} pasos"))

    return cuadros


def animar(cuadros_a, cuadros_d):
    n = max(len(cuadros_a), len(cuadros_d))
    fig, (ax_a, ax_d) = plt.subplots(1, 2, figsize=(10, 5.5))

    im_a = ax_a.imshow(cuadros_a[0][0], cmap=COLORES, vmin=-0.5, vmax=5.5)
    im_d = ax_d.imshow(cuadros_d[0][0], cmap=COLORES, vmin=-0.5, vmax=5.5)
    for ax in (ax_a, ax_d):
        ax.set_xticks([])
        ax.set_yticks([])
    ax_a.set_title("A* (criterio menor_h)")
    ax_d.set_title("Dijkstra")

    def actualizar(i):
        ca = cuadros_a[min(i, len(cuadros_a) - 1)]
        cd = cuadros_d[min(i, len(cuadros_d) - 1)]
        im_a.set_data(ca[0])
        im_d.set_data(cd[0])
        ax_a.set_xlabel(ca[1])
        ax_d.set_xlabel(cd[1])
        return im_a, im_d

    anim = FuncAnimation(fig, actualizar, frames=n, interval=1000 / FPS)
    archivo_gif = CAPTURAS / "etapa0_25_busqueda_comparacion.gif"
    anim.save(archivo_gif, writer=PillowWriter(fps=FPS))
    print("Animación guardada en:", archivo_gif)

    actualizar(n - 1)
    archivo_png = CAPTURAS / "etapa0_26_busqueda_final.png"
    fig.savefig(archivo_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Figura final guardada en:", archivo_png)


def verificar(grid, inicio, meta, ruta_a, exp_a, ruta_d, exp_d):
    with cp.mapa(grid):
        ruta_ref, exp_ref = planner.astar_detalle(inicio, meta, "menor_h")
        ruta_dref, exp_dref = dijkstra.dijkstra_detalle(inicio, meta)
    assert len(exp_a) == exp_ref and len(ruta_a) == len(ruta_ref)
    assert len(exp_d) == exp_dref and len(ruta_d) == len(ruta_dref)
    print("Verificación: la búsqueda coincide con planner.py y dijkstra.py")


def main():
    grid = gen.generar(N_CELDAS, SEMILLA, P_BUCLE)
    size = grid.shape[0]
    inicio, meta = (1, 1), (size - 2, size - 2)

    with cp.mapa(grid):
        ruta_a, exp_a = busqueda(inicio, meta, astar=True)
        ruta_d, exp_d = busqueda(inicio, meta, astar=False)

    verificar(grid, inicio, meta, ruta_a, exp_a, ruta_d, exp_d)
    print(f"A*: {len(exp_a)} nodos expandidos, {len(ruta_a) - 1} pasos")
    print(f"Dijkstra: {len(exp_d)} nodos expandidos, {len(ruta_d) - 1} pasos")

    cuadros_a = construir_cuadros(grid, inicio, meta, ruta_a, exp_a)
    cuadros_d = construir_cuadros(grid, inicio, meta, ruta_d, exp_d)
    animar(cuadros_a, cuadros_d)


if __name__ == "__main__":
    main()
