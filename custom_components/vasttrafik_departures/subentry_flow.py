"""Subentry flow for Västtrafik routes."""

from __future__ import annotations

import logging
from typing import Any

from hass_nabucasa import _LOGGER
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigSubentryFlow,
    SubentryFlowResult,
)

from pyvasttrafik import VasttrafikClient

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_ORIGIN,
    CONF_TOWARDS,
)


class RouteSubentryFlowHandler(ConfigSubentryFlow):
    """Handle adding a Västtrafik route."""

    def __init__(self) -> None:
        """Initialize route flow."""
        self._origin_results: dict[str, str] = {}
        self._destination_results: dict[str, str] = {}

        self._origin_gid: str | None = None
        self._origin_name: str | None = None

        self._destination_gid: str | None = None
        self._destination_name: str | None = None

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Start adding a route."""

        return await self.async_step_origin_search()

    async def async_step_origin_search(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Search for origin stop."""

        _LOGGER.warning("ORIGIN SEARCH STARTED")

        errors: dict[str, str] = {}

        if user_input is not None:
            query = user_input["search"]

            config_entry = self._get_entry()

            client_id = config_entry.data[CONF_CLIENT_ID]
            client_secret = config_entry.data[CONF_CLIENT_SECRET]

            async with VasttrafikClient(
                client_id,
                client_secret,
            ) as client:
                locations = await client.search_locations(
                    query,
                    location_types={"stoparea"},
                )

            if not locations:
                errors["base"] = "no_stops_found"
            else:
                self._origin_search = query
                self._origin_results = {
                    location.gid: location.name
                    for location in locations
                }

                return await self.async_step_origin_select()

        return self.async_show_form(
            step_id="origin_search",
            data_schema=vol.Schema(
                {
                    vol.Required("search"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_origin_select(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Select origin stop."""

        if user_input is not None:
            self._origin_gid = user_input[CONF_ORIGIN]
            self._origin_name = self._origin_results[self._origin_gid]

            return await self.async_step_destination_search()

        return self.async_show_form(
            step_id="origin_select",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ORIGIN): vol.In(
                        self._origin_results
                    ),
                }
            ),
        )
    async def async_step_destination_search(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Search for destination stop."""

        errors: dict[str, str] = {}

        if user_input is not None:
            query = user_input["search"]

            config_entry = self._get_entry()

            client_id = config_entry.data[CONF_CLIENT_ID]
            client_secret = config_entry.data[CONF_CLIENT_SECRET]

            async with VasttrafikClient(
                client_id,
                client_secret,
            ) as client:
                locations = await client.search_locations(
                    query,
                    location_types={"stoparea"},
                )

            if not locations:
                errors["base"] = "no_stops_found"
            else:
                self._destination_results = {
                    location.gid: location.name
                    for location in locations
                }

                return await self.async_step_destination_select()

        return self.async_show_form(
            step_id="destination_search",
            data_schema=vol.Schema(
                {
                    vol.Required("search"): str,
                }
            ),
            errors=errors,
        )
    async def async_step_destination_select(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Select destination stop."""

        if user_input is not None:
            self._destination_gid = user_input[CONF_TOWARDS]
            self._destination_name = self._destination_results[
                self._destination_gid
            ]

            return self.async_create_entry(
                title=f"{self._origin_name} → {self._destination_name}",
                data={
                    CONF_ORIGIN: self._origin_gid,
                    CONF_TOWARDS: self._destination_gid,
                },
            )

        return self.async_show_form(
            step_id="destination_select",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TOWARDS): vol.In(
                        self._destination_results
                    ),
                }
            ),
        )