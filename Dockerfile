FROM python:3.9
MAINTAINER Team. M-to-M

RUN apt-get update
RUN apt-get install -y gdal-bin python3-gdal
WORKDIR /app

ENV PATH="${PATH}:/root/.poetry/bin"
ENV POETRY_VIRTUALENVS_CREATE=false
COPY poetry.lock pyproject.toml /app/
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
RUN poetry config virtualenvs.create false \
    && poetry update \
    && poetry install --no-interaction --no-dev

COPY . .

# migration 파일은 로컬에서 생성 및 테스트 후 업로드한다.
# RUN python3 ./manage.py makemigrations
# RUN python3 ./manage.py migrate

ENV DJANGO_SETTINGS_MODULE Troy.settings.development

CMD ["uwsgi", "--ini", "uwsgi.ini"]
#CMD ["python", "./manage.py", "runserver","0.0.0.0:8000"]