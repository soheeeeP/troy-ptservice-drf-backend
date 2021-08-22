FROM nginx:latest

COPY .config/nginx/nginx.conf /usr/local/etc/nginx/nginx.conf

COPY .config/nginx/nginx-troy.conf /usr/local/etc/nginx/sites-available/

RUN mkdir -p /usr/local/etc/nginx/sites-enabled/\
    && ln -s /usr/local/etc/nginx/sites-available/nginx-app.conf /usr/local/etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]