import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node

def generate_launch_description():
    maps_dir_arg = DeclareLaunchArgument(
        'maps_dir',
        default_value=os.path.expanduser('~/ros2_ws/src/Asymmetric-radiation/asymmetric_radiation_core/maps'),
        description='Directory containing radiation maps'
    )
    map_path_arg = DeclareLaunchArgument(
        'map_path',
        default_value='explored_map.npy',
        description='Map file name or absolute path'
    )
    sensor_map_path_arg = DeclareLaunchArgument(
        'sensor_map_path',
        default_value='radiation_map_complex.npy',
        description='Path to the true radiation field for virtual geiger sensor'
    )
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    
    use_virtual_geiger_arg = DeclareLaunchArgument(
        'use_virtual_geiger',
        default_value='true',
        description='Start the simulated geiger counter (set to false on real robot)'
    )

    use_alara_reflex_arg = DeclareLaunchArgument(
        'use_alara_reflex',
        default_value='false',
        description='Enable or disable the ALARA speed reflex plugin'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    radiation_field_server_node = Node(
        package='asymmetric_radiation_core',
        executable='radiation_field_server',
        name='radiation_field_server',
        output='screen',
        parameters=[{
            'maps_dir': LaunchConfiguration('maps_dir'),
            'map_path': LaunchConfiguration('map_path'),
            'use_sim_time': False
        }]
    )

    radiation_mapper_node = Node(
        package='asymmetric_radiation_plugins',
        executable='radiation_mapper_node',
        name='radiation_mapper',
        output='screen',
        parameters=[{
            'maps_dir': LaunchConfiguration('maps_dir'),
            'map_path': LaunchConfiguration('map_path'),
            'use_sim_time': False,
            'worker_use_sim_time': use_sim_time
        }]
    )

    alara_reflex_node = Node(
        package='asymmetric_radiation_plugins',
        executable='alara_speed_reflex_node',
        name='alara_speed_reflex_node',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_alara_reflex')),
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    virtual_geiger_node = Node(
        package='asymmetric_radiation_plugins',
        executable='virtual_geiger_node',
        name='virtual_geiger',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_virtual_geiger')),
        parameters=[{
            'maps_dir': LaunchConfiguration('maps_dir'),
            'map_path': LaunchConfiguration('sensor_map_path'),
            'use_sim_time': False,
            'worker_use_sim_time': use_sim_time
        }]
    )

    return LaunchDescription([
        maps_dir_arg,
        map_path_arg,
        sensor_map_path_arg,
        use_sim_time_arg,
        use_virtual_geiger_arg,
        use_alara_reflex_arg,
        radiation_field_server_node,
        radiation_mapper_node,
        virtual_geiger_node,
        alara_reflex_node
    ])
