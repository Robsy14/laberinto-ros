#!/usr/bin/env bash
# Etapa 1 - Captura una rafaga de imagenes de la VENTANA ACTIVA (Gazebo)
# y las junta en un GIF. Pensado para grabar la esfera rodando.
#
# Uso:  ./rafaga_gif.sh NN nombre  [n_frames] [intervalo_s] [espera_inicial_s]
# Ej:   ./rafaga_gif.sh 04 esfera_rueda 20 0.3 5
#
# Pasos: espera N s (para enfocar Gazebo), captura la ventana activa
#        n_frames veces, y genera etapa1_NN_nombre.gif
set -euo pipefail
NN="${1:?Falta numero (ej 04)}"
NOMBRE="${2:?Falta nombre (ej esfera_rueda)}"
FRAMES="${3:-20}"
INTERVALO="${4:-0.3}"
ESPERA="${5:-5}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"

echo "Enfoca la ventana de Gazebo. Empiezo en ${ESPERA} s..."
for s in $(seq "${ESPERA}" -1 1); do printf '  %s\r' "$s"; sleep 1; done
echo
echo "Capturando ${FRAMES} frames cada ${INTERVALO}s..."
for i in $(seq -w 1 "${FRAMES}"); do
  gnome-screenshot -w -f "${TMP}/f_${i}.png"
  printf '  frame %s/%s\r' "$i" "$FRAMES"
  sleep "${INTERVALO}"
done
echo

SALIDA_GIF="${DIR}/etapa1_${NN}_${NOMBRE}.gif"
echo "Generando GIF..."
convert -delay 20 -loop 0 -resize 800x "${TMP}"/f_*.png "${SALIDA_GIF}"
echo "GIF: ${SALIDA_GIF}"
# Guarda tambien el primer y ultimo frame como PNG (utiles para el informe)
cp "${TMP}/f_$(printf '%02d' 1).png" "${DIR}/etapa1_${NN}_${NOMBRE}_inicio.png" 2>/dev/null || true
ls "${TMP}"/f_*.png | tail -1 | xargs -I{} cp {} "${DIR}/etapa1_${NN}_${NOMBRE}_fin.png"
rm -rf "${TMP}"
echo "Listo."
