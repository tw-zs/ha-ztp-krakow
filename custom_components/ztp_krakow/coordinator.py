"""Data update coordinator for ZTP Krak\u00f3w."""

from datetime import timedelta
import logging
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    DOMAIN,
    API_BUS_URL,
    API_TRAM_URL,
    STOP_TYPE_BUS,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class ZtpKrakowCoordinator(DataUpdateCoordinator):
    """Class to manage fetching ZTP Krakow data."""

    def __init__(self, hass: HomeAssistant, stop_id: str, stop_type: str) -> None:
        """Initialize."""
        self.stop_id = stop_id
        self.stop_type = stop_type

        if stop_type == STOP_TYPE_BUS:
            self.api_url = API_BUS_URL.format(stop_id=stop_id)
        else:
            self.api_url = API_TRAM_URL.format(stop_id=stop_id)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            session = async_get_clientsession(self.hass)
            # Disable SSL verification as their certificates are sometimes problematic
            async with async_timeout.timeout(10):
                response = await session.get(self.api_url, ssl=False)
                response.raise_for_status()
                data = await response.json()
                return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
