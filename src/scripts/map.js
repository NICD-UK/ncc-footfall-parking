import 'leaflet';
import $ from 'jquery';
import carparks from '../../public/assets/data/carparks';

export default function(data) {
    
    if(data.state.city_state === 'busy') {
        $('#city-status-busy').toggleClass('d-none');
    } else if (data.state.city_state === 'average') {
        $('#city-status-average').toggleClass('d-none');
    } else {
        $('#city-status-quiet').toggleClass('d-none');
    }
    
    const map = L.map('map', { zoomControl: false, maxZoom: 16 }).setView([54.9759, -1.6128], 15);


    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
    }).addTo(map);

    L.control.zoom({
        position:'topright'
    }).addTo(map);

    var northEnd = new L.LatLng(54.977758, -1.613620);
    var midPoint = new L.LatLng(54.975865, -1.612830);
    var southEnd = new L.LatLng(54.974312, -1.611817);
    var pointList = [northEnd, midPoint, southEnd];

    var line = new L.Polyline(pointList, {
        color: 'blue',
        weight: 4,
        opacity: 0.75,
        smoothFactor: 1
    });
    
    line.addTo(map);

    carparks.forEach(function(carpark){

        const currentData = data.carparks.carparks.find(obj => { return obj.name === carpark.name; });
        const spaces = currentData ? (carpark.capacity - currentData.occupancy) : carpark.capacity;
        const state = currentData ? currentData.state : 'unknown';

        const marker = L.divIcon({
            html: '<img alt="marker-' + state + '" src="../../public/assets/images/map-marker-' + state + '.png"><span class="spaces">' + spaces + '</span>',
            iconSize: [60, 60],
            iconAnchor: [30, 60],
            className: 'car-park-marker'
        });

        if(carpark.location.length === 2) {
            L.marker(carpark.location, { icon: marker }).addTo(map)
            .bindPopup('There are ' + spaces + ' spaces remaing at ' + carpark.name + '.');
        }
    });
}
