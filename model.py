import config
# import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

Base = declarative_base()
# Base.query = session.query_property()

ENGINE = None
Session = None

def connect():
    global engine
    global Session

    engine = create_engine("sqlite:///listings.db", echo=False)
    Session = sessionmaker(bind=engine)

    return Session()

def create_tables():
    engine = create_engine("sqlite:///listings.db", echo=False)
    Base.metadata.create_all(engine)

class Listings(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True)
    list_date = Column(DateTime, nullable=False)
    pending_date = Column(DateTime, nullable=True)
    close_escrow_date = Column(DateTime, nullable=True)
    listing_status = Column(String(15), nullable=False)
    list_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=True)
    property_type = Column(String(64), nullable=False)
    bathrooms_count = Column(Integer, nullable=True)
    bedrooms_count = Column(Integer, nullable=True)
    living_sq_ft = Column(Integer, nullable=True)
    lot_size = Column(Integer, nullable=True)
    address = Column(String(64), nullable=True)
    street_name = Column(String(64), nullable=True)
    street_suffix = Column(String(15), nullable=True)
    street_number = Column(String(64), nullable=True)
    county_name = Column(String(64), nullable=True)
    postal_code = Column(String(15), nullable=True)
    city_name = Column(String(64), nullable=True)
    neighborhood = Column(String(64), nullable=True)
    mls_id = Column(String(64), nullable=True)
    description = Column(String(1000), nullable=True)
    parcel_number = Column(String(15), nullable=True)
    state = Column(String(15), nullable= True)
    full_address = Column(String(64), nullable= True)
    latitude = Column(Integer, nullable=True)
    longitude = Column(Integer, nullable=True)
    county_id = Column(Integer, nullable=True)
    zip_id = Column(Integer, nullable=True)
    bg_id = Column(Integer, nullable=True)

class Neighborhoods(Base):
    __tablename__ = "neighborhoods"
    
    id = Column(Integer, primary_key=True)
    state = Column(String(15), nullable=False)
    county = Column(String(64), nullable=False)
    city = Column(String(64), nullable=False)
    neighborhood = Column(String(64), nullable=False)
    neighborhood_id = Column(String(64), nullable=False)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(String(10000), nullable=False)
    coordinates = Column(String(10000), nullable=False) 

class Counties(Base):
    __tablename__ = "counties"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(String(15), nullable=True)
    state = Column(String(15), nullable=True)
    county = Column(String(15), nullable=True)
    name = Column(String(15), nullable=False)
    lsad = Column(String(50), nullable=False)
    censusarea = Column(String(50), nullable=False)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(String(10000), nullable=False)
    coordinates = Column(String(10000), nullable=False) 

class Zipcodes(Base):
    __tablename__ = "zipcodes"
    
    id = Column(Integer, primary_key=True)   
    zcta = Column(String(100), nullable=True)
    geoid = Column(String(100), nullable=True)
    classfp = Column(String(100), nullable=True)
    mtfcc = Column(String(100), nullable=True)
    # funcstat = Column(String(15), nullable=True)
    # aland = Column(String(15), nullable=True)
    # awater = Column(String(15), nullable=True)
    # intptlat = Column(String(15), nullable=True)
    # intptlon = Column(String(15), nullable=True)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(String(10000), nullable=False)
    coordinates = Column(String(10000), nullable=False) 


class Blockgroups(Base):
    __tablename__ = "blockgroups"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(String(15), nullable=True)
    state = Column(String(15), nullable=True)
    county = Column(String(15), nullable=True)
    tract = Column(String(15), nullable=True)
    blockgroup = Column(String(15), nullable=True)
    name = Column(String(15), nullable=True)
    lsad = Column(String(15), nullable=True)
    censusarea = Column(String(15), nullable=True)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(String(10000), nullable=False)
    coordinates = Column(String(10000), nullable=False) 


# class Vertices(Base):
#     __tablename__ = "polygons"
    
    # def to_json(self):
    #     self_dict =  {
    #             "address" : self.address,

    #         }

    #     return JSON.dumps(self_dict)


if __name__ == "__main__":
    create_tables()
    # session = connect()


    # session = Session()
