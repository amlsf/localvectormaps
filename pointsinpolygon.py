import model
# import csv
# import datetime
import re
import sqlite3
# from decimal import *
import json
# import shapefile

# model.session = model.connect()

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
# NOTE make sure in long-lat order according to database
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

# print point_inside_polygon(x,y,poly)


# JUST A TEST function - not actually using neighborhoods
#TODO: Best way to loop through entire table and change stuff along the way - 
    # would it be too slow to swallow the entire table and loop through like that? 
def point_in_neighborhood(session):
    listings = session.query(model.Listings).all()
    neighborhoods = session.query(model.Neighborhoods).all()

# JSON dump everything
    for polygon in neighborhoods:
        polygon.coordinates = json.loads(polygon.coordinates)
        polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

    # for polygon in neighborhoods:
    #     print polygon.coordinates
    #     print type(polygon.coordinates)
        # print polygon.polypoint_starts
        # print type(polygon.polypoint_starts)

#TODO better way to do this that might be faster without multiple big O? better way to code it up so not so confusing? 
# Loop through each house in the listings
    for house in listings:
        # print "House id is %r" % house.id
        z = 0
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in neighborhoods:
            # !!TODO should I just break out of inner for loop if found? Maybe change to a while loop to break out so its faster and prevent duplicates? (check for overlap)
            # TODO while not house.county_id: (TODO consider changing to -1 and do a "while not -1", but then couldn't change or rerun so can break out as soon as neighborhood found, no need to keep looking)

            # if z < len(neighborhoods):
            #     z += 1
                # print "%r out of 948 neighborhoods" % z
                # print "House id is %r" % house.id
                # print "neighorbood id is %r" % polygon.id
                # polygon.coordinates = json.loads(polygon.coordinates) 
                # print polygon.coordinates
            # if it is a multipolygon
            if polygon.polygon_count > 1:
                i = 0
                # polygon.polypoint_starts = json.loads(polygon.polypoint_starts)
                # loop through each polygon in multipolygon and take slice of coordinates using polypoint_starts list
                for s in range(len(polygon.polypoint_starts)):
                    i += 1
                    # if it's the last polygon, pull slice through rest of list so not out of index range
                    if i == len(polygon.polypoint_starts):
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:]):
                            house.county_id = polygon.id
                            print "multipolygon, last one in the list. neighborhood Id is: %r" % house.county_id
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.county_id = polygon.id
                            print "multipolygon, SOMEWHERE in the list. neighborhood Id is: %r" % house.county_id
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
# TODO use county column for now, will change over later
                    house.county_id = polygon.id
                    print "single polygon, neighborhood Id is: %r" % house.county_id

# TODO check if coordinates is long/lat in that order?     
                # print "neighborhood id insert is %r" % house.county_id
        if not house.county_id:
            print "neighborhood not found!"

# Cancel any changes to neighborhoods with JSON dumps so database doesn't freak out
    for polygon in neighborhoods:
        session.expire(polygon)

        # polygon.coordinates = json.dumps(polygon.coordinates)
        # polygon.polypoint_starts = json.dumps(polygon.polypoint_starts)

    session.commit()

# TODO: run again and check print statements - howcome multipolygons always last one in list?
#   check howcome all region id's identified are in ~200-300 range - because all those there out of all of US file? 
def point_in_counties(session):
    listings = session.query(model.Listings).all()
    regions = session.query(model.Counties).all()

# JSON dump everything
    for polygon in regions:
        polygon.coordinates = json.loads(polygon.coordinates)
        polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

    # for polygon in regions:
    #     print polygon.coordinates
    #     print type(polygon.coordinates)
        # print polygon.polypoint_starts
        # print type(polygon.polypoint_starts)

# Loop through each house in the listings
    for house in listings:
        # print "House id is %r" % house.id
        z = 0
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in regions:

            # if z < len(regions):
            #     z += 1
                # print "%r out of 948 regions" % z
                # print "House id is %r" % house.id
                # print "neighorbood id is %r" % polygon.id
                # print polygon.coordinates
            # if it is a multipolygon
            if polygon.polygon_count > 1:
                i = 0
                # loop through each polygon in multipolygon and take slice of coordinates using polypoint_starts list
                for s in range(len(polygon.polypoint_starts)):
                    i += 1
                    # if it's the last polygon, pull slice through rest of list so not out of index range
                    if i == len(polygon.polypoint_starts):
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:]):
                            house.county_id = polygon.id
                            print "multipolygon, last one in the list. region Id is: %r" % house.county_id
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.county_id = polygon.id
                            print "multipolygon, SOMEWHERE in the list. region Id is: %r" % house.county_id
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
                    house.county_id = polygon.id
                    print "single polygon, region Id is: %r" % house.county_id
                # print "region id insert is %r" % house.county_id
        if not house.county_id:
            print "region not found!"

