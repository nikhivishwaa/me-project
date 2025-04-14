FROM python:3.12-alpine

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py createroles

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000"]