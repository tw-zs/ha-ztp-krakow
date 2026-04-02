"""Constants for the ZTP Krak\u00f3w integration."""

DOMAIN = "ztp_krakow"
CONF_STOP_ID = "stop_id"
CONF_STOP_NAME = "stop_name"
CONF_STOP_TYPE = "stop_type"

STOP_TYPE_BUS = "bus"
STOP_TYPE_TRAM = "tram"

API_BUS_URL = "https://ttss.mpk.krakow.pl/internetservice/services/passageInfo/stopPassages/stop?stop={stop_id}"
API_TRAM_URL = "http://www.ttss.krakow.pl/internetservice/services/passageInfo/stopPassages/stop?stop={stop_id}"

DEFAULT_UPDATE_INTERVAL = 30
