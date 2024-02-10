console.log('Connecting...');

var socket = io.connect(
  window.location.protocol + "//" + document.domain + ":" + location.port
);
socket.on("connect", function () {
  console.log("Connected...!", socket.connected);
  socket.emit("update_sid");
});

socket.on("processed_image", function (image) {
  console.log("update image")
  photo.setAttribute("src", image);
});
