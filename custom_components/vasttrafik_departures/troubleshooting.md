# Troubleshooting

Common issues and checks for **Västtrafik Departures**.

## API credentials could not be verified

Home Assistant may show:

```text
The API credentials could not be verified.
```

Check that:

- The Client ID is correct.
- The Client secret is correct.
- The credentials belong to the same Västtrafik developer application.
- The application has access to **Planera Resa API v4**.
- No extra spaces were copied before or after either value.

## Could not connect to Västtrafik

Home Assistant may show:

```text
Could not connect to Västtrafik.
```

Check:

- Home Assistant has Internet access.
- DNS is working.
- No firewall, proxy, or DNS filter is blocking the request.
- Västtrafik services are reachable.

## No stops were found

The route flow may show:

```text
No stops were found. Try another search.
```

The integration searches Västtrafik stop areas.

Try a shorter search phrase or only part of the stop name.

## Destination and Line destination are different

This is expected.

`Destination` is the stop selected when the route was configured.

`Line destination` is the short direction reported for the first leg of the journey.

Example:

```text
Destination: Hötorget, Borås
Line destination: Hässleholmen
```

## Entity names are in the wrong language

The Config Flow follows the Home Assistant UI language.

Entity names use Home Assistant's backend/default language when the entities are created.

Changing only the UI language may therefore change the setup dialogs without renaming existing entities.

## A removed route still appears

Current route entities are registered using the route's `config_subentry_id`.

Removing the route device should therefore also remove the corresponding route subentry and its entities.

If stale entities from an older version remain:

1. Restart Home Assistant.
2. Check **Settings → Devices & Services → Entities**.
3. Remove stale registry entries if necessary.
4. Recreate the route.

## Departure Board state is a number

This is intentional.

The `Departure board` sensor state is the number of departure rows currently available.

The actual journey rows are stored in the:

```text
departures
```

attribute.

## Cancelled binary sensor and Status do not match

This can be expected.

The `Status` sensor checks the first leg of the next journey.

The `Cancelled` binary sensor checks all legs of the next journey.

A later connecting leg can therefore be cancelled while the first leg is not.

## Refresh interval

Each route has its own refresh interval.

Available values:

```text
30
60
120
300
```

seconds.

The configured interval is also available in the Departure Board sensor's `refresh_interval` attribute.

## Integration does not appear after manual installation

Check that the directory is exactly:

```text
config/custom_components/vasttrafik_departures/
```

and contains at least:

```text
manifest.json
__init__.py
config_flow.py
sensor.py
```

Restart Home Assistant completely after copying the files.

## Reporting a bug

Include:

- Home Assistant version
- Integration version
- Steps to reproduce
- Expected result
- Actual result
- Relevant log lines

Do not include:

```text
Client ID
Client secret
API tokens
other private credentials
```
