console.log('Connecting...');
var socket = io.connect(
  window.location.protocol + "//" + document.domain + ":" + location.port
);
socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
  socket.emit("update_sid");
});

socket.on("init_marker", function (data) {
  window.document.getElementById('vehicle_id').innerText = data.id;
  moveMap(data.lat, data.lon);
  moveMarker(data)
  show_hide_vehicle_card(true);
});

socket.on("update_vehicle", function (data) {
  updateParams(data.params)
  moveMarker(data.params)
  photo.setAttribute("src", data.image);
});

function setReady() {
  var test_mode = window.document.getElementById("test_mode").value;
  socket.emit("ready", {"test_mode": test_mode});
}
