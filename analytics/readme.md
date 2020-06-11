# NCC NE1 back-end

On Timer tick (settings in `function.json` file under `schedule` entry) following is executed: 
* pulls footfall data, 
* pulls carpark data,
* measures UO API response time,
* formats the output,
* persist to blob storage (historical file),
* overwrite the latest blob file.


ToDo:
* refactor code (tons of shortcuts),
* try before accessing possibly empty results,
* move from VM to azure function,
* other improvements (search for ToDo in the code).

City state output:

```json
{
    "timestamp": "2020-06-11T23:50:16.939814+00:00",
    "response_time_us": 752696,
    "city_state": "quiet",
    "footfall": [{
        "sensor_name": "PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_0",
        "number_of_datapoints": 24,
        "average_people_count": 0.0
    }, {
        "sensor_name": "PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_1",
        "number_of_datapoints": 24,
        "average_people_count": 0.0
    }]
}
```

Carparks output:

```json
{
    "timestamp": "2020-06-12T00:40:17.676495+01:00",
    "response_time_us": 280607,
    "carparks": [{
            "name": "Eldon Square",
            "timestamp": "2020-06-11T21:59:26+01:00",
            "capacity": 497,
            "occupancy": 8,
            "reserved_bays": 0,
            "free_spaces": 489,
            "state": "quiet"
        },
        {
            "name": "Claremont Road",
            "timestamp": "2020-06-12T00:39:07+01:00",
            "capacity": 225,
            "occupancy": 0,
            "reserved_bays": 0,
            "free_spaces": 225,
            "state": "quiet"
        },
        {
            "name": "Dean Street",
            "timestamp": "2020-06-12T00:39:17+01:00",
            "capacity": 257,
            "occupancy": 52,
            "reserved_bays": 0,
            "free_spaces": 205,
            "state": "quiet"
        },
        {
            "name": "Eldon Garden",
            "timestamp": "2020-06-11T21:59:25+01:00",
            "capacity": 449,
            "occupancy": 24,
            "reserved_bays": 0,
            "free_spaces": 425,
            "state": "quiet"
        },
        {
            "name": "Ellison Place",
            "timestamp": "2020-06-12T00:38:37+01:00",
            "capacity": 126,
            "occupancy": 0,
            "reserved_bays": 0,
            "free_spaces": 126,
            "state": "quiet"
        },
        {
            "name": "Grainger Town",
            "timestamp": "2020-06-11T23:56:14+01:00",
            "capacity": 410,
            "occupancy": 10,
            "reserved_bays": 0,
            "free_spaces": 400,
            "state": "quiet"
        },
        {
            "name": "Manors",
            "timestamp": "2020-06-11T21:59:22+01:00",
            "capacity": 484,
            "occupancy": 16,
            "reserved_bays": 0,
            "free_spaces": 468,
            "state": "quiet"
        }
    ]
}
```

## Azure docs - TimerTrigger

The `TimerTrigger` makes it incredibly easy to have your functions executed on a schedule. This sample demonstrates a simple use case of calling your function every 5 minutes.

### How it works

For a `TimerTrigger` to work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression)(See the link for full details). A cron expression is a string with 6 separate expressions which represent a given schedule via patterns. The pattern we use to represent every 5 minutes is `0 */5 * * * *`. This, in plain text, means: "When seconds is equal to 0, minutes is divisible by 5, for any hour, day of the month, month, day of the week, or year".

### Learn more

<TODO> Documentation
