"""Configuration for the Q train arrival display."""

# MTA GTFS-realtime feed for the N/Q/R/W lines (no API key required).
# Note: the slash in "nyct/gtfs-nqrw" must stay percent-encoded as %2F --
# it's a single API Gateway path parameter, not two path segments. An
# unencoded slash returns a misleading 403 MissingAuthenticationTokenException.
FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"

# Stop ID for 96th St, downtown (Manhattan-bound side toward Coney Island)
STOP_ID = "Q05S"

# Route we care about
ROUTE_ID = "Q"

# Label shown on the display for this direction
DESTINATION_LABEL = "CONEY ISLAND"

# How often to refresh arrival data, in seconds
REFRESH_INTERVAL_SECONDS = 30

# Maximum number of upcoming arrivals to display
MAX_ARRIVALS = 2

# HTTP request timeout when fetching the feed, in seconds
REQUEST_TIMEOUT_SECONDS = 10

# --- LED matrix hardware (rpi-rgb-led-matrix RGBMatrixOptions) ---

# 4x Adafruit 64x32 panels (product 5036) chained into a single 256x32 display
PANEL_ROWS = 32
PANEL_COLS = 64
CHAIN_LENGTH = 4
PARALLEL_CHAINS = 1

# Adafruit RGB Matrix Bonnet (product 3211)
HARDWARE_MAPPING = "adafruit-hat"

# Raise if you see flicker/ghosting on the Pi Zero 2 W; 2-4 is typical
GPIO_SLOWDOWN = 2

# Percent brightness; keep well under 100 given the 2x 5A supplies
BRIGHTNESS = 70

# BDF fonts bundled with https://github.com/hzeller/rpi-rgb-led-matrix
# Adjust this path to wherever that repo is cloned on the Pi.
FONT_DIR = "/home/pi/rpi-rgb-led-matrix/fonts"
LABEL_FONT_FILE = f"{FONT_DIR}/7x13B.bdf"
BULLET_FONT_FILE = f"{FONT_DIR}/5x7.bdf"

# Layout, in pixels, of each 16px-tall arrival row
BULLET_DIAMETER = 15
BULLET_CENTER_X = 9
LABEL_X = 22
RIGHT_MARGIN = 4
