import '../styles/index.scss';
import 'bootstrap';
import $ from 'jquery';
import map from './map';
import carparks from './carparks';

const data = {};

$.ajax({
    method: "GET",
    cache: false,
    url: 'https://nccfootfallparking.blob.core.windows.net/api-data/latest.json',
    success: function(response) {
        data = response;
        console.log(data);
    },
    error: function(error) {
        console.error(error);
    }
});

// Run page dependant code
switch (window.location.pathname) {
    case '/index.html':
        map();
        break;
    case '/carparks.html':
        carparks();
        break;
    default:
        break;
}

$('.currentCapacityCount').text(123);

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#menu-toggle").toggleClass("is-active");
});
