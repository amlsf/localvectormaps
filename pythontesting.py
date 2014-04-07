import unittest
import model
import medianinsertdb
import seed
import calculations
import json

# class TestZipcodes(unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.session = model.connect("postgresql+psycopg2://postgres:password@localhost/testlocalvector")

#     def setUp(self):
#         seed.load_zips(self.session)
#         seed.load_slist(self.session, "data/offmarket3fix_5onlyTEST2.csv") 

#     def tearDown(self):
#         self.session.query(model.Listings).delete()
#         self.session.query(model.Zipcodes).delete()
#         self.session.commit()

#     def test_insert_median_sales_price(self):
#         medianinsertdb.insert_median_sales_price(self.session)
        
#         one_row = self.session.query(model.Zipcodes).filter_by(geoid='93426').all()
#         self.assertEqual(one_row[0].median_sales_price, 0)
#         self.assertEqual(one_row[0].count_median_sales, 1)

#         ten_rows = self.session.query(model.Zipcodes).filter_by(geoid='94019').all()
#         self.assertEqual(ten_rows[0].median_sales_price, 0)
#         self.assertEqual(ten_rows[0].count_median_sales, 10)

#         twenty_rows = self.session.query(model.Zipcodes).filter_by(geoid='93908').all()
#         self.assertEqual(twenty_rows[0].median_sales_price, 319000)
#         self.assertEqual(twenty_rows[0].count_median_sales, 20)

#         eleven_rows = self.session.query(model.Zipcodes).filter_by(geoid='93921').all()
#         self.assertEqual(eleven_rows[0].median_sales_price, 810000)
#         self.assertEqual(eleven_rows[0].count_median_sales, 11)

#         no_rows = self.session.query(model.Zipcodes).filter_by(geoid='93925').all()
#         self.assertEqual(no_rows[0].median_sales_price, 0)
#         self.assertEqual(no_rows[0].count_median_sales, 0)


#     def test_insert_median_sales_psf(self):
#         medianinsertdb.insert_median_sales_psf(self.session)

#         one_row = self.session.query(model.Zipcodes).filter_by(geoid='93426').all()
#         # one_row_round = one_row[0].median_sales_psf
#         self.assertEqual(one_row[0].median_sales_psf, 0)

#         ten_rows = self.session.query(model.Zipcodes).filter_by(geoid='94019').all()
#         self.assertEqual(ten_rows[0].median_sales_psf, 0)

#         twenty_rows = self.session.query(model.Zipcodes).filter_by(geoid='93908').all()
#         twenty_rows_round = round(twenty_rows[0].median_sales_psf,3)
#         self.assertEqual(twenty_rows_round, float(228.197))

#         eleven_rows = self.session.query(model.Zipcodes).filter_by(geoid='93921').all()
#         eleven_rows_round = round(eleven_rows[0].median_sales_psf,3)
#         self.assertEqual(eleven_rows_round, float(1193.333))

#         no_rows = self.session.query(model.Zipcodes).filter_by(geoid='93925').all()
#         self.assertEqual(no_rows[0].median_sales_price, None)


class TestZipcodeannual(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.session = model.connect("postgresql+psycopg2://postgres:password@localhost/testlocalvector")

    def setUp(self):
        seed.load_zips(self.session)
        seed.load_slist(self.session, "data/offmarket3fix_5onlyTEST2.csv") 

    # def tearDown(self):
    #     self.session.query(model.Listings).delete()
    #     self.session.query(model.Zipcodes).delete()
    #     self.session.query(model.Zipcodeannual).delete()
    #     self.session.commit()

    def test_populate_prices_table(self):
        for year in range(2006, 2014):
            medianinsertdb.populate_prices_table(self.session, year)

        one_row = self.session.query(model.Zipcodeannual).filter_by(geoid='93426', year=2013).all()
        self.assertEqual(one_row[0].year, 2013)
        self.assertEqual(one_row[0].year_median_sp, 0)
        self.assertEqual(one_row[0].year_median_spsf, 0)
        self.assertEqual(one_row[0].year_count_median_sp, 1)

        ten_rows = self.session.query(model.Zipcodeannual).filter_by(geoid='94019', year=2013).all()
        self.assertEqual(ten_rows[0].year, 2013)
        self.assertEqual(ten_rows[0].year_median_sp, 0)
        self.assertEqual(ten_rows[0].year_median_spsf, 0)
        self.assertEqual(ten_rows[0].year_count_median_sp, 10)

        # same zipcode for eleven and twenty rows
        eleven_rows_mixedyr = self.session.query(model.Zipcodeannual).filter_by(geoid='95124', year=2006).all()
        self.assertEqual(eleven_rows_mixedyr[0].year, 2006)
        self.assertEqual(eleven_rows_mixedyr[0].year_median_sp, 660000)
        eleven_rows_round = round(eleven_rows_mixedyr[0].year_median_spsf,3)
        self.assertEqual(eleven_rows_round, 644.231)
        self.assertEqual(eleven_rows_mixedyr[0].year_count_median_sp, 11)

        twenty_rows_mixedyr = self.session.query(model.Zipcodeannual).filter_by(geoid='95124', year=2007).all()
        self.assertEqual(twenty_rows_mixedyr[0].year, 2007)
        self.assertEqual(twenty_rows_mixedyr[0].year_median_sp, 629500)
        twenty_rows_round = round(twenty_rows_mixedyr[0].year_median_spsf,3)
        self.assertEqual(twenty_rows_round, 614.663)
        self.assertEqual(twenty_rows_mixedyr[0].year_count_median_sp, 20)

        no_rows = self.session.query(model.Zipcodeannual).filter_by(geoid='95124', year=2008).all()
        self.assertEqual(no_rows[0].year, 2008)
        self.assertEqual(no_rows[0].year_median_sp, 0)
        self.assertEqual(no_rows[0].year_median_spsf, 0)
        self.assertEqual(no_rows[0].year_count_median_sp, 0)

# class Testgrowth(unittest.TestCase):
#     @classmethod
#     def setUpClass(self):
#         self.session = model.connect("postgresql+psycopg2://postgres:password@localhost/testlocalvector")

#     def setUp(self):
#         seed.load_zips(self.session)
#         seed.load_slist(self.session, "data/offmarket3fix_5onlyTEST2.csv") 

#     def tearDown(self):
#         self.session.query(model.Listings).delete()
#         self.session.query(model.Zipcodes).delete()
#         self.session.query(model.Zipcodeannual).delete()
#         self.session.commit()

#     def test_psf_median_comp(self):
#         for year in range(2006, 2014):
#             medianinsertdb.populate_prices_table(self.session, year)

#         zip_95124 = calculations.psf_median_comp(self.session, 2006, 2007)
#         zip_95124 = json.loads(zip_95124)

#         change = round(zip_95124['95124']['change'], 4)

#         self.assertEqual(change, -0.0459)

#         self.assertEqual(zip_95124['95124']['baseSp'], 660000)
#         basePsf = round(zip_95124['95124']['basePsf'],3)
#         self.assertEqual(basePsf, 644.231)
#         self.assertEqual(zip_95124['95124']['baseCount'],11)

#         self.assertEqual(zip_95124['95124']['compSp'], 629500)
#         compPsf = round(zip_95124['95124']['compPsf'],3)
#         self.assertEqual(compPsf, 614.663)
#         self.assertEqual(zip_95124['95124']['compCount'],20)

#         self.assertEqual(zip_95124['95124']['county'],'Santa Clara')


if __name__ == '__main__':
    unittest.main()
