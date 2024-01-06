from setuptools import setup, find_packages

setup(
    name="json_data_source",
    version="0.1",
    packages=find_packages(),
    entry_points={"data_source": ["json_data_source=json_data_source.data_source_loader:JsonDataSourceLoader"]},
    zip_safe=False
)
