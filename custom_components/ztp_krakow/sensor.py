"""Sensor platform for ZTP Krak\u00f3w."""

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from datetime import timedelta
import homeassistant.util.dt as dt_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_STOP_NAME, CONF_STOP_ID, CONF_STOP_TYPE, CONF_LINE


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ZTP Krak\u00f3w sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    stop_name = entry.data.get(CONF_STOP_NAME)
    stop_id = entry.data.get(CONF_STOP_ID)
    stop_type = entry.data.get(CONF_STOP_TYPE)
    line = entry.data.get(CONF_LINE, "")

    async_add_entities(
        [ZtpKrakowStopSensor(coordinator, stop_name, stop_id, stop_type, line)]
    )


class ZtpKrakowStopSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ZTP Krak\u00f3w Stop sensor."""

    def __init__(self, coordinator, stop_name, stop_id, stop_type, line):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._stop_name = stop_name
        self._stop_id = stop_id
        self._stop_type = stop_type
        self._line = line

        self._attr_name = f"Przystanek {stop_name}"
        if self._line:
            self._attr_name += f" (Linia {self._line})"

        self._attr_unique_id = (
            f"ztp_krakow_{stop_type}_{stop_id}_{self._line}"
            if self._line
            else f"ztp_krakow_{stop_type}_{stop_id}"
        )
        self._attr_icon = "mdi:bus" if stop_type == "bus" else "mdi:tram"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP

    def _get_filtered_departures(self):
        """Filter departures by line if configured."""
        if not self.coordinator.data or "actual" not in self.coordinator.data:
            return []

        deps = self.coordinator.data["actual"]

        if self._line:
            line_str = str(self._line).strip().lower()
            deps = [
                d
                for d in deps
                if str(d.get("patternText", "")).strip().lower() == line_str
            ]

        return deps

    @property
    def native_value(self):
        """Return the state of the sensor (time to next departure)."""
        deps = self._get_filtered_departures()
        if not deps:
            return None

        first_dep = deps[0]
        # API zwraca actualRelativeTime w sekundach od teraz
        rel_time = first_dep.get("actualRelativeTime")
        if rel_time is not None:
            return dt_util.utcnow() + timedelta(seconds=rel_time)
            
        return None

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        deps = self._get_filtered_departures()
        if not deps:
            return {"departures": []}

        status_map = {
            "PREDICTED": "na \u017cywo",
            "PLANNED": "wed\u0142ug rozk\u0142adu",
            "STOPPING": "na przystanku",
            "DEPARTED": "odjecha\u0142",
        }

        departures = []
        for dep in deps:
            mixed_time = dep.get("mixedTime", "").replace(" %UNIT_MIN%", " min")
            raw_status = dep.get("status", "")

            departures.append(
                {
                    "line": dep.get("patternText", ""),
                    "direction": dep.get("direction", ""),
                    "time": dep.get("actualTime", ""),
                    "minutes": mixed_time,
                    "status": status_map.get(raw_status, raw_status),
                }
            )

        return {"departures": departures}
