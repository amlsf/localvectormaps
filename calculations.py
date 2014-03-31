import model
import re
import sqlite3
import json
import numpy

# # TODO How to tie the region and region_id? use some sort of dictionary?
# def sales_price(session, region, region_id, time1, time2):
#     regions = session.query(REGION).all()
#     houses = session.query(model.Listings).filter_by(REGION_ID=region.id, listing_status !="Active").all()


# def sales_psf(session, region, time):
#     pass

# def comp_sales_psf(session, region, time):
#     pass

# TODO change this from active listings to sold listings
# TODO try doing median calculations all in Database with SQL alchemy? How do with SQL alchemy and feed to JSON? 
def county_activemedian(session):
    regions = session.query(model.Counties).all()

    medians = {}
    for region in regions:
        houses = session.query(model.Listings).filter_by(county_id=region.id, listing_status="Active").all()
        prices = []
        for houseprice in houses:
            prices.append(houseprice.list_price)
        if len(prices) != 0:
            median = numpy.median(prices)
            medians[region.geoid] = median
        else: 
            medians[region.geoid] = 0            

    return json.dumps(medians)

    # using text() with sqlAlchemy
# def county_activemedian(session):
#     s = text("SELECT * from listings") 
#     engine.execute(s)


def county_psf(session):
    regions = session.query(model.Counties).all()

    medians = {}
    for region in regions:
        houses = session.query(model.Listings).filter_by(county_id=region.id, listing_status="Active").all()
        prices = []
# Filter out the regions with no houses
        if len(houses) != 0:
            for houseprice in houses:
                if houseprice.living_sq_ft != 0:
                    # print houseprice.list_price,houseprice.mls_id, houseprice.id
                    psf = houseprice.list_price/houseprice.living_sq_ft
                    prices.append(psf)
                # blocks = (max(prices) - min(prices))/4
            if len(prices) != 0:
                median = numpy.median(prices)
                medians[region.geoid] = median
            else: 
                medians[region.geoid] = 0

    return json.dumps(medians)


# TODO later, region will be an argument according to zoom level
# Make this better
def range_comp(session, baseyear, compyear):
    regions = session.query(model.Counties).all()

    percent_change = {}
    for region in regions:
        # print region.id
        base_houses = session.query(model.Listings).filter_by(county_id=region.id, listing_status="Active").all()
        comp_houses = session.query(model.Listings).filter_by(county_id=region.id, listing_status="Active").all()

        base_prices = []
        if len(base_houses) != 0:
            for b in base_houses:
                if b.living_sq_ft != 0 and b.list_date.year == baseyear:
                    psf = b.list_price/b.living_sq_ft
                    base_prices.append(psf)
        if len(base_prices) != 0:
            base_median = numpy.median(base_prices)
        else: 
            base_median = 0

        comp_prices = []
        if len(comp_houses) != 0:
            for c in base_houses: 
                if c.living_sq_ft != 0 and c.list_date.year == compyear:
                    psf = c.list_price/c.living_sq_ft
                    comp_prices.append(psf)
        if len(comp_prices) != 0:
            comp_median = numpy.median(comp_prices)
        else: 
            base_median = 0

        if base_median != 0 and comp_median != 0:
            median_comp = float(comp_median)/base_median - 1
        else: 
            median_comp = 0

        percent_change[region.geoid] = median_comp

    return json.dumps(percent_change)



# finds the median active house price for each block group and inserts into color column of block group table
# TODO look into insertion sort algorithm to speed up? 
# TODO change this from active listings to sold listings
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
    # county_activemedian(session)
    # county_psf(session)
    range_comp(session, 2011, 2013)

if __name__ == "__main__":
    s = model.connect()
    main(s)


