import 'leaflet';
import carparks from '../../public/assets/data/carparks';

export default function() {
    const map = L.map('map', { zoomControl: false }).setView([54.9759, -1.6128], 14);

L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.control.zoom({
    position:'topright'
}).addTo(map);

const states = ['quiet', 'average', 'busy'];

const markers = [];

states.forEach(function(state){
    markers[state] = L.divIcon({
        html: '<i class="feather icon-map-pin ' + state + '"></i>',
        iconSize: [30, 30],
        className: 'car-park-marker'
    });
});

let currentCapacity = 0;

carparks.forEach(function(carpark){
    if(carpark.location.length === 2) {
        currentCapacity += carpark.capacity;
        L.marker(carpark.location, { icon: markers.busy }).addTo(map)
        .bindPopup('There are only ' + carpark.capacity + ' spaces remaing at ' + carpark.name + '.');
    }
});
}