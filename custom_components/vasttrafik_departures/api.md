# Entity and data reference

Technical reference for the entities exposed by **Västtrafik
Departures**.

Each configured route is represented by its own Home Assistant device
and has its own set of entities.

## Sensors

### Next departure

Suffix:

``` text
next_departure
```

State:

``` text
HH:MM
```

The state is the effective departure time of the first leg in the next
journey.

Additional attributes:

``` text
origin
destination
route_name
departures
```

The first departure row is also copied into the sensor attributes.

------------------------------------------------------------------------

### Minutes until departure

Suffix:

``` text
minutes_until
```

State:

``` text
integer
```

Unit:

``` text
min
```

Represents the number of whole minutes until the effective departure
time of the next journey.

------------------------------------------------------------------------

### From

Suffix:

``` text
from
```

State:

``` text
string
```

The configured origin stop name.

------------------------------------------------------------------------

### Destination

Suffix:

``` text
destination
```

State:

``` text
string
```

The configured destination stop name.

This is the destination selected when the route was configured.

------------------------------------------------------------------------

### Line destination

Suffix:

``` text
line_destination
```

State:

``` text
string
```

The short direction of the first leg, normally corresponding to the
destination shown for the vehicle or line.

This is separate from the configured route destination.

------------------------------------------------------------------------

### Travel duration

Suffix:

``` text
travel_duration
```

State:

``` text
integer
```

Unit:

``` text
min
```

Calculated from the journey departure and arrival times.

------------------------------------------------------------------------

### Number of changes

Suffix:

``` text
number_of_changes
```

State:

``` text
integer
```

The number of changes reported for the journey.

------------------------------------------------------------------------

### Line

Suffix:

``` text
line
```

State:

``` text
string
```

The line designation for the first leg of the journey.

Examples may include values such as:

``` text
1
100
VY
```

------------------------------------------------------------------------

### Transport mode

Suffix:

``` text
transport_mode
```

State:

``` text
string
```

The normalized transport mode for the first leg.

The entity icon is selected dynamically from the transport mode.

------------------------------------------------------------------------

### Platform

Suffix:

``` text
platform
```

State:

``` text
string
```

The platform or stop position of the origin of the first leg.

------------------------------------------------------------------------

### Delay

Suffix:

``` text
delay
```

State:

``` text
integer
```

Unit:

``` text
min
```

The delay of the first leg in minutes.

------------------------------------------------------------------------

### Status

Suffix:

``` text
status
```

Possible states:

``` text
on_time
delayed
cancelled
```

Rules:

-   `cancelled` if the first leg is cancelled
-   `delayed` if delay is greater than 0 minutes
-   `on_time` otherwise

------------------------------------------------------------------------

### Departure board

Suffix:

``` text
departure_board
```

State:

``` text
integer
```

The state is the number of departure rows currently available.

Attributes:

``` text
route_name
origin
destination
refresh_interval
departures
```

## Departure board row schema

The `departures` attribute is a list of dictionaries.

Each row currently contains:

  -----------------------------------------------------------------------
  Attribute               Type                    Description
  ----------------------- ----------------------- -----------------------
  `time`                  string / null           Effective departure
                                                  time in ISO 8601 format

  `display_time`          string / null           Effective departure
                                                  time formatted as
                                                  `HH:MM`

  `planned_time`          string / null           Planned departure time
                                                  in ISO 8601 format

  `estimated_time`        string / null           Estimated departure
                                                  time in ISO 8601 format

  `minutes_until`         integer / null          Minutes until departure

  `line`                  string / null           Line designation

  `direction`             string / null           Full direction value
                                                  from journey data

  `line_destination`      string / null           Short direction / line
                                                  destination

  `transport_mode`        string / null           Normalized transport
                                                  mode

  `platform`              string / null           Origin platform or stop
                                                  position

  `delay_minutes`         integer                 Delay in minutes

  `cancelled`             boolean                 Whether the first leg
                                                  is cancelled

  `status`                string                  `on_time`, `delayed` or
                                                  `cancelled`

  `number_of_changes`     integer / null          Number of journey
                                                  changes

  `travel_duration`       integer / null          Total journey duration
                                                  in minutes
  -----------------------------------------------------------------------

Example:

``` yaml
departures:
  - time: "2026-08-13T19:57:00+02:00"
    display_time: "19:57"
    planned_time: "2026-08-13T19:55:00+02:00"
    estimated_time: "2026-08-13T19:57:00+02:00"
    minutes_until: 4
    line: "1"
    direction: "Hässleholmen"
    line_destination: "Hässleholmen"
    transport_mode: "bus"
    platform: "A"
    delay_minutes: 2
    cancelled: false
    status: "delayed"
    number_of_changes: 0
    travel_duration: 16
```

## Binary sensor

### Cancelled

Suffix:

``` text
cancelled
```

Possible states:

``` text
on
off
unknown
```

The binary sensor checks all legs in the next journey.

-   `on` if any leg is cancelled
-   `off` if no leg is cancelled
-   unknown if there is no usable journey data

Note that this differs slightly from the `Status` sensor and the
individual departure-board row, which use the first leg of the journey.

## Entity IDs

Home Assistant creates entity IDs from the configured route name and
entity name.

Do not rely on a fixed example entity ID in reusable YAML.

Find the actual entity IDs under:

``` text
Settings → Devices & Services → Entities
```

## Data refresh

Each route has its own coordinator and refresh interval.

The Departure Board sensor exposes the configured interval in its
`refresh_interval` attribute.
