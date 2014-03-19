# // Heat map data
# var taxiData = [
# // {% for }
# //   new google.maps.LatLng({{ item.lat }}, {{ item.lng }}),
# // {% endfor %}
#   new google.maps.LatLng(37.782745, -122.444586),
#   new google.maps.LatLng(37.782842, -122.443688),
#   new google.maps.LatLng(37.782919, -122.442815),
#   new google.maps.LatLng(37.782992, -122.442112),
#   new google.maps.LatLng(37.783100, -122.441461),
#   new google.maps.LatLng(37.783206, -122.440829),
#   new google.maps.LatLng(37.783273, -122.440324),
#   new google.maps.LatLng(37.783316, -122.440023),
#   ];

import json

f = open("CAneighborhoods.txt")
x = f.read()

# print x

y = json.loads(x)

# print y['type'] # returns "FeatureCollection"
# print y['features'] # returns list of all the neighborhoods

z = 0
# print len(y['features']) # returns 948 different neighbrhoods
# print y['features'][z] #returns first neighborhood all details
# print y['features'][947] #returns last neighborhood all details

# print y['features'][z]['geometry']['type'] #returns geometry type - polygon or multi-polygon? 
# print y['features'][z]['type'] #returns "feature"
# print y['features'][z]['properties']['COUNTY']
# print y['features'][z]['properties']['CITY']
# print y['features'][z]['properties']['STATE']
# print y['features'][z]['properties']['REGIONID']
# print y['features'][z]['properties']['NAME']

# #returns coordinates (wrapped in a bunch of lists of lists)
# print len(y['features'][z]['geometry']['coordinates'][0]) # returns full list of vertices
# print y['features'][z]['geometry']['coordinates'][0][len(y['features'][z]['geometry']['coordinates'][0])-1] #returns last item

# for i in range(len(y['features'])):
#     # print y['features'][i]

#     print "\n"
#     print i
#     print "type: %s" % y['features'][i]['type'] #returns feature
#     print "geometric type: %s" % y['features'][i]['geometry']['type'] #returns geometry type - polygon or multi-polygon?         
#     print "County: %s" % y['features'][i]['properties']['COUNTY']
#     print "City: %s" % y['features'][i]['properties']['CITY']
#     print "State: %s" % y['features'][i]['properties']['STATE']
#     print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
#     print "Neighborhood: %s" % y['features'][i]['properties']['NAME']
#     coordinates = y['features'][i]['geometry']['coordinates'][0]  

#     # coordinates of vertices
    # print len(coordinates)
    # for o in range(len(coordinates))

    # y['features'][z]['geometry']['coordinates'][0][len(y['features'][z]['geometry']['coordinates'][0])-1]



for i in range(len(y['features'])):
    # print y['features'][i]

    geotype = y['features'][i]['geometry']['type'] 
    coordinates = y['features'][i]['geometry']['coordinates'] 

    # if geotype != "MultiPolygon" or geotype != "Polygon":
    #     print i
    #     print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
    #     print "geometric type: %s" % y['features'][i]['geometry']['type'] #returns geometry type - polygon or multi-polygon?         

    # for j in range(len(coordinates)):
    #     if geotype == "Polygon":
    #         print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
    #         print len(coordinates[j])

    # if geotype == "Polygon" and len(coordinates) > 1:
    #     print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
    #     print len(coordinates[0])

    # if geotype == "MultiPolygon":
    #     print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
    #     print len(coordinates[0][1])

    if geotype == "Polygon":
        for x in range(len(coordinates[0])):
            print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
            print "Vertice #: %s" % x
            print coordinates[0][x]

    if geotype == "MultiPolygon":
        for x in range(len(coordinates)):
                for a in range(len(coordinates[x][0])):
                    print "RegionID: %s" % y['features'][i]['properties']['REGIONID']
                    print "Multi-Polygon #: %s" % x
                    print "Vertice #: %s" % a
                    print coordinates[x][0][a]


