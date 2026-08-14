# Dashboard examples

This page contains example Home Assistant dashboard configurations for
Västtrafik Departures.

## Simple entities card

``` yaml
type: entities
title: Home → City
entities:
  - sensor.home_to_city_next_departure
  - sensor.home_to_city_minutes_until_departure
  - sensor.home_to_city_line
  - sensor.home_to_city_line_destination
  - sensor.home_to_city_platform
  - sensor.home_to_city_travel_duration
  - sensor.home_to_city_delay
  - binary_sensor.home_to_city_cancelled
```

## Compact glance-style view

``` yaml
type: glance
title: Home → City
entities:
  - entity: sensor.home_to_city_minutes_until_departure
    name: Departure
  - entity: sensor.home_to_city_line
    name: Line
  - entity: sensor.home_to_city_platform
    name: Platform
  - entity: sensor.home_to_city_travel_duration
    name: Travel time
```

## Conditional cancelled warning

``` yaml
type: conditional
conditions:
  - entity: binary_sensor.home_to_city_cancelled
    state: "on"
card:
  type: markdown
  content: |
    ## ⚠️ Departure cancelled
    The next configured journey is cancelled.
```

## Delay warning

``` yaml
type: conditional
conditions:
  - condition: numeric_state
    entity: sensor.home_to_city_delay
    above: 0
card:
  type: markdown
  content: |
    ## ⏱ Delay
    The next departure is delayed.
```

## Departure board attributes

The `Departure board` sensor exposes upcoming departures in the
`departures` attribute.

Typical structure:

``` yaml
departures:
  - display_time: "19:57"
    line: "1"
    line_destination: "Hässleholmen"
    transport_mode: "bus"
    platform: "A"
    minutes_until: 4
    delay_minutes: 0
    cancelled: false
    status: "on_time"
```

This is intended for custom dashboard cards and templates.

## Markdown card using the next departure sensor

``` yaml
type: markdown
content: |
  ## 🚍 Home → City

  **Next departure:** {{ states('sensor.home_to_city_next_departure') }}

  **In:** {{ states('sensor.home_to_city_minutes_until_departure') }} min

  **Line:** {{ states('sensor.home_to_city_line') }}

  **Towards:** {{ states('sensor.home_to_city_line_destination') }}

  **Platform:** {{ states('sensor.home_to_city_platform') }}
```

## Notes

Entity IDs depend on the route name and Home Assistant's entity naming.

Use **Settings → Devices & Services → Entities** to find the exact
entity IDs for your installation.
