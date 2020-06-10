# TimerTrigger Azure Function

On Timer tick (settings in `function.json` file under `schedule` entry) following is executed: 
* pulls footfall data, 
* pulls carpark data,
* adds metadata info,
* formats the output.

ToDo:
* deploy as a azure function,
* persist to blob storage (historical file),
* overwrite the latest blob file,   
* other improvements (search for ToDo in the code).

Example output:

```json
{
    "timestamp": "2020-06-10T23:06:03.942126+01:00",
    "response_time_us": 306687,
    "city_state": "quiet",
    "footfall": [{
        "sensor_name": "PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_0",
        "number_of_datapoints": 22,
        "average_people_count": 1.7
    }, {
        "sensor_name": "PER_PEOPLE_NORTHUMERLAND_LINE_LONG_DISTANCE_HEAD_1",
        "number_of_datapoints": 22,
        "average_people_count": 1.5
    }],
    "carparks": [{
        "name": "Car park at Eldon Garden",
        "timestamp": "2020-06-10T21:59:14+01:00",
        "capacity": 449,
        "occupancy": 17,
        "state": "quiet"
    }]
}
```

## Azure docs - TimerTrigger

The `TimerTrigger` makes it incredibly easy to have your functions executed on a schedule. This sample demonstrates a simple use case of calling your function every 5 minutes.

### How it works

For a `TimerTrigger` to work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression)(See the link for full details). A cron expression is a string with 6 separate expressions which represent a given schedule via patterns. The pattern we use to represent every 5 minutes is `0 */5 * * * *`. This, in plain text, means: "When seconds is equal to 0, minutes is divisible by 5, for any hour, day of the month, month, day of the week, or year".

### Learn more

<TODO> Documentation
