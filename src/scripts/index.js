import '../styles/index.scss';
import 'bootstrap';
import $ from 'jquery';
import map from './map';
import carparks from './carparks';
import carparkData from '../../public/assets/data/carparks';

const data = {};

function getCityState() {
    return $.ajax({
        method: "GET",
        cache: false,
        url: 'https://nccfootfallparking.blob.core.windows.net/api-data/latest_city_state.json'
    });
}

function getParking() {
    return $.ajax({
        method: "GET",
        cache: false,
        url: 'https://nccfootfallparking.blob.core.windows.net/api-data/latest_car_parks.json'
    });
}

function ISOtoLocale(date) {
    const offsetMs = date.getTimezoneOffset() * 60 * 1000;
    const msLocal =  date.getTime() - offsetMs;
    const dateLocal = new Date(msLocal);
    const iso = dateLocal.toISOString();
    const isoLocal = iso.slice(0, 19);
    return isoLocal;
}

$.when(getCityState(), getParking()).done(function(state, parking){
    data.state = state[1] === 'success' ? JSON.parse(state[0]) : null;
    data.carparks = parking[1] === 'success' ? JSON.parse(parking[0]) : null;

    const localUpdate = ISOtoLocale(new Date(data.carparks.timestamp));

    let serverDate = (localUpdate.split('T')[0]).split('-');
    let serverTime = (localUpdate.split('T')[1]).split('.')[0];

    let lastUpdated = serverDate[2] + '/' + serverDate[1] + '/' + serverDate[0] + ' ' + serverTime;

    $('#lastUpdated').text(lastUpdated);

    if(data.state.city_state === 'busy') {
        $('#city-status-badge-busy').toggleClass('d-none');
    } else if (data.state.city_state === 'average') {
        $('#city-status-badge-average').toggleClass('d-none');
    } else {
        $('#city-status-badge-quiet').toggleClass('d-none');
    }

    const totalSpaces = (carparkData.map(carpark => { return carpark.capacity; })).reduce((a, b) => a + b, 0),
          totalOccupancy = (data.carparks.carparks.map(carpark => { return carpark.occupancy; })).reduce((a, b) => a + b, 0);

    const occupancyRate = totalOccupancy/totalSpaces;

    if(occupancyRate > .7) {
        $('.currentCapacityCount.badge').addClass('badge-danger');
    } else if (occupancyRate > .35) {
        $('.currentCapacityCount.badge').addClass('badge-warning');
    }
    else {
        $('.currentCapacityCount.badge').addClass('badge-success');
    }

    $('.currentCapacityCount').text(totalSpaces - totalOccupancy);

    // Run page dependant code
    switch (window.location.pathname) {
        case '/':
            map(data);
            break;
        case '/index.html':
            map(data);
            break;
        case '/carparks.html':
            carparks(data.carparks.carparks);
            break;
        default:
            break;
    }
});

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#menu-toggle").toggleClass("is-active");
});
