# Etapa 1 — Modelo del entorno en Gazebo

Paquete ROS 2 (`maze_platform`) con el modelo de la plataforma inclinable de
2 GDL, el laberinto 7x7 y la esfera, para ROS 2 Jazzy + Gazebo Harmonic.

## Archivos
- `urdf/maze_platform.urdf.xacro`: base -> joint_x -> marco -> joint_y ->
  plataforma + 16 paredes + bordes. Limites de +-8 grados. Plugins de gz-sim.
- `worlds/maze.sdf`: mundo con fisica a 1 ms, gravedad y esfera de 20 mm en S.
- `launch/display.launch.py`: Gazebo + robot_state_publisher + spawn + bridge.
- `rviz/maze.rviz`: vista con RobotModel y TF.

## Correspondencia con la Etapa 0
Las 16 paredes se generan 1:1 desde la matriz MAZE de src/maze.py:
  celda (r,c) -> x=(c-3)*0.040 ; y=(3-r)*0.040
  S=(0,0) -> (-0.120, 0.120) ; G=(6,6) -> (0.120, -0.120)

## Compilar y ejecutar
    cd ros2_ws
    source /opt/ros/jazzy/setup.bash
    colcon build --packages-select maze_platform
    source install/setup.bash
    ros2 launch maze_platform display.launch.py

## Pruebas de la Etapa 1
1. El modelo se carga en Gazebo sin errores.
2. Rotacion de articulaciones (+-8 grados):
     gz topic -t /cmd_joint_x -m gz.msgs.Double -p 'data: 0.1396'
     gz topic -t /cmd_joint_y -m gz.msgs.Double -p 'data: -0.1396'
     gz topic -t /cmd_joint_x -m gz.msgs.Double -p 'data: 0.0'
3. La esfera rueda, choca con las paredes y responde a la gravedad.
4. Ajuste de masa/friccion/paso (1 ms) para acercarse a la Etapa 0.

## Capturas y video
    ../../capturas/etapa1/capturar.sh 01 modelo_cargado
    ../../capturas/etapa1/capturar.sh 02 articulacion_x_8grados 8
    # Video: Ctrl+Alt+Shift+R (grabador de GNOME). Mover de ~/Videos a videos/etapa1/.
