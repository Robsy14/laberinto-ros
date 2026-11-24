"""Etapa 1 - Lanza Gazebo Harmonic con la plataforma de laberinto."""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg = get_package_share_directory("maze_platform")
    xacro_file = os.path.join(pkg, "urdf", "maze_platform.urdf.xacro")
    world_file = os.path.join(pkg, "worlds", "maze.sdf")
    rviz_file = os.path.join(pkg, "rviz", "maze.rviz")

    robot_description = Command(["xacro ", xacro_file])

    gui = LaunchConfiguration("gui")
    rviz = LaunchConfiguration("rviz")
    jsp_gui = LaunchConfiguration("jsp_gui")

    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": True,
        }],
    )

    jsp = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
        condition=IfCondition(jsp_gui),
    )

    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"
            ])
        ),
        launch_arguments={
            "gz_args": [world_file, " -r -v 4"],
            "on_exit_shutdown": "true",
        }.items(),
    )

    spawn = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic", "/robot_description",
            "-name", "maze_platform",
            "-z", "0.0",
        ],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/world/maze_world/model/maze_platform/joint_state"
            "@sensor_msgs/msg/JointState[gz.msgs.Model",
        ],
        remappings=[
            ("/world/maze_world/model/maze_platform/joint_state", "/joint_states"),
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_file],
        output="screen",
        condition=IfCondition(rviz),
        parameters=[{"use_sim_time": True}],
    )

    return LaunchDescription([
        DeclareLaunchArgument("gui", default_value="true"),
        DeclareLaunchArgument("rviz", default_value="false"),
        DeclareLaunchArgument("jsp_gui", default_value="true"),
        rsp,
        jsp,
        gz,
        spawn,
        bridge,
        rviz_node,
    ])
