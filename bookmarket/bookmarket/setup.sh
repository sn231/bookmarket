django-admin startproject bookmarket
cd bookmarket
python manage.py startapp books
python manage.py startapp users
python manage.py startapp messages
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser 