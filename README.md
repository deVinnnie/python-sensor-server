Master Thesis - IoT server
=========================


Loading Fixture Data
--------------------

`python manage.py loaddata dummy-data.json sensors.json`


Setup
-----

### Installing Dependencies

`pip install -r requirements.txt`

### Django Setup

`
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata dummy-data.json sensors.json measurements.json
python manage.py createsuperuser
`
