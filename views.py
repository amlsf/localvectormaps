from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import calculations
import json

app = Flask(__name__)
app.config.from_object(config)

model.session = model.connect()

app.secret_key = "secretkey"


@app.route("/")
def leaflet():
    return render_template("leaflet.html")

# returns active listings longlat for making active listings markers
@app.route("/leafactivelistings")
def leafactive():
    active_listings = model.session.query(model.Listings).filter_by(listing_status='Active').all()
    activelatlong = [
        {'latitude': l.latitude, 'longitude': l.longitude, 'list_price': l.list_price, \
        'bathrooms': l.bathrooms_count, 'bedrooms': l.bedrooms_count, 'squarefeet': l.living_sq_ft, \
        'address': l.address, 'city': l.city_name, 'postal_code': l.postal_code, 'county': l.county_name, \
        'neighborhood': l.neighborhood, 'mls_id': l.mls_id, 'description': l.description, 'url': l.property_url} \
        for l in active_listings
        ]
    return json.dumps(activelatlong)

# retuns JSON dictionary of geoid:medianprice per region
@app.route("/geoidpricesajax")
def geoidpricesajax():    
    return calculations.total_median(model.session)

@app.route("/geochanges", methods=['PUT','POST'])
def geochanges():
    # try:
    body = request.json
    # print request.json
    baseyear = int(body["baseyear"])
    # print baseyear
    compyear = int(body["compyear"])
        # print compyear
    # except ValueError, err:
    #     print 'Error: ' + err
    #     return
    return calculations.psf_median_comp(model.session, baseyear, compyear)

leafactive()

if __name__ == "__main__":
    app.run(debug=True)
