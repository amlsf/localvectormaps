# For loading data into the database once it's been set up and tables created from model.py
import model
import csv
import datetime
import re
import sqlite3
from decimal import *
import json
import shapefile

# loads active data file
def load_alist(session):
    with open("data/activedata2.csv") as f:
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
            state, full_address, latitude, longitude = row

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

            if list_price == '':
                list_price = float(list_price)

            # list_price = int(list_price)
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
                state = state,
                full_address = full_address,
                latitude = latitude,
                longitude = longitude)
            session.add(u)

    session.commit()
    f.close()

# loads sold data file
def load_slist(session):
    with open("data/offmarket2.csv") as f:
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
            state, full_address, latitude, longitude = row

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

            if list_price == '':
                list_price = float(list_price)

            # list_price = int(list_price)
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
                state = state,
                full_address = full_address,
                latitude = latitude,
                longitude = longitude)
            session.add(u)

    session.commit()
    f.close()

#         reader = csv.reader(f, delimiter = "\t")
#         counter = 0
# # skips header row
#         for row in reader:
#             counter += 1
#             if counter == 1:
#                 continue

# # unpacks row into tuple
#             print row
#             list_date, pending_date, close_escrow_date, listing_status, list_price, sell_price, property_type, \
#             bathrooms_count, bedrooms_count, living_sq_ft, lot_size, address, street_name, street_suffix, \
#             street_number, county_name, postal_code, city_name, neighborhood, mls_id, description, parcel_number, \
#             state, full_address, latitude, longitude = row

# # checks for blanks and inputs beginnig of time if blank
#             if list_date == '': 
#                 listing_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
#             else: 
#                 listing_date = datetime.datetime.strptime(list_date, "%Y-%m-%dT%H:%M:%S")
#             if pending_date == '':
#                 pend_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
#             else:
#                 pend_date = datetime.datetime.strptime(pending_date, "%Y-%m-%dT%H:%M:%S")
#             if close_escrow_date == '':
#                 closing_escrow_date = datetime.datetime.strptime("1970-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
#             else: 
#                 closing_escrow_date = datetime.datetime.strptime(close_escrow_date, "%Y-%m-%dT%H:%M:%S")

# # converts to integers, if empty used dummy -1 placeholder
#             if sell_price == '':
#                 sell_price = -1
#             else:                
#                 sell_price = int(sell_price) 

#             if lot_size == '':
#                 lot_size = -1
#             else:
#                 lot_size = int(float(lot_size)) 
            
#             if living_sq_ft == '':
#                 living_sq_ft = -1
#             else: 
#                 living_sq_ft = int(float(living_sq_ft)) 

#             list_price = int(list_price)
#             bathrooms_count = float(bathrooms_count) 
#             bedrooms_count = int(bedrooms_count) 

# # populates rows in database
#             u = model.Listings(list_date = listing_date, 
#                 pending_date = pend_date, 
#                 close_escrow_date = closing_escrow_date, 
#                 listing_status = listing_status, 
#                 list_price = list_price, 
#                 sell_price = sell_price, 
#                 property_type = property_type, 
#                 bathrooms_count = bathrooms_count, 
#                 bedrooms_count = bedrooms_count, 
#                 living_sq_ft = living_sq_ft, 
#                 lot_size = lot_size, 
#                 address = address, 
#                 street_name = street_name, 
#                 street_suffix = street_suffix,
#                 street_number = street_number,
#                 county_name = county_name,
#                 postal_code = postal_code,
#                 city_name = city_name,
#                 neighborhood = neighborhood.decode("latin-1"),
#                 mls_id = mls_id.decode("latin-1"),
#                 description = description.decode("latin-1"),
#                 parcel_number = parcel_number.decode("latin-1"),
#                 state = state,
#                 full_address = full_address,
#                 latitude = latitude,
#                 longitude = longitude)

#             session.add(u)

#     session.commit()
#     f.close()

def load_neighborhoods(session):

    shpfile = shapefile.Reader("data/maps/ZillowNeighborhoods-CA/ZillowNeighborhoods-CA.shp")

# iterates through to convert each item to a "real" list so it can then be converted to JSON
    for (i, y) in zip(shpfile.iterShapes(), shpfile.iterRecords()):
        for x in range(len(i.points)):
            i.points[x] = list(i.points[x])
        # print i.points

        u = model.Neighborhoods(state = y[0],
            county = y[1],
            city = y[2],
            neighborhood = y[3],
            neighborhood_id = y[4],
            polygon_count = len(i.parts), # if it is a multipolygon will be >1
# iterates through to convert each item to a "real" list so it can then be converted to JSON
            polypoint_starts = json.dumps(list(i.parts)), # this returns a list of list position for start of each multipolygon
            #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# WARNING - these coordinates are backwards - longitude then lat (not latlong)
            coordinates = json.dumps(list(i.points)) # this returns a list of all coordinates
            )

        session.add(u)

    session.commit()

