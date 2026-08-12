"""Binary sensors for Västtrafik Departures."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VasttrafikRouteCoordinator
from .entity import VasttrafikEntityMixin


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    """Set up Västtrafik binary sensors."""
    entities: list[BinarySensorEntity] = []
    device_registry = dr.async_get(hass)

    for subentry in entry.subentries.values():
        if subentry.subentry_type != "route":
            continue

        coordinator = hass.data[DOMAIN][entry.entry_id]["coordinators"].get(subentry.subentry_id)
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

        entities.append(VasttrafikCancelledBinarySensor(coordinator=coordinator, entry=entry, subentry_id=subentry.subentry_id, device_entry=device_entry))

    async_add_entities(entities)


class VasttrafikCancelledBinarySensor(
    VasttrafikEntityMixin,
    CoordinatorEntity[VasttrafikRouteCoordinator],
    BinarySensorEntity,
):
    """Represent whether the next journey is cancelled."""

    _attr_name = "Cancelled"
    _attr_icon = "mdi:cancel"

    def __init__(self, *, coordinator: VasttrafikRouteCoordinator, entry: ConfigEntry, subentry_id: str, device_entry: dr.DeviceEntry) -> None:
        super().__init__(coordinator)
        self._init_vasttrafik_entity(entry=entry, subentry_id=subentry_id, device_entry=device_entry, suffix="cancelled")

    @property
    def is_on(self) -> bool | None:
        journey = self.next_journey
        if journey is None or not journey.legs:
            return None
        return any(leg.cancelled for leg in journey.legs)
