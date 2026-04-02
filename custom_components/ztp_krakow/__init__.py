"""The ZTP Krak\u00f3w integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import DOMAIN, CONF_STOP_ID, CONF_STOP_TYPE
from .coordinator import ZtpKrakowCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ZTP Krak\u00f3w from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    stop_id = entry.data[CONF_STOP_ID]
    stop_type = entry.data[CONF_STOP_TYPE]

    coordinator = ZtpKrakowCoordinator(hass, stop_id, stop_type)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
