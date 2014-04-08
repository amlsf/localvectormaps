# For loading data into the database once it's been set up and tables created from model.py

import model
import csv
import datetime
import re
# import sqlite3
from decimal import *
import json
import shapefile
import sys

# loads active data file
def load_alist(session, alist):

    with open(alist) as f:
        reader = csv.reader(f, delimiter = ",")
        counter = 0
# skips header row

        for row in reader:
            counter += 1
            if counter == 1:
                continue

# unpacks row into tuple 
            list_date, pending_date, close_escrow_date, listing_status, list_price, sell_price, property_type, \
            bathrooms_count, bedrooms_count, living_sq_ft, lot_size, address, street_name, street_suffix, \
            street_number, county_name, postal_code, city_name, neighborhood, mls_id, description, parcel_number, \
            property_url, latitude, longitude = row

# checks for blanks and inputs None if blank
            if list_date == '': 
                listing_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            else: 
                listing_date = datetime.datetime.strptime(list_date, "%Y-%m-%d")
            if pending_date == '':
                pend_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            else:
                pend_date = datetime.datetime.strptime(pending_date, "%Y-%m-%d")
            if close_escrow_date == '':
                closing_escrow_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            else: 
                closing_escrow_date = datetime.datetime.strptime(close_escrow_date, "%Y-%m-%d")

# converts to integers
            list_price = int(list_price)
            # if list_price == '':
            #     list_price = float(list_price)

            if sell_price == '':
                sell_price = -1
            else:                
                sell_price = int(sell_price) 

            if lot_size == '':
                lot_size = -1
            else:
                lot_size = int(float(lot_size)) 
            
            if living_sq_ft == '':
                living_sq_ft = -1
            else: 
                living_sq_ft = int(float(living_sq_ft)) 

            bathrooms_count = float(bathrooms_count) 
            bedrooms_count = int(bedrooms_count) 
            latitude = float(latitude)
            longitude = float(longitude)

# populates rows in database
            u = model.Listings(list_date = listing_date, 
                pending_date = pend_date, 
                close_escrow_date = closing_escrow_date, 
                listing_status = listing_status, 
                list_price = list_price, 
                sell_price = sell_price, 
                property_type = property_type, 
                bathrooms_count = bathrooms_count, 
                bedrooms_count = bedrooms_count, 
                living_sq_ft = living_sq_ft, 
                lot_size = lot_size, 
                address = address, 
                street_name = street_name, 
                street_suffix = street_suffix,
                street_number = street_number,
                county_name = county_name,
                postal_code = postal_code,
                city_name = city_name,
                neighborhood = neighborhood.decode("latin-1"),
                mls_id = mls_id.decode("latin-1"),
                description = description.decode("latin-1"),
                parcel_number = parcel_number.decode("latin-1"),
                property_url = property_url,
                # state = state,
                # full_address = full_address,
                latitude = latitude,
                longitude = longitude) 
                # zip_geoid = "__NOZIP")
            session.add(u)

    session.commit()
    f.close()


# loads sold data file
def load_slist(session, slist):
    with open(slist) as f:
        reader = csv.reader(f, delimiter = ",")
        counter = 0
# skips header row
        for row in reader:
            counter += 1
            if counter == 1:
                continue

# unpacks row into tuple 
            list_date, pending_date, close_escrow_date, listing_status, list_price, sell_price, property_type, \
            bathrooms_count, bedrooms_count, living_sq_ft, lot_size, address, street_name, street_suffix, \
            street_number, county_name, postal_code, city_name, neighborhood, mls_id, description, parcel_number = row

# checks for blanks and inputs None if blank
            if list_date == '': 
                listing_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            else: 
                listing_date = datetime.datetime.strptime(list_date, "%Y-%m-%dT%H:%M:%S")
            if pending_date == '':
                pend_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            else:
                pend_date = datetime.datetime.strptime(pending_date, "%Y-%m-%dT%H:%M:%S")
            if close_escrow_date == '':
                closing_escrow_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            else: 
                closing_escrow_date = datetime.datetime.strptime(close_escrow_date, "%Y-%m-%dT%H:%M:%S")

# converts to integers
            list_price = int(list_price)
            # if list_price == '':
                #     list_price = float(list_price)

            if sell_price == '':
                sell_price = -1
            else:                
                sell_price = int(sell_price) 

            if lot_size == '':
                lot_size = -1
            else:
                lot_size = int(float(lot_size)) 
            
            if living_sq_ft == '':
                living_sq_ft = -1
            else: 
                living_sq_ft = int(float(living_sq_ft)) 

            if bathrooms_count == '':
                bathrooms_count = -1
            else:
                bathrooms_count = float(bathrooms_count) 

            if bedrooms_count == '':
                bedrooms_count = -1
            else:
                bedrooms_count = int(bedrooms_count) 
            # latitude = float(latitude)
            # longitude = float(longitude)

# populates rows in database
            u = model.Listings(list_date = listing_date, 
                pending_date = pend_date, 
                close_escrow_date = closing_escrow_date, 
                listing_status = listing_status, 
                list_price = list_price, 
                sell_price = sell_price, 
                property_type = property_type, 
                bathrooms_count = bathrooms_count, 
                bedrooms_count = bedrooms_count, 
                living_sq_ft = living_sq_ft, 
                lot_size = lot_size, 
                address = address, 
                street_name = street_name, 
                street_suffix = street_suffix,
                street_number = street_number,
                county_name = county_name,
                postal_code = postal_code,
                city_name = city_name,
                neighborhood = neighborhood.decode("latin-1"),
                mls_id = mls_id.decode("latin-1"),
                description = description.decode("latin-1"),
                parcel_number = parcel_number.decode("latin-1"))
# Load a dummy row for foreign key constraint so can fill in later with insert join or Ray Casting algorithm
                # zip_geoid = "__NOZIP")
                # state = state,
                # full_address = full_address,
                # latitude = latitude,
                # longitude = longitude)
            session.add(u)

    session.commit()
    f.close()


def load_zips(session):

# Load a dummy row for foreign key constraint so can fill in later with insert join or Ray Casting algorithm
    # u = model.Zipcodes(geoid = "__NOZIP")
    # session.add(u)
    # session.commit()

    shpfile = shapefile.Reader("data/maps/tl_2013_us_zcta510zipcodes/subsetzips.shp")

    for (i, y) in zip(shpfile.iterShapes(), shpfile.iterRecords()):
        for x in range(len(i.points)):
            i.points[x] = list(i.points[x])
        # print i.points

        u = model.Zipcodes(zcta = y[0].decode("latin-1"),
            geoid = y[1].decode("latin-1"),
            # classfp = y[2].decode("latin-1"),
            # mtfcc = y[3].decode("latin-1"),
            polygon_count = len(i.parts), # if it is a multipolygon will be >1
# iterates through to convert each item to a "real" list so it can then be converted to JSON
            polypoint_starts = json.dumps(list(i.parts)), # this returns a list of position for start of each multipolygon
            #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# WARNING - these coordinates are backwards - longitude then lat (not latlong)
            coordinates = json.dumps(list(i.points))) # this returns a list of all coordinates

        session.add(u)

    session.commit()


def load_countyprices(session):
    county_list =["Monterey", "San Benito", "San Mateo", "Santa Clara", "Santa Cruz"]

    for item in county_list:
        u = model.Countyprices(item)
        session.add(u)

    session.commit()

def main():
    if len(sys.argv) < 2:
        connectionstring = model.defaultconnectionstring
    else: 
        connectionstring = sys.argv[1]

    session = model.connect(connectionstring)

    load_alist(session, "data/activedata_20140330fixltlg2.csv")
    load_slist(session, "data/offmarket3fix_5only.csv")

    load_zips(session)


if __name__ == "__main__":
    main()
