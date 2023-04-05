export PYTHONPATH=$(pwd)/src/app
python -m unittest discover -s src/tests/ -v
