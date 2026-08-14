# Examples

Practical Home Assistant examples for **Västtrafik Departures**.

## Notify when departure is close

``` yaml
alias: Bus leaves soon
trigger:
  - platform: numeric_state
    entity_id: sensor.home_to_city_minutes_until_departure
    below: 5
condition:
  - condition: state
    entity_id: binary_sensor.home_to_city_cancelled
    state: "off"
action:
  - service: notify.mobile_app_phone
    data:
      message: >
        Line {{ states('sensor.home_to_city_line') }}
        leaves in {{ states('sensor.home_to_city_minutes_until_departure') }} minutes.
mode: single
```

## Notify about a delay

``` yaml
alias: Västtrafik delay warning
trigger:
  - platform: numeric_state
    entity_id: sensor.home_to_city_delay
    above: 0
action:
  - service: notify.mobile_app_phone
    data:
      message: >
        Your next departure is delayed by
        {{ states('sensor.home_to_city_delay') }} minutes.
mode: single
```

## Notify when a journey is cancelled

``` yaml
alias: Västtrafik cancellation warning
trigger:
  - platform: state
    entity_id: binary_sensor.home_to_city_cancelled
    to: "on"
action:
  - service: notify.mobile_app_phone
    data:
      message: "The next configured Västtrafik journey is cancelled."
mode: single
```

## Show route information in a Markdown card

``` yaml
type: markdown
content: |
  ## 🚍 Home → City

  **Departure:** {{ states('sensor.home_to_city_next_departure') }}

  **Leaves in:** {{ states('sensor.home_to_city_minutes_until_departure') }} min

  **Line:** {{ states('sensor.home_to_city_line') }}

  **Towards:** {{ states('sensor.home_to_city_line_destination') }}

  **Platform:** {{ states('sensor.home_to_city_platform') }}

  **Travel time:** {{ states('sensor.home_to_city_travel_duration') }} min
```

## Template: friendly departure text

``` jinja
{% set minutes = states('sensor.home_to_city_minutes_until_departure') | int %}
{% set line = states('sensor.home_to_city_line') %}
{% set destination = states('sensor.home_to_city_line_destination') %}

{% if is_state('binary_sensor.home_to_city_cancelled', 'on') %}
The next journey is cancelled.
{% elif minutes == 0 %}
Line {{ line }} towards {{ destination }} is leaving now.
{% elif minutes == 1 %}
Line {{ line }} towards {{ destination }} leaves in 1 minute.
{% else %}
Line {{ line }} towards {{ destination }} leaves in {{ minutes }} minutes.
{% endif %}
```

## Template: status text

``` jinja
{% set delay = states('sensor.home_to_city_delay') | int(0) %}

{% if is_state('binary_sensor.home_to_city_cancelled', 'on') %}
Cancelled
{% elif delay > 0 %}
Delayed by {{ delay }} min
{% else %}
On time
{% endif %}
```

## Use the departure board attributes

Example template that reads the first departure:

``` jinja
{% set departures =
  state_attr('sensor.home_to_city_departure_board', 'departures') or []
%}

{% if departures %}
  {% set departure = departures[0] %}
  {{ departure.line }}
  towards {{ departure.line_destination }}
  at {{ departure.display_time }}
{% else %}
  No departures available
{% endif %}
```

## List all available departure-board rows

``` jinja
{% set departures =
  state_attr('sensor.home_to_city_departure_board', 'departures') or []
%}

{% for departure in departures %}
{{ departure.display_time }}
Line {{ departure.line }}
→ {{ departure.line_destination }}
{% if departure.platform %}(Platform {{ departure.platform }}){% endif %}
{% endfor %}
```

## Notes

Replace the example entity IDs with the entity IDs created in your own
Home Assistant installation.

The exact entity IDs depend on the configured route name and Home
Assistant's naming rules.
