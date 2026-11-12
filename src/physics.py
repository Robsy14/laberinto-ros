"""Modelo físico simplificado de la esfera sobre la plataforma (Etapa 0).

Convención: un ángulo positivo en un eje inclina la plataforma de modo que
la esfera acelera en el sentido positivo de ese eje.

La esfera maciza rueda sin deslizar, así que su aceleración a lo largo de la
pendiente es a = (5/7) g sen(theta). Los ángulos se usan en radianes.
"""

import math

G = 9.81
K_ESFERA = 5.0 / 7.0  # esfera maciza rodando sin deslizar


def aceleracion(theta_rad):
    """Aceleración a lo largo de un eje, en m/s², para un ángulo en radianes."""
    return K_ESFERA * G * math.sin(theta_rad)


def simular(theta_x, theta_y, t_total=0.5, dt=0.001,
            pos0=(0.0, 0.0), vel0=(0.0, 0.0)):
    """Integra el movimiento con inclinación constante (Euler semi-implícito).

    theta_x, theta_y en radianes. Devuelve un diccionario con listas de
    tiempo, posición (m) y velocidad (m/s) en cada paso.
    """
    ax = aceleracion(theta_x)
    ay = aceleracion(theta_y)

    x, y = pos0
    vx, vy = vel0
    n_pasos = int(round(t_total / dt))

    resultado = {"t": [0.0], "x": [x], "y": [y], "vx": [vx], "vy": [vy]}
    for i in range(1, n_pasos + 1):
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        resultado["t"].append(i * dt)
        resultado["x"].append(x)
        resultado["y"].append(y)
        resultado["vx"].append(vx)
        resultado["vy"].append(vy)
    return resultado

