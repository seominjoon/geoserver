# export PYTHONPATH=$PYTHONPATH:/Library/Python/2.7/site-packages
# export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
# export PYTHONPATH=$PYTHONPATH:/usr/local/lib/wxPython-3.0.0.0/lib/python2.7/site-packages
# export PYTHONPATH=$PYTHONPATH:/usr/local/lib/wxPython-3.0.0.0/lib/python2.7/site-packages/wx-3.0-osx_cocoa
# export PYTHONPATH=$PYTHONPATH:/Users/minjoon/Documents/workspace/GeoSolver
# export PYTHONPATH=$PYTHONPATH:/Users/minjoon/Documents/workspace/TinyOCR
# export PYTHONPATH=$PYTHONPATH:/Users/minjoon/PycharmProjects/geosolver
python manage.py $1 $2 --settings=geoserver.settings.local
