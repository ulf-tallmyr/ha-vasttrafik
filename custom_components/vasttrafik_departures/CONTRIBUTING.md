# Contributing

Contributions to **Västtrafik Departures** are welcome.

## Before you start

For larger changes, please open an issue first so the implementation can
be discussed before significant work is done.

For small fixes, documentation updates, and minor improvements, a pull
request is fine.

## Development setup

Clone the repository:

``` bash
git clone https://github.com/ulf-tallmyr/ha-vasttrafik.git
cd ha-vasttrafik
```

The Home Assistant integration is located in:

``` text
custom_components/vasttrafik_departures/
```

The integration depends on the Python package:

``` text
pyvasttrafik
```

## Testing changes

Before opening a pull request:

1.  Copy the updated integration to your Home Assistant test instance.
2.  Restart Home Assistant.
3.  Confirm the integration loads without errors.
4.  Test adding a route.
5.  Test removing a route.
6.  Confirm entities are created and removed correctly.
7.  Confirm GitHub Actions validation passes.

## Code style

Please keep changes:

-   Focused
-   Readable
-   Backwards compatible where practical
-   Consistent with existing Home Assistant patterns

Avoid unnecessary refactoring in pull requests that primarily fix a bug
or add one feature.

## Translations

Translations are stored in:

``` text
custom_components/vasttrafik_departures/translations/
```

Current language files:

``` text
en.json
sv.json
```

When adding new entity names, config-flow fields, or states, update the
relevant translation files.

## Config Subentries

Each configured route is stored as a Home Assistant Config Subentry.

Each route should:

-   Have its own coordinator
-   Have its own device
-   Register its entities using the route's `config_subentry_id`
-   Clean up correctly when the route is removed

## Pull requests

A pull request should include:

-   A clear title
-   A short description of the change
-   Testing notes
-   Screenshots when the change affects the UI
-   Any relevant issue number

## Bug reports

Please include:

-   Home Assistant version
-   Integration version
-   Relevant log output
-   Steps to reproduce
-   Expected behavior
-   Actual behavior

Do not include API secrets, Client IDs, Client Secrets, or other private
credentials.

## Feature requests

Feature requests are welcome.

Please explain:

-   What problem the feature solves
-   How you expect it to work
-   Why it belongs in the integration

## Commit messages

Use short, descriptive commit messages.

Examples:

``` text
Fix subentry entity cleanup
Add route refresh interval
Improve Swedish translations
Update README
```

## License

By contributing, you agree that your contributions will be licensed
under the project's MIT License.
