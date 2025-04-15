#### Project Preview

<img src='project_images/home.png' height=380>
<img src='project_images/login.png' height=380>
<img src='project_images/calculator.png' height=380>

#### Setup the Project
`Requirements:`<br>
- `8 GB RAM`<br>
- `Code Editor` [VSCode](https://code.visualstudio.com/download)<br>
- `Git CLI` [Download](https://git-scm.com/downloads)<br>
- `python 3.11 or above` [Download](https://www.python.org/downloads/release/python-3110/)<br>
- `Web Browser Chrome`<br>

##### Open the Project to `VS Code` or Any `Other IDE`

##### Update the file name of `.env.example` to `.env` and update the `EMAIL_HOST_USER` & `EMAIL_HOST_PASSWORD`:
- Obtain Your App Password from here : [Visit](https://myaccount.google.com/apppasswords)
- * You can skip the email setting by keeping it as default


##### Open Integrated Terminal in IDE for running Following Commands
##### Create Virtual Environment for the Project
```
python -m venv env
```

##### Activate Virtual Enviroment
```
.\env\Scripts\activate
```
###### InCase if you are getting error in above command so run the following Command in Powershell ISE
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
- Choose `Yes to All`
- And run the envionment activation commands


##### Download the Dependencies
```
pip install -r requirements.txt
```

##### Prepeare DataBase
```
python manage.py makemigrations
python manage.py migrate
python manage.py createroles
```

###### Database setup is done now Create Admin User
```
python manage.py createsuperuser
```

##### Run the Project
```
python manage.py runserver
```


###### Run Project with new Terminal
```
.\env\Scripts\activate
python manage.py runserver
```

##### Visit Project Website: [URL](http://127.0.0.1:8000/)
##### Visit Project's Live Website: [URL](https://tonnamatrix.nikhivishwa.tech/)