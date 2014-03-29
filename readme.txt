# NOTE FROM AMY

Please look at leaflet-start branch, ignore master
Please ignore all other files except the following:

FRONT END

1. leaflet.html - this is the main html file (you will notice in the views.py that the url route "/leaflet" is the main route to view that renders this template

2. leaflet.js

3. master.html - this is just a "wrapper" with the basic structural template of the page

4. CSS files aren't really being used yet (but the main one being imported other than leaflet API ones are leaflet.css, main.css, and bootstrap.

BACK END

1. views.py this is the main file that determines the routes and data fed to the front end

2. calculations.py this is the file for calculations and database querying referenced in views.py

3. model.py is my data model


DATA PRE-PROCESSING (these are less important, just for one time data processing)

1. seed.py this seeds data to my Postgres database from files held in my local directory

2. pointsinpolygon.py Ray Casting algorithm that places each house longlat in appropriate region
