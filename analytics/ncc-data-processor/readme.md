# TimerTrigger Azure Function

On Timer tick (settings in `function.json` file under `schedule` entry) following is executed: 
* pulls footfall data, 
* pulls carpark data,
* adds metadata info,
* formats the output.

ToDo:
* find where is actual footfall measurement,
* set the thresholds for footfall busyness levels,
* persist to blob storage (historical file),
* overwrite the latest blob file,   
* deploy as a azure function,
* other improvements (search for ToDo in the code).

Example output:

```json
{
    "timestamp": "2020-06-09 21:42:38.820476",
    "response_time_ms": 683372,
    "footfall": [{
        "sensor_name": "PER_PEOPLE_NC_B6324B1",
        "measurement": -1,
        "status": "quiet"
    }, {
        "sensor_name": "PER_PEOPLE_NORTHUMERLAND_LINE_SHORT_DISTANCE_HEAD_6",
        "measurement": -1,
        "status": "average"
    }],
    "carparks": [{
        "name": "Car park at Eldon Garden",
        "timestamp": "2020-06-09T20:42:04.000Z",
        "capacity": 449,
        "occupancy": 19,
        "status": "quiet"
    }]
}
```

## Azure docs - TimerTrigger

The `TimerTrigger` makes it incredibly easy to have your functions executed on a schedule. This sample demonstrates a simple use case of calling your function every 5 minutes.

### How it works

For a `TimerTrigger` to work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression)(See the link for full details). A cron expression is a string with 6 separate expressions which represent a given schedule via patterns. The pattern we use to represent every 5 minutes is `0 */5 * * * *`. This, in plain text, means: "When seconds is equal to 0, minutes is divisible by 5, for any hour, day of the month, month, day of the week, or year".

### Learn more

<TODO> Documentation
