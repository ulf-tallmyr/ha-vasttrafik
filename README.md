# Västtrafik Departures

[![Open your Home Assistant instance and open this repository in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ulf-tallmyr&repository=ha-vasttrafik&category=integration)

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

[![GitHub Release](https://img.shields.io/github/v/release/ulf-tallmyr/ha-vasttrafik)](https://github.com/ulf-tallmyr/ha-vasttrafik/releases)

[![PyPI version](https://img.shields.io/pypi/v/pyvasttrafik.svg)](https://pypi.org/project/pyvasttrafik/)

[![Validate](https://github.com/ulf-tallmyr/ha-vasttrafik/actions/workflows/validate.yml/badge.svg)](https://github.com/ulf-tallmyr/ha-vasttrafik/actions/workflows/validate.yml)

A Home Assistant integration for Västtrafik departures.

## Features

- Search for stops and stations.
- Configure multiple routes.
- Real-time departures.
- Delay information.
- Multiple transport types.
- Support for buses, trams, trains and ferries.

## Installation

### HACS

1. Open HACS.
2. Add the repository URL.
3. Install the integration.
4. Restart Home Assistant.
5. Add the integration from the UI.

### Manual installation

Copy the `custom_components/vasttrafik_departures` directory to your Home Assistant installation.

## Configuration

The integration requires:

- Client ID
- Client secret

Both can be obtained from the Västtrafik developer portal.

## Example attributes

```yaml
next_departure: "2026-08-09T20:32:00+02:00"
minutes_until: 8
line: "1"
direction: "Hässleholmen via Sjukhuset"
short_direction: "Hässleholmen"
```

## Credits

Created by Ulf Tallmyr.