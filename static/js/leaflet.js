//TODO: factor out code so not so many global variables
// TODO maybe use leaflet layer controls http://leafletjs.com/examples/layers-control.html
//TODO How to organize when there are so many f-ing dependencies????
// Gotta speed up the layering of geoJSON - too slow! Maybe change to county, subcounty, zips (no BG, census tracts?)

mapid = 125674;
// TODO: set as env var
apikey = "99d055cec8794a33b9e2cb09553e3506";

var map = L.map('map').setView([37.785067, -122.473021], 7);

// initialized when /geoidpricesajax result is available
var geoIdPrices = null;
var geoIdPricesMax = null;
var geoIdPricesMin = null;
// var maxPrice = null;
// var minPrice = null;
// var blocks = null;
var blocks = null;
var heatLayer;

// route variables for radio button selections
var geoidpricesajax = "/geoidpricesajax";
var psf = "/psf";
var geochanges = "/geochanges";

var initLeaflet = function (active_listings) {

    // var metric_route = geoidpricesajax;
    // var region = counties;

    addBaseMap();
    showHeatMap(counties, geoidpricesajax);
    // addCounties();
    // addBlockGroups();

    toggleHeatMap(counties);
    showActive();
    selectMetric();


//////////////////////Zoom function
    map.on("zoomend",function(e){
      console.log( "zoom level is " + map.getZoom());
      var zoom = map.getZoom();
      if (zoom < 10) {
        showHeatMap(counties, geoidpricesajax);
      } else if (zoom < 12) {
        map.removeLayer(heatLayer);
        addBlockGroups();
      }
    });
};


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

// SECTION lays base map and region geojson layers
function addBaseMap() {
    L.tileLayer('http://{s}.tile.cloudmade.com/'+apikey+'/'+mapid+'/256/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    maxZoom: 20
}).addTo(map);
}

// counties is defined in the geojson js file imported in script tag in html
function addCounties(){
    L.geoJson(counties).addTo(map);
}

function addBlockGroups(){
    L.geoJson(blockgroups).addTo(map);
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION creates active listing markers
var markers = new L.FeatureGroup();

function createMarkers(active_listings) {
    for (i = 0; i < active_listings.length; i++) {
      var marker = L.marker(active_listings[i]);
      markers.addLayer(marker);
      break;
  }
  map.addLayer(markers);
}


// TODO QUESTION: note to self: 'event' is when the input[] "active" .changes (.target is the object)
// TODO why doesn't a .click() or .toggle() work?
// TODO why is this removing the map? (works when just add one marker)
// TODO make this go faster (special layer or cluster circles-show more markers as zoom in-view only) (see Rhonda's emails)
// TODO schedule deferred exeecution with setTimeout function at 0 ms of adding gmarkers before re-enabling form and removing spinner?
// Toggle checkbox to display active listings
function showActive() {
  $('input[name=active]').change(function(event) {
    if (event.target.checked) {
  // this disables checkbox
      event.target.disabled = true;
// TODO put spinner bar in here? 
    // $('#imgid').show()
      // console.log('disabled checkbox');
      $.ajax({
        url: "/leafactivelistings",
      }).done(function(data) {
        prices = $.parseJSON(data);
        createMarkers(prices);
        // addActiveMarkers(prices);
        event.target.disabled = false;
        // $('#imgid').hide()
      });
    } else {
      map.removeLayer(markers);
    }
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////

// SECTION Adds/removes colors the choropleth map

// get max and min price in region and $ amount per block level, called in getLevel()
// geoIdPrices is a global variable that is defined in ajax call in showHeatMap() function 
// remove the counties with nothing so not calculated in min price
function getBlocks() {
  var prices = [];
  for (var key in geoIdPrices) {
      if (geoIdPrices[key] !== 0) {
      prices.push(geoIdPrices[key]);
      }
  }
    maxPrice = Math.max.apply(Math, prices);
    minPrice = Math.min.apply(Math, prices);
    blocks = (maxPrice - minPrice)/4;
    // console.log("price list is" + prices);
    // console.log("maxprice is " + maxPrice);
    // console.log("minprice is " + minPrice);
    // console.log("block amount is " + blocks);
    return {maxPrice: maxPrice,
      minPrice: minPrice,
      blocks: blocks
    };
}

// use the blocks to determine the particular house price color level, called in style fxn with getColor()
function getLevel(price) {
    blocks = getBlocks();
    level = (price - blocks.minPrice)/blocks.blocks;
    return level;
}

// dicts of color levels, called in style function with getLevel()
// This is shorthand notation ? is "if" then do what's before colon:, else do whatever is after 
function getColor(level) {
    return level > 3 ? '#800026' :
           level > 2  ? '#BD0026' :
           level > 1  ? '#E31A1C' :
           // d > 100  ? '#FC4E2A' :
           // d > 50   ? '#FD8D3C' :
           // d > 20   ? '#FEB24C' :
           // d > 10   ? '#FED976' :
           level > 0 ? '#FFEDA0':
                      '#FFFFFF';
}
// var colorDict = {
//     1: "#F1917C",
//     2: "#F18064",
//     3: "#D67159",
//     4: "#D65E3A"
// }


// This is used in heatColors(), iterates through counties by geoID in heatColors and pulls geoID
var style = function(feature) {
// TODO check: this references my geojson, actually wouldn't I change it to the variable name.dictkey.dictkey?
    var geoId = feature.properties.GEO_ID;
    // console.log(geoIdPrices);
    return {
    // replace median with geoIdPrices[geoId]
        fillColor: getColor(getLevel(geoIdPrices[geoId])),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
};

// this iterates through style function and matches geoid from counties geojson to style dict (same as style() if had done other notation in setting up style function)
function heatColors(region) {
    heatLayer = L.geoJson(region, {
      style: style,
// This is from user interaction section for hover and click in
      onEachFeature: onEachFeature
    }).addTo(map);
}

function showHeatMap(region, urli) {
      $.ajax({
// pulls "data" from the data returned in the path /geoidpricesajax
      url: urli,
// .done is a callback, submits function and waits for callback
      }).done(function(data){
// extra careful with browser issues
      if (console && console.log ) {
// takes JSON data and converts it JS objects 
        geoIdPrices = $.parseJSON(data);
// call heatColors AFTER stuff above has loaded
      // console.log(geoIdPrices)
        heatColors(region);
      }
    });
}

// toggle checkbox to show and remove heatmap layer
// TODO change this to a toggle button like Gmaps one with abbreviated notation
// TODO why is the disabled not working when toggling heatmap back on? 
function toggleHeatMap(region) {
  $('input[name=toggleheat]').change(function(event){
    if (event.target.checked) {
      event.target.disabled = true;
      heatColors(region);
      event.target.disabled = false;
    } else {
      map.removeLayer(heatLayer);
    }
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION User interaction - hover and click in to region
// highlight and bring to front e.target (action for mouseover)
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });
// IE and Opera have issues with bringToFront on mouseover
    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
// for mousehover pop-up info (see section in info pop-ups)
    info.update(layer.feature.properties);
}

// reset to default colors (action for mouseout)
function resetHighlight(e) {
    heatLayer.resetStyle(e.target);
// for mousehover pop-up info to remove (see section in info pop-ups)
    info.update();
}

// click listener that zooms to the state
function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

// used in heatColors() fxn
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION show info pop-ups on mouse hover
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that will update the control based on feature properties passed (tied to user interaction onEachFeature() highlight and reset features)
info.update = function (props) {
    this._div.innerHTML = '<h4>Median Value</h4>' +  (props ?
        '<b>' + props.NAME + '</b><br />' + props.GEO_ID + ' name / geoid'
        : 'Hover over a region');
};

info.addTo(map);

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION Legend
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 1, 2, 3, 4],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i]) + '"></i> ' +
            grades[i] + (grades[i - 1] ? '&ndash;' + grades[i + 1] + '<br>': '<br>');

            // '<i style="background:' + getColor(grades[i]) + '"></i> ' +
            // grades[i] + (grades[i - 1]
            //              ? '<br>'
            //              : (condition ? true : '&ndash;' + grades[i + 1] + '<br>'));
    }

    return div;
};

