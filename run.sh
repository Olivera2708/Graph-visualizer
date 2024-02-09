cd core
python setup.py install
cd ..

cd api
python setup.py install
cd ..

cd json_data_source
python setup.py install
cd ..

cd xml_data_source
python setup.py install
cd ..

cd SimpleVisualizer
python setup.py install
cd ..

cd BlockVisualizer
python setup.py install
cd ..

python GraphVisualizer/manage.py runserver