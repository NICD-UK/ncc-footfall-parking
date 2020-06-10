
import carparks from '../../public/assets/data/carparks';
import $ from 'jquery';

export default function() {

    const states = ['quiet', 'average', 'busy'];

    let html = '';
    carparks.forEach(function(carpark){

        let statusClass = 'success';

        if (carpark.capacity < 100) {
            statusClass = 'warning';
        }
        
        if (carpark.capacity < 50) {
            statusClass = 'danger';
        }

        html += '<div class="list-group-item list-group-item-action carpark-list-item">' +
        '<div class="d-flex w-100 justify-content-between">' +
          '<h5 class="mb-1">' + carpark.name + '</h5>' +
          '<small><span class="badge badge-' + statusClass + ' badge-pill">' + carpark.capacity + '</span></small>' +
        '</div>' +
        '<p class="mb-1">' + carpark.address + '</p>' +
        '</div>';
    });

    $('#carpark-list').html(html);
}