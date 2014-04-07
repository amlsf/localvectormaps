from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import model
import calculations
import json
import sys

app = Flask(__name__)
app.config.from_object(config)

if len(sys.argv) < 2:
    connectionstring = model.defaultconnectionstring
else: 
    connectionstring = sys.argv[1]

model.session = model.connect(connectionstring)

app.secret_key = "secretkey"


@app.route("/")
def leaflet():
    return render_template("leaflet.html")

# returns active listings longlat for making active listings markers
@app.route("/leafactivelistings")
def leafactive():
    return calculations.active_listings(model.session)

# retuns JSON dictionary of geoid:medianprice per region
@app.route("/geoidpricesajax")
def geoidpricesajax():    
    return calculations.total_median(model.session)

@app.route("/geochanges", methods=['PUT','POST'])
def geochanges():
    # try:
    body = request.json
    baseyear = int(body["baseyear"])
    compyear = int(body["compyear"])
        # print compyear
    # except ValueError, err:
    #     print 'Error: ' + err
    #     return
    return calculations.psf_median_comp(model.session, baseyear, compyear)


@app.route("/play")
def graphs():
    return render_template("testgraphs.html")




leafactive()

if __name__ == "__main__":
    app.run(debug=True)
