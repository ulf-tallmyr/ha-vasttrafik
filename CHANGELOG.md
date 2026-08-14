# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-08-14

### Changed

- Added Hassfest validation for Home Assistant compatibility checks.
- Added Sweden (`SE`) as the HACS country metadata in preparation for inclusion in the HACS default repository.

## [1.0.0] - 2026-08-14

### Added

- Multiple routes using Home Assistant Config Subentries.
- One Home Assistant device per configured route.
- Custom route names.
- Configurable refresh interval per route.
- Sensors for origin, destination, line destination, next departure, minutes until departure, travel duration, number of changes, line, transport mode, platform, delay, status and departure board.
- Binary sensor for cancelled journeys.
- Structured departure-board attributes for dashboards and templates.
- English and Swedish translations.
- Local Home Assistant branding with light and dark icons and logos.
- Documentation for configuration, entities, dashboards, examples and troubleshooting.

### Changed

- Refactored shared entity logic into `entity.py`.
- Refactored journey and departure helpers into `helpers.py`.
- Refactored transport-mode presentation into `icons.py`.
- Improved route setup and entity naming.
- Improved HACS metadata and validation.

### Fixed

- Removing a route device now also removes the corresponding Config Subentry.
- Route entities are registered with their `config_subentry_id` so they are removed together with the route.
- Correct handling of Västtrafik short direction / line destination.

## [0.1.1] - 2026-08-10

### Added

- Home Assistant integration.
- HACS support.
- Config flow support.
- Route subentries.
- DataUpdateCoordinator support.
- Real-time departure information.
- Delay information.
- Multiple route support.
- Support for buses, trams, trains and ferries.
- `short_direction` support.

### Changed

- Improved sensor attributes.
- Improved error handling.
