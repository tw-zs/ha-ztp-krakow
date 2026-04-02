"""Data update coordinator for ZTP Kraków."""

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
    API_BUS_VEHICLES_URL,
    API_TRAM_VEHICLES_URL,
    STOP_TYPE_BUS,
    DEFAULT_UPDATE_INTERVAL,
    MODE_STOP,
    MODE_LINE,
)

_LOGGER = logging.getLogger(__name__)


class ZtpKrakowCoordinator(DataUpdateCoordinator):
    """Class to manage fetching ZTP Krakow data."""

    def __init__(
        self, hass: HomeAssistant, stop_type: str, mode: str, identifier: str
    ) -> None:
        """Initialize."""
        self.stop_type = stop_type
        self.mode = mode
        self.identifier = identifier

        if mode == MODE_STOP:
            if stop_type == STOP_TYPE_BUS:
                self.api_url = API_BUS_URL.format(stop_id=identifier)
            else:
                self.api_url = API_TRAM_URL.format(stop_id=identifier)
        else:
            if stop_type == STOP_TYPE_BUS:
                self.api_url = API_BUS_VEHICLES_URL
            else:
                self.api_url = API_TRAM_VEHICLES_URL

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

                # If we are in line mode, we fetch ALL vehicles, but we should filter them
                # here so we don't store 1000 vehicles in HA state unnecessarily
                if self.mode == MODE_LINE:
                    vehicles = data.get("vehicles", [])
                    # The name usually looks like "192 Dworzec Główny Wschód"
                    # We look for vehicles whose name starts with "LINE "
                    line_prefix = f"{self.identifier} "
                    filtered = [
                        v
                        for v in vehicles
                        if str(v.get("name", "")).startswith(line_prefix)
                        and not v.get("isDeleted")
                    ]
                    return {"vehicles": filtered}

                return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
