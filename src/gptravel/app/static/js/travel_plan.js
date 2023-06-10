var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

var map = L.map('map').setView(geoCoordinates, 5);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

var latlngs = Array();

// Creating markers
for (let i = 0; i < markerCoordinates.length; i++) {
    var marker = L.marker(markerCoordinates[i]).addTo(map);
    latlngs.push(marker.getLatLng());
}

var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);

// Zoom the map to the polyline
map.fitBounds(polyline.getBounds());