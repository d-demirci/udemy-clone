FROM guacozy/guacozy-server 
RUN apk add py3-mysqlclient
RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev ;\
    pip install mysqlclient;\
    apk del .build-deps 

WORKDIR /app

COPY settings.py /app/guacozy/guacozy_server/guacozy_server/settings.py
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



# Django service
EXPOSE 8000 80 443

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
