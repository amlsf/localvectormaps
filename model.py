import config
import os
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, extract, or_
from sqlalchemy.sql import text, func
from sqlalchemy.dialects.postgresql import FLOAT, DOUBLE_PRECISION, VARCHAR
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from flask.ext.login import UserMixin
import logging
import sys

defaultconnectionstring = "postgresql+psycopg2://postgres:password@localhost/postgres"

Base = declarative_base()

ENGINE = None
Session = None

def connect(connectionstring):
    global engine
    global Session

    engine = create_engine(connectionstring, echo=False)

    Session = sessionmaker(bind=engine)

    return Session()

def create_tables(connectionstring):
    engine = create_engine(connectionstring, echo=False)
    Base.metadata.create_all(engine)


class Listings(Base):
    __tablename__ = "listings"

# only sold data for the first half of 2013, 5 counties
# includes all the property types, filter out later with detached (only single family) vs. attached (active is only detached; sold is only res. single family home)
    
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
# just use address or else street_suffix might product an error
    street_suffix = Column(VARCHAR, nullable=True)
    street_number = Column(VARCHAR, nullable=True)
    county_name = Column(VARCHAR, nullable=True)
    postal_code = Column(VARCHAR, nullable=True)
    city_name = Column(VARCHAR, nullable=True)
    neighborhood = Column(VARCHAR, nullable=True)
    mls_id = Column(VARCHAR, nullable=True)
    description = Column(VARCHAR, nullable=True)
# this will be blank 
    parcel_number = Column(VARCHAR, nullable=True)
    property_url = Column(VARCHAR, nullable=True)
    latitude = Column(DOUBLE_PRECISION, nullable=True)
    longitude = Column(DOUBLE_PRECISION, nullable=True)
    zip_geoid = Column(VARCHAR, nullable=True)
    zip_id = Column(Integer, nullable=True)


class Zipcodeannual(Base):
    __tablename__ = "zipcodeprices"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(VARCHAR, nullable=True)
    zcta = Column(VARCHAR, nullable=True)
    year = Column(Integer, nullable=True)
    year_median_sp = Column(Integer, nullable=True)
    year_median_spsf=Column(DOUBLE_PRECISION, nullable=True)
    year_count_median_sp=Column(Integer, nullable=True)

class Zipcodes(Base):
    __tablename__ = "zipcodes"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(VARCHAR, nullable=True)
    zcta = Column(VARCHAR, nullable=True)
    polygon_count = Column(Integer, nullable=True)
    polypoint_starts = Column(VARCHAR, nullable=True)
    coordinates = Column(VARCHAR, nullable=True) 
    median_sales_price = Column(Integer, nullable=True)
    median_sales_psf = Column(DOUBLE_PRECISION, nullable=True)
    count_median_sales = Column(Integer, nullable=True)
    time_series_psf = Column(VARCHAR, nullable=True) 

class Countyprices(Base):
    __tablename__ = "countyprices"
    
    id = Column(Integer, primary_key=True)   
    geoid = Column(VARCHAR, nullable=True)
# there are only 5
    county = Column(VARCHAR, nullable=True)
    name = Column(VARCHAR, nullable=True)
    median_sales_price = Column(Integer, nullable=True)
    median_sales_psf = Column(DOUBLE_PRECISION, nullable=True)
    count_median_sales = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    year_median_sp = Column(Integer, nullable=True)
    year_median_spsf=Column(DOUBLE_PRECISION, nullable=True)
    year_count_median_sp=Column(Integer, nullable=True)


# across all data
class Aggprices(Base):
    __tablename__ = "aggprices"

    id = Column(Integer, primary_key=True)
    median_sales_price = Column(Integer, nullable=True)
    median_sales_psf = Column(DOUBLE_PRECISION, nullable=True)
    count_median_sales = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    year_median_sp = Column(Integer, nullable=True)
    year_median_spsf=Column(DOUBLE_PRECISION, nullable=True)
    year_count_median_sp=Column(Integer, nullable=True)

# TODO (optional) would need to get national prices for all single family homes (ask Ilya?)
class Nationalprices(Base):
    __tablename__ = "nationalprices"

    id = Column(Integer, primary_key=True)
    median_sales_price = Column(Integer, nullable=True)
    median_sales_psf = Column(DOUBLE_PRECISION, nullable=True)
#TODO check if have count
    # count_median_sales = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    year_median_sp = Column(Integer, nullable=True)
    year_median_spsf=Column(DOUBLE_PRECISION, nullable=True)

def main():
    if len(sys.argv) < 2:
        connectionstring = defaultconnectionstring
    else: 
        connectionstring = sys.argv[1]
    create_tables(connectionstring)

    create_tables(sys.argv[1])


if __name__ == "__main__":
    main()


# test database = "postgresql+psycopg2://postgres:password@localhost/testlocalvector"
# Use this for heroku
# engine = create_engine("postgresql+psycopg2://postgres:password@localhost/postgres", echo=False)
# engine = create_engine(os.environ.get("DATABASE_URL"), echo=False)
# engine = create_engine("sqlite:///listings.db", echo=False)
