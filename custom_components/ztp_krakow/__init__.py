"""The ZTP Krak\u00f3w integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from .const import (
    DOMAIN,
    CONF_STOP_ID,
    CONF_STOP_TYPE,
    CONF_MODE,
    CONF_LINE,
    MODE_STOP,
    MODE_LINE,
)
from .coordinator import ZtpKrakowCoordinator

PLATFORMS = [Platform.SENSOR, Platform.DEVICE_TRACKER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ZTP Krak\u00f3w from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    mode = entry.data.get(CONF_MODE, MODE_STOP)
    stop_type = entry.data.get(CONF_STOP_TYPE)

    if mode == MODE_STOP:
        identifier = entry.data.get(CONF_STOP_ID)
    else:
        identifier = entry.data.get(CONF_LINE)

    coordinator = ZtpKrakowCoordinator(hass, stop_type, mode, identifier)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    platforms_to_load = []
    if mode == MODE_STOP:
        platforms_to_load.append(Platform.SENSOR)
    else:
        platforms_to_load.append(Platform.DEVICE_TRACKER)

    await hass.config_entries.async_forward_entry_setups(entry, platforms_to_load)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    mode = entry.data.get(CONF_MODE, MODE_STOP)
    platforms_to_unload = (
        [Platform.SENSOR] if mode == MODE_STOP else [Platform.DEVICE_TRACKER]
    )

    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, platforms_to_unload
    ):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
