import 'leaflet';
import $ from 'jquery';
import carparks from '../../public/assets/data/carparks';

export default function(data) {

    console.log(data);
    
    if(data.state.city_state === 'busy') {
        $('#city-status-busy').toggleClass('d-none');
    } else if (data.state.city_state === 'average') {
        $('#city-status-average').toggleClass('d-none');
    } else {
        $('#city-status-quiet').toggleClass('d-none');
    }
    
    const map = L.map('map', { zoomControl: false }).setView([54.9759, -1.6128], 15);

    L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.control.zoom({
        position:'topright'
    }).addTo(map);

    carparks.forEach(function(carpark){

        const currentData = data.carparks.carparks.find(obj => { return obj.name === carpark.name; });
        console.log(currentData);

        const spaces = currentData ? (carpark.capacity - currentData.occupancy) : carpark.capacity;
        const state = currentData ? currentData.state : 'unknown';

        const marker = L.divIcon({
            html: '<img alt="marker-' + state + '" src="../../public/assets/images/map-marker-' + state + '.png"><span class="spaces">' + spaces + '</span>',
            iconSize: [40, 40],
            iconAnchor: [20, 40],
            className: 'car-park-marker'
        });

        if(carpark.location.length === 2) {
            L.marker(carpark.location, { icon: marker }).addTo(map)
            .bindPopup('There are ' + spaces + ' spaces remaing at ' + carpark.name + '.');
        }
    });
}