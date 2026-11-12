"""Controlador PD por eje con punto de anticipación (Etapa 0).

Cada eje recibe una inclinación theta (rad) y la esfera acelera con
physics.aceleracion(theta). El controlador calcula:

    theta = Kp * e - Kd * v_filtrada

con las ganancias de un sistema de segundo orden:

    Kp = omega_n^2 / (k g)
    Kd = 2 zeta omega_n / (k g)

donde k g = (5/7) g.

La física usa la posición real. El controlador solo ve una medición de la
posición, afectada opcionalmente por ruido gaussiano (parámetro ruido).
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parent))
import maze
import physics

TAMANO_CELDA = 0.040          # m
RADIO_ESFERA = 0.010          # m
LIMITE_ANG = math.radians(8)  # rad
TOL_WAYPOINT = 0.005          # m: distancia para dar por alcanzado un punto
K_G = physics.K_ESFERA * physics.G


def cell_a_xy(cell):
    """Centro de una celda en metros. La fila 0 queda arriba."""
    r, c = cell
    filas = maze.MAZE.shape[0]
    return ((c + 0.5) * TAMANO_CELDA, (filas - r - 0.5) * TAMANO_CELDA)


def ruta_escalon():
    """Ruta de prueba: 40 mm en x, sobre la fila inferior del laberinto."""
    return [(0.02, 0.02), (0.06, 0.02)]


def ganancias(omega_n=4.0, zeta=0.7):
    kp = omega_n ** 2 / K_G
    kd = 2 * zeta * omega_n / K_G
    return kp, kd


def comando(error, velocidad, kp, kd):
    """Inclinación de un eje (rad), saturada a ±8°."""
    theta = kp * error - kd * velocidad
    return max(-LIMITE_ANG, min(LIMITE_ANG, theta))


def choca(x, y):
    """True si la esfera invade una pared o sale del tablero."""
    filas, cols = maze.MAZE.shape
    if x < 0 or y < 0 or x > cols * TAMANO_CELDA or y > filas * TAMANO_CELDA:
        return True

    c0 = int(x // TAMANO_CELDA)
    r0 = filas - 1 - int(y // TAMANO_CELDA)
    for r in range(r0 - 1, r0 + 2):
        for c in range(c0 - 1, c0 + 2):
            if 0 <= r < filas and 0 <= c < cols and maze.MAZE[r, c] == 1:
                xmin = c * TAMANO_CELDA
                xmax = xmin + TAMANO_CELDA
                ymin = (filas - 1 - r) * TAMANO_CELDA
                ymax = ymin + TAMANO_CELDA
                dx = max(xmin - x, 0.0, x - xmax)
                dy = max(ymin - y, 0.0, y - ymax)
                if math.hypot(dx, dy) < RADIO_ESFERA:
                    return True
    return False


def seguir(ruta, t_max=8.0, dt=0.001, omega_n=4.0, zeta=0.7, tau_v=0.01,
           ruido=0.0, semilla=None):
    """Simula el seguimiento de una ruta (lista de puntos en metros).

    ruido: desviación estándar (m) del error de medición de la posición.
    semilla: semilla del generador aleatorio, para repetir resultados.

    La velocidad usada por el PD pasa por un filtro de primer orden de
    constante tau_v. Devuelve el historial, si llegó a la meta, si hubo
    colisión y el tiempo.
    """
    kp, kd = ganancias(omega_n, zeta)
    alpha = dt / (tau_v + dt)
    ultimo = len(ruta) - 1
    meta = ruta[-1]
    rng = np.random.default_rng(semilla)

    x, y = ruta[0]
    vx = vy = 0.0
    vfx = vfy = 0.0
    idx = 0
    llego = False
    colision = False
    hist = {"t": [], "x": [], "y": [], "thx": [], "thy": [], "ex": [], "ey": []}

    t = 0.0
    for _ in range(int(round(t_max / dt))):
        if ruido > 0:
            mx = x + rng.normal(0.0, ruido)
            my = y + rng.normal(0.0, ruido)
        else:
            mx, my = x, y

        while idx < ultimo and math.hypot(ruta[idx][0] - mx, ruta[idx][1] - my) < TOL_WAYPOINT:
            idx += 1
        ox, oy = ruta[idx]
        ex, ey = ox - mx, oy - my
        thx = comando(ex, vfx, kp, kd)
        thy = comando(ey, vfy, kp, kd)

        vx += physics.aceleracion(thx) * dt
        vy += physics.aceleracion(thy) * dt
        x += vx * dt
        y += vy * dt
        vfx += alpha * (vx - vfx)
        vfy += alpha * (vy - vfy)
        t += dt

        hist["t"].append(t)
        hist["x"].append(x)
        hist["y"].append(y)
        hist["thx"].append(thx)
        hist["thy"].append(thy)
        hist["ex"].append(ex)
        hist["ey"].append(ey)

        if choca(x, y):
            colision = True
            break
        if (idx == ultimo
                and math.hypot(meta[0] - x, meta[1] - y) < 0.002
                and math.hypot(vx, vy) < 0.002):
            llego = True
            break

    return {"hist": hist, "llego": llego, "colision": colision, "tiempo": t}
