"""Data coordinator for Västtrafik Departures."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from pyvasttrafik import VasttrafikClient
from pyvasttrafik.exceptions import (
    VasttrafikAuthenticationError,
    VasttrafikConnectionError,
    VasttrafikResponseError,
)

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    DEFAULT_NUMBER_OF_DEPARTURES,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class VasttrafikRouteCoordinator(DataUpdateCoordinator):
    """Fetch journeys for one configured route."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        *,
        origin_gid: str,
        destination_gid: str,
        origin_name: str | None = None,
        destination_name: str | None = None,
        route_name: str | None = None,
        update_interval: int = DEFAULT_UPDATE_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""

        self._client = VasttrafikClient(
            config_entry.data[CONF_CLIENT_ID],
            config_entry.data[CONF_CLIENT_SECRET],
        )

        self._origin_gid = origin_gid
        self._destination_gid = destination_gid
        self.origin_name = origin_name
        self.destination_name = destination_name
        self.route_name = route_name
        self.refresh_interval = update_interval

        super().__init__(
            hass,
            _LOGGER,
            name=route_name or f"Västtrafik {origin_gid} → {destination_gid}",
            config_entry=config_entry,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        """Fetch upcoming journeys."""
        try:
            return await self._client.get_journeys(
                self._origin_gid,
                self._destination_gid,
                limit=DEFAULT_NUMBER_OF_DEPARTURES,
            )
        except VasttrafikAuthenticationError as err:
            raise UpdateFailed(
                "Västtrafik authentication failed"
            ) from err
        except (
            VasttrafikConnectionError,
            VasttrafikResponseError,
        ) as err:
            raise UpdateFailed(
                f"Error communicating with Västtrafik: {err}"
            ) from err

    async def async_shutdown(self) -> None:
        """Close the Västtrafik API client."""
        await self._client.close()
