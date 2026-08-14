# Changelog

All notable changes to this project will be documented in this file.

The format is based on **Keep a Changelog** and this project follows **Semantic Versioning**.

## [Unreleased]

### Added

- Native Home Assistant Config Flow.
- Support for multiple routes using Config Subentries.
- One Home Assistant device per configured route.
- Custom route names.
- Configurable refresh interval per route.
- Real-time journey and departure information.
- Sensors for:
  - From
  - Destination
  - Line destination
  - Next departure
  - Minutes until departure
  - Travel duration
  - Number of changes
  - Line
  - Transport mode
  - Platform
  - Delay
  - Status
  - Departure board
- Binary sensor for cancelled journeys.
- Structured departure-board attributes for dashboards and templates.
- English and Swedish translations.
- Local Home Assistant brand assets.
- HACS support and repository validation workflow.

### Changed

- Refactored shared entity logic into `entity.py`.
- Refactored journey and departure helpers into `helpers.py`.
- Refactored transport-mode presentation into `icons.py`.
- Improved entity and device naming.
- Improved route setup flow.
- Improved HACS metadata and repository validation.

### Fixed

- Removing a route device now also removes the corresponding Config Subentry.
- Route entities are registered with their `config_subentry_id` so they are removed together with the route.
- Correct handling of Västtrafik short direction / line destination.
- Various HACS validation issues.

## [0.1.1]

- Current development version before the 1.0 release candidate.
- Uses `pyvasttrafik==0.1.1`.
