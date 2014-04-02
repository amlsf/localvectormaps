//TODO: factor out code so not so many global variables
//TODO maybe use leaflet layer controls http://leafletjs.com/examples/layers-control.html
//TODO How to organize when there are so many f-ing dependencies????
// Gotta speed up the layering of geoJSON - too slow! Maybe change to county, subcounty, zips (no BG, census tracts?)

mapid = 125674;
// TODO: set as env var
apikey = "99d055cec8794a33b9e2cb09553e3506";

var map = L.map('map').setView([36.685067, -121.73021], 9);


                // var map = new L.Map('map', {
                //     zoomControl: false,
                //     center: new L.LatLng(37.75042,-122.489),
                //     zoom: 12,
                //     layers: [baseLayer, heatmapLayer]
                // });
                // new L.Control.Zoom({
                //     position: 'topright'
                // }).addTo(map);

             // var baseLayer = L.tileLayer(
             //        'http://{s}.tile.cloudmade.com/38be25219f7c4b6f8953354a1b2e583f/82651/256/{z}/{x}/{y}.png', 
             //        {
             //            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
             //            maxZoom: 18
             //        }
             //    );

              // var heatmapLayer = L.TileLayer.heatMap({

// initialized when /geoidpricesajax result is available
var geoIdPrices = null;
// var geoIdPricesMax = null;
// var geoIdPricesMin = null;
// var maxPrice = null;
// var minPrice = null;
// var blocks = null;
var heatLayer;
var legend;
var tierCount = 6;

// route variables for radio button selections
var geoidpricesajax = "/geoidpricesajax";
var psf = "/psf";
var geochanges = "/geochanges";

