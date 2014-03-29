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
var geoidpricesajax = "/geoidpricesajax";

var initLeaflet = function (active_listings) {
    addBaseMap();
    // addActiveMarkers(active_listings);
    // addPolygon(active_listings.slice(0,3));
    // addCounties();
    // addBlockGroups();
    showHeatMap(counties, geoidpricesajax);
    toggleHeatMap(counties);
    showActive();

    selectMetric();
};


function selectMetric(){
  $('#SP, #SPS, #SPSC').change(function(){
  if ($("#SP").is(":checked")) {
    console.log("you clicked SP");
  } else if ($("#SPS").is(":checked")) {
    console.log("you clicked SPS");
  } else if ($("#SPSC").is(":checked")) {
    console.log("you clicked SPSC");
  }
  });
}

//   $('#SPS').change(function(event){
//     if (event.target.checked){
//     console.log("you printed SPS");
//     } else {
//       console.log("you're awesome");
//     }
//   });
// }

//   $('input[name=active]').change(function(event) {
//     if (event.target.checked) {
//   // this disables checkbox
//       event.target.disabled = true;
// // TODO put spinner bar in here? 
//     // $('#imgid').show()
//       // console.log('disabled checkbox');
//       $.ajax({
//         url: "/leafactivelistings",
//       }).done(function(data) {
//         prices = $.parseJSON(data);
//         createMarkers(prices);
//         // addActiveMarkers(prices);
//         event.target.disabled = false;
//         // $('#imgid').hide()
//       });
//     } else {
//       map.removeLayer(markers);
//     }
//   });
// }



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



var markers = new L.FeatureGroup();

function createMarkers(active_listings) {
    for (i = 0; i < active_listings.length; i++) {
      var marker = L.marker(active_listings[i]);
      markers.addLayer(marker);
      break;
  }
  map.addLayer(markers);
}

// function addActiveMarkers(active_listings) {
//     for (i = 0; i < active_listings.length; i++) {
//         L.marker(active_listings[i]).addTo(map);
//         break;
//         // add some sort of qualifier here
//     }
// }
// function addPolygon(points) {
//     L.polygon(points).addTo(map);
// }

// TODO QUESTION: note to self: 'event' is when the input[] "active" .changes (.target is the object)
// TODO why doesn't a .click() or .toggle() work?
// TODO why is this removing the map? (works when just add one marker)
// TODO make this go faster (special layer or cluster circles-show more markers as zoom in-view only) (see Rhonda's emails)
// TODO schedule deferred exeecution with setTimeout function at 0 ms of adding gmarkers before re-enabling form and removing spinner?
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



// get max and min price in region and $ amount per block level, called in getLevel()
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
    // console.log(blocks.maxPrice);
    // console.log(blocks.minPrice);
    // console.log(blocks.blocks);
    blocks = getBlocks();
    level = (price - blocks.minPrice)/blocks.blocks;
    // console.log(level);
    // console.log("geoId is :" )
    // console.log("median price is")
    return level;
}

// dicts of color levels, called in style function with getLevel()
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
    heatLayer = L.geoJson(region, {style: style}).addTo(map);
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
