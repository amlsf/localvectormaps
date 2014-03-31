# TODO change so inputting geoid of region (isntead of autoncrement id) into listings table - easier to reference
import model
import re
# import sqlite3
import json
import numpy


# delete from only listings where property_type not in('Res. Single Family', 'Detached');
# delete from only listings where living_sq_ft = -1;
# delete from only listings where living_sq_ft = 0;
# update listings set zip_id = (select z.id from zipcodes z where postal_code = z.zcta);
# update listings set zip_geoid = (select z.geoid from zipcodes z where postal_code = z.zcta);

# 6. run median calculations and update into SQL database
# (make sure to only put in median if more than X # of houses in the zipcode)
# - WRITE DOWN zctas & remove any empty zipcode regions manually from database once shapefile loaded (if not already done so in step 1)
# - remove those from geojson too

def insert_median_sales_price(session):
    regions = session.query(model.Zipcodes).all()

    for region in regions:
# this will just take sold listings
        houses = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').all()
        prices = []
        for houseprice in houses:
            prices.append(houseprice.sell_price)
            print "Houseprice postal_code is: %r" % houseprice.postal_code
# ignore any zipcodes with fewer than 10 data points
        if len(prices) > 10:
            median = numpy.median(prices)
        else:
            median = 0

        print "zcta: %r, pricelist: %r" % (region.zcta, prices)
        print "median is %r" % median
# set the column in the listings table to the median price
        region.median_sales_price = median

    session.commit()


def insert_median_sales_psf(session):
    regions = session.query(model.Zipcodes).all()

    for region in regions:
        houses = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').all()
        prices = []
    # Filter out the regions with no houses
        if len(houses) != 0:
            for houseprice in houses:
    # Extra cautious that living_sq_ft is not 0, cannot divie by 0
                if houseprice.living_sq_ft != 0:
                    psf = float(houseprice.sell_price)/houseprice.living_sq_ft
                    prices.append(psf)
                    print "Houseprice postal_code is: %r" % houseprice.postal_code
    # ignore any zipcodes with fewer than 10 data points
                else: 
                    median = 0
            if len(prices) > 10:
                median = numpy.median(prices)
            else:
                median = 0

            print "zcta: %r, pricelist: %r" % (region.zcta, prices)
            print "median is %r" % median
        else:
            median = 0
# set the column in the listings table to the median price
        region.median_sales_psf = median

    session.commit()


def insert_median_sales_psf_year(session, year):
    regions = session.query(model.Zipcodes).all()

    for region in regions:
        houses = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').filter(model.extract('year', model.Listings.list_date)==year).all()
        prices = []
    # Filter out the regions with no houses
        if len(houses) != 0:
            for houseprice in houses:
    # Extra cautious that living_sq_ft is not 0, cannot divie by 0
                if houseprice.living_sq_ft != 0:
                    psf = float(houseprice.sell_price)/houseprice.living_sq_ft
                    prices.append(psf)
                    print "Houseprice postal_code is: %r" % houseprice.postal_code
                    print "House sell date is %r" % houseprice.list_date
    # ignore any zipcodes with fewer than 10 data points
                else: 
                    median = 0
            if len(prices) > 10:
                median = numpy.median(prices)
            else:
                median = 0

            print "zcta: %r, pricelist: %r" % (region.zcta, prices)
            print "median is %r" % median
        else:
            median = 0
# set the column in the listings table to the median price
        # columninsert = 'region.median_sales_psf_' + year

        region.median_sales_psf_2013 = median

    session.commit()



def main(session):

#TODO maybe add 2005, 2006, 2007, 2008
    # region.median_sales_psf_2009
    # region.median_sales_psf_2010
    # region.median_sales_psf_2011
    # region.median_sales_psf_2012
    # region.median_sales_psf_2013

    # insert_median_sales_price(session)
    # insert_median_sales_psf(session)

    insert_median_sales_psf_year(session, 2013)
    # region.median_sales_psf_2009 = median
    # region.median_sales_psf_2010 = median
    # region.median_sales_psf_2011 = median
    # region.median_sales_psf_2012 = median
    # region.median_sales_psf_2013 = median

if __name__ == "__main__":
    s = model.connect()
    main(s)


