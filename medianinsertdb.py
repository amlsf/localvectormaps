# TODO change so inputting geoid of region (isntead of autoncrement id) into listings table - easier to reference
import model
import re
import sqlite3
import json


def insert_medians(session):




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



def main(session):
    insert_medians(session) 

if __name__ == "__main__":
    s = model.connect()
    main(s)


