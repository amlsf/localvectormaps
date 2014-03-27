mapid = 125674; 
// TODO: set as env var
apikey = "99d055cec8794a33b9e2cb09553e3506"

var map = L.map('map').setView([37.785067, -122.473021], 7);

// initialized when /geoidpricesajax result is available
var geoIdPrices = null;
var geoIdPricesMax = null;
var geoIdPricesMin = null;
// var maxPrice = null;
// var minPrice = null;
// var blocks = null;
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
        geoIdPrices = $.parseJSON(data);
// call heatColors AFTER stuff above has loaded
        // console.log(geoIdPrices)
        blocks = getBlocks();
        // getLevel(need to put some price here);
        heatColors();
      }
    });


    // $('input[name=box2]').change(function(event) {
    //     if (event.target.checked) {
    //       event.target.disabled = true;
    //       console.log('disabled checkbox');
    //       window.setTimeout(function() {
    //         addActiveMarkers(active_listings);
    //         event.target.disabled = false;
    //         console.log('re-enabled checkbox');
    //       }, 0);
    //     } else {
    //       console.log("TODO remove markers")
    //     }
    //     // console.log('jquery: ' + event.target.checked);
    //     // TODO put spinner bar in here? 
    // });

    setupCheckbox();
}


function setupCheckbox() {
  $('input[name=box2]').change(function(event) {
    if (event.target.checked) {
      event.target.disabled = true;
      console.log('disabled checkbox');
      $.ajax({
            // TODO url: "/activelistings",
          }).done(function(data) {
            addActiveMarkers(active_listings);            
            event.target.disabled = false;
          });
        } else {
          // console.log("TODO remove markers")
        }
        // TODO put spinner bar in here? 
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


function getBlocks() {
  var prices = [];
  for (key in geoIdPrices) {
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
    }
}

function getLevel(price) {
    // console.log(blocks.maxPrice);
    // console.log(blocks.minPrice);
    // console.log(blocks.blocks);
    level = (price - blocks.minPrice)/blocks.blocks;
    // console.log(level);
    // console.log("geoId is :" )
    // console.log("median price is")
    return level;
}

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

var style = function(feature) {
// TODO this references my geojson, actually wouldn't I change it to the variable name.dictkey.dictkey? 
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
}

function heatColors() {
    L.geoJson(counties, {style: style}).addTo(map);
}



// var colorDict = {
//     1: "#F1917C",
//     2: "#F18064",
//     3: "#D67159",
//     4: "#D65E3A"
// }
