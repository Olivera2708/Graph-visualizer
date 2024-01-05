from setuptools import find_packages, setup

setup(
    name='SimpleVisualization',
    version='0.1',
    packages=find_packages(),
    package_data={'simpleVisualizer': ['templates/*.html']},
    entry_points={
        'visualizer':
            ['load_json=simpleVisualizer.simpleVisualizer:SimpleVisualisation'],
    },
    zip_safe=False
)
