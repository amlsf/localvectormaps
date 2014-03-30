#TODO move postgres password to environment
# TODO add relations
# Change region ids to use US census burea geoids

import config
import os
# import bcrypt
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import text, func
from sqlalchemy.dialects.postgresql import FLOAT, DOUBLE_PRECISION, VARCHAR

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

from flask.ext.login import UserMixin

Base = declarative_base()
# Base.query = session.query_property()

ENGINE = None
Session = None

def connect():
    global engine
    global Session

    engine = create_engine("postgresql+psycopg2://postgres:ratcatdog1@localhost/postgres", echo=False)
# Use this for heroku
    # engine = create_engine(os.environ.get("DATABASE_URL"), echo=False)
    # engine = create_engine("sqlite:///listings.db", echo=False)

    Session = sessionmaker(bind=engine)

    return Session()

def create_tables():
    engine = create_engine("postgresql+psycopg2://postgres:ratcatdog1@localhost/postgres", echo=False)
# Use this for heroku
    # engine = create_engine(os.environ.get("DATABASE_URL"), echo=False)
    # engine = create_engine("sqlite:///listings.db", echo=False)

    Base.metadata.create_all(engine)

class Listings(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True)
    list_date = Column(DateTime, nullable=False)
    pending_date = Column(DateTime, nullable=True)
    close_escrow_date = Column(DateTime, nullable=True)
    listing_status = Column(VARCHAR, nullable=False)
    list_price = Column(Integer, nullable=False)
    sell_price = Column(Integer, nullable=True)
    property_type = Column(VARCHAR, nullable=False)
    bathrooms_count = Column(Integer, nullable=True)
    bedrooms_count = Column(Integer, nullable=True)
    living_sq_ft = Column(Integer, nullable=True)
    lot_size = Column(Integer, nullable=True)
    address = Column(VARCHAR, nullable=True)
    street_name = Column(VARCHAR, nullable=True)
    street_suffix = Column(VARCHAR, nullable=True)
    street_number = Column(VARCHAR, nullable=True)
    county_name = Column(VARCHAR, nullable=True)
    postal_code = Column(VARCHAR, nullable=True)
    city_name = Column(VARCHAR, nullable=True)
    neighborhood = Column(VARCHAR, nullable=True)
    mls_id = Column(VARCHAR, nullable=True)
    description = Column(VARCHAR, nullable=True)
    parcel_number = Column(VARCHAR, nullable=True)
    state = Column(VARCHAR, nullable= True)
    full_address = Column(VARCHAR, nullable= True)
    latitude = Column(DOUBLE_PRECISION, nullable=True)
    longitude = Column(DOUBLE_PRECISION, nullable=True)
    # nb_id = Column(Integer, nullable=True)
    county_id = Column(Integer, nullable=True)
    zip_id = Column(Integer, nullable=True)
    bg_id = Column(Integer, nullable=True)


class Neighborhoods(Base):
    __tablename__ = "neighborhoods"
    
    id = Column(Integer, primary_key=True)
    state = Column(VARCHAR, nullable=False)
    county = Column(VARCHAR, nullable=False)
    city = Column(VARCHAR, nullable=False)
    neighborhood = Column(VARCHAR, nullable=False)
    neighborhood_id = Column(VARCHAR, nullable=False)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(VARCHAR, nullable=False)
    coordinates = Column(VARCHAR, nullable=False) 

class Counties(Base):
    __tablename__ = "counties"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(VARCHAR, nullable=True)
    state = Column(VARCHAR, nullable=True)
    county = Column(VARCHAR, nullable=True)
    name = Column(VARCHAR, nullable=False)
    lsad = Column(VARCHAR, nullable=False)
    censusarea = Column(VARCHAR, nullable=False)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(VARCHAR, nullable=False)
    coordinates = Column(VARCHAR, nullable=False)
    # color = Column(String(15), nullable = False) #not going to use column in future

class Zipcodes(Base):
    __tablename__ = "zipcodes"
    
    id = Column(Integer, primary_key=True)   
    zcta = Column(VARCHAR, nullable=True)
    geoid = Column(VARCHAR, nullable=True)
    classfp = Column(VARCHAR, nullable=True)
    # mtfcc = Column(String(100), nullable=True)
    # funcstat = Column(String(15), nullable=True)
    # aland = Column(String(15), nullable=True)
    # awater = Column(String(15), nullable=True)
    # intptlat = Column(String(15), nullable=True)
    # intptlon = Column(String(15), nullable=True)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(VARCHAR, nullable=False)
    coordinates = Column(VARCHAR, nullable=False) 


class Blockgroups(Base):
    __tablename__ = "blockgroups"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(VARCHAR, nullable=True)
    state = Column(VARCHAR, nullable=True)
    county = Column(VARCHAR, nullable=True)
    tract = Column(VARCHAR, nullable=True)
    blockgroup = Column(VARCHAR, nullable=True)
    name = Column(VARCHAR, nullable=True)
    lsad = Column(VARCHAR, nullable=True)
    censusarea = Column(VARCHAR, nullable=True)
    polygon_count = Column(Integer, nullable=False)
    polypoint_starts = Column(VARCHAR, nullable=False)
    coordinates = Column(VARCHAR, nullable=False)
    # color = Column(String(16), nullable=True)    


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
