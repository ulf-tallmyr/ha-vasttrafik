# Västtrafik Departures

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