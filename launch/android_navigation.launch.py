import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    nav_config_path = os.path.join(get_package_share_directory('android_navigation'),'config','config.yaml')

    return LaunchDescription([
        IncludeLaunchDescription(
            launch_description_source=([
                get_package_share_directory('android_localization'),
                '/launch/only_android_localization.launch.py'
            ])
        ),
        IncludeLaunchDescription(
            launch_description_source=([
                get_package_share_directory('android_bringup'),
                '/launch/android_bringup.launch.py'
            ]),
            launch_arguments={
                'params_file': nav_config_path
            }.items()
        ),
        IncludeLaunchDescription(
            launch_description_source=([
                get_package_share_directory('ldlidar_node'),
                '/launch/ldlidar_with_mgr.launch.py'
            ])
        ),
        IncludeLaunchDescription(
            launch_description_source=([
                get_package_share_directory('android_navigation'),
                '/launch/android_bringup.launch.py'
            ])
        ),
        Node(
            ## Configure the TF of the robot to the origin of the map coordinatesf
            package='tf2_ros',
            executable='static_transform_publisher',
            namespace='',
            output='screen',
            arguments=['0.046', '0.0', '0.107', '-1.5708', '0.0', '0.0', 'android_camera', 'ldlidar_base']
        )
        
    ])