mapid = 125674; 
// TODO: set as env var
apikey = "99d055cec8794a33b9e2cb09553e3506"

var map = L.map('map').setView([37.785067, -122.473021], 7);

// initialized when /geoidpricesajax result is available
var geoIdPrices = null;
var geoIdPricesMax = null;
var geoIdPricesMin = null;
var maxPrice = null;
var minPrice = null;
var blocks = null;

var initLeaflet = function (active_listings) {
    addBaseMap();
    // addActiveMarkers(active_listings);
    // addPolygon(active_listings.slice(0,3));
    // addCounties();
    // addBlockGroups();
    // fetch geoid price info

// .done is a callback, submits function and waits for callback
  $.ajax({
    url: "/geoidpricesajax",
  })
// pulls "data" from the data returned in the path /geoidpricesajax
    .done(function( data ) {
// extra careful with browser issues
      if ( console && console.log ) {
// takes JSON data and converts it JS objects 
        var geoIdPrices = $.parseJSON(data);
// call heatColors AFTEr stuff above has loaded
        heatColors();
      }
    });
}

function addBaseMap() {
    L.tileLayer('http://{s}.tile.cloudmade.com/'+apikey+'/'+mapid+'/256/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    maxZoom: 20
}).addTo(map);
}

function addActiveMarkers(active_listings) {
    for (i = 0; i < active_listings.length; i++) {
        L.marker(active_listings[i]).addTo(map);
    }    
}

function addPolygon(points) {
    L.polygon(points).addTo(map);
}

// counties is defined in the geojson js file imported in script tag in html
function addCounties(){
    L.geoJson(counties).addTo(map);
}

function addBlockGroups(){
    L.geoJson(blockgroups).addTo(map);
}


function getLevel(price) {
  var prices = [];
  for key in geoIdPrices:
    prices.push(geoIdPrices[key]);
  maxPrice = Math.max.apply(Math, prices);
  minPrice = Math.max.apply(Math, prices);
  blocks = (maxPrice - minPrice)/4;
  level = (price - minPrice)/blocks
}


function getColor(level) {
    return level > 3 ? '#800026' :
           level > 2  ? '#BD0026' :
           level > 1  ? '#E31A1C' :
           // d > 100  ? '#FC4E2A' :
           // d > 50   ? '#FD8D3C' :
           // d > 20   ? '#FEB24C' :
           // d > 10   ? '#FED976' :
                      '#FFEDA0';
}


var style = function(feature) {
// TODO this references my geojson, actually wouldn't I change it to the variable name.dictkey.dictkey? 
    var geoId = feature.properties.GEO_ID;

    return {
    // replace median with geoIdPrices[geoId]
        fillColor: getColor(geoIdPrices[geoId]),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function heatColors() {
    L.geoJson(counties, {style: style}).addTo(map);
}




// function medianColor() {
//     (max - min)/4

// }

// function getColor(d) {
//     return d > 1000 ? '#800026' :
//            d > 500  ? '#BD0026' :
//            d > 200  ? '#E31A1C' :
//            d > 100  ? '#FC4E2A' :
//            d > 50   ? '#FD8D3C' :
//            d > 20   ? '#FEB24C' :
//            d > 10   ? '#FED976' :
//                       '#FFEDA0';