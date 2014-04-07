LocalVector Maps
=================
LocalVector Maps is a real estate data visualization and exploratory tool that uses colorful choropleth maps as an intuitive approach to help residential real estate buyers quickly absorb a large amount of data in order to compare local prices, identify specific high growth areas, visualize the recovery of the real estate market since the 2009 meltdown, and explore homes currently for sale within five Bay Area counties. 

I built this application with the goal to make a large amount of data useful and easily digestible. Partially due to the proprietary nature of the MLS data used in this application, I noticed a lack of exploratory, interactive tools that displayed real estate growth and recovery over time in addition to price levels. While line graphs exist that show growth, they are limiting in the number of regions that can be compared at the same time.

I had in mind people like my parents and other mom-and-pop investors who invest their nest eggs in real estate on the side with their nest eggs and have limited access to research tools that help them gain a bigger picture understanding of the landscape of investment opportunities. This app will be hosted shortly as a new feature in a friend's real estate startup, LocalVector.

Developed in 3.5 weeks at Hackbright Academy's Software Engineering Fellowship in the Winter 2014 cohort. 

#####Note on cloning this repository:
Note that this application uses licensed Multiple Listing Services (MLS) data, it is not possible to run this repository locally on your machine. The site where the app will be hosted will be posted shortly.

#####Technologies & tools used:
The application is built using the Flask framework and is written in Python in the back-end, Javascript in the front-end, and uses a PostgreSQL database.

1. Front-end: Javascript, jQuery, AJAX, HTML, CSS, Bootstrap, D3
2. Back-end: Python, Flask, SQLAlchemy, PostgreSQL
3. GIS-related: Leaflet API, Cloudmade, QuantumGIS, GeoJSON, Python shapefile library, markercluster library

Summary of Features
-------------------

![Main page] (/screenshots/1openingpage.JPG)
![Other page] (/screenshots/10-activelistings.JPG)

#####1. Choropleth Map 
The map offers visualization of 3 different metrics split out by zipcode. A button in the control panel on the left toggles off the choropleth layer if users want a clearer view of the map. For a more intuitive experience, the controls showing the metric options disappear when the user turns toggles off the choropleth. The three metric options displayed on the map are:  
  *	Median sales price of homes
  *	Median sales price per square foot
  *	Percent change in median sales price between any two years of the user's choice 
      *	This uses a diverging color scheme instead of sequential as for the metrics above. 
      *	The Python script ensures a minimum number of houses in each region to avoid skewing the data

#####2. Range slider for year on year comparison
  * When a user selects the third metric (price change comparison) to view, a range slider appears that allows a selection of any base year and comparison year to view the % change in median price between the two years. 

#####3.	Information boxes on mouseover
  * When the mouse hovers over any region, the region is highlighted and an information box on the upper right corner shows additional details about the region such as median price and number of homes sold, and exact % change where appropriate.
  * Additionally, in the Price Comparison heatmap view, a time series chart displays the median price/sqft each year for the mouseover region.
  * Clicking on any particular region automatically zooms in to pull the region into the full viewport.

#####4.	Legend 
  *	The legend updates dynamically with the dataset with a clear label giving the user a clear understanding of what she is viewing. It updates based on the metric and the years selected. 
  *	The code allows the legend to automatically scale with the range of any particular dataset that the user chooses to view

#####5.	Toggle Active listings & Markerclusters
  *	In the control panel on the left, a button allows user to toggle on markers for active listings. When the users click on the markers, a pop-up displays showing detailed listing information including list price, address, # of beds/bath, a description of the property, and the MLS listing number. Users can also click on the address and be taken to a separate detailed listings page.  
  *	The display uses a markercluster API to improve performance and avoid overwhelming the user with too many markers. When the user mouses over a particular cluster, a polygon appears on the map displaying what region the cluster covers. Upon clicking the cluster, the map automatically zooms in and the clusters split out into smaller clusters and map pins at the most zoomed in level. Double clicking zooms back out to the original view.   


