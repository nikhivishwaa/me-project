```
.\env\Scripts\activate
cd .\meapp\
python manage.py runserver
```

##### cloud eunning commands

```
sudo su
```
```
cd /var/www/Mechanical-Project
```
```
git pull git@github.com:nikhivishwaa/me-project.git
```
```
source prodenv/bin/activate
cd meapp/
pip install -r requirements.txt
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py collectstatic --noinput
```
```
yes
```
```
python manage.py runserver
```

```
deactivate
```

```
a2dissite 000-default.conf
a2ensite 000-default.conf
service apache2 restart
```