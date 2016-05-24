Master Thesis - IoT server
=========================


Loading Fixture Data
--------------------

`python manage.py loaddata dummy-data.json sensors.json`


Setup
-----

### Set up virtualenv and install Dependencies

`virtualenv -p /usr/bin/python3.3 env`
(p flag indicates the python version to use, must be installed on system)

Use `source env/bin/activate` to use the virtual environment.

Install dependencies:
`pip install -r requirements.txt`

### Django Setup

`
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata dummy-data.json sensors.json measurements.json
python manage.py createsuperuser
`
Running Development Server
--------------------------

`python manage.py runserver`