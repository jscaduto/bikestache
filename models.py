from sqlalchemy import Column, Integer, String, Float, func
from geoalchemy2 import Geography
from database import Base, db_session

METERS_PER_MILE = 1609.34


class BikeStache(Base):
    """Represents a bike rack (or bikestache)."""
    __tablename__ = 'bikestache'
    id = Column(Integer, primary_key=True)
    location = Column(String(200))
    address = Column(String(120))
    bike_parking = Column(String(120))
    placement = Column(String(50))
    racks = Column(Integer)
    spaces = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    geog = Column(Geography('POINT'))

    def __init__(self, location, latitude, longitude):
        """BikeStache object requires following properties.

        Arguments:
        location -- name of bikestache general location
        latitude/longitude -- bikestache coordinates in degrees
        """
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<BikeStache id:{0} name:{1} @({2},{3})>'.format(
            self.id,
            self.location,
            self.latitude,
            self.longitude)

    def as_dict(self):
        """Returns BikeStache object as a dictionary"""
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # remove 'geog' as it does not jsonify well
        del d['geog']
        return d


def find_closest_stache(lat, lng, dist=5):
    """Query bikestache table for closest rack within a given distance.

    Arguments:
    lat/lng -- origin coordinates in degrees

    Keyword Arguments:
    dist -- range in miles from origin (defaults 5)
    """
    meters = float(dist) * METERS_PER_MILE
    lng_lat = '{0} {1}'.format(lng, lat)
    geo_txt = 'SRID=4326;POINT({0})'.format(lng_lat)

    query = db_session.query(BikeStache)
    query = query.filter(func.ST_DWithin(BikeStache.geog,
                         func.ST_GeogFromText(geo_txt), meters))
    query = query.order_by(func.ST_Distance(BikeStache.geog,
                           func.ST_GeogFromText(geo_txt)))
    return query.first()
