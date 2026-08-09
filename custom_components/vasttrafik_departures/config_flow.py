"""Config flow for the Västtrafik integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from pyvasttrafik import VasttrafikClient
from pyvasttrafik.exceptions import (
    VasttrafikAuthenticationError,
    VasttrafikConnectionError,
    VasttrafikResponseError,
)

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_ORIGIN,
    CONF_TOWARDS,
    DOMAIN,
)


class VasttrafikConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._client_id: str | None = None
        self._client_secret: str | None = None

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle Västtrafik API credentials."""

        errors: dict[str, str] = {}

        if user_input is not None:
            client_id = user_input[CONF_CLIENT_ID]
            client_secret = user_input[CONF_CLIENT_SECRET]

            try:
                async with VasttrafikClient(
                    client_id,
                    client_secret,
                ) as client:
                    await client.authenticate()

            except VasttrafikAuthenticationError:
                errors["base"] = "invalid_auth"

            except (
                VasttrafikConnectionError,
                VasttrafikResponseError,
            ):
                errors["base"] = "cannot_connect"

            else:
                self._client_id = client_id
                self._client_secret = client_secret

                return await self.async_step_route()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CLIENT_ID): str,
                    vol.Required(CONF_CLIENT_SECRET): str,
                }
            ),
            errors=errors,
        )

    async def async_step_route(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Configure the route."""

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_CLIENT_ID: self._client_id,
                    CONF_CLIENT_SECRET: self._client_secret,
                    CONF_NAME: user_input[CONF_NAME],
                    CONF_ORIGIN: user_input[CONF_ORIGIN],
                    CONF_TOWARDS: user_input[CONF_TOWARDS],
                },
            )

        return self.async_show_form(
            step_id="route",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default="Västtrafik",
                    ): str,
                    vol.Required(CONF_ORIGIN): str,
                    vol.Required(CONF_TOWARDS): str,
                }
            ),
        )