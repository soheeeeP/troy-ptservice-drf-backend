FROM ubuntu:18.04
MAINTAINER Team. M-to-M

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    gdal-bin python3-gdal \
    curl apt-utils apt-transport-https \
    git \
    vim \
    python3.7 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    nginx \
    supervisor \
    mysql-client \
    libmysqlclient-dev \
    unixodbc-dev \
    sqlite3 \
    locales && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip setuptools
RUN apt-get install python3-setuptools
RUN pip3 install gunicorn[gevent]

WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt
ARG SETTINGS_ARG=production
ENV DJANGO_SETTINGS_MODULE Troy.settings.$SETTINGS_ARG
ENV SERVICE_ENV=$SERVICE_ARG
#RUN python3 ./manage.py migrate

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY .ci-cd/config/nginx/nginx.conf /etc/nginx/sites-available/default
COPY .ci-cd/config/nginx/supervisord.conf /etc/supervisor/conf.d/
EXPOSE 80
EXPOSE 443

CMD ["supervisord", "-n"]