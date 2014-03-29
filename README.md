bikestache
==========

bikestache is a web app that helps you find a place to park your bike.

About
==========

Built on postgres w\ postgris extension for geospatial searching. (neither of which i was familiar with before this project)
Uses psycopg2 as a postgres adapater.

Server side is Flask with SQLAlchemy w/ extension GeoAlchemy2.

Client is Javascript and some jQuery.

My first time using Flask as well but I thought I would try it out as a change of pace from Django (which I've been using at work for the last year) and cherrypy (which I play with in my freetime).

Backend Setup
==========

install postgresql and postgris
in psql:

```
CREATE TABLE bikestache( 
  id SERIAL PRIMARY KEY,
  location VARCHAR(128),
  address VARCHAR(128),
  bike_parking VARCHAR(128),
  placement VARCHAR(128),
  racks SMALLINT,
  spaces SMALLINT,
  latitude NUMERIC,
  longitude NUMERIC,
  geog GEOGRAPHY(Point)
); 

COPY bikestache(location,address,bike_parking,placement,racks,spaces,latitude,longitude) FROM <Bicycle_Parking__Public.csv> DELIMITER ',' CSV;

UPDATE bikestache
SET geog = ST_GeographyFromText('POINT(' || longitude || ' ' || latitude || ')');
```

QuickStart
==========

```
clone project
pip install -r requirements.txt
python app.py
```
