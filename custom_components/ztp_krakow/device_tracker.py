"""Device tracker platform for ZTP Krak\u00f3w."""

from homeassistant.components.device_tracker import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_LINE, CONF_STOP_TYPE


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ZTP Krak\u00f3w device trackers."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    line = entry.data.get(CONF_LINE)
    stop_type = entry.data.get(CONF_STOP_TYPE)

    # For device trackers, we actually want to create an entity for EVERY vehicle.
    # Since they come and go, we can handle it by dynamically adding entities
    # when the coordinator updates, but for simplicity we will start by adding
    # currently known vehicles and let a listener handle new ones.

    tracked_vehicles = set()

    def async_update_vehicles():
        """Update tracking entities."""
        if not coordinator.data or "vehicles" not in coordinator.data:
            return

        new_vehicles = []
        for vehicle in coordinator.data["vehicles"]:
            v_id = vehicle.get("id")
            if v_id and v_id not in tracked_vehicles:
                tracked_vehicles.add(v_id)
                new_vehicles.append(
                    ZtpKrakowVehicle(coordinator, v_id, line, stop_type)
                )

        if new_vehicles:
            async_add_entities(new_vehicles)

    # Initial load
    async_update_vehicles()

    # Listen for new vehicles on coordinator updates
    entry.async_on_unload(coordinator.async_add_listener(async_update_vehicles))


class ZtpKrakowVehicle(CoordinatorEntity, TrackerEntity):
    """Representation of a ZTP Krak\u00f3w vehicle on map."""

    def __init__(self, coordinator, vehicle_id, line, stop_type):
        """Initialize the tracker."""
        super().__init__(coordinator)
        self._vehicle_id = vehicle_id
        self._line = line
        self._stop_type = stop_type

        self._attr_unique_id = f"ztp_krakow_vehicle_{self._vehicle_id}"
        self._attr_icon = "mdi:bus" if stop_type == "bus" else "mdi:tram"
        self._attr_name = f"{'Autobus' if stop_type == 'bus' else 'Tramwaj'} {line}"

    @property
    def _vehicle_data(self):
        """Get the current data for this vehicle."""
        if not self.coordinator.data or "vehicles" not in self.coordinator.data:
            return None

        for v in self.coordinator.data["vehicles"]:
            if v.get("id") == self._vehicle_id:
                return v
        return None

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        data = self._vehicle_data
        if data and "latitude" in data:
            return data["latitude"] / 3600000.0
        return None

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        data = self._vehicle_data
        if data and "longitude" in data:
            return data["longitude"] / 3600000.0
        return None

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        data = self._vehicle_data
        if not data:
            return {}

        return {
            "name": data.get("name", ""),
            "heading": data.get("heading", ""),
            "category": data.get("category", ""),
        }
