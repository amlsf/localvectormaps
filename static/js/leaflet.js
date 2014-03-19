mapid = 125438; 
// TODO: set as env var
apikey = "99d055cec8794a33b9e2cb09553e3506"

var map = L.map('map').setView([37.785067, -122.473021], 13);

L.tileLayer('http://{s}.tile.cloudmade.com/'+apikey+'/'+mapid+'/256/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
    maxZoom: 18
}).addTo(map);


var initLeaflet = function (active_listings) {
    // addActiveMarkers(active_listings);
    addPolygon(active_listings.slice(0,3));
}

function addActiveMarkers(active_listings) {
    for (i = 0; i < active_listings.length; i++) {
        L.marker(active_listings[i]).addTo(map);
    }    
}

function addPolygon(points) {
    L.polygon(points).addTo(map);
}