Project Walk Through
--------------------
###Planning
######Leaflet, Cloudmade, OpenStreetMap

With no prior experience with GIS or cartography, one of the biggest tasks was determining what data I wanted use and how to display it on the map, as well as navigating the sea of geo systems and tools. It was quite a challenge finding and quickly getting up to speed on the ecosystem of tools in the geo space, understanding how they fit together and their pros and cons to decide which ones would be best suited for this project. 

The application uses the Leaflet and Cloudmade API. I built some preliminary applications using Google Maps and explored Mapbox and CartoDB, but Leaflet had more features and 3rd party libraries I could use for customizing a map, had excellent documentation, and because it's open source, I didn't need to worry about Terms of Service. 

Choropleth maps are thematic maps in which areas are shaded or patterned in proportion to the measurement of statistical variable. They're similar to heatmaps, though I chose not to go down that route because in cartography (and I discovered all the heatmap libraries used this method), in addition to values, heatmaps also reflect the density of data points in a region, which would not have been an accurate representation of the data for the purposes of this project. 

In terms of granularity of detail, I felt that either the zipcode or neighborhood level would be granular enough without being overwhelming and ultimately settled on zipcodes as neighborhood boundaries were less clear cut. I chose to start with 3 metrics: sales price for those with a budget in mind, sales price per square foot to normalize for an apples-to-apples comparison, and price % change between any two years of the user's choosing between 2006-2013. 

###Acquiring and Parsing Real Estate and Geo Data
######QuantumGIS, Shapefile library, Mapquest Bulk Geocoder, PostgreSQL, SQLAlchemy
A bulk of the work involved writing the various Python scripts to parse the geodata and pre-process the real estate data. 

The US Census Bureau has large shapefiles gigabytes in size containing latitude and longitudinal pairs of the polygon vertices to draw each region onto a map throughout the US. Many of the regions consist of hundreds of vertices and multiple separate polygons. 

I learned how to use an open source GIS system called QuantumGIS to quickly visualize the shapefiles and convert them to a GeoJSON format for displaying as a layer on the map. I also used the Python shapefile library to extract data from the shapefile and seed into my database where I then trimmed the unnecessary regions. I wrote another Python script to modify the GeoJSON to extract a subset of the data once I determined those regions from the previous step in the process. It was an interesting task to figure out how to structure and store all the longlat data so that it could be accessed easily and written with less code.  

I then used the Python csv module to seed the MLS data of over 200,000 homes into my database, while validating, cleaning and normalizing the data. The next step was to use a tool provided by Mapquest to bulk geocode the addresses to acquire their latlong coordinates for placement on the map.

###Displaying Data with Performance in Mind
######AJAX, JQuery, Markercluster library, GeoJSON

I had originally used a Leaflet feature that drew each region's polygon by feeding my latlong data from the database to the client, but found this to be extremely slow so I switched to another method that used GeoJSON formats so that the frontend could handle all drawing of each polygon and avoided making extra server calls. While this increased the speed, it was still slower than I would have liked. I then switched to using a smoothed out version of the shapefiles with simplified vertices that still retained the shape. (As a next step for the future, to further improve performance by avoiding drawing hundreds of polygons altogether, I would want to use a tool called Tilemill to style the tiles ahead of time and then Mapbox's hosting services to serve the tiles/data.) 

The next step was to write a number of scripts to pre-calculate the various metrics I planned to display on the map. I had originally coded the server side to calculate these metrics dynamically with each client request, but found this affected performance negatively. So I updated my database model and wrote the scripts to pre-process and store as much of the metric calculations in the database ahead of time as possible, such as the medians of the total price, price per square foot, and number of homes sold broken out by region and time period. As I plan to build out more features and filters in the future that allow more combinations of options for the users, I would likely need to consider more of a balance between pre-calculations, server-side and client-side computations.

