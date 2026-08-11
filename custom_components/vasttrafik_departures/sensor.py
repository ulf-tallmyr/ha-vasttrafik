"""Sensors for Västtrafik Departures."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import VasttrafikRouteCoordinator


TRANSPORT_MODE_NAMES: dict[str, str] = {
    "bus": "Bus",
    "tram": "Tram",
    "train": "Train",
    "ferry": "Ferry",
    "taxi": "Taxi",
}

TRANSPORT_MODE_ICONS: dict[str, str] = {
    "bus": "mdi:bus",
    "tram": "mdi:tram",
    "train": "mdi:train",
    "ferry": "mdi:ferry",
    "taxi": "mdi:taxi",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Västtrafik route sensors."""

    entities: list[SensorEntity] = []
    device_registry = dr.async_get(hass)

    for subentry in entry.subentries.values():
        if subentry.subentry_type != "route":
            continue

        coordinator = hass.data[DOMAIN][entry.entry_id]["coordinators"].get(
            subentry.subentry_id
        )
        if coordinator is None:
            continue

        device_entry = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            config_subentry_id=subentry.subentry_id,
            identifiers={(DOMAIN, subentry.subentry_id)},
            name=subentry.title,
            manufacturer="Västtrafik",
            model="Route",
        )

        common = {
            "coordinator": coordinator,
            "entry": entry,
            "subentry_id": subentry.subentry_id,
            "device_entry": device_entry,
        }

        entities.extend(
            [
                VasttrafikDepartureSensor(**common),
                VasttrafikMinutesUntilSensor(**common),
                VasttrafikSimpleSensor(
                    **common,
                    name="From",
                    suffix="from",
                    icon="mdi:map-marker-outline",
                    value_getter=_origin,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    name="Destination",
                    suffix="destination",
                    icon="mdi:map-marker",
                    value_getter=_destination,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    name="Line destination",
                    suffix="line_destination",
                    icon="mdi:sign-direction",
                    value_getter=_line_destination,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    name="Travel duration",
                    suffix="travel_duration",
                    icon="mdi:clock-outline",
                    value_getter=_travel_duration,
                    native_unit_of_measurement=UnitOfTime.MINUTES,
                    device_class=SensorDeviceClass.DURATION,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    name="Number of changes",
                    suffix="number_of_changes",
                    icon="mdi:swap-horizontal",
                    value_getter=_number_of_changes,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    name="Line",
                    suffix="line",
                    icon="mdi:bus",
                    value_getter=_line,
                ),
                VasttrafikTransportModeSensor(**common),
                VasttrafikSimpleSensor(
                    **common,
                    name="Platform",
                    suffix="platform",
                    icon="mdi:sign-real-estate",
                    value_getter=_platform,
                ),
                VasttrafikDelaySensor(**common),
                VasttrafikDepartureBoardSensor(**common),
            ]
        )

    async_add_entities(entities)


