#### Setup the Project
`Requirements:`<br>
- `8 GB RAM`<br>
- `Code Editor VSCode / Pycharm`<br>
- `Git CLI`<br>
- `Docker Desktop`<br>
- `Web Browser Chrome`<br>
- `python 3.11 or above`<br>


#### Run Project via Docker
```
docker build -t . tmatrix
```


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
