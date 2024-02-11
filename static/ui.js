function setReady() {
    var xhttp = new XMLHttpRequest()
    var test_mode = window.document.getElementById("test_mode").value;
    xhttp.open('GET', `ready?test_mode=${test_mode}`, true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send();
}

function show_hide_vehicle_card(show) {
    var card = window.document.getElementById("drone_config_menu_container");
    if (show) {
        card.style.display = 'block';
    } else {
        card.style.display = 'none';
    }
}

function refresh() {
    map.removeLayer(droneMarker);
    map.setView(START_POINT, 7);
    droneMarker = {};
    is_focus = false;
    var xhttp = new XMLHttpRequest()
    xhttp.open('GET', 'refresh', true);
    xhttp.setRequestHeader("Content-type", 'application/json;charset=UTF-8');
    xhttp.send();
    var vehicle_params = window.document.getElementsByClassName('vehicle_param');
    for (var i = 0; i < vehicle_params.length; i++) {
        vehicle_params[i].innerText = 'None';
    }
    window.document.getElementById('vehicle_details').innerText = 'Waiting for connection...';
    window.document.getElementById('drone_config_menu_container').style.display='none';
}