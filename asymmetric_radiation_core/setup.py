import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'asymmetric_radiation_core'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*.npy') + glob('maps/*.json') + glob('maps/*.csv')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='oleksandr',
    maintainer_email='proskurin1408@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'radiation_field_server = asymmetric_radiation_core.radiation_field_server:main',
            'baseline_field_server = asymmetric_radiation_core.baseline_field_server:main',
            'virtual_geiger = asymmetric_radiation_core.virtual_geiger:main',
            'dose_logger = asymmetric_radiation_core.dose_logger:main',
            'generate_map = asymmetric_radiation_core.generate_map:main',
            'view_map = asymmetric_radiation_core.view_map:main',
            'radiation_mapper = asymmetric_radiation_core.radiation_mapper:main',
            'ground_truth_logger = asymmetric_radiation_core.ground_truth_logger:main',
            'radiation_run_logger = asymmetric_radiation_core.radiation_run_logger:main',
        ],
    },
)
