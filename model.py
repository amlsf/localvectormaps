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
    street_suffix = Column(String(64), nullable=True)
    street_number = Column(Integer, nullable=True)
    county_name = Column(String(64), nullable=True)
    postal_code = Column(Integer, nullable=True)
    city_name = Column(String(64), nullable=True)

def connect():
    global engine
    global Session

    engine = create_engine("sqlite:///listings.db", echo=False)
    Session = sessionmaker(bind=engine)

    return Session()

def create_tables():
    Base.metadata.create_all(engine)


def main(session):
    pass

if __name__ == "__main__":
    session = connect()
    session = Session()
    # create_tables()

    main()

