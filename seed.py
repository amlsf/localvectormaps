# For loading data into the database once it's been set up and tables created from model.py

import model
import csv
import datetime
import re
# import sqlite3
from decimal import *
import json
import shapefile

# loads active data file
def load_alist(session):

    with open("data/activedata_20140330fixltlg2.csv") as f:
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
def load_slist(session):
    with open("data/offmarket3fix_5only.csv") as f:
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

# TODO Look into auto-geocoding data with Sarah's ruby script?

# # TODO For extra dummy row for foreign key to insert join later: 
# # county_geoid = "__NOCOUNTY", 
# # bg_geoid = "__NOBG"
# #     u = model.Zipcodes(geoid = "__NOZIP")
# #     session.add(u)
# #     session.commit()

# def load_counties(session):
#     # 3221 records or something (the more dense version had a more like 34xx)

#     shpfile = shapefile.Reader("data/maps/gz_2010_us_050_00_500k/gz_2010_us_050_00_500k.shp")
#     # shapes = shpfile.shapes()
#     shapeRecs = shpfile.shapeRecords()

# # iterates through to convert each item to a "real" list so it can then be converted to JSON    for x in range(len(shapeRecs)):
#     for x in range(len(shapeRecs)):
#         for y in range(len(shapeRecs[x].shape.points)):
#             shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

#     # for x in range(10):
#     #     for y in range(len(shapeRecs[x].shape.points)):
#     #         shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

#         u = model.Counties(geoid = shapeRecs[x].record[0].decode("latin-1"),
#             state = shapeRecs[x].record[1].decode("latin-1"),
#             county = shapeRecs[x].record[2].decode("latin-1"),
#             name = shapeRecs[x].record[3].decode("latin-1"),
#             lsad = shapeRecs[x].record[4].decode("latin-1"), # Legal/Statistical area descriptor
#             censusarea = unicode(shapeRecs[x].record[5]),
#             polygon_count = len(shapeRecs[x].shape.parts), # if it is a multipolygon will be >1
# # iterates through to convert each item to a "real" list so it can then be converted to JSON
#             polypoint_starts = json.dumps(list(shapeRecs[x].shape.parts)), # this returns a list of list position for start of each multipolygon
#             #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# # WARNING - these coordinates are backwards - longitude then lat (not latlong)
#             coordinates = json.dumps(list(shapeRecs[x].shape.points))) # this returns a list of all coordinates
#         session.add(u)

#     session.commit()

# #TODO put in check to make sure geoid are unique and print error if not
#     # select count(distinct c.geoid) from counties c;
#     # select count(*) from counties;


# def load_blockgroups(session):
#     # 23203 records

#     shpfile = shapefile.Reader("data/maps/gz_2010_06_150_00_500kblockgroups/gz_2010_06_150_00_500k.shp")
#     # shapes = shpfile.shapes()
#     shapeRecs = shpfile.shapeRecords()

#     for x in range(len(shapeRecs)):
#         for y in range(len(shapeRecs[x].shape.points)):
#             shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

#     # for x in range(10):
#     #     for y in range(len(shapeRecs[x].shape.points)):
#     #         shapeRecs[x].shape.points[y] = list(shapeRecs[x].shape.points[y])

#         u = model.Blockgroups(geoid = shapeRecs[x].record[0].decode("latin-1"),
#             state = shapeRecs[x].record[1].decode("latin-1"),
#             county = shapeRecs[x].record[2].decode("latin-1"),
#             tract = shapeRecs[x].record[3].decode("latin-1"),
#             blockgroup = shapeRecs[x].record[4].decode("latin-1"),
#             name = shapeRecs[x].record[5].decode("latin-1"),
#             lsad = shapeRecs[x].record[6].decode("latin-1"),
#             censusarea = unicode(shapeRecs[x].record[5]),
#             polygon_count = len(shapeRecs[x].shape.parts), # if it is a multipolygon will be >1
# # iterates through to convert each item to a "real" list so it can then be converted to JSON
#             polypoint_starts = json.dumps(list(shapeRecs[x].shape.parts)), # this returns a list of list position for start of each multipolygon
#             #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# # WARNING - these coordinates are backwards - longitude then lat (not latlong)
#             coordinates = json.dumps(list(shapeRecs[x].shape.points))) # this returns a list of all coordinates
#         session.add(u)

#     session.commit()


# def load_neighborhoods(session):

#     shpfile = shapefile.Reader("data/maps/ZillowNeighborhoods-CA/ZillowNeighborhoods-CA.shp")

# # iterates through to convert each item to a "real" list so it can then be converted to JSON
#     for (i, y) in zip(shpfile.iterShapes(), shpfile.iterRecords()):
#         for x in range(len(i.points)):
#             i.points[x] = list(i.points[x])
#         # print i.points

#         u = model.Neighborhoods(state = y[0],
#             county = y[1],
#             city = y[2],
#             neighborhood = y[3],
#             neighborhood_id = y[4],
#             polygon_count = len(i.parts), # if it is a multipolygon will be >1
# # iterates through to convert each item to a "real" list so it can then be converted to JSON
#             polypoint_starts = json.dumps(list(i.parts)), # this returns a list of list position for start of each multipolygon
#             #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
# # WARNING - these coordinates are backwards - longitude then lat (not latlong)
#             coordinates = json.dumps(list(i.points)) # this returns a list of all coordinates
#             )

#         session.add(u)

#     session.commit()

def main(session):
    load_alist(session)
    # load_slist(session)

# TODO Delete from counties where zcta not between 90001 - 96162 inclusive
    # load_zips(session)

# next run medianinsertdb.py

    # load_neighborhoods(session)
# TODO Delete from counties where State not '06'
    # load_counties(session) 
    # load_blockgroups(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
