"""Constants for the ZTP Kraków integration."""

DOMAIN = "ztp_krakow"
CONF_STOP_ID = "stop_id"
CONF_STOP_NAME = "stop_name"
CONF_STOP_TYPE = "stop_type"
CONF_LINE = "line"
CONF_DIRECTION = "direction"
CONF_MODE = "mode"

MODE_STOP = "stop"
MODE_LINE = "line"

STOP_TYPE_BUS = "bus"
STOP_TYPE_TRAM = "tram"

API_BUS_URL = "https://ttss.mpk.krakow.pl/internetservice/services/passageInfo/stopPassages/stop?stop={stop_id}"
API_TRAM_URL = "http://www.ttss.krakow.pl/internetservice/services/passageInfo/stopPassages/stop?stop={stop_id}"

API_BUS_STOPS_URL = "https://ttss.mpk.krakow.pl/internetservice/geoserviceDispatcher/services/stopinfo/stops?left=-648000000&bottom=-324000000&right=648000000&top=324000000"
API_TRAM_STOPS_URL = "http://www.ttss.krakow.pl/internetservice/geoserviceDispatcher/services/stopinfo/stops?left=-648000000&bottom=-324000000&right=648000000&top=324000000"

API_BUS_VEHICLES_URL = "https://ttss.mpk.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles?lastUpdate=0"
API_TRAM_VEHICLES_URL = "http://www.ttss.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles?lastUpdate=0"

API_BUS_ROUTES_URL = (
    "https://ttss.mpk.krakow.pl/internetservice/services/routeInfo/route"
)
API_TRAM_ROUTES_URL = (
    "http://www.ttss.krakow.pl/internetservice/services/routeInfo/route"
)

DEFAULT_UPDATE_INTERVAL = 30
