// initialize variables outside funciton so can use them universally 
var map, pointArray, heatmap;


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
  var mapOptions = {
  // Centers on Sydney
    center: new google.maps.LatLng(37.774546, -122.433523),
    zoom: 13,  
    // mapTypeId:google.maps.MapTypeId.ROADMAP
    // mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  // instantiate JS "map" object, passing it the div element and map properties
  map = new google.maps.Map(document.getElementById("map-canvas"),
      mapOptions);

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












// just input this directly into ajax
// CENTER MARKER & CLICK ZOOM marker to center of map, zooms when clicked
  // var marker = new google.maps.Marker({
  //   position: map.getCenter(),
  //   map: map,
  //   title: 'Click to zoom'
    // animation:google.maps.Animation.BOUNCE
  // });

// 3 seconds after the center of the map has changed, pan back to the
// marker.
  // google.maps.event.addListener(map, 'center_changed', function() {
  //   window.setTimeout(function() {
  //     map.panTo(marker.getPosition());
  //   }, 3000);
  // });

// TODO Howcome I don't need to set the marker here? marker.setMap()
  // google.maps.event.addListener(marker, 'click', function() {
  //   map.setZoom(200);
  //   // map.setCenter(marker.getPosition());
  // });




  // HEATMAP input the array data into some variable that makes it an array? 
  pointArray = new google.maps.MVCArray(taxiData);
  // instantiate heatmap visualization object with arrayg
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
  });
// set map on the map
    heatmap.setMap(map);
  }


// TODO What is this? The following code instructs the application to load the Maps 
// API after the page has fully loaded (using window.onload) and write the Maps 
// JavaScript API into a <script> tag within the page. Additionally, we instruct the
// API to only execute the initialize() function after the API has fully loaded by
// passing callback=initialize to the Maps API bootstrap:
function loadScript() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&' +
      'callback=initialize';
  document.body.appendChild(script);
}

// window.onload = loadScript;


// HEATMAP BUTTONS Create a bunch of buttons that let you do stuff
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



// EVENT LISTENER to load map after page has loaded. What is this??? 
google.maps.event.addDomListener(window, 'load', initialize);

// Example of how to use ajax
// $.ajax({
//   url: "/activelistings",
//   success: function(data){
//   console.log(data) 
//   }
// });

// $.ajax({
//   url: "/activelistings",
//   success: function(data){
//     var listings = JSON.parse(data);
//     for (var i = 0; i < listings.length; i++) {
//       var elt = document.createElement("div");
//       elt.textContent = listings[i].address;
//       document.body.appendChild(elt);
//     }
//   }
// });


