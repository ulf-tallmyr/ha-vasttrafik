"""Sensors for Västtrafik Departures."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VasttrafikRouteCoordinator
from .entity import VasttrafikEntityMixin
from .helpers import departure_rows, journey_duration_minutes
from .icons import transport_mode_icon, transport_mode_state


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Västtrafik route sensors."""

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
            name=coordinator.route_name or subentry.title,
            manufacturer="Västtrafik",
            model="Route",
        )

        route_entities: list[SensorEntity] = []

        common = {
            "coordinator": coordinator,
            "entry": entry,
            "subentry_id": subentry.subentry_id,
            "device_entry": device_entry,
        }

        route_entities.extend(
            [
                VasttrafikDepartureSensor(**common),
                VasttrafikMinutesUntilSensor(**common),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="from",
                    translation_key="from",
                    icon="mdi:map-marker-outline",
                    value_getter=_origin,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="destination",
                    translation_key="destination",
                    icon="mdi:map-marker",
                    value_getter=_destination,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="line_destination",
                    translation_key="line_destination",
                    icon="mdi:sign-direction",
                    value_getter=_line_destination,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="travel_duration",
                    translation_key="travel_duration",
                    icon="mdi:clock-outline",
                    value_getter=_travel_duration,
                    native_unit_of_measurement=UnitOfTime.MINUTES,
                    device_class=SensorDeviceClass.DURATION,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="number_of_changes",
                    translation_key="number_of_changes",
                    icon="mdi:swap-horizontal",
                    value_getter=_number_of_changes,
                ),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="line",
                    translation_key="line",
                    icon="mdi:bus",
                    value_getter=_line,
                ),
                VasttrafikTransportModeSensor(**common),
                VasttrafikSimpleSensor(
                    **common,
                    suffix="platform",
                    translation_key="platform",
                    icon="mdi:sign-real-estate",
                    value_getter=_platform,
                ),
                VasttrafikDelaySensor(**common),
                VasttrafikStatusSensor(**common),
                VasttrafikDepartureBoardSensor(**common),
            ]
        )

        async_add_entities(
            route_entities,
            config_subentry_id=subentry.subentry_id,
        )


class VasttrafikBaseSensor(
    VasttrafikEntityMixin,
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
        suffix: str,
        translation_key: str,
        icon: str,
    ) -> None:
        """Initialize a Västtrafik sensor."""
        super().__init__(coordinator)
        self._init_vasttrafik_entity(
            entry=entry,
            subentry_id=subentry_id,
            device_entry=device_entry,
            suffix=suffix,
            translation_key=translation_key,
        )
        self._attr_icon = icon


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
        suffix: str,
        translation_key: str,
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
            suffix=suffix,
            translation_key=translation_key,
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

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            **kwargs,
            suffix="next_departure",
            translation_key="next_departure",
            icon="mdi:bus-clock",
        )

    @property
    def native_value(self) -> str | None:
        leg = self.next_leg
        if leg is None or leg.effective_departure_time is None:
            return None
        return leg.effective_departure_time.strftime("%H:%M")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        departures = departure_rows(self.coordinator, self.minutes_until)
        return {
            "origin": self.coordinator.origin_name,
            "destination": self.coordinator.destination_name,
            "route_name": self.coordinator.route_name,
            "departures": departures,
            **(departures[0] if departures else {}),
        }


class VasttrafikMinutesUntilSensor(VasttrafikBaseSensor):
    """Represent minutes until the next departure."""

    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_device_class = SensorDeviceClass.DURATION

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            **kwargs,
            suffix="minutes_until",
            translation_key="minutes_until",
            icon="mdi:timer-outline",
        )

    @property
    def native_value(self) -> int | None:
        leg = self.next_leg
        return (
            self.minutes_until(leg.effective_departure_time)
            if leg is not None
            else None
        )


class VasttrafikTransportModeSensor(VasttrafikBaseSensor):
    """Represent the transport mode."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            **kwargs,
            suffix="transport_mode",
            translation_key="transport_mode",
            icon="mdi:transit-connection-variant",
        )

    @property
    def native_value(self) -> str | None:
        leg = self.next_leg
        return transport_mode_state(
            leg.transport_mode if leg is not None else None
        )

    @property
    def icon(self) -> str:
        leg = self.next_leg
        return transport_mode_icon(
            leg.transport_mode if leg is not None else None
        )


class VasttrafikDelaySensor(VasttrafikBaseSensor):
    """Represent delay in minutes."""

    _attr_native_unit_of_measurement = UnitOfTime.MINUTES

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            **kwargs,
            suffix="delay",
            translation_key="delay",
            icon="mdi:clock-alert-outline",
        )

    @property
    def native_value(self) -> int | None:
        leg = self.next_leg
        return leg.delay_minutes if leg is not None else None


class VasttrafikStatusSensor(VasttrafikBaseSensor):
    """Represent next departure status."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            **kwargs,
            suffix="status",
            translation_key="status",
            icon="mdi:traffic-light",
        )

    @property
    def native_value(self) -> str | None:
        leg = self.next_leg
        if leg is None:
            return None
        if leg.cancelled:
            return "cancelled"
        if (leg.delay_minutes or 0) > 0:
            return "delayed"
        return "on_time"


class VasttrafikDepartureBoardSensor(VasttrafikBaseSensor):
    """Represent a departure board."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            **kwargs,
            suffix="departure_board",
            translation_key="departure_board",
            icon="mdi:view-list-outline",
        )

    @property
    def native_value(self) -> int:
        return len(departure_rows(self.coordinator, self.minutes_until))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "route_name": self.coordinator.route_name,
            "origin": self.coordinator.origin_name,
            "destination": self.coordinator.destination_name,
            "refresh_interval": self.coordinator.refresh_interval,
            "departures": departure_rows(
                self.coordinator,
                self.minutes_until,
            ),
        }


def _travel_duration(sensor: VasttrafikSimpleSensor) -> int | None:
    journey = sensor.next_journey
    return journey_duration_minutes(journey) if journey is not None else None


def _number_of_changes(sensor: VasttrafikSimpleSensor) -> int | None:
    journey = sensor.next_journey
    return journey.number_of_changes if journey is not None else None


def _line(sensor: VasttrafikSimpleSensor) -> str | None:
    leg = sensor.next_leg
    return leg.line_designation if leg is not None else None


def _origin(sensor: VasttrafikSimpleSensor) -> str | None:
    return sensor.coordinator.origin_name


def _destination(sensor: VasttrafikSimpleSensor) -> str | None:
    return sensor.coordinator.destination_name


def _line_destination(sensor: VasttrafikSimpleSensor) -> str | None:
    leg = sensor.next_leg
    return leg.short_direction if leg is not None else None


def _platform(sensor: VasttrafikSimpleSensor) -> str | None:
    leg = sensor.next_leg
    if leg is None or leg.origin is None:
        return None
    return leg.origin.platform