var initLeaflet = function (active_listings) {

    // var metric_route = geoidpricesajax;
    // var region = counties;

    addBaseMap();
    showHeatMap(zips, geoidpricesajax);

    // addCounties();
    // addZips();
    // addBlockGroups();

// controls: 
    toggleHeatMap(zips);
    showActive();
    selectMetric();

    setupSlider();
    // setupMinSlider();
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

// add zipcodes function
function addZips(){
    L.geoJson(zips).addTo(map);
}


// function addBlockGroups(){
//     L.geoJson(blockgroups).addTo(map);
// }

//////////////////////Zoom function
    // map.on("zoomend",function(e){
    //   console.log( "zoom level is " + map.getZoom());
    //   var zoom = map.getZoom();
    //   if (zoom < 10) {
    //     showHeatMap(zips, geoidpricesajax);
    //   } else if (zoom < 12) {
    //     map.removeLayer(heatLayer);
    //     addBlockGroups();
    //   }
    // });


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION creates active listing markers with details pop-ups
// var markers = new L.FeatureGroup();

var markers = new L.MarkerClusterGroup();

function createMarkers(active_listings) {
    for (i = 0; i < active_listings.length; i++) {
      var lat = active_listings[i]['latitude'];
      var longi = active_listings[i]['longitude'];
      var address = active_listings[i]['address'];
      var list_price = active_listings[i]['list_price'];
      var city = active_listings[i]['city'];
      var postal_code = active_listings[i]['postal_code'];
      var county = active_listings[i]['county'];
      var bedrooms = active_listings[i]['bedrooms'];
      var bathrooms = active_listings[i]['bathrooms'];
      var squarefeet = active_listings[i]['squarefeet'];
      var mls_id = active_listings[i]['mls_id'];
      var description = active_listings[i]['description'];
      var url = active_listings[i]['url'];
      var psf = list_price / squarefeet;
      var marker = L.marker(new L.LatLng(lat, longi), {
        address: address,
        city: city,
        postal_code: postal_code,
        county:county,
        list_price: list_price,
        psf: psf,
        bedrooms:bedrooms,
        bathrooms:bathrooms,
        squarefeet:squarefeet,
        description:description,
        mls_id:mls_id,
        url:url
      });
// TODO: bind url somehow here? 
      marker.bindPopup(
        "<b>Address:</b> " + "<a href='" + url + "'>" + address + ", " + city + ", " + postal_code + ", " + county + " County  </a> <br>"  +
        "<b>Ask Price/PSF:</b> " + list_price + " / " + psf + "<br>" +
        "<b>Bedrooms:</b> " + bedrooms + ", " + "<b> Bathrooms:</b> " + bathrooms + ", " + "<b>SF:</b> " + squarefeet + "<br>" +
        description + "<br>" +
        "<b>MLS listing number:</b> " + mls_id
        );
      markers.addLayer(marker);
  }
  map.addLayer(markers);
}


// Toggle checkbox to display active listings
// QUESTIONS 
// note to self: 'event' is when the input[] "active" .changes (.target is the object)
// why doesn't a .click() or .toggle() work?
// schedule deferred exeecution with setTimeout function at 0 ms of adding gmarkers before re-enabling form and removing spinner?
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

// SECTION Adds/removes colors on the choropleth map

// get max and min price in region and $ amount per block level, called in getLevel()
// geoIdPrices is a global variable that is defined in ajax call in showHeatMap() function 
// remove the counties with nothing so not calculated in min price
function getLevelAmounts() {
  var prices = [];
  for (var key in geoIdPrices) {
      if (geoIdPrices[key] !== 0) {
      prices.push(geoIdPrices[key]);
      }
  }
    var maxAmount = Math.max.apply(Math, prices);
    var minAmount = Math.min.apply(Math, prices);
    var steps = (maxAmount - minAmount)/tierCount;
    // console.log("price list is" + prices);
    // console.log("maxprice is " + maxAmount);
    // console.log("minprice is " + minAmount);
    // console.log("block amount is " + steps);
    return {maxAmount: maxAmount,
      minAmount: minAmount,
      steps: steps
    };
}


// use the $ blocks to determine the particular house price color level, called in style fxn with getColor()
function getLevel(price) {
    var steps = getLevelAmounts();
    var level = (price - steps.minAmount)/steps.steps;
    return level;
}


// dicts of color levels, called in style function with getLevel()
// This is shorthand notation ? is "if" then do what's before colon:, else do whatever is after 
function getColor(level) {
    alpha = (level+1)/tierCount;

    return 'rgba(255,0,0,' + alpha + ')';

    // return level >= 5  ? 'rgba(255,0,0,1)' :
           // level >= 4  ? 'rgba(255,0,0,0.8)' :
           // level >= 3  ? 'rgba(255,0,0,0.6)' :
           // level >= 2  ? 'rgba(255,0,0,0.4)' :
           // level >= 1  ? 'rgba(0,255,0,0.2)' :
           //            'rgba(0,0,255,1)';
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
    var geoId = feature.properties.GEOID10;
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
        removeLegend();
        createLegend();
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
      createLegend();
      event.target.disabled = false;
    } else {
      map.removeLayer(heatLayer);
      removeLegend();
    }
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION User interaction - hover to highlight and click in to region and to front e.target (action for mouseover)
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


// TODO how to incorporate with click clusters and incorporate click out? 
// used in heatColors() fxn
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

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
        '<b>' + props.ZCTA5CE10 + '</b><br />' + props.GEOID10 + ' name / geoid':
        'Hover over a region');
};

info.addTo(map);

////////////////////////////////////////////////////////////////////////////////////////////////

// SECTION Legend

// Formats money
Number.prototype.formatMoney = function(c, d, t){
var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c,
    d = d == undefined ? "." : d,
    t = t == undefined ? "," : t,
    s = n < 0 ? "-" : "",
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };

function createLegend() {

  legend = L.control({position: 'bottomright'});

  legend.onAdd = function (map) {

      var div = L.DomUtil.create('div', 'info legend'),
          // grades = [0, 1, 2, 3, 4, 5],
          labels = [],
          steps = getLevelAmounts(),
          stepAmount = steps.steps,
          minAmount = steps.minAmount,
          maxAmount = steps.maxAmount;
      // loop through our density intervals and generate a label with a colored square for each interval
          console.log(geoIdPrices);
          console.log(maxAmount);
          console.log(minAmount);
          console.log(stepAmount);

// Makes a different legend type if YoY Change % option is selected
      if ($("#SPSC").is(":checked")) {
        console.log("regenerating legend for SPSC");
        for (var x = 0; x < tierCount; x++) {
            div.innerHTML +=
                '<i style="background:' + getColor(x) + '"></i> ' +
                '$'+((x*stepAmount)+minAmount).formatMoney(0) +
                  ( x+1 < tierCount ?
                    ' +' + '<br>':
                    '&ndash;' + '$' + maxAmount.formatMoney(0)
                    // '&ndash;' + '$'+(((grades[x + 1]*stepAmount)+minAmount)).formatMoney(0) + '<br>':
                    );
        }
// Makes a different legend type if overall $ price option selected 
      } else {
        for (var x = 0; x < tierCount; x++) {
            div.innerHTML +=
                '<i style="background:' + getColor(x) + '"></i> ' +
                '$'+((x*stepAmount)+minAmount).formatMoney(0) +
                  ( x+1 < tierCount ?
                    ' +' + '<br>':
                    '&ndash;' + '$' + maxAmount.formatMoney(0)
                    // '&ndash;' + '$'+(((grades[x + 1]*stepAmount)+minAmount)).formatMoney(0) + '<br>':
                    );
        }
      }

      return div;
  };

  legend.addTo(map);

}


