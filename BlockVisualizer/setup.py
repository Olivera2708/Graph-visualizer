from setuptools import find_packages, setup

setup(
    name='BlockVisualizer',
    version='0.1',
    packages=find_packages(),
    package_data={'blockVisualizer': ['templates/*.html']},
    entry_points={
        'visualizer':
            ['load_json=blockVisualizer.blockVisualizer:BlockVisualizer'],
    },
    zip_safe=False
)
