"""Subentry flow for Västtrafik routes."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigSubentryFlow,
    SubentryFlowResult,
)

from pyvasttrafik import VasttrafikClient

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_DESTINATION_NAME,
    CONF_ORIGIN,
    CONF_ORIGIN_NAME,
    CONF_ROUTE_NAME,
    CONF_TOWARDS,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
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
        errors: dict[str, str] = {}

        if user_input is not None:
            locations = await self._search_locations(user_input["search"])
            if not locations:
                errors["base"] = "no_stops_found"
            else:
                self._origin_results = {
                    location.gid: location.name for location in locations
                }
                return await self.async_step_origin_select()

        return self.async_show_form(
            step_id="origin_search",
            data_schema=vol.Schema({vol.Required("search"): str}),
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
                {vol.Required(CONF_ORIGIN): vol.In(self._origin_results)}
            ),
        )

    async def async_step_destination_search(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Search for destination stop."""
        errors: dict[str, str] = {}

        if user_input is not None:
            locations = await self._search_locations(user_input["search"])
            if not locations:
                errors["base"] = "no_stops_found"
            else:
                self._destination_results = {
                    location.gid: location.name for location in locations
                }
                return await self.async_step_destination_select()

        return self.async_show_form(
            step_id="destination_search",
            data_schema=vol.Schema({vol.Required("search"): str}),
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
            return await self.async_step_route_settings()

        return self.async_show_form(
            step_id="destination_select",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TOWARDS): vol.In(
                        self._destination_results
                    )
                }
            ),
        )

    async def async_step_route_settings(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> SubentryFlowResult:
        """Configure route display name and refresh interval."""
        default_title = f"{self._origin_name} → {self._destination_name}"

        if user_input is not None:
            route_name = user_input.get(CONF_ROUTE_NAME) or default_title
            return self.async_create_entry(
                title=route_name,
                data={
                    CONF_ORIGIN: self._origin_gid,
                    CONF_ORIGIN_NAME: self._origin_name,
                    CONF_TOWARDS: self._destination_gid,
                    CONF_DESTINATION_NAME: self._destination_name,
                    CONF_ROUTE_NAME: route_name,
                    CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL],
                },
            )

        return self.async_show_form(
            step_id="route_settings",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_ROUTE_NAME,
                        default=default_title,
                    ): str,
                    vol.Required(
                        CONF_UPDATE_INTERVAL,
                        default=DEFAULT_UPDATE_INTERVAL,
                    ): vol.In([30, 60, 120, 300]),
                }
            ),
        )

    async def _search_locations(self, query: str):
        """Search Västtrafik stop areas."""
        config_entry = self._get_entry()
        async with VasttrafikClient(
            config_entry.data[CONF_CLIENT_ID],
            config_entry.data[CONF_CLIENT_SECRET],
        ) as client:
            return await client.search_locations(
                query,
                location_types={"stoparea"},
            )
