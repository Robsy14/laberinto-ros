#!/usr/bin/env bash
# Etapa 1 - Ayudante de capturas con gnome-screenshot.
# Uso:  ./capturar.sh NN nombre_corto [segundos_de_espera]
# Ej:   ./capturar.sh 01 modelo_cargado 5
set -euo pipefail
NN="${1:?Falta el numero de captura (ej. 01)}"
NOMBRE="${2:?Falta el nombre corto (ej. modelo_cargado)}"
ESPERA="${3:-5}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SALIDA="${DIR}/etapa1_${NN}_${NOMBRE}.png"
echo "Captura: ${SALIDA}"
echo "Cambia a la ventana que quieras capturar. Disparo en ${ESPERA} s..."
for s in $(seq "${ESPERA}" -1 1); do printf '  %s\r' "$s"; sleep 1; done
echo
gnome-screenshot -f "${SALIDA}"
echo "Guardada: ${SALIDA}"
