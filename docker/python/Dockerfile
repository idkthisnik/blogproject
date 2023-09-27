FROM python:3


COPY ./docker/python/driver/freetds.conf blog/backend/etc/freetds/freetds.conf
COPY ./docker/python/driver/odbc.ini blog/backend/etc/odbc.ini
COPY ./docker/python/driver/odbcinst.ini blog/backend/etc/odbcinst.ini

RUN apt-get update && apt-get install -y unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc

COPY ./backend /blog/backend

WORKDIR /blog/backend

EXPOSE 14555

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "14555"]