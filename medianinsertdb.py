import model
import re
# import sqlite3
import json
import numpy

# This script inserts to each zipcode in Zipcodes table the total median price, median PSF price, count for all time and per year

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
        region.count_median_sales = len(prices)

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



def populate_prices_table(session, year):
    regions = session.query(model.Zipcodes).all()

    for region in regions:

# # PART I - get the aggregate data 
#         houses = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').all()

# # PART 1 whole median price for whole period
#         total_prices = []
#         for houseprice in houses:
#             total_prices.append(houseprice.sell_price)
#             print "Houseprice postal_code is: %r" % houseprice.postal_code
# # ignore any zipcodes with fewer than 10 data points
#         if len(total_prices) > 10:
#             total_median = numpy.median(total_prices)
#         else:
#             total_median = 0

#         print "zcta: %r, pricelist: %r" % (region.zcta, total_prices)
#         print "total median is %r" % total_median

# # PART 2 median price psf for whole period
#         total_psf_prices = []
#     # Filter out the regions with no houses
#         if len(houses) != 0:
#             for houseprice in houses:
#     # Extra cautious that living_sq_ft is not 0, cannot divie by 0
#                 if houseprice.living_sq_ft != 0:
#                     psf = float(houseprice.sell_price)/houseprice.living_sq_ft
#                     total_psf_prices.append(psf)
#                     print "Houseprice postal_code is: %r" % houseprice.postal_code
#     # ignore any zipcodes with fewer than 10 data points
#                 else: 
#                     total_median_psf = 0
#             if len(total_psf_prices) > 10:
#                 total_median_psf = numpy.median(total_psf_prices)
#             else:
#                 total_median_psf = 0

#             print "zcta: %r, pricelist: %r" % (region.zcta, total_psf_prices)
#             print "median is %r" % total_median_psf
#         else:
#             total_median_psf = 0

# PART II - get the yearly data 
        houses_year = session.query(model.Listings).filter_by(zip_id=region.id, property_type='Res. Single Family').filter(model.extract('year', model.Listings.list_date)==year).all()
# PART 3 this will just take sold listings total sales prices per year
        prices = []
        for houseprice in houses_year:
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


# PART 4 calculates the psf per year
        psf_prices = []
    # Filter out the regions with no houses
        if len(houses_year) != 0:
            for houseprice in houses_year:
    # Extra cautious that living_sq_ft is not 0, cannot divie by 0
                if houseprice.living_sq_ft != 0:
                    psf = float(houseprice.sell_price)/houseprice.living_sq_ft
                    psf_prices.append(psf)
                    print "Houseprice postal_code is: %r" % houseprice.postal_code
                    print "House sell date is %r" % houseprice.list_date
    # ignore any zipcodes with fewer than 10 data points
                else: 
                    psf_median = 0
            if len(psf_prices) > 10:
                psf_median = numpy.median(psf_prices)
            else:
                psf_median = 0

            print "zcta: %r, pricelist: %r" % (region.zcta, psf_prices)
            print "psf_median is %r" % psf_median
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


def main(session):

    # insert_median_sales_price(session)
    # insert_median_sales_psf(session)

    # populate_prices_table(session, 2005)

    for year in range(2006,2014):
        populate_prices_table(session, year)

if __name__ == "__main__":
    s = model.connect()
    main(s)


