
import carparks from '../../public/assets/data/carparks';
import $ from 'jquery';

export default function(data) {

    const states = {
        'quiet': 'success',
        'average': 'warning',
        'busy': 'danger'
    };

    let html = '';

    carparks.forEach(function(carpark){

        const currentData = data.find(obj => { return obj.name === carpark.name; });

        console.log(currentData);

        let statusClass = currentData ? states[currentData.state] : 'secondary';
        let spaces = currentData ? (carpark.capacity - currentData.occupancy) : carpark.capacity;

        html += '<div class="list-group-item list-group-item-action carpark-list-item">' +
        '<div class="d-flex w-100 justify-content-between">' +
          '<h5 class="mb-1">' + carpark.name + '</h5>' +
          '<small><span class="badge badge-' + statusClass + ' badge-pill">' + spaces + '</span></small>' +
        '</div>' +
        '<p class="mb-1">' + carpark.address + '</p>' +
        '</div>';
    });

    $('#carpark-list').html(html);
}