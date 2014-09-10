python geoserver/manage.py syncdb --settings=geoserver.settings.local
python geoserver/manage.py sql questions --settings=geoserver.settings.local
python geoserver/manage.py sql deptrees --settings=geoserver.settings.local
python geoserver/manage.py runserver --settings=geoserver.settings.local
