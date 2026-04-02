"""Config flow for ZTP Kraków."""

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
    CONF_DIRECTION,
    CONF_MODE,
    MODE_STOP,
    MODE_LINE,
    STOP_TYPE_BUS,
    STOP_TYPE_TRAM,
    API_BUS_STOPS_URL,
    API_TRAM_STOPS_URL,
    API_BUS_ROUTES_URL,
    API_TRAM_ROUTES_URL,
)

_LOGGER = logging.getLogger(__name__)


class ZtpKrakowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZTP Kraków."""

    VERSION = 1

    def __init__(self):
        self.config_mode = None
        self.stop_type = None
        self.stops_dict = {}
        self.routes_dict = {}
        self.selected_stop_id = None
        self.selected_stop_name = None
        self.selected_line = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step to choose mode."""
        errors = {}

        if user_input is not None:
            self.config_mode = user_input[CONF_MODE]
            self.stop_type = user_input[CONF_STOP_TYPE]

            if self.config_mode == MODE_STOP:
                return await self.async_step_stop()
            else:
                return await self.async_step_line()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_MODE, default=MODE_STOP): vol.In(
                    {
                        MODE_STOP: "Przystanek (Odjazdy)",
                        MODE_LINE: "Linia (Pojazdy na mapie)",
                    }
                ),
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
            final_stop_id = manual_id if manual_id else stop_id

            if not final_stop_id:
                errors["base"] = "missing_stop_id"
            else:
                self.selected_stop_id = final_stop_id
                self.selected_stop_name = user_input.get(
                    CONF_STOP_NAME, self.stops_dict.get(final_stop_id, final_stop_id)
                )
                return await self.async_step_line_filter()

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

                        self.stops_dict = {
                            k: v
                            for k, v in sorted(
                                raw_dict.items(), key=lambda item: item[1]
                            )
                        }
            except Exception as e:
                _LOGGER.error("Error fetching stops: %s", e)

        if self.stops_dict:
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_STOP_ID): vol.In(self.stops_dict),
                }
            )
        else:
            data_schema = vol.Schema(
                {
                    vol.Required(CONF_STOP_NAME): str,
                    vol.Required("manual_stop_id"): str,
                }
            )
            errors["base"] = "cannot_connect_stops"

        return self.async_show_form(
            step_id="stop",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_line_filter(self, user_input=None):
        """Handle the step to select a line to filter."""
        errors = {}

        if user_input is not None:
            self.selected_line = user_input.get(CONF_LINE, "")

            if self.selected_line == "Wszystkie":
                self.selected_line = ""

            if self.selected_line:
                return await self.async_step_direction()
            else:
                return await self._create_stop_entry()

        if not self.routes_dict:
            session = async_get_clientsession(self.hass)
            url = (
                API_BUS_ROUTES_URL
                if self.stop_type == STOP_TYPE_BUS
                else API_TRAM_ROUTES_URL
            )

            try:
                async with async_timeout.timeout(10):
                    response = await session.get(url, ssl=False)
                    if response.status == 200:
                        data = await response.json()
                        routes_obj = data.get("routes", [])

                        self.routes_dict = {
                            r.get("name", ""): r.get("directions", [])
                            for r in routes_obj
                            if "name" in r
                        }
            except Exception as e:
                _LOGGER.error("Error fetching routes: %s", e)

        line_options = ["Wszystkie"]
        if self.routes_dict:
            line_options.extend(sorted(self.routes_dict.keys()))

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LINE, default="Wszystkie"): vol.In(line_options),
            }
        )

        return self.async_show_form(
            step_id="line_filter",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_direction(self, user_input=None):
        """Handle the step to select a direction."""
        errors = {}

        if user_input is not None:
            self.selected_direction = user_input.get(CONF_DIRECTION, "")

            if self.selected_direction == "Wszystkie":
                self.selected_direction = ""

            return await self._create_stop_entry()

        direction_options = ["Wszystkie"]
        if self.selected_line in self.routes_dict:
            dirs = self.routes_dict[self.selected_line]
            if dirs:
                direction_options.extend(dirs)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DIRECTION, default="Wszystkie"): vol.In(
                    direction_options
                ),
            }
        )

        return self.async_show_form(
            step_id="direction",
            data_schema=data_schema,
            errors=errors,
        )

    async def _create_stop_entry(self):
        """Finalize stop entry creation."""
        unique_id = f"stop_{self.stop_type}_{self.selected_stop_id}"
        if self.selected_line:
            unique_id += f"_{self.selected_line}"
            if hasattr(self, "selected_direction") and self.selected_direction:
                unique_id += f"_{self.selected_direction}"

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        title = f"{self.selected_stop_name}"
        if self.selected_line:
            title += f" (Linia {self.selected_line}"
            if hasattr(self, "selected_direction") and self.selected_direction:
                title += f" kier. {self.selected_direction}"
            title += ")"

        data = {
            CONF_MODE: MODE_STOP,
            CONF_STOP_TYPE: self.stop_type,
            CONF_STOP_ID: self.selected_stop_id,
            CONF_STOP_NAME: self.selected_stop_name,
            CONF_LINE: self.selected_line,
            CONF_DIRECTION: getattr(self, "selected_direction", ""),
        }

        return self.async_create_entry(title=title, data=data)

    async def async_step_line(self, user_input=None):
        """Handle the step to select a line for tracking."""
        errors = {}

        if user_input is not None:
            line = user_input.get(CONF_LINE, "").strip()

            if not line:
                errors["base"] = "missing_line"
            else:
                unique_id = f"line_{self.stop_type}_{line}"

                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                title = f"Linia {line} ({'Autobus' if self.stop_type == STOP_TYPE_BUS else 'Tramwaj'})"

                data = {
                    CONF_MODE: MODE_LINE,
                    CONF_STOP_TYPE: self.stop_type,
                    CONF_LINE: line,
                }

                return self.async_create_entry(title=title, data=data)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LINE): str,
            }
        )

        return self.async_show_form(
            step_id="line",
            data_schema=data_schema,
            errors=errors,
        )