def load_counties(session):
    # 3221 records or something (the more dense version had a more like 34xx)

    shpfile = shapefile.Reader("data/maps/gz_2010_us_050_00_500k/gz_2010_us_050_00_500k.shp")
    # shapes = shpfile.shapes()
    shapeRecs = shpfile.shapeRecords()

# iterates through to convert each item to a "real" list so it can then be converted to JSON    for x in range(len(shapeRecs)):
        for y in range(len(shapeRecs[x].shape.points)):
            shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

    # for x in range(10):
    #     for y in range(len(shapeRecs[x].shape.points)):
    #         shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

        u = model.Counties(geoid = shapeRecs[x].record[0].decode("latin-1"),
            state = shapeRecs[x].record[1].decode("latin-1"),
            county = shapeRecs[x].record[2].decode("latin-1"),
            name = shapeRecs[x].record[3].decode("latin-1"),
            lsad = shapeRecs[x].record[4].decode("latin-1"), # Legal/Statistical area descriptor
            censusarea = unicode(shapeRecs[x].record[5]),
            polygon_count = len(shapeRecs[x].shape.parts), # if it is a multipolygon will be >1
# iterates through to convert each item to a "real" list so it can then be converted to JSON
            polypoint_starts = json.dumps(list(shapeRecs[x].shape.parts)), # this returns a list of list position for start of each multipolygon
            #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# WARNING - these coordinates are backwards - longitude then lat (not latlong)
            coordinates = json.dumps(list(shapeRecs[x].shape.points))) # this returns a list of all coordinates
        session.add(u)

    session.commit()

def load_zips(session):

    shpfile = shapefile.Reader("data/maps/tl_2013_us_zcta510zipcodes/tl_2013_us_zcta510.shp")

    for (i, y) in zip(shpfile.iterShapes(), shpfile.iterRecords()):
        for x in range(len(i.points)):
            i.points[x] = list(i.points[x])
        # print i.points

        u = model.Zipcodes(zcta = y[0].decode("latin-1"),
            geoid = y[1].decode("latin-1"),
            classfp = y[2].decode("latin-1"),
            mtfcc = y[3].decode("latin-1"),
            polygon_count = len(i.parts), # if it is a multipolygon will be >1
# iterates through to convert each item to a "real" list so it can then be converted to JSON
            polypoint_starts = json.dumps(list(i.parts)), # this returns a list of position for start of each multipolygon
            #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# WARNING - these coordinates are backwards - longitude then lat (not latlong)
            coordinates = json.dumps(list(i.points))) # this returns a list of all coordinates

        session.add(u)

    session.commit()

def load_blockgroups(session):
    # 23203 records

    shpfile = shapefile.Reader("data/maps/gz_2010_06_150_00_500kblockgroups/gz_2010_06_150_00_500k.shp")
    # shapes = shpfile.shapes()
    shapeRecs = shpfile.shapeRecords()

    for x in range(len(shapeRecs)):
        for y in range(len(shapeRecs[x].shape.points)):
            shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

    # for x in range(10):
    #     for y in range(len(shapeRecs[x].shape.points)):
    #         shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

        u = model.Blockgroups(geoid = shapeRecs[x].record[0].decode("latin-1"),
            state = shapeRecs[x].record[1].decode("latin-1"),
            county = shapeRecs[x].record[2].decode("latin-1"),
            tract = shapeRecs[x].record[3].decode("latin-1"),
            blockgroup = shapeRecs[x].record[4].decode("latin-1"),
            name = shapeRecs[x].record[5].decode("latin-1"),
            lsad = shapeRecs[x].record[6].decode("latin-1"),
            censusarea = unicode(shapeRecs[x].record[5]),
            polygon_count = len(shapeRecs[x].shape.parts), # if it is a multipolygon will be >1
# iterates through to convert each item to a "real" list so it can then be converted to JSON
            polypoint_starts = json.dumps(list(shapeRecs[x].shape.parts)), # this returns a list of list position for start of each multipolygon
            #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# WARNING - these coordinates are backwards - longitude then lat (not latlong)
            coordinates = json.dumps(list(shapeRecs[x].shape.points))) # this returns a list of all coordinates
        session.add(u)

    session.commit()

def main(session):
    # load_alist(session)
    load_slist(session)
# TODO run slist again

# TODO Check this once loaded against the geojson files I have
    # load_neighborhoods(session)
    # load_counties(session) 
    # load_blockgroups(session)

# TODO THIS IS GOING TO TAKE A LONG TIME, hope it works!
    # load_zips(session)


if __name__ == "__main__":
    s = model.connect()
    main(s)
