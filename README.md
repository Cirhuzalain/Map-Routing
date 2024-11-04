# Map Routing

## Prerequisites
You need to have Python and pip install on your machine

## Clone the project
You can clone the repository with `git clone https://github.com/Cirhuzalain/Map-Routing.git`
After cloning the project use `cd Map-Routing/`

## Create and activate virtual environment
Use `virtualenv -p python3.10 env` and `source env/bin/activate` command

## Install Dependencies
Use `pip install -r requirements.txt` command and Add required environment variable (check routes/settings.py and getroutes/utils.py)

## Run the project
Use `python manage.py makemigrations` follow by `python manage.py migrate` and lastly `python manage.py runserver`

## Built with
* Django
* Google Routes API
* Geopy