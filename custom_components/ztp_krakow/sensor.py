"""Sensor platform for ZTP Kraków."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_STOP_NAME, CONF_STOP_ID, CONF_STOP_TYPE


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ZTP Kraków sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    stop_name = entry.data[CONF_STOP_NAME]
    stop_id = entry.data[CONF_STOP_ID]
    stop_type = entry.data[CONF_STOP_TYPE]

    async_add_entities(
        [ZtpKrakowStopSensor(coordinator, stop_name, stop_id, stop_type)]
    )


class ZtpKrakowStopSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ZTP Kraków Stop sensor."""

    def __init__(self, coordinator, stop_name, stop_id, stop_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._stop_name = stop_name
        self._stop_id = stop_id
        self._stop_type = stop_type

        self._attr_name = f"Przystanek {stop_name}"
        self._attr_unique_id = f"ztp_krakow_{stop_type}_{stop_id}"
        self._attr_icon = "mdi:bus" if stop_type == "bus" else "mdi:tram"
        self._attr_native_unit_of_measurement = "min"

    @property
    def native_value(self):
        """Return the state of the sensor (time to next departure)."""
        if not self.coordinator.data or "actual" not in self.coordinator.data:
            return None

        actual_departures = self.coordinator.data["actual"]
        if not actual_departures:
            return None

        for dep in actual_departures:
            mixed_time = dep.get("mixedTime", "")
            if "%UNIT_MIN%" in mixed_time:
                minutes_str = mixed_time.split(" ")[0]
                try:
                    return int(minutes_str)
                except ValueError:
                    pass
            elif mixed_time == "":
                # Could be departures right now. e.g., "0 min" usually has %UNIT_MIN% but maybe some don't.
                pass
        return None

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        if not self.coordinator.data or "actual" not in self.coordinator.data:
            return {"departures": []}

        departures = []
        for dep in self.coordinator.data["actual"]:
            mixed_time = dep.get("mixedTime", "").replace(" %UNIT_MIN%", " min")

            departures.append(
                {
                    "line": dep.get("patternText", ""),
                    "direction": dep.get("direction", ""),
                    "time": dep.get("actualTime", ""),
                    "minutes": mixed_time,
                    "status": dep.get("status", ""),
                }
            )

        return {"departures": departures}
