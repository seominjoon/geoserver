# GeoServer
Web framework for GeoSolver

## Local server hosting: general instruction
1. Make sure you have Python 2 (tested on 2.7.6) and MySQL installed.
2. Clone this repository, as well as `geosolver` and `equationtree`. They have to be added to the `$PYTHONPATH`. 
3. Make sure the MySQL root acess credentials agrees with `DATABASES` in `geoserver/geoserver/settings/local.py`.
4. Log in to MySQL server and create a database `geodb` in MySQL:
```mysql
create database geodb;
```
5. Install all required packages for the server by typing on the terminal:
```bash
pip install numpy scipy scikit-learn sympy networkx nltk inflect pyparsing matplotlib pydot2 mysql-python django django-picklefield jsonfield django-storages boto django-modeldict pillow unipath beautifulsoup4 requests
```
6. Install OpenCV 3 (tested on 3.0.0). Make sure python wrappers are accessible via `$PYTHONPATH`.
7. Change directory to `geoserver/geoserver`. 
8. Type on the terminal: 
```python manage.py migrate --settings=geoserver.settings.local```
This will set up all tables in the `geodb` database.
9. To run the server, type on the terminal (in the same directory, `geoserver/geoserver`: 
```python manage.py runserver --settings=geoserver.settings.local```
Note that if you want to make the server visible to other computers, you specify the ip address to be `0`, i.e. `python manage.py runserver 0:8080 --settings=geoserver.settings.local` (`8080` is port number of your choice).
