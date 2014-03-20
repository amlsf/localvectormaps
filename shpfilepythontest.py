# TODO check for multi polygons

import shapefile
import json

# county full data and cartographic boundaries only
# zillow = shapefile.Reader("data/maps/tl_2013_us_county/tl_2013_us_county.shp")
# zillow = shapefile.Reader("data/maps/gz_2010_us_050_00_500k/gz_2010_us_050_00_500k.shp")

# zip codes
zillow = shapefile.Reader("data/maps/tl_2013_us_zcta510zipcodes/tl_2013_us_zcta510.shp")

# block groups
# zillow = shapefile.Reader("data/maps/gz_2010_06_150_00_500kblockgroups/gz_2010_06_150_00_500k.shp")


# prints out database attributes
print zillow.fields

shapes = zillow.shapes()
shapeRecs = zillow.shapeRecords()

# print len(shapes)

# print "This is the number of records: %s" % len(shapeRecs)
print shapeRecs[0].record  # calls the 1st record as a list
# print shapeRecs[1].record 
# print shapes[0].parts
print shapeRecs[0].shape.points


# print shapeRecs[0].shape.points #returns all the points of the shape
# print len(shapeRecs[0].shape.points)
# print shapeRecs[0].shape.points[0] # prints the first lat/long points of the first record's shape


# get list of shapefile's records (without the coordinates)
# print zillow.records()
# get number of records
# print len(zillow.records())
# print len(zillow.fields) #this returns 6 elements, but there are only 5, ignore first one
# print zillow.fields[1][0] # state
# print zillow.fields[2][0] # County
# print zillow.fields[3][0] # city
# print zillow.fields[4][0] # name of neighbohood
# print zillow.fields[5][0] # region id

# print zillow.record(0)[0] #prints first record's state
# print zillow.record(0)[1] #prints first record's county
# print zillow.record(0)[2] #prints first record's city
# print zillow.record(0)[3] #prints first record's neighborhood
# print zillow.record(0)[4] #prints first record's regionid

# get list of Shapes objects describing geo of each shape record
# shapes = zillow.shapes()



# # get # of shapes (same as getting number of records above)
# print len(shapes)
# #TODO This only seems to return a 5 - what about getting polygons and multipolygons? 
# # for i in range(len(shapes)):
# #     if shapes[i].shapeType!= 5:
# #         print shapes[i].shapeType

# # prints points in each shape
# print shapes[4].points[0] # prints first point of first shape
# print len(shapes[4].points) #  prints number of points in first shape


# # shape = zillow.iterShapes()
# # print shape
# # print len(list(zillow.iterShapes()))

# # read both the record and the shapes and gets whoel list of them
# shapeRecs = zillow.shapeRecords()
# print len(shapeRecs)
# print "This is the number of records: %s" % len(shapeRecs)
# print shapeRecs[4].record  # calls the 5th record as a list
# print shapeRecs[4].shape.points #returns all the points of the shape
# print len(shapeRecs[4].shape.points)
# print shapeRecs[4].shape.points[0] # prints the first lat/long points of the first record's shape

# # parts: Parts simply group collections of points into shapes. 
# If the shape record has multiple parts this attribute contains the index of the first point of each part. 
# If there is only one part then a list containing 0 is returned.
# print len(shapes[4].parts)
# print shapes[4].parts

# print len(zillow.fields)
# for i in range(1, len(zillow.fields)):
#     print zillow.fields[i][0]



# for x in range(0, len(shapeRecs)):
#     for i in range(1, len(zillow.fields)):
#         # if print len(shapes[i].parts) > 1:

#         # else: 
#         print zillow.fields[i][0] 
#         print shapeRecs[x].record[i-1]

# print shapeRecs[0].record[0]
# print shapeRecs[0].record[1]
# print shapeRecs[0].record[2]
# print shapeRecs[0].record[3]
# print shapeRecs[0].record[4]

# shpfile = shapefile.Reader("ZillowNeighborhoods-CA/ZillowNeighborhoods-CA.shp")

# shapes = shpfile.shapes()
# shapeRecs = shpfile.shapeRecords()


# print shapes[4].points # prints first point of first shape
# print len(shapes[1].points)

# print len(shapeRecs[4].shape.points)

# # for every shape 
# polygon_counter = 1
# for x in range(len(shapeRecs)):
#     if len(shapes[x].parts) > 1:
#         for y in shapes[x].parts:
#             if 


#     else:

#         state = shapeRecs[x].record[0]
#         county = shapeRecs[x].record[1]
#         city = shapeRecs[x].record[2]
#         neighborhood = shapeRecs[x].record[3]
#         neighborhood_id = shapeRecs[x].record[4]
#         polygonct_start1 = len(shapes[x].parts) # if it is a multipolygon will be >1
#         poly_pointstarts =  shapes[x].parts # this returns a list of list position for start of each multipolygon
#         #need to use json.loads(sqlalchemyobject.coordinates) to get back as list
#         coordinates = shapeRecs[x].shape.points
    
#         print state




