from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model

app = Flask(__name__)
app.config.from_object(config)

model.session = model.connect()

block_groups = model.session.query(model.Blockgroups).all()

#TODO look into insertion sort algorithm to speed up? 
for bg in block_groups:
    houses = model.session.query(model.Listings).filter_by(bg_id=bg.id).all()
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

    bg.color = median
#TODO - change color later, not need for sliders and checkboxes filtering

session.commit()