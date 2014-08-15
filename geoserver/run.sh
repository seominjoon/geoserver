python manage.py syncdb --settings=geoserver.settings.local
python manage.py sql questions --settings=geoserver.settings.local
python manage.py sql deptrees --settings=geoserver.settings.local
python manage.py runserver --settings=geoserver.settings.local
