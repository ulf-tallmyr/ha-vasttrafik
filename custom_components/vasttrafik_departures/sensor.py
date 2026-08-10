"""Sensors for Västtrafik Departures."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    CONF_ORIGIN,
    CONF_TOWARDS,
    DOMAIN,
)
from .coordinator import VasttrafikRouteCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Västtrafik route sensors."""

    entities: list[VasttrafikDepartureSensor] = []

    for subentry in entry.subentries.values():
        if subentry.subentry_type != "route":
            continue

        origin_gid = subentry.data[CONF_ORIGIN]
        destination_gid = subentry.data[CONF_TOWARDS]

        coordinator = VasttrafikRouteCoordinator(
            hass,
            entry,
            origin_gid=origin_gid,
            destination_gid=destination_gid,
        )
        hass.data[DOMAIN][entry.entry_id]["coordinators"][
            subentry.subentry_id
        ] = coordinator
        await coordinator.async_config_entry_first_refresh()

        entities.append(
            VasttrafikDepartureSensor(
                coordinator=coordinator,
                entry=entry,
                subentry_id=subentry.subentry_id,
                title=subentry.title,
            )
        )

    async_add_entities(entities)


class VasttrafikDepartureSensor(
    CoordinatorEntity[VasttrafikRouteCoordinator],
    SensorEntity,
):
    """Represent upcoming departures for one configured route."""

    _attr_icon = "mdi:bus"

    def __init__(
        self,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        title: str,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)

        self._attr_name = title
        self._attr_unique_id = f"{entry.entry_id}_{subentry_id}"

    @property
    def native_value(self) -> str | None:
        """Return the next departure time as HH:MM."""

        leg = self._next_leg

        if leg is None:
            return None

        departure_time = leg.effective_departure_time

        if departure_time is None:
            return None

        return departure_time.strftime("%H:%M")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return detailed departure information."""

        journeys = self.coordinator.data or []

        departures: list[dict[str, Any]] = []

        for journey in journeys:
            if not journey.legs:
                continue

            leg = journey.legs[0]
            departure_time = leg.effective_departure_time

            departures.append(
                {
                    "time": (
                        departure_time.isoformat()
                        if departure_time is not None
                        else None
                    ),
                    "planned_time": (
                        leg.planned_departure_time.isoformat()
                        if leg.planned_departure_time is not None
                        else None
                    ),
                    "estimated_time": (
                        leg.estimated_departure_time.isoformat()
                        if leg.estimated_departure_time is not None
                        else None
                    ),
                    "minutes_until": self._minutes_until(
                        departure_time
                    ),
                    "line": leg.line_designation,
                    "direction": leg.direction,
                    "short_direction": leg.short_direction,
                    "transport_mode": leg.transport_mode,
                    "platform": (
                        leg.origin.platform
                        if leg.origin is not None
                        else None
                    ),
                    "delay_minutes": leg.delay_minutes,
                    "cancelled": leg.cancelled,
                }
            )

        next_departure = departures[0] if departures else None

        attributes: dict[str, Any] = {
            "departures": departures,
        }

        if next_departure is not None:
            attributes.update(
                {
                    "next_departure": next_departure["time"],
                    "minutes_until": next_departure["minutes_until"],
                    "line": next_departure["line"],
                    "direction": next_departure["direction"],
                    "short_direction": next_departure["short_direction"],
                    "transport_mode": next_departure["transport_mode"],
                    "platform": next_departure["platform"],
                    "delay_minutes": next_departure["delay_minutes"],
                    "cancelled": next_departure["cancelled"],
                }
            )

        return attributes

    @property
    def _next_leg(self):
        """Return the first leg of the next journey."""

        journeys = self.coordinator.data or []

        for journey in journeys:
            if journey.legs:
                return journey.legs[0]

        return None

    @staticmethod
    def _minutes_until(
        departure_time: datetime | None,
    ) -> int | None:
        """Return minutes until departure."""

        if departure_time is None:
            return None

        now = dt_util.now()

        if departure_time.tzinfo is not None:
            now = now.astimezone(departure_time.tzinfo)

        seconds = (departure_time - now).total_seconds()

        return max(0, int(seconds // 60))