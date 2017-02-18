# GeoServer
Web framework for GeoSolver. Currently, you can use this to access our geometry question dataset. 
Raw data in JSON format is available [here](http://seominjoon.github.io/geosolver).

## Local server hosting: general instruction
1. Make sure you have Python 2 (tested on 2.7.6).
2. Install mysql dependencies:
```
sudo apt-get install mysql-server libmysqlclient-dev
```
To start server, run `sudo /etc/init.d/mysql start`, and to enter console, `sudo mysql -u root -p`.

3. Clone this repository, as well as `geosolver` and `equationtree`. They have to be added to the `$PYTHONPATH`. 
4. Make sure the MySQL root acess credentials agrees with `DATABASES` in `GeoServer/geoserver/geoserver/settings/local.py`.
5. Log in to MySQL server and create a database `geodb` in MySQL: 

  ```mysql
  create database geodb;
  ```
  
  If you already have `geodb`, make sure to drop it before creating it (by `drop database geodb`), or come up with a new name (e.g. `geodb2`) and update the database name in `GeoServer/geoserver/geoserver/settings/local.py`.
  
6. Install all required packages for the server by typing on the terminal: 
  
  ```bash
  pip install -r requirements.txt
  ```
  
6. Install OpenCV 3 (tested on 3.0.0). Make sure python wrappers are accessible via `$PYTHONPATH`.
 Refer to this: `https://www.learnopencv.com/install-opencv-3-on-yosemite-osx-10-10-x/` and `https://milq.github.io/install-opencv-ubuntu-debian/`

7. Change directory to `GeoServer/geoserver`. 
8. Type on the terminal: 
  ```bash
  python manage.py migrate --settings=geoserver.settings.local
  ```
  This will set up all tables in the `geodb` database.

9. To run the server, type on the terminal (in the same directory, `GeoServer/geoserver`): 
  ```bash
  python manage.py runserver --settings=geoserver.settings.local
  ```

  You should see something like `Starting development server at http://127.0.0.1:8000`.
  Note that if you want to make the server visible to other computers, you specify the ip address to be `0`, i.e. `python manage.py runserver 0:8080 --settings=geoserver.settings.local` (`8080` is port number of your choice).
  
10. Check if everything is good by accessing `http://localhost:8000/questions/list/all`. You should see a webpage with an empty table.

## Loading dumped data
Now that you have server running, you want to load data on it (otherwise you will have to upload every question yourself!).

1. Download the media folder, which contains all the images: [media.tar.gz](https://s3-us-west-2.amazonaws.com/geosolver-server/dump/68bd697ca57cdac1f2738a8d7e468fdccd7e5545/media.tar.gz)
2. Unzip the media folder in GeoServer/geoserver (so that you have GeoServer/geoserver/media folder).
3. Download json files, which contain text data and links to the images:
[questions.json](https://s3-us-west-2.amazonaws.com/geosolver-server/dump/68bd697ca57cdac1f2738a8d7e468fdccd7e5545/questions.json)
[labels.json](https://s3-us-west-2.amazonaws.com/geosolver-server/dump/68bd697ca57cdac1f2738a8d7e468fdccd7e5545/labels.json)
[semantics.json](https://s3-us-west-2.amazonaws.com/geosolver-server/dump/68bd697ca57cdac1f2738a8d7e468fdccd7e5545/semantics.json)
4. Text data can be loaded with the json files in GeoServer/geoserver:

  ```bash
  python manage.py loaddata questions.json --settings=geoserver.settings.local
  python manage.py loaddata labels.json --settings=geoserver.settings.local
  python manage.py loaddata semantics.json --settings=geoserver.settings.local
  ```
  
4. Now you should be able to see questions when accessing `http://localhost:8000/questions/list/all`.

## Tags
- aaai: 67 training high school questions from AAAI 2014 paper
- practice: 64 practice SAT questions from EMNLP 2015 paper
- official: 55 official SAT questions from EMNLP 2015 paper
- all: everything in the dataset

If you want to look at TAG questions, go to `http://localhost:8000/questions/list/TAG`. (e.g. `http://localhost:8000/questions/list/practice`). 

If you want to look at both practice and official questions, go to `http://localhost:8000/questions/list/practice+official`.

if you want to look at questions by their ids: `http://localhost:8000/questions/list/963+968+969/`

## Manually adding data
If you are adding your own data, see the following instructions.

### Common (training or testing)
1. Add question: Go to `http://localhost:8000/questions/upload`. Check "HasChoices" if the question is a multiple-choice question. Answer is always numeric. if "HasChoices", enter 1 for first choice, 2 for second choice, and so on.
2. Add choices: Go to `http://localhost:8000/questions/upload/choice`. For number, 1 means it is the first choice, 2 means it is the second choice, and so on.
3. Try to find your new question in `http://localhost:8000/quetions/list/all`.
4. You can also use `geosolver.database.geoserver_interface.upload_question` for automating these uploads with text files.

Note that there are a few conventions for writing equations in text. For special characters such as "pi" or "degree", use `\pi` and `\degree`. For now, you need to explicitly include `*` whenever there is multiplication betwee two numbers or variables. Use `/` for division. We advise you to look at existing questions (`questions/list/all`) for reference. You can also view/edit `geosolver.expression.expression_parser` (note that currently our expression parser is based on deterministic CFG). 

### Training
Training questions require the logical forms annotated. Go to `http://localhost:8000/semantics/list/all/`. 
Click "Annotate" on the Action column (right) to annotate/update the logical forms of existing questions.

### Testing
Testing questions require the OCR labels annotated. Go to `http://localhost:8000/labels/list/all/`. 
Click "Annotate" on the Action column (right) to annotate/update the labels of existing questions. 
The "Text" field shows the labels recorded for the selected question, where "type" refers to the entity type of the label.
There are several possible types:

1. "point": label for point
2. "line": label for line (e.g. l)
3. "length line": label for length of line (e.g. 4, x)
4. "angle": label for angle
5. "angle angle": label for measure of angle (e.g. 90 degree sign, 40 degrees, x degrees, etc.)
6. "angle arc": label for the measure of the angle of arc
Distictions among #3-6 could be confusing, and it will be probably better to take a look at existing labels to learn about them.

In order to record, you can either directly manipulate the JSON in the "Text" field, or: 1. click a label on the image. 2. type in the label in English in the first box. 3. type in the "entity type" in the second box. 4. Click "Click". Then the label will be automatically added to the JSON. 

When you are done annotating everything, click "Upload".

## Ubuntu helps
* To meet the python and MySQL requirements, run:
  
  ```bash
  apt-get install python mysql-server libmysqlclient-dev
  ```
  
* If you are going to install numpy / scipy via pip, you want to install:
  
  ```bash
  apt-get install gfortran
  ```
  
* To log-in to MySQL, run:
  
  ```bash
  mysql -u root -p
  ```
  
* To change MySQL password:
  1. stop the mysql server: `sudo /etc/init.d/mysql stop`
  2. start the mysqld configuration: `sudo mysqld --skip-grant-tables &`
  3. log in to MySQL as root: `mysql -u root mysql`
  4. replace YOURNEWPASSWORD with your new password: `UPDATE user SET Password=PASSWORD('YOURNEWPASSWORD') WHERE User='root'; FLUSH PRIVILEGES; exit;`
  5. kill the temporary server: `sudo killall -9 mysqld ?`
  6. start the normal server: `sudo service mysql start`

