"""Config flow for ZTP Krak\u00f3w."""

import voluptuous as vol
import aiohttp
import async_timeout
import logging

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    CONF_STOP_TYPE,
    CONF_LINE,
    STOP_TYPE_BUS,
    STOP_TYPE_TRAM,
    API_BUS_STOPS_URL,
    API_TRAM_STOPS_URL,
)

_LOGGER = logging.getLogger(__name__)


class ZtpKrakowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZTP Krak\u00f3w."""

    VERSION = 1

    def __init__(self):
        self.stop_type = None
        self.stops_dict = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step to choose stop type."""
        errors = {}

        if user_input is not None:
            self.stop_type = user_input[CONF_STOP_TYPE]
            return await self.async_step_stop()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_STOP_TYPE, default=STOP_TYPE_BUS): vol.In(
                    {
                        STOP_TYPE_BUS: "Autobus",
                        STOP_TYPE_TRAM: "Tramwaj",
                    }
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_stop(self, user_input=None):
        """Handle the step to select a stop from the list."""
        errors = {}

        if user_input is not None:
            stop_id = user_input.get(CONF_STOP_ID, "")
            manual_id = user_input.get("manual_stop_id", "")

            # Use manual ID if provided, otherwise the dropdown one
            final_stop_id = manual_id if manual_id else stop_id

            if not final_stop_id:
                errors["base"] = "missing_stop_id"
            else:
                stop_name = user_input.get(
                    CONF_STOP_NAME, self.stops_dict.get(final_stop_id, final_stop_id)
                )
                line = user_input.get(CONF_LINE, "")

                unique_id = f"{self.stop_type}_{final_stop_id}"
                if line:
                    unique_id += f"_{line}"

                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                title = f"{stop_name}"
                if line:
                    title += f" (Linia {line})"

                data = {
                    CONF_STOP_TYPE: self.stop_type,
                    CONF_STOP_ID: final_stop_id,
                    CONF_STOP_NAME: stop_name,
                    CONF_LINE: line,
                }

                return self.async_create_entry(title=title, data=data)

        # Try to fetch stops for the dropdown
        if not self.stops_dict:
            session = async_get_clientsession(self.hass)
            url = (
                API_BUS_STOPS_URL
                if self.stop_type == STOP_TYPE_BUS
                else API_TRAM_STOPS_URL
            )

            try:
                async with async_timeout.timeout(10):
                    response = await session.get(url, ssl=False)
                    if response.status == 200:
                        data = await response.json()
                        stops_obj = data.get("stops", [])

                        raw_dict = {}
                        for stop in stops_obj:
                            s_id = stop.get("shortName")
                            if s_id:
                                raw_dict[s_id] = (
                                    f"{stop.get('name', 'Nieznany')} ({s_id})"
                                )

                        # Sort alphabetically by name
                        self.stops_dict = {
                            k: v
                            for k, v in sorted(
                                raw_dict.items(), key=lambda item: item[1]
                            )
                        }
            except Exception as e:
                _LOGGER.error("Error fetching stops: %s", e)
                # Fallback to empty dict

        if self.stops_dict:
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_STOP_ID): vol.In(self.stops_dict),
                    vol.Optional(CONF_LINE, default=""): str,
                }
            )
        else:
            # Fallback manual schema
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_STOP_NAME): str,
                    vol.Required("manual_stop_id"): str,
                    vol.Optional(CONF_LINE, default=""): str,
                }
            )
            errors["base"] = "cannot_connect_stops"

        return self.async_show_form(
            step_id="stop",
            data_schema=data_schema,
            errors=errors,
        )
