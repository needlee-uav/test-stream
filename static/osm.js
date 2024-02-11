const START_POINT = [48, 16];
var map = L.map('map', { 
    zoomControl: false, 
    dragging: false
});
var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
});
map.addLayer(layer);

map.setView(START_POINT, 7);

var droneMarker = {};
var is_focus = false;
var LeafIcon = L.Icon.extend({options: {iconSize: [32, 32], iconAnchor: [16, 5]}});
var icon = new LeafIcon({iconUrl: 'https://cdn-icons-png.flaticon.com/512/399/399308.png'});

function moveMarker(params) {
    console.log("move marker")
    console.log(params)
    map.removeLayer(droneMarker);
    droneMarker = new L.Marker([params.lat, params.lon], {icon: icon, rotationAngle: params.h})
    droneMarker.addTo(map);
}

function moveMap(lat, lon) {
    map.flyTo([lat, lon], 17, {animate: true, duration: 3});  
}

function updateParams(params) {
    // vehicle_details
    window.document.getElementById('vehicle_id').innerText = "Test run";
    window.document.getElementById('vehicle_details').innerText = "Connected";
    window.document.getElementById('lat_param').innerText = `Lat: ${params.lat}`;
    window.document.getElementById('lon_param').innerText = `Lon: ${params.lon}`;
    window.document.getElementById('h_param').innerText = `Heading: ${params.h}`;
    window.document.getElementById('alt_param').innerText = `Alt: ${params.alt}`;
}

function updateLoc() {
    var xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'update_loc', true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send();
    xhttp.addEventListener('load', reqListener);
    
    function reqListener() {
        var res = this.responseText.toString().split(";");
        if (res[0] != 0) {  
            moveMarker(res[0], res[1], res[2]);
            updateParams(res[0], res[1], res[2], res[3]);
            if (!is_focus) {
                moveMap(res[0], res[1]);
                show_hide_vehicle_card();
                is_focus = true;
            }
        }
    }
    setTimeout(function(){ updateLoc() }, 500);  
}