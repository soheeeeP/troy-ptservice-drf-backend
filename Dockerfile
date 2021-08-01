FROM python:3

WORKDIR usr/src/app
COPY . .
RUN pip3 install -r ./requirements.txt

RUN python3 ./manage.py makemigrations
RUN python3 ./manage.py migrate
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
