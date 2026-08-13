"""Shared entity helpers for Västtrafik Departures."""

from __future__ import annotations

from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.util import dt as dt_util

from .coordinator import VasttrafikRouteCoordinator


class VasttrafikEntityMixin:
    """Shared helpers for Västtrafik entities."""

    coordinator: VasttrafikRouteCoordinator

    def _init_vasttrafik_entity(
        self,
        *,
        entry: ConfigEntry,
        subentry_id: str,
        device_entry: dr.DeviceEntry,
        suffix: str,
        translation_key: str,
    ) -> None:
        """Initialize common entity metadata."""
        self.device_entry = device_entry
        self._attr_unique_id = f"{entry.entry_id}_{subentry_id}_{suffix}"
        self._attr_has_entity_name = True
        self._attr_translation_key = translation_key

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
