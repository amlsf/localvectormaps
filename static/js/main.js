// initialize variables outside funciton so can use them universally 
var map, pointArray, heatmap, geocoder;

// Heat map data
var taxiData = [
  new google.maps.LatLng(37.782745, -122.444586),
  new google.maps.LatLng(37.782842, -122.443688),
  new google.maps.LatLng(37.782919, -122.442815),
  new google.maps.LatLng(37.782992, -122.442112),
  new google.maps.LatLng(37.783100, -122.441461),
  new google.maps.LatLng(37.783206, -122.440829),
  new google.maps.LatLng(37.783273, -122.440324),
  new google.maps.LatLng(37.783316, -122.440023),
  ];



// <!--start  Asyncronously loading the API,  -->
// <!-- start create JS object literal to hold number of map properties
//  -->
function initialize() {
  // CREATE MAP
  var mapOptions = {
  // Centers on Sydney
    center: new google.maps.LatLng(37.785067, -122.473021),
    zoom: 13,  
    // mapTypeId:google.maps.MapTypeId.ROADMAP
    // mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  // instantiate JS "map" object, passing it the div element and map properties
  map = new google.maps.Map(document.getElementById("map-canvas"),
      mapOptions);


  // GEOCODER & CREATE MARKERS for codeAddress() in toolbar
  geocoder = new google.maps.Geocoder();


  // CREATE sample MARKER at 14th Ave
  var myLatlng = new google.maps.LatLng(37.785067, -122.473021);

  var samplemarker = new google.maps.Marker({
    position:myLatlng,
    map: map,
    title:"Hello World!"
  });

  // samplemarker.setMap(map);

  // CREATE sample POLYGON OVERLAY
  var bermudaTriangle;

  // Define the LatLng coordinates for the polygon's path.
  var triangleCoords = [
    new google.maps.LatLng(37.774252, -122.190262),
    new google.maps.LatLng(37.466465, -122.118292),
    new google.maps.LatLng(37.321384, -122.75737),
    new google.maps.LatLng(37.774252, -122.190262)
  ];

  // Construct the polygon.
  bermudaTriangle = new google.maps.Polygon({
    paths: triangleCoords,
    strokeColor: '#000000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#000000',
    fillOpacity: 0.35
  });

  bermudaTriangle.setMap(map);




  // CREATE HEATMAP input the array data into some variable that makes it an array? 
  pointArray = new google.maps.MVCArray(taxiData);
  // instantiate heatmap visualization object with arrayg
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
  });
// set heatmap on the map
    heatmap.setMap(map);

// This is pulling function from heatmap.html file so that function runs after map instantiated. This calls makeMarkers()
    drawMarkers();

} // END Initializer




// GEOCODE for search bar and set marker on the map
function codeAddress() {
  var address = document.getElementById('address').value;
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

  // CREATE MARKERS function for active listings, called in heatmap.html
var markers = [];
function makeMarkers(latitude, longitude) {
  var myLatlng = new google.maps.LatLng(latitude, longitude);

  var marker = new google.maps.Marker({
    position:myLatlng,
    map: map
  });

  // console.log(marker);

  markers.push(marker);
  marker.setMap(map);
}

// CREATE HEATMAP BUTTONS Create a bunch of buttons that let you do stuff
function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}



// EVENT LISTENER to load map after page has loaded.
google.maps.event.addDomListener(window, 'load', initialize);