class VasttrafikBaseSensor(
    CoordinatorEntity[VasttrafikRouteCoordinator],
    SensorEntity,
):
    """Base class for Västtrafik sensors."""

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
        name: str,
        suffix: str,
        icon: str,
    ) -> None:
        """Initialize a Västtrafik sensor."""

        super().__init__(coordinator)

        self.device_entry = device_entry
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{subentry_id}_{suffix}"
        self._attr_has_entity_name = True

    @property
    def next_journey(self):
        """Return the next journey."""
        journeys = self.coordinator.data or []
        return journeys[0] if journeys else None

    @property
    def next_leg(self):
        """Return the first leg of the next journey."""
        journey = self.next_journey

        if journey is not None and journey.legs:
            return journey.legs[0]

        return None

    @staticmethod
    def minutes_until(departure_time: datetime | None) -> int | None:
        """Return whole minutes until departure."""
        if departure_time is None:
            return None

        now = dt_util.now()

        if departure_time.tzinfo is not None:
            now = now.astimezone(departure_time.tzinfo)

        seconds = (departure_time - now).total_seconds()
        return max(0, int(seconds // 60))


ValueGetter = Callable[["VasttrafikSimpleSensor"], Any]


class VasttrafikSimpleSensor(VasttrafikBaseSensor):
    """Sensor whose value is provided by a getter function."""

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
        name: str,
        suffix: str,
        icon: str,
        value_getter: ValueGetter,
        native_unit_of_measurement: str | None = None,
        device_class: SensorDeviceClass | None = None,
    ) -> None:
        """Initialize a simple Västtrafik sensor."""

        super().__init__(
            coordinator=coordinator,
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            name=name,
            suffix=suffix,
            icon=icon,
        )

        self._value_getter = value_getter
        self._attr_native_unit_of_measurement = native_unit_of_measurement
        self._attr_device_class = device_class

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        return self._value_getter(self)


class VasttrafikDepartureSensor(VasttrafikBaseSensor):
    """Represent the next departure."""

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
    ) -> None:
        """Initialize the next-departure sensor."""

        super().__init__(
            coordinator=coordinator,
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            name="Next departure",
            suffix="next_departure",
            icon="mdi:bus-clock",
        )

    @property
    def native_value(self) -> str | None:
        """Return the next departure time as HH:MM."""
        leg = self.next_leg
        if leg is None or leg.effective_departure_time is None:
            return None
        return leg.effective_departure_time.strftime("%H:%M")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return detailed information for upcoming departures."""
        departures = _departure_rows(self.coordinator)

        attributes: dict[str, Any] = {
            "origin": self.coordinator.origin_name,
            "destination": self.coordinator.destination_name,
            "departures": departures,
        }

        if departures:
            next_departure = departures[0]
            attributes.update(
                {
                    "next_departure": next_departure["time"],
                    "minutes_until": next_departure["minutes_until"],
                    "line": next_departure["line"],
                    "direction": next_departure["direction"],
                    "line_destination": next_departure["line_destination"],
                    "transport_mode": next_departure["transport_mode"],
                    "platform": next_departure["platform"],
                    "delay_minutes": next_departure["delay_minutes"],
                    "cancelled": next_departure["cancelled"],
                    "number_of_changes": next_departure["number_of_changes"],
                    "travel_duration": next_departure["travel_duration"],
                }
            )

        return attributes


class VasttrafikMinutesUntilSensor(VasttrafikBaseSensor):
    """Represent minutes until the next departure."""

    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_device_class = SensorDeviceClass.DURATION

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
    ) -> None:
        """Initialize the minutes-until-departure sensor."""

        super().__init__(
            coordinator=coordinator,
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            name="Minutes until departure",
            suffix="minutes_until",
            icon="mdi:timer-outline",
        )

    @property
    def native_value(self) -> int | None:
        """Return minutes until the next departure."""
        leg = self.next_leg
        if leg is None:
            return None
        return self.minutes_until(leg.effective_departure_time)


class VasttrafikTransportModeSensor(VasttrafikBaseSensor):
    """Represent the transport mode."""

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
    ) -> None:
        """Initialize the transport-mode sensor."""

        super().__init__(
            coordinator=coordinator,
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            name="Transport mode",
            suffix="transport_mode",
            icon="mdi:transit-connection-variant",
        )

    @property
    def native_value(self) -> str | None:
        """Return a user-friendly transport mode."""
        leg = self.next_leg
        if leg is None or leg.transport_mode is None:
            return None

        mode = str(leg.transport_mode)
        return TRANSPORT_MODE_NAMES.get(
            mode.casefold(),
            mode.replace("_", " ").title(),
        )

    @property
    def icon(self) -> str:
        """Return an icon matching the current transport mode."""
        leg = self.next_leg
        if leg is None or leg.transport_mode is None:
            return "mdi:transit-connection-variant"

        return TRANSPORT_MODE_ICONS.get(
            str(leg.transport_mode).casefold(),
            "mdi:transit-connection-variant",
        )


class VasttrafikDelaySensor(VasttrafikBaseSensor):
    """Represent delay status."""

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
    ) -> None:
        """Initialize the delay sensor."""

        super().__init__(
            coordinator=coordinator,
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            name="Delay",
            suffix="delay",
            icon="mdi:clock-alert-outline",
        )

    @property
    def native_value(self) -> str | None:
        """Return a friendly delay status."""
        leg = self.next_leg
        if leg is None or leg.delay_minutes is None:
            return None

        delay = leg.delay_minutes
        if delay <= 0:
            return "On time"
        return f"{delay} min"


class VasttrafikDepartureBoardSensor(VasttrafikBaseSensor):
    """Represent a compact departure board."""

    def __init__(
        self,
        *,
        coordinator: VasttrafikRouteCoordinator,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
    ) -> None:
        """Initialize the departure-board sensor."""

        super().__init__(
            coordinator=coordinator,
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            name="Departure board",
            suffix="departure_board",
            icon="mdi:view-list-outline",
        )

    @property
    def native_value(self) -> int:
        """Return the number of available departure rows."""
        return len(_departure_rows(self.coordinator))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return structured departures for dashboards."""
        return {
            "origin": self.coordinator.origin_name,
            "destination": self.coordinator.destination_name,
            "departures": _departure_rows(self.coordinator),
        }


