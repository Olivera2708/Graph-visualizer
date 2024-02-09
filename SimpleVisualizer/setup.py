from setuptools import find_packages, setup

setup(
    name='SimpleVisualizer',
    version='0.1',
    packages=find_packages(),
    package_data={'simpleVisualizer': ['templates/*.html']},
    entry_points={
        'visualizer':
            ['simple_visualizer=simpleVisualizer.simpleVisualizer:SimpleVisualizer'],
    },
    zip_safe=False
)
