mapid = 125674; 
// TODO: set as env var
apikey = "99d055cec8794a33b9e2cb09553e3506"

var map = L.map('map').setView([37.785067, -122.473021], 7);

// var max = ;

// var min = ;

// var colorDict = {
//     1: "#F1917C",
//     2: "#F18064",
//     3: "#D67159",
//     4: "#D65E3A"
// }


var initLeaflet = function (active_listings) {
    addBaseMap();
    // addActiveMarkers(active_listings);
    // addPolygon(active_listings.slice(0,3));
    // addCounties();
    // addBlockGroups();
    heatColors();
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


function getColor(price) {
    return price > 1000 ? '#800026' :
           price > 500  ? '#BD0026' :
           price > 200  ? '#E31A1C' :
           // d > 100  ? '#FC4E2A' :
           // d > 50   ? '#FD8D3C' :
           // d > 20   ? '#FEB24C' :
           // d > 10   ? '#FED976' :
                      '#FFEDA0';
}


function style(feature) {
    return {
        fillColor: getColor(feature.properties.density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function heatColors(){
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