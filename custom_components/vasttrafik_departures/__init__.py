"""The Västtrafik integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import (
    CONF_DESTINATION_NAME,
    CONF_ORIGIN,
    CONF_ORIGIN_NAME,
    CONF_ROUTE_NAME,
    CONF_TOWARDS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
)
from .coordinator import VasttrafikRouteCoordinator

PLATFORMS = ["sensor", "binary_sensor"]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up the integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up a Västtrafik config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"coordinators": {}}

    for subentry in entry.subentries.values():
        if subentry.subentry_type != "route":
            continue

        origin_name = subentry.data.get(CONF_ORIGIN_NAME)
        destination_name = subentry.data.get(CONF_DESTINATION_NAME)

        if (
            (origin_name is None or destination_name is None)
            and "→" in subentry.title
        ):
            title_origin, title_destination = (
                part.strip() for part in subentry.title.split("→", 1)
            )
            origin_name = origin_name or title_origin
            destination_name = destination_name or title_destination

        route_name = subentry.data.get(CONF_ROUTE_NAME) or subentry.title

        coordinator = VasttrafikRouteCoordinator(
            hass,
            entry,
            origin_gid=subentry.data[CONF_ORIGIN],
            destination_gid=subentry.data[CONF_TOWARDS],
            origin_name=origin_name,
            destination_name=destination_name,
            route_name=route_name,
            update_interval=subentry.data.get(
                CONF_UPDATE_INTERVAL,
                DEFAULT_UPDATE_INTERVAL,
            ),
        )

        await coordinator.async_config_entry_first_refresh()
        hass.data[DOMAIN][entry.entry_id]["coordinators"][
            subentry.subentry_id
        ] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(
        entry.add_update_listener(_async_reload_entry)
    )
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a Västtrafik config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
    if not unload_ok:
        return False

    entry_data = hass.data[DOMAIN].pop(entry.entry_id, {})
    for coordinator in entry_data.get("coordinators", {}).values():
        await coordinator.async_shutdown()

    return True


async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    device_entry: DeviceEntry,
) -> bool:
    """Remove the route subentry when its device is deleted."""

    subentry_id = device_entry.config_subentry_id

    if subentry_id is None:
        return False

    subentry = config_entry.subentries.get(subentry_id)

    if subentry is None or subentry.subentry_type != "route":
        return False

    hass.config_entries.async_remove_subentry(
        config_entry,
        subentry_id,
    )

    return True


async def _async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload the config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
