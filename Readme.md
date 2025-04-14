#### Setup the Project
`Requirements:`<br>
- `8 GB RAM`<br>
- `Code Editor` [VSCode](https://code.visualstudio.com/download)<br>
- `Git CLI` [Download](https://git-scm.com/downloads)<br>
- `Web Browser Chrome`<br>
- `python 3.11 or above`<br>

##### Update the name of `.env.example` to `.env` and update the `EMAIL_HOST_USER` & `EMAIL_HOST_PASSWORD`:
- [Visit](https://myaccount.google.com/apppasswords)

##### Create Virtual Environment for the Project
```
python -m venv env
```

##### Activate Virtual Enviroment & Prepare Database
```
.\env\Scripts\activate
python manage.py makemigrations
python manage.py migrate
python manage.py createroles
python manage.py collectstatic --no-input
```

###### Database setup is done now Create Admin User
```
python manage.py createsuperuser
```

###### InCase if you are getting error in above command so run the following Command in Powershell ISE
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
- Choose `Yes to All`
- And run the envionment activation commands

##### Run the Project
```
python manage.py runserver
```


###### Run Project with new Terminal
```
.\env\Scripts\activate
python manage.py runserver
```