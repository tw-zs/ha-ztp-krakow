"""Config flow for ZTP Kraków."""

import voluptuous as vol
from homeassistant import config_entries
from .const import (
    DOMAIN,
    CONF_STOP_ID,
    CONF_STOP_NAME,
    CONF_STOP_TYPE,
    STOP_TYPE_BUS,
    STOP_TYPE_TRAM,
)


class ZtpKrakowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZTP Kraków."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_STOP_TYPE]}_{user_input[CONF_STOP_ID]}"
            )
            self._abort_if_unique_id_configured()

            title = f"{user_input[CONF_STOP_NAME]} ({user_input[CONF_STOP_ID]})"
            return self.async_create_entry(title=title, data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_STOP_NAME): str,
                vol.Required(CONF_STOP_ID): str,
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
