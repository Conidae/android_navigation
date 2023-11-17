from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'android_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob('launch/*.launch.py')),
        (os.path.join('share',package_name,'config'),glob('config/*.yaml')),
        (os.path.join('share',package_name,'maps'),glob('maps/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='reita',
    maintainer_email='Conidae52@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cmd_gps_wp_node=android_navigation.cmd_gps_wp_node:main',
            'make_wp_enter_node=android_navigation.make_wp_enter_node:main'
        ],
    },
)
