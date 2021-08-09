FROM python:3.9

RUN apt-get update
WORKDIR /app
COPY . .

ENV PATH="${PATH}:/root/.poetry/bin"
ENV POETRY_VIRTUALENVS_CREATE=false
COPY poetry.lock pyproject.toml /app/
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
&& poetry update \
&& poetry install

RUN pip3 install -r ./requirements.txt

RUN python3 ./manage.py makemigrations
RUN python3 ./manage.py migrate

ENV DJANGO_SETTINGS_MODULE Troy.settings.production
CMD ["python", "./manage.py", "runserver","0.0.0.0:8000"]
EXPOSE 8000
