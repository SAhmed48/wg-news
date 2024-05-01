# wg-news

# Initial Project setup
## create virtual envrionment using the following command:
python -m venv virtual_environment_name
### Activate Virtual environment
cd virtual_environment_name/Scripts

run activate

run pip install wagtail


### Go back to root folder
cd ../../ 

### setup project and install requirements
run wagtail start site_name

cd site_name

run pip install -e requirements.txt

run python manage.py makemigrations

run python manage.py migrate
