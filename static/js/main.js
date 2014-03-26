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
  // Centers on Fremont
    // center: new google.maps.LatLng(37.529577, -121.996294),

  // Center in SF
    center: new google.maps.LatLng(37.751251,-122.451568),

    zoom: 13,  
    // mapTypeId:google.maps.MapTypeId.ROADMAP
    // mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  // instantiate JS "map" object, passing it the div element and map properties
  map = new google.maps.Map(document.getElementById("map-canvas"),
      mapOptions);


  // GEOCODER & CREATE MARKERS for codeAddress() in toolbar
  geocoder = new google.maps.Geocoder();


  // CREATE sample MARKER in Fremont
// in Fremont 
// inside 
  // var myLatlng = new google.maps.LatLng(37.528516,-121.994178);
  // var myLatlng = new google.maps.LatLng(37.529577,-121.996294);
// outside
  var myLatlng = new google.maps.LatLng(37.534642,-121.994815);


// in SF
// this one is inside triangle
  // var myLatlng = new google.maps.LatLng(37.76481,-122.456752);
// this one is outside of triangle
  // var myLatlng = new google.maps.LatLng(37.751251,-122.451568);


  var samplemarker = new google.maps.Marker({
    position:myLatlng,
    map: map,
    title:"Hello World!"
  });

  samplemarker.setMap(map);

  // CREATE sample POLYGON OVERLAY
  var bermudaTriangle;

  // Define the LatLng coordinates for the polygon's path.

// Centers in Fremont
// var triangleCoords = [
//     new google.maps.LatLng(37.5228600000001, -121.987571), 
//     new google.maps.LatLng(37.52263, -121.98773), 
//     new google.maps.LatLng(37.52266, -121.98781), 
//     new google.maps.LatLng(37.5232400000001, -121.989271), 
//     new google.maps.LatLng(37.52396, -121.99067), 
//     new google.maps.LatLng(37.5243, -121.99135), 
//     new google.maps.LatLng(37.52473, -121.99218), 
//     new google.maps.LatLng(37.5251400000001, -121.99297), 
//     new google.maps.LatLng(37.52567, -121.99408), 
//     new google.maps.LatLng(37.52587, -121.99449), 
//     new google.maps.LatLng(37.5272099999999, -121.99729), 
//     new google.maps.LatLng(37.52755, -121.99798), 
//     new google.maps.LatLng(37.52814, -121.99908), 
//     new google.maps.LatLng(37.52824, -121.99927), 
//     new google.maps.LatLng(37.5285, -121.99983), 
//     new google.maps.LatLng(37.52854, -121.999941), 
//     new google.maps.LatLng(37.52974, -122.00237), 
//     new google.maps.LatLng(37.53019, -122.002181), 
//     new google.maps.LatLng(37.53094, -122.00187), 
//     new google.maps.LatLng(37.5312400000001, -122.001811), 
//     new google.maps.LatLng(37.53144, -122.00177), 
//     new google.maps.LatLng(37.5316800000001, -122.00174), 
//     new google.maps.LatLng(37.53221, -122.00167), 
//     new google.maps.LatLng(37.53319, -122.00121), 
//     new google.maps.LatLng(37.53637, -121.998581), 
//     new google.maps.LatLng(37.53453, -121.99497), 
//     new google.maps.LatLng(37.5344451818793, -121.994803647041), 
//     new google.maps.LatLng(37.5336426476268, -121.99322964437701), 
//     new google.maps.LatLng(37.5329800000001, -121.99193), 
//     new google.maps.LatLng(37.5323, -121.9906), 
//     new google.maps.LatLng(37.53068, -121.98744), 
//     new google.maps.LatLng(37.52987, -121.98584), 
//     new google.maps.LatLng(37.52855, -121.98326), 
//     new google.maps.LatLng(37.5276500000001, -121.98403), 
//     new google.maps.LatLng(37.52695, -121.98464), 
//     new google.maps.LatLng(37.52634, -121.98517), 
//     new google.maps.LatLng(37.52482, -121.986321), 
//     new google.maps.LatLng(37.5238000000001, -121.98701), 
//     new google.maps.LatLng(37.52347, -121.9872), 
//     new google.maps.LatLng(37.5228600000001, -121.987571),
//     new google.maps.LatLng(37.5228600000001, -121.987571)
//     ]

// Centers around SF
  var triangleCoords = [
    new google.maps.LatLng(37.785067, -122.473021),
    new google.maps.LatLng(37.739238, -122.47408),
    new google.maps.LatLng(37.781944, -122.405511),
    new google.maps.LatLng(37.785067, -122.473021)
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
