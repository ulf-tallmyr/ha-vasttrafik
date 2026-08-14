# Configuration

Configuration for **Västtrafik Departures** is handled entirely through
the Home Assistant user interface.

## Add the integration

Open:

``` text
Settings → Devices & Services → Add Integration
```

Search for:

``` text
Västtrafik Departures
```

Enter:

-   Client ID
-   Client Secret

The integration validates the credentials before creating the config
entry.

If authentication fails, Home Assistant shows an invalid-authentication
error.

If the API cannot be reached, Home Assistant shows a connection error.

## Add a route

After the integration has been added, add a new route to the Västtrafik
config entry.

Each route is stored as a Home Assistant Config Subentry.

The route setup consists of five steps:

1.  Search for origin
2.  Select origin
3.  Search for destination
4.  Select destination
5.  Configure route settings

Only Västtrafik stop areas are returned in the stop search.

## Route name

The route name is optional.

The default value is:

``` text
<origin> → <destination>
```

Example:

``` text
Norra Sjöbogatan 55, Borås → Hötorget, Borås
```

You can replace this with a shorter name such as:

``` text
Home → City
```

The route name is also used as the Home Assistant device name for the
route.

## Refresh interval

Each route has its own refresh interval.

Available values:

       Interval Description
  ------------- --------------------------
     30 seconds Frequent updates
     60 seconds Default / normal updates
    120 seconds Reduced API traffic
    300 seconds Low-frequency updates

The selected interval is stored with the route and exposed by the
Departure Board sensor as the `refresh_interval` attribute.

## Multiple routes

A single Västtrafik integration config entry can contain multiple
routes.

Example:

``` text
Västtrafik
├── Home → City
├── City → Home
├── Home → Work
└── Work → Home
```

Each route has:

-   Its own Config Subentry
-   Its own update coordinator
-   Its own Home Assistant device
-   Its own sensors
-   Its own cancelled binary sensor
-   Its own refresh interval

## Removing a route

Removing the Home Assistant device for a route also removes the
corresponding route Config Subentry.

The entities belonging to that route are registered using the route's
`config_subentry_id`, so Home Assistant removes them together with the
route.

Removing one route does not remove the main Västtrafik integration or
any other configured routes.

## Origin and destination

The configured route destination and the destination displayed on the
vehicle are two different values.

### Destination

The stop selected when configuring the route.

Example:

``` text
Hötorget, Borås
```

### Line destination

The destination / short direction reported for the first leg of the
journey.

Example:

``` text
Hässleholmen
```

A journey can therefore have:

``` text
Destination: Hötorget, Borås
Line destination: Hässleholmen
```

This is expected.

## Language

The integration includes English and Swedish translations.

The Config Flow follows the Home Assistant UI language.

Entity names use Home Assistant's backend/default language when the
entities are created.

Changing only the UI language does not necessarily rename
already-created entities.

## API credentials

The main config entry stores:

``` text
client_id
client_secret
```

Individual route subentries store route-specific configuration such as:

``` text
origin
origin_name
towards
destination_name
route_name
update_interval
```

Do not publish Client IDs or Client Secrets in bug reports, screenshots,
logs, or GitHub issues.