function removeLegend() {
  if (legend !== undefined) {
    legend.removeFrom(map);
  }
}


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////


// SECTION select metrics to view on choropleth map
function selectMetric(){
  $('#SP, #SPS, #SPSC').change(function(){
    if ($('input[name=toggleheat]').is(":checked")){
      if ($("#SP").is(":checked")) {
          console.log("you clicked SP");
          map.removeLayer(heatLayer);
          $("#year-slider").addClass("is-nodisplay");
          $("#slider-range").hide();
          showHeatMap(zips, geoidpricesajax);
      } else if ($("#SPS").is(":checked")) {
          console.log("you clicked SPS");
          map.removeLayer(heatLayer);
          $("#slider-range").hide();
          $("#year-slider").addClass("is-nodisplay");
          showHeatMap(zips,psf);
      } else if ($("#SPSC").is(":checked")) {
          console.log("you clicked SPSC");
          map.removeLayer(heatLayer);
          $("#year-slider").removeClass("is-nodisplay");
          $("#slider-range").show();
          growthChange(2009, 2013, geochanges, zips);
      }
    }
  });
}


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
// Section - Recovery Growth % Change

// TODO Make this work - make sure only works/shows when "Sales PSF Comparison" is checked
//  Think I need to make it somehow clear when it changes again
// TODO make this slider work for sales price and sales PSF ranges too? (But sthg needs to look diff since would be inclusive whereas this is just YoY)
// TODO understand what's happening here
// TODO get it so that the first view that shows is the 2007-2013 range upon click of radio button
  // make so doesn't show when toggle heatmap button unchcked, remove this document ready stuff and put it in a function and attach event handler

// This is the double slider for % change
function setupSlider() {
  $( "#slider-range" ).slider({
    range: true,
    min: 2009,
    max: 2013,
      // default values
      values: [ 2009, 2013 ],
      // TODO: this pulls the values from the slider and puts it on the label, what's below?
      slide: function( event, ui ) {
        $( "#year" ).val( "" + ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      },
      // when anything changes, run the function growthChange()
      // change: function(event, ui) {
      //   growthChange(ui.values[ 0 ], ui.values[ 1 ], geochanges, zips);
      // },
      stop: function(event, ui) {
            // when the user lets go and stops changing the slider
        map.removeLayer(heatLayer);
        growthChange(ui.values[ 0 ], ui.values[ 1 ], geochanges, zips);
      }
    });
  // Setting up slider before any user action based on default values
  $( "#year" ).val( "" + $( "#slider-range" ).slider( "values", 0 ) +
    " - " + $( "#slider-range" ).slider( "values", 1 ) );
  $("#slider-range").hide();
// Don't need to remove layer, already setup in selectMetric()
}

function growthChange(baseyear, compyear, urli, region) {
      $.ajax({
      url: urli,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({"baseyear":baseyear, "compyear":compyear})
      }).done(function(data){
        geoIdPrices = $.parseJSON(data);
        heatColors(region);
        removeLegend();
        createLegend();
      // console.log(data);
    });
}

// function setupMinSlider() {
//     $( "#slider" ).slider({
//       value:2013,
//       min: 2009,
//       max: 2013,
//       step: 1,
//       slide: function( event, ui ) {
//         $( "#comp-year" ).val( "" + ui.value );
//       },
//       stop: function( event, ui ) {
//             // when the user lets go and stops changing the slider
//           growthChange(ui.values[ 0 ], ui.values[ 1 ], geochanges, zips);
//       }
//     });
//     $( "#comp-year" ).val( "" + $( "#slider" ).slider( "value" ) );
//   }


