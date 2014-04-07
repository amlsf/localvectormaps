import model
import re
# import sqlite3
import json
import numpy
import sys

# This script inserts to each zipcode in Zipcodes table the total median price, median PSF price, count for all time and per year

def insert_median_sales_price(session):
    regions = session.query(model.Zipcodes).all()

    for region in regions:
# this will just take sold listings
        # houses = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').all()
        houses = session.query(model.Listings).filter_by(postal_code=region.zcta, property_type='Res. Single Family').all()
        prices = []
        for houseprice in houses:
            prices.append(houseprice.sell_price)
            # print "Houseprice postal_code is: %r" % houseprice.postal_code

            # if region.zcta == '93908':
            #     print "Looking at 93908 sell_price is %r" % (houseprice.sellprice)       

# ignore any zipcodes with fewer than 10 data points
        if len(prices) > 10:
            median = numpy.median(prices)
        else:
            median = 0

        # print "zcta: %r, pricelist: %r" % (region.zcta, prices)
        # print "median is %r" % median
# set the column in the listings table to the median price
        region.median_sales_price = median
        region.count_median_sales = len(prices)

    session.commit()


def insert_median_sales_psf(session):
    regions = session.query(model.Zipcodes).all()

    for region in regions:
        # houses = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').all()
        houses = session.query(model.Listings).filter_by(postal_code=region.zcta, property_type='Res. Single Family').all()
        prices = []
    # Filter out the regions with no houses
        if len(houses) != 0:
            for houseprice in houses:
    # Extra cautious that living_sq_ft is not 0, cannot divie by 0
                if houseprice.living_sq_ft != 0:
                    psf = float(houseprice.sell_price)/houseprice.living_sq_ft
                    prices.append(psf)
                    # print "Houseprice postal_code is: %r" % houseprice.postal_code
    # ignore any zipcodes with fewer than 10 data points
                else: 
                    median = 0
            if len(prices) > 10:
                median = numpy.median(prices)
            else:
                median = 0

            # print "zcta: %r, pricelist: %r" % (region.zcta, prices)
            # print "median is %r" % median
        else:
            median = 0
# set the column in the listings table to the median price
        region.median_sales_psf = median

    session.commit()



def populate_prices_table(session, year):
    regions = session.query(model.Zipcodes).all()

    for region in regions:

# calculates the annual total sales price data 
        # houses_year = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').filter(model.extract('year', model.Listings.close_escrow_date)==year).all()
        houses_year = session.query(model.Listings).filter_by(postal_code=region.zcta, property_type='Res. Single Family').filter(model.extract('year', model.Listings.close_escrow_date)==year).all()
# this will just take sold listings total sales prices per year
        prices = []
        for houseprice in houses_year:
            prices.append(houseprice.sell_price)
            # print "Houseprice postal_code is: %r" % houseprice.postal_code
# ignore any zipcodes with fewer than 10 data points
        if len(prices) > 10:
            median = numpy.median(prices)
        else:
            median = 0

        # print "zcta: %r, pricelist: %r" % (region.zcta, prices)
        # print "median is %r" % median
# set the column in the listings table to the median price


#  calculates the psf per year
        psf_prices = []
    # Filter out the regions with no houses
        if len(houses_year) != 0:
            for houseprice in houses_year:
    # Extra cautious that living_sq_ft is not 0, cannot divie by 0
                if houseprice.living_sq_ft != 0:
                    psf = float(houseprice.sell_price)/houseprice.living_sq_ft
                    psf_prices.append(psf)
                    # print "Houseprice postal_code is: %r" % houseprice.postal_code
                    # print "House sell date is %r" % houseprice.close_escrow_date
    # ignore any zipcodes with fewer than 10 data points
                else: 
                    psf_median = 0
            if len(psf_prices) > 10:
                psf_median = numpy.median(psf_prices)
            else:
                psf_median = 0

            # print "zcta: %r, pricelist: %r" % (region.zcta, psf_prices)
            # print "psf_median is %r" % psf_median
        else:
            psf_median = 0


# set the column in the listings table to the median price
        # columninsert = 'region.median_sales_psf_' + year

        u = model.Zipcodeannual(
            geoid = region.geoid,
            zcta = region.zcta,
            year = year,
            year_median_sp = median, 
            year_median_spsf = psf_median,
            year_count_median_sp = len(prices))

        session.add(u)

    session.commit()


def insert_psf_time_series(session):
    regions = session.query(model.Zipcodes).all()

    for region in regions:

        graph = []
        counter = 1
        for year in range(2006,2014):
            point_dict = {}
            yearresult = session.query(model.Zipcodeannual).filter_by(geoid=region.geoid, year=year).all()
            point_dict['x'] = counter
            point_dict['y'] = yearresult[0].year_median_spsf
            counter += 1
            graph.append(point_dict) 

        graphjson = json.dumps(graph)
        # print graphjson
        region.time_series_psf = graphjson

    session.commit()

def main():
    if len(sys.argv) < 2:
        connectionstring = model.defaultconnectionstring
    else: 
        connectionstring = sys.argv[1]

    session = model.connect(connectionstring)

    # insert_psf_time_series(session)

    # insert_median_sales_price(session)
    # insert_median_sales_psf(session)

    # populate_prices_table(session, 2005)

    # for year in range(2006,2014):
    #     populate_prices_table(session, year)

if __name__ == "__main__":
    main()


