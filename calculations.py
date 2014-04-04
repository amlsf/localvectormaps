import model
import re
import sqlite3
import json
import numpy

zip_county_dict ={'95030' : 'Santa Clara', '95004' : 'San Benito', '95076' : 'Santa Cruz', '94303' : 'Santa Clara', '95023' : 'San Benito', '94028' : 'San Mateo', '95033' : 'Santa Clara', '93901' : 'Monterey', '94022' : 'Santa Clara', '94301' : 'Santa Clara', '95066' : 'Santa Cruz', '95122' : 'Santa Clara', '94080' : 'San Mateo', '95112' : 'Santa Clara', '95019' : 'Santa Cruz', '94065' : 'San Mateo', '94404' : 'San Mateo', '94024' : 'Santa Clara', '95120' : 'Santa Clara', '95054' : 'Santa Clara', '95041' : 'Santa Cruz', '95111' : 'Santa Clara', '95148' : 'Santa Clara', '95139' : 'Santa Clara', '93905' : 'Monterey', '94306' : 'Santa Clara', '94043' : 'Santa Clara', '95002' : 'Santa Clara', '95128' : 'Santa Clara', '95062' : 'Santa Cruz', '95134' : 'Santa Clara', '94027' : 'San Mateo', '95006' : 'Santa Cruz', '94044' : 'San Mateo', '95035' : 'Santa Clara', '94015' : 'San Mateo', '94305' : 'Santa Clara', '94402' : 'San Mateo', '93923' : 'Monterey', '95003' : 'Santa Cruz', '94070' : 'San Mateo', '95127' : 'Santa Clara', '95136' : 'Santa Clara', '94062' : 'San Mateo', '95075' : 'San Benito', '93940' : 'Monterey', '94019' : 'San Mateo', '95032' : 'Santa Clara', '95039' : 'Monterey', '93926' : 'Monterey', '95123' : 'Santa Clara', '95124' : 'Santa Clara', '94061' : 'San Mateo', '94002' : 'San Mateo', '93960' : 'Monterey', '94086' : 'Santa Clara', '95133' : 'Santa Clara', '95117' : 'Santa Clara', '95014' : 'Santa Clara', '95060' : 'Santa Cruz', '94085' : 'Santa Clara', '95070' : 'Santa Clara', '95050' : 'Santa Clara', '95064' : 'Santa Cruz', '94025' : 'San Mateo', '95017' : 'Santa Cruz', '95121' : 'Santa Clara', '94304' : 'Santa Clara', '95140' : 'Santa Clara', '95037' : 'Santa Clara', '93924' : 'Monterey', '95119' : 'Santa Clara', '95131' : 'Santa Clara', '93962' : 'Monterey', '93953' : 'Monterey', '93908' : 'Monterey', '93907' : 'Monterey', '94060' : 'San Mateo', '93925' : 'Monterey', '94063' : 'San Mateo', '95132' : 'Santa Clara', '95046' : 'Santa Clara', '94005' : 'San Mateo', '95045' : 'San Benito', '95008' : 'Santa Clara', '95007' : 'Santa Cruz', '93920' : 'Monterey', '95110' : 'Santa Clara', '95051' : 'Santa Clara', '95020' : 'Santa Clara', '93930' : 'Monterey', '93906' : 'Monterey', '93933' : 'Monterey', '94037' : 'San Mateo', '94010' : 'San Mateo', '95130' : 'Santa Clara', '94087' : 'Santa Clara', '94041' : 'Santa Clara', '94020' : 'San Mateo', '95043' : 'San Benito', '94030' : 'San Mateo', '95012' : 'Monterey', '95126' : 'Santa Clara', '95135' : 'Santa Clara', '95125' : 'Santa Clara', '95065' : 'Santa Cruz', '94038' : 'San Mateo', '94403' : 'San Mateo', '95116' : 'Santa Clara', '95010' : 'Santa Cruz', '95129' : 'Santa Clara', '94014' : 'San Mateo', '94089' : 'Santa Clara', '94066' : 'San Mateo', '93950' : 'Monterey', '95118' : 'Santa Clara', '93921' : 'Monterey', '95018' : 'Santa Cruz', '94401' : 'San Mateo', '94040' : 'Santa Clara', '93927' : 'Monterey', '95005' : 'Santa Cruz', '93955' : 'Monterey', '95073' : 'Santa Cruz', '95138' : 'Santa Clara'}

# Gets total sales prices for SP and SPS radio buttons
def total_median(session):
    regions = session.query(model.Zipcodes).all()

    medians = {}
    for region in regions:
        # session.query(model.Listings)
        # print region.geoid
        medians[region.geoid] = {'median_sales_price':region.median_sales_price,
                'median_sales_psf':region.median_sales_psf,
                'count_median_sales':region.count_median_sales,
                'county': zip_county_dict[region.geoid]  
                }

    return json.dumps(medians)


def psf_median_comp(session, year1, year2):
    regions = session.query(model.Zipcodes).all()

    growth = {}
    for region in regions:

#this should only return one row
        year1result = session.query(model.Zipcodeannual).filter_by(geoid=region.geoid, year=year1).all()
        year2result = session.query(model.Zipcodeannual).filter_by(geoid=region.geoid, year=year2).all()

        # .filter(model.extract('year', model.Zipcodeannual.year)==year1)
        basemedian = year1result[0].year_median_spsf
        compmedian = year2result[0].year_median_spsf

        if basemedian != 0 and compmedian != 0:
            change = float(compmedian)/basemedian-1 
        else: 
            change = -2

        growth[region.geoid] = {'change':change,
                'baseSp':year1result[0].year_median_sp,
                'basePsf':basemedian,
                'baseCount':year1result[0].year_count_median_sp,
                'compSp':year2result[0].year_median_sp,
                'compPsf':compmedian,
                'compCount':year2result[0].year_count_median_sp,
                'county': zip_county_dict[region.geoid]}

    return json.dumps(growth)


def main(session):
    total_median(session)
    # psf_median_comp(session, 2005, 2006)
    
    # sp_median_byzip(session)
    # psf_median_byzip(session)
    # psf_median_comp(session, 2009, 2012)
    
    # county_activemedian(session)
    # county_psf(session)
    # range_comp(session, 2011, 2013)

if __name__ == "__main__":
    s = model.connect()
    main(s)