def _isoformat(value: datetime | None) -> str | None:
    """Return an ISO formatted datetime when available."""
    return value.isoformat() if value is not None else None


def _journey_duration_minutes(journey: Any) -> int | None:
    """Return total journey duration in whole minutes."""
    departure_time = journey.departure_time
    arrival_time = journey.arrival_time

    if departure_time is None or arrival_time is None:
        return None

    seconds = (arrival_time - departure_time).total_seconds()
    return max(0, round(seconds / 60))


def _departure_rows(coordinator: VasttrafikRouteCoordinator) -> list[dict[str, Any]]:
    """Build structured departure rows."""
    rows: list[dict[str, Any]] = []

    for journey in coordinator.data or []:
        if not journey.legs:
            continue

        leg = journey.legs[0]
        departure_time = leg.effective_departure_time
        mode = (
            str(leg.transport_mode)
            if leg.transport_mode is not None
            else None
        )

        rows.append(
            {
                "time": _isoformat(departure_time),
                "display_time": (
                    departure_time.strftime("%H:%M")
                    if departure_time is not None
                    else None
                ),
                "planned_time": _isoformat(leg.planned_departure_time),
                "estimated_time": _isoformat(leg.estimated_departure_time),
                "minutes_until": VasttrafikBaseSensor.minutes_until(
                    departure_time
                ),
                "line": leg.line_designation,
                "direction": leg.direction,
                "line_destination": leg.short_direction,
                "transport_mode": (
                    TRANSPORT_MODE_NAMES.get(
                        mode.casefold(),
                        mode.replace("_", " ").title(),
                    )
                    if mode is not None
                    else None
                ),
                "platform": leg.origin.platform if leg.origin else None,
                "delay_minutes": leg.delay_minutes,
                "cancelled": leg.cancelled,
                "number_of_changes": journey.number_of_changes,
                "travel_duration": _journey_duration_minutes(journey),
            }
        )

    return rows


def _travel_duration(sensor: VasttrafikSimpleSensor) -> int | None:
    """Return total duration of the configured journey."""
    journey = sensor.next_journey
    return _journey_duration_minutes(journey) if journey is not None else None


def _number_of_changes(sensor: VasttrafikSimpleSensor) -> int | None:
    """Return the number of changes."""
    journey = sensor.next_journey
    return journey.number_of_changes if journey is not None else None


def _line(sensor: VasttrafikSimpleSensor) -> str | None:
    """Return the first line used by the journey."""
    leg = sensor.next_leg
    return leg.line_designation if leg is not None else None


def _origin(sensor: VasttrafikSimpleSensor) -> str | None:
    """Return the configured origin."""
    return sensor.coordinator.origin_name


def _destination(sensor: VasttrafikSimpleSensor) -> str | None:
    """Return the configured destination."""
    return sensor.coordinator.destination_name


def _line_destination(sensor: VasttrafikSimpleSensor) -> str | None:
    """Return the destination displayed for the first line."""
    leg = sensor.next_leg
    return leg.short_direction if leg is not None else None


def _platform(sensor: VasttrafikSimpleSensor) -> str | None:
    """Return the departure platform."""
    leg = sensor.next_leg
    if leg is None or leg.origin is None:
        return None
    return leg.origin.platform
