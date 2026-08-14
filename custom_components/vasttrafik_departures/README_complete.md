# 🚍 Västtrafik Departures

[![Open your Home Assistant instance and add this repository in
HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ulf-tallmyr&repository=ha-vasttrafik&category=integration)

[![Validate](https://github.com/ulf-tallmyr/ha-vasttrafik/actions/workflows/validate.yml/badge.svg)](https://github.com/ulf-tallmyr/ha-vasttrafik/actions/workflows/validate.yml)
[![GitHub
Release](https://img.shields.io/github/v/release/ulf-tallmyr/ha-vasttrafik)](https://github.com/ulf-tallmyr/ha-vasttrafik/releases)
[![PyPI](https://img.shields.io/pypi/v/pyvasttrafik.svg)](https://pypi.org/project/pyvasttrafik/)

A modern Home Assistant integration for the **Västtrafik Journey
Planning API**.

------------------------------------------------------------------------

# Features

-   Native Config Flow
-   Multiple routes using Home Assistant Subentries
-   One Home Assistant device per route
-   Automatic cleanup when a route is removed
-   Real-time departure information
-   Delay and cancellation detection
-   Dashboard-friendly sensors
-   Binary sensor for cancelled departures
-   Configurable refresh interval
-   HACS compatible
-   Localized UI

------------------------------------------------------------------------

# Installation

## HACS

1.  Open HACS.
2.  Add this repository as a Custom Repository.
3.  Install **Västtrafik Departures**.
4.  Restart Home Assistant.
5.  Add the integration from **Settings → Devices & Services**.

## Manual

Copy:

``` text
custom_components/vasttrafik_departures
```

to:

``` text
config/custom_components/
```

Restart Home Assistant.

------------------------------------------------------------------------

# API credentials

Create an application in the Västtrafik Developer Portal.

Required credentials:

-   Client ID
-   Client Secret

Enter both during Config Flow.

------------------------------------------------------------------------

# Configuration

Each configured route becomes its own Home Assistant device.

Additional routes can be added later using **Add Route**.

------------------------------------------------------------------------

# Sensors

  Sensor                    Description
  ------------------------- ------------------------------
  Next departure            Timestamp for next departure
  Minutes until departure   Remaining minutes
  From                      Origin stop
  Destination               Destination stop
  Line                      Line number
  Line destination          Destination shown on vehicle
  Platform                  Platform / Stop position
  Travel duration           Planned journey time
  Number of changes         Transfers
  Delay                     Delay in minutes
  Transport mode            Bus, Tram, Train or Ferry
  Status                    Journey status
  Departure board           Upcoming departures

------------------------------------------------------------------------

# Binary Sensors

  Binary Sensor   Description
  --------------- -------------------------------------------------
  Cancelled       Indicates whether the next journey is cancelled

------------------------------------------------------------------------

# Dashboard example

``` yaml
type: entities
title: Work commute
entities:
  - sensor.home_work_next_departure
  - sensor.home_work_minutes_until_departure
  - sensor.home_work_line
  - sensor.home_work_platform
  - binary_sensor.home_work_cancelled
```

------------------------------------------------------------------------

# Automation example

``` yaml
trigger:
  - platform: numeric_state
    entity_id: sensor.home_work_minutes_until_departure
    below: 5

action:
  - service: notify.mobile_app_phone
    data:
      message: "Your bus leaves in less than 5 minutes."
```

------------------------------------------------------------------------

# Screenshots

Create a folder:

``` text
docs/screenshots/
```

Recommended images:

-   config-flow.png
-   routes.png
-   entities.png
-   dashboard.png

------------------------------------------------------------------------

# Roadmap

## Version 1.0

-   Config Flow
-   HACS support
-   Multiple routes
-   Subentries
-   Device cleanup
-   Dashboard sensors
-   Binary sensors

## Future

-   Dedicated Lovelace card
-   Journey summary entity
-   Additional travel metadata

------------------------------------------------------------------------

# Contributing

Bug reports, feature requests and pull requests are welcome.

------------------------------------------------------------------------

# License

MIT License

Created by **Ulf Tallmyr**