legend.addTo(map);


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION select metrics to view on choropleth map
function selectMetric(){
  $('#SP, #SPS, #SPSC').change(function(){
    if ($('input[name=toggleheat]').is(":checked")){
      if ($("#SP").is(":checked")) {
        console.log("you clicked SP");
        map.removeLayer(heatLayer);
        showHeatMap(counties, geoidpricesajax);
      } else if ($("#SPS").is(":checked")) {
        console.log("you clicked SPS");
        map.removeLayer(heatLayer);
        showHeatMap(counties,psf);
      } else if ($("#SPSC").is(":checked")) {
        console.log("you clicked SPSC");
        map.removeLayer(heatLayer);

// TODO trying to just get the slider bar and label to show when click on SPSC, need to also remove when not clicked
    // var sliderLabel =
    //   "<p><label for='year'>Year-on-year comparison:</label><input type='text' id='year' style='border:0; color:#f6931f; font-weight:bold;'' readonly></p>";

    // $('#slider-range').prepend(sliderLabel);

      }
    }
  });
}


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// TODO Make this work - make sure only works/shows when "Sales PSF Comparison" is checked
//  Think I need to make it somehow clear when it changes again
// TODO make this slider work for sales price and sales PSF ranges too? (But sthg needs to look diff since would be inclusive whereas this is just YoY)
// TODO understand what's happening here
// TODO get it so that the first view that shows is the 2007-2013 range upon click of radio button
  // make so doesn't show when toggle heatmap button unchcked, remove this document ready stuff and put it in a function and attach event handler

// This is the double slider for % change
 $(function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 2006,
      max: 2013,
      // default values
      values: [ 2007, 2013 ],
      // TODO: this pulls the values from the slider and puts it on the label, what's below?
      slide: function( event, ui ) {
        $( "#year" ).val( "" + ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      },
      // when anything changes, run the function growthChange()
      change: function(event, ui) {
        growthChange(ui.values[ 0 ], ui.values[ 1 ], geochanges, counties);
      }
      // ,
      //   stop: function(event, ui) {
      //       // when the user stopped changing the slider
      //       $.POST("to.php",{first_value:ui.values[0], second_value:ui.values[1]},function(data){},'json');
      // }      
    });
// TODO don't understand what this does, something else the function does. Is this actually what marks on label?
    $( "#year" ).val( "" + $( "#slider-range" ).slider( "values", 0 ) +
      " - " + $( "#slider-range" ).slider( "values", 1 ) );
  });


function growthChange(baseyear, compyear, urli, region) {
      $.ajax({
      url: urli,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({"baseyear":baseyear, "compyear":compyear})
      }).done(function(data){
        geoIdPrices = $.parseJSON(data);
        heatColors(region);
      // console.log(data);
    });
}

// function showHeatMap(region, urli) {
//       $.ajax({
// // pulls "data" from the data returned in the path /geoidpricesajax
//       url: urli,
// // .done is a callback, submits function and waits for callback
//       }).done(function(data){
// // extra careful with browser issues
//       if (console && console.log ) {
// // takes JSON data and converts it JS objects 
//         geoIdPrices = $.parseJSON(data);
// // call heatColors AFTER stuff above has loaded
//       // console.log(geoIdPrices)
//         heatColors(region);
//       }
//     });
// }