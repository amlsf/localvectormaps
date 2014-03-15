# For loading data into the database once it's been set up and tables created from model.py
import model
import csv
import datetime
import re
import sqlite3
from decimal import *

# loads active data file
def load_alist(session):
    with open("data/active_data1.txt") as f:
        reader = csv.reader(f, delimiter = "\t")
        counter = 0
# skips header row
        for row in reader:
            counter += 1
            if counter == 1:
                continue

# unpacks row into tuple 
            list_date, pending_date, close_escrow_date, listing_status, list_price, sell_price, property_type, \
            bathrooms_count, bedrooms_count, living_sq_ft, lot_size, address, street_name, street_suffix, \
            street_number, county_name, postal_code, city_name = row

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

            list_price = int(list_price)
            bathrooms_count = float(bathrooms_count) 
            bedrooms_count = int(bedrooms_count) 

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
                city_name = city_name)
            session.add(u)

    session.commit()
    f.close()

# loads sold data file
def load_slist(session):
    with open("data/sold_data1.txt") as f:
        reader = csv.reader(f, delimiter = "\t")
        counter = 0
# skips header row
        for row in reader:
            counter += 1
            if counter == 1:
                continue

# unpacks row into tuple 
            list_date, pending_date, close_escrow_date, listing_status, list_price, sell_price, property_type, \
            bathrooms_count, bedrooms_count, living_sq_ft, lot_size, address, street_name, street_suffix, \
            street_number, county_name, postal_code, city_name = row

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

            list_price = int(list_price)
            bathrooms_count = float(bathrooms_count) 
            bedrooms_count = int(bedrooms_count) 

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
                city_name = city_name)
            session.add(u)

    session.commit()
    f.close()

def main(session):
    load_alist(session)
    # load_slist(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
