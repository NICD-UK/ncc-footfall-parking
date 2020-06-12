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

$.when(getCityState(), getParking()).done(function(state, parking){
    data.state = state[1] === 'success' ? JSON.parse(state[0]) : null;
    data.carparks = parking[1] === 'success' ? JSON.parse(parking[0]) : null;
    console.log(data);

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
            map(data.state);
            break;
        case '/index.html':
            map(data.state);
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
