from setuptools import setup, find_packages

setup(
    name="xml_data_source",
    version="0.1",
    packages=find_packages(),
    entry_points={"data_source": ["xml_data_source=xml_data_source.data_source_loader:XMLDataSourceLoader"]},
    zip_safe=False
)