# Cancel any changes to regions with JSON dumps so database doesn't freak out
    for polygon in regions:
        session.expire(polygon)

    session.commit()

def point_in_blockgroups(session):
    listings = session.query(model.Listings).all()
    regions = session.query(model.Blockgroups).all()

# JSON dump everything
    for polygon in regions:
        polygon.coordinates = json.loads(polygon.coordinates)
        polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

    # for polygon in regions:
    #     print polygon.coordinates
    #     print type(polygon.coordinates)
        # print polygon.polypoint_starts
        # print type(polygon.polypoint_starts)

# Loop through each house in the listings
    for house in listings:
        # print "House id is %r" % house.id
        z = 0
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in regions:
            # if z < len(regions):
            #     z += 1
                # print "%r out of 948 regions" % z
                # print "House id is %r" % house.id
                # print "neighorbood id is %r" % polygon.id
                # print polygon.coordinates
            # if it is a multipolygon
            if polygon.polygon_count > 1:
                i = 0
                # loop through each polygon in multipolygon and take slice of coordinates using polypoint_starts list
                for s in range(len(polygon.polypoint_starts)):
                    i += 1
                    # if it's the last polygon, pull slice through rest of list so not out of index range
                    if i == len(polygon.polypoint_starts):
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:]):
                            house.bg_id = polygon.id
                            print "multipolygon, last one in the list. region Id is: %r" % house.bg_id
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.bg_id = polygon.id
                            print "multipolygon, SOMEWHERE in the list. region Id is: %r" % house.bg_id
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
                    house.bg_id = polygon.id
                    print "single polygon, region Id is: %r" % house.bg_id
                # print "region id insert is %r" % house.bg_id
        if not house.bg_id:
            print "region not found!"

# Cancel any changes to regions with JSON dumps so database doesn't freak out
    for polygon in regions:
        session.expire(polygon)

    session.commit()


def point_in_zips(session):
    listings = session.query(model.Listings).all()
    regions = session.query(model.Zipcodes).all()

# JSON dump everything
    for polygon in regions:
        polygon.coordinates = json.loads(polygon.coordinates)
        polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

    # for polygon in regions:
    #     print polygon.coordinates
    #     print type(polygon.coordinates)
        # print polygon.polypoint_starts
        # print type(polygon.polypoint_starts)

# Loop through each house in the listings
    for house in listings:
        # print "House id is %r" % house.id
        z = 0
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in regions:
            # if z < len(regions):
            #     z += 1
                # print "%r out of 948 regions" % z
                # print "House id is %r" % house.id
                # print "neighorbood id is %r" % polygon.id
                # print polygon.coordinates
            # if it is a multipolygon
            if polygon.polygon_count > 1:
                i = 0
                # loop through each polygon in multipolygon and take slice of coordinates using polypoint_starts list
                for s in range(len(polygon.polypoint_starts)):
                    i += 1
                    # if it's the last polygon, pull slice through rest of list so not out of index range
                    if i == len(polygon.polypoint_starts):
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:]):
                            house.zip_id = polygon.id
                            print "multipolygon, last one in the list. region Id is: %r" % house.zip_id
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.zip_id = polygon.id
                            print "multipolygon, SOMEWHERE in the list. region Id is: %r" % house.zip_id
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
                    house.zip_id = polygon.id
                    print "single polygon, region Id is: %r" % house.zip_id
                # print "region id insert is %r" % house.zip_id
        if not house.zip_id:
            print "region not found!"

# Cancel any changes to regions with JSON dumps so database doesn't freak out
    for polygon in regions:
        session.expire(polygon)

    session.commit()

def main(session):
    # TEST ONLY 
    # point_in_neighborhood(session)

    # point_in_counties(session) 
    # point_in_blockgroups(session)
    point_in_zips(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)


