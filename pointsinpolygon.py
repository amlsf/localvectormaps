import model
import re
import sqlite3
import json

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
# NOTE make sure in long-lat order according to database

# this is catching concave polygons - read Ray Casting algorithm
# TODO look at Keunwoo's notes
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
# TODO: don't need n+1, goes an extra time around
    for i in range(n+1):
# modulus function makes it wrap around at end after iterating through points of polygon sequentially
        p2x,p2y = poly[i % n]
# Case 0: check if ray from point crosses bounding box of polygon line, otherwise ignore
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
# counting number of times x-axis ray from point crosses polygon lines in positive direction (odd # times means inside, even outside)
    # any polygon lines that the ray doesn't cross are ignored 

# detecting if it's hortizontal (parallel) so that the x ray never crosses
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x

#TODO bug here, if first line in the polygon is horizontal, this xinters never gets set and would throw an error, otherwise it's comparing to a random xinters
                    if p1x == p2x or x <= xinters:
# flipping back and forth between even and odd number of crossings for whole polygon:
                        inside = not inside
# advances to next point
        p1x,p1y = p2x,p2y

    return inside

#TODO: Best way to loop through entire table and change stuff along the way - 
    # would it be too slow to swallow the entire table and loop through like that? 
    # Could do a loop through limit 100 at a time, and then offset 101, and then length


def point_in_neighborhood(session):
    listings = session.query(model.Listings).all()
    neighborhoods = session.query(model.Neighborhoods).all()

# JSON dump everything
    for polygon in neighborhoods:
        polygon.coordinates = json.loads(polygon.coordinates)
        polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

#TODO better way to do this that might be faster without multiple big O? better way to code it up so not so confusing? 

# Loop through each house in the listings
    for house in listings:
        breaker = 0
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in neighborhoods:
            if breaker == 1:
                break
            # if it is a multipolygon
            if polygon.polygon_count > 1:
                i = 0
                # loop through each polygon in multipolygon and take slice of coordinates using polypoint_starts list
                for s in range(len(polygon.polypoint_starts)):
                    i += 1
                    # if it's the last polygon, pull slice through rest of list so not out of index range
                    if i == len(polygon.polypoint_starts):
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:]):
                            house.nb_id = polygon.id
                            breaker = 1
                            print "multipolygon, last one in the list. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.neighborhood, house.nb_id, polygon.neighborhood)
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.nb_id = polygon.id
                            breaker = 1
                            print "multipolygon, SOMEWHERE in the list. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.neighborhood, house.nb_id, polygon.neighborhood)
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
                    house.nb_id = polygon.id
                    breaker = 1
                    print "single polygon. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.neighborhood, house.nb_id, polygon.neighborhood)

# TODO check if coordinates is long/lat in that order?     
        if not house.nb_id:
            print "neighborhood not found!"

# Cancel any changes to neighborhoods with JSON dumps so database doesn't freak out
    for polygon in neighborhoods:
        session.expire(polygon)

    session.commit()


# TODO: run again and check print statements - howcome multipolygons always last one in list? check howcome all region id's identified are in ~200-300 range - because all those there out of all of US file? 
def point_in_counties(session):
    listings = session.query(model.Listings).all()
    regions = session.query(model.Counties).all()

# JSON dump everything
    for polygon in regions:
        polygon.coordinates = json.loads(polygon.coordinates)
        polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

# Loop through each house in the listings
    for house in listings:
        breaker = 0
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in regions:
            if breaker == 1:
                break
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
                            breaker = 1
                            print "multipolygon, last one in the list. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.county_name, house.county_id, polygon.name)
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.county_id = polygon.id
                            breaker = 1
                            print "multipolygon, SOMEWHERE in the list. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.county_name, house.county_id, polygon.name)
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
                    house.county_id = polygon.id
                    breaker = 1
                    print "single polygon, house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.county_name, house.county_id, polygon.name)
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

# Loop through each house in the listings
    for house in listings:
        breaker = 0        
# With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
        for polygon in regions:
            if breaker == 1:
                break            
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
                            breaker = 1
                            print "multipolygon, last one in the list. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.county_name, house.bg_id, polygon.county)
                    else:  
                        if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
                            house.bg_id = polygon.id
                            breaker = 1
                            print "multipolygon, SOMEHWERE in the list. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.county_name, house.bg_id, polygon.county)
            # for regular polygons: 
            else: 
                if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
                    house.bg_id = polygon.id
                    breaker = 1
                    print "Single polygon. house_id: %r, house region: %r :::: region id: %r region name: %r" % (house.id, house.county_name, house.bg_id, polygon.county)
        if not house.bg_id:
            print "region not found!"

# Cancel any changes to regions with JSON dumps so database doesn't freak out
    for polygon in regions:
        session.expire(polygon)

    session.commit()


# def point_in_zips(session):
#     listings = session.query(model.Listings).all()
#     regions = session.query(model.Zipcodes).all()

# # JSON dump everything
#     for polygon in regions:
#         polygon.coordinates = json.loads(polygon.coordinates)
#         polygon.polypoint_starts = json.loads(polygon.polypoint_starts)

# # Loop through each house in the listings
#     for house in listings:
#         breaker = 0
# # With each house, loop through each (neighborhood), county, zip, block group to see if it's in the polygon
#         for polygon in regions:
#             if breaker == 1:
#                 break
#             # if it is a multipolygon
#             if polygon.polygon_count > 1:
#                 i = 0
#                 # loop through each polygon in multipolygon and take slice of coordinates using polypoint_starts list
#                 for s in range(len(polygon.polypoint_starts)):
#                     i += 1
#                     # if it's the last polygon, pull slice through rest of list so not out of index range
#                     if i == len(polygon.polypoint_starts):
#                         if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:]):
#                             house.zip_id = polygon.id
#                             breaker = 1
#                             print "multipolygon, last one in the list. house_id: %r, house zip: %r :::: house zcta zip_id: %r" % (house.id, house.postal_code, house.zip_id)
#                     else:  
#                         if point_inside_polygon(house.longitude,house.latitude,polygon.coordinates[polygon.polypoint_starts[s]:polygon.polypoint_starts[s+1]]):
#                             house.zip_id = polygon.id
#                             breaker = 1
#                             print "multipolygon, SOMEWHERE in the list. house_id: %r, house zip: %r :::: house zcta zip_id: %r" % (house.id, house.postal_code, house.zip_id)
#             # for regular polygons: 
#             else: 
#                 if point_inside_polygon(house.longitude, house.latitude, polygon.coordinates):
#                     house.zip_id = polygon.id
#                     breaker = 1
#                     print "single polygon. house_id: %r, house zip: %r :::: house zcta zip_id: %r" % (house.id, house.postal_code, house.zip_id)

#         if not house.zip_id:
#             print "region not found!"

# # Cancel any changes to regions with JSON dumps so database doesn't freak out
#     for polygon in regions:
#         session.expire(polygon)

#     session.commit()

def main(session):
# Don't need to use
    # point_in_neighborhood(session)

#TODO just run counties (in case names not normalized in BD) and blockgroups, use sql query to match up zipcodes
    point_in_counties(session) 
    # point_in_blockgroups(session)

#TODO just run sql join, don't need to use this
    # point_in_zips(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)


