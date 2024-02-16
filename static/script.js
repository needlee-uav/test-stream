console.log('Connecting...');
var socket = io.connect(
  window.location.protocol + "//" + document.domain + ":" + location.port
);
socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
  socket.emit("update_sid");
});

socket.on("init_marker", function (data) {
  console.log(data)
  if (data.id == "") {
    console.log("No vehicles connected");
    return
  }
  window.document.getElementById('vehicle_id').innerText = data.id;
  if (data.test_mode) {
    window.document.getElementById('test_mode').style = "display: inline";
    displayReadyButton();
  }
  window.document.getElementById('params').style = "display: inline";
  moveMap(data.lat, data.lon);
  moveMarker(data)
});

socket.on("update_vehicle", function (data) {
  updateParams(data.params)
  moveMarker(data.params)
  photo.setAttribute("src", data.image);
});

function setReady() {
  const MODES = new Map();
  MODES.set('Soft takeoff and land no GPS', 1);
  MODES.set('Test offboard commands', 2);
  MODES.set('Test GPS route navigation', 3);
  MODES.set('Test emergency', 4);
  MODES.set('Test camera streaming', 5);
  MODES.set('Test capturing', 6);
  MODES.set('Test following', 7);
  
  var test_mode = window.document.getElementById("test_mode_name").innerText;
  console.log(MODES.get(test_mode))
  window.document.getElementById("ready_button_container").style.display = "none";
  socket.emit("ready", {"test_mode": test_mode});
}
