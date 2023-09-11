FROM python:3.10

WORKDIR /catalog

COPY requirements.txt /catalog/
RUN pip install -r requirements.txt

COPY . /catalog/

RUN python music_catalog/manage.py makemigrations
RUN python music_catalog/manage.py migrate

CMD ["python", "music_catalog/manage.py", "runserver", "0.0.0.0:8000"]