Initially, I tried rendering the active listings as individual markers but identified that having the Leaflet API draw each marker individually as a performance bottleneck. I investigated other rendering techniques such as UTFGrids and markerclustering, ultimately deciding on the latter. This not only improved the speed but also the user experience and navigation. While the markerclustering library is handling the rendering and animation, I needed to prepare the data to be rendered and figure out how to pass it correctly and quickly to achieve this result. I initially used Jinja, the method we learned in Hackbright's curriculum, to pass the data from the back-end to the front-end but switched over to JSON and AJAX techniques to improve efficiency. 

Another complication was how to pass the relative values to the render the appropriate color in each region. Normally, the API assumes you have your values embedded in the GeoJSON. However, in my case, the map displayed different subsets of data and rendering a different GeoJSON for each dataset would have been time-consuming and inefficient. I used an AJAX call to a handler that created a separate JSON with just the relative values to then link together with the GeoJSON data on the client side. 

######Jquery UI, Bootstrap, D3

On the front-end I used the Jquery UI library for the range slider, bootstrap to style the buttons, Mapbrewer to select the colorscheme, and D3 for the time series graphs.

Sample Data Insights
--------------------
Here is a sample scenario of how a user might find insight from this tool and use it to then research possible homes to purchase. 

By 2009-2010, real estate home values had reached bottom compared to the peak in 2006. If you select the slider bar to compare 2006 as the base year and 2009 as the comparison year, this is the apparent from the overwhelming warm colors covering the map. 
![Loss] (/screenshots/3-2006-2009.JPG)

Recently, real estate values have been recovering as you can see from the overwhelming green when you select 2011-2013 on the range slider. As one might expect, growth is especially strong near San Francisco, around Palo Alto, and Monterrey. 
![Growth] (/screenshots/4-2011-2013.JPG)

If you compare using the baseline of the 2006 peak in order to gauge whether prices have returned to previous highs by comparing each of the years of 2010-2013 to 2006, you'll notice a single, rapidly growing green hot spot centered around Mountain View and Palo Alto, which indicates those regions have median home values that are now exceeding 2006 highs and are growing at a faster pace than the areas around San Francisco and Monterrey, which have not yet returned to previous highs. 
![Improving] (/screenshots/6-2006-2011.JPG)
![Improving More] (/screenshots/8-2006-2013.JPG)

You might then toggle on the active listings and research homes currently for sale around the fringes of the growing green hotspot or speculate that San Francisco and Monterrey still have good potential for growth. 
![Searching] (/screenshots/9-2006-2013 with clusters.JPG)

Extensions
----------
#####Additional Options and Filters

In the future, I'll be adding options to view additional cuts of the data, including the ability to filter by number of bedrooms, baths, square footage and price level both for the heatmap and the active listing markers. I would also like to create different zoom levels that show the regions broken out with increasing granularity such as block groups. 

I realized from the project this is much more complex than it seems in terms of both coding and managing performance. For one thing, as I noted earlier, as the number of permutations of options that a user can select grows, it makes it less feasible to pre-calculate and store every scenario in the database and having intensive dynamic server side calculations can significantly slow down the application. 

On the front-end coding side, I noticed that as you add more options, the complexity involved with number of conditional statements and edge cases grows (along with your code) at a quadratic rate. As of now, I have my code written such that every change a user makes triggers a chain of reactions across the page, so each time a new option is introduced, the number of interactions, code accounting for conditionals and edge cases grows at a quadratic rate. Ideally the code would grow at a linear rate with additional user optionality. To achieve this, I would need to refactor my code and build a unified change hander that acts as a function of the overall state of the form at any time.

In addition, since block group information isn't available in my real estate data, I would need to run a Ray Casting algorithm to determine the membership of each home within the appropriate block group. This might also require using the UTFGrid technique to handle the large amount of data objects on the map.

#####Interactive Time Series Graphs

I'd like to create interactive time series line graphs that allow the user to select multiple metrics and regions to compare on the same graph. 

#####Predictive Analytics

The next step would be to create predictive algorithms that focus on predicting future prices and growth potential. One idea is to run linear regressions on each region and identify potentially undervalued homes based on where the ask price falls relative to the linear regression. 
