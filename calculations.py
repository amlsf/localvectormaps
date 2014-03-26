import model
import re
import sqlite3
import json

#TODO faster to do this within the database? How do with SQL alchemy? 

def county_activemedian(session):
    regions = session.query(model.Counties).all()

    medians = {}
    for region in regions:
        houses = session.query(model.Listings).filter_by(county_id=region.id, listing_status="Active").all()
        prices = []
        for houseprice in houses:
            prices.append(houseprice.list_price)
        # blocks = (max(prices) - min(prices))/4
        prices.sort()
        length = len(prices)
        if length == 0:
            median = 0 
            # print "length is 0, median is %r" % median
            medians[region.geoid] = median
        elif length % 2 == 0:
            median = (prices[length/2-1] + prices[length/2])/2
            # print "length is even, median for county %r is %r" % (region.name, median)
            medians[region.geoid] = median
        else:
            median = prices[length/2]
            # print "length is odd, median for county %r is %r" % (region.name, median)
            medians[region.geoid] = median
 
    return json.dumps(medians)

# finds the median active house price for each block group and inserts into color column of block group table
#TODO look into insertion sort algorithm to speed up? 
def blockgroups_activemedian(session):
    regions = session.query(model.Blockgroups).all()

    for region in regions:
        houses = model.session.query(model.Listings).filter_by(bg_id=region.id, listing_status="Active").all()
        prices = []
        for houseprice in houses:
            prices.append(houseprice.list_price)
        prices.sort()
        length = len(prices)
        if length == 0:
            median = 0 
            print "length is 0, median is %r" % median
        elif length % 2 == 0:
            median = (prices[length/2-1] + prices[length/2])/2
            print "length is even, median is %r" % median
        else:
            median = prices[length/2]
            print "length is odd, median is %r" % median

        # region.color = median
    #TODO - change color later, not need for sliders and checkboxes filtering
    # session.commit()



def main(session):
    county_activemedian(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)


