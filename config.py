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
DESTINATION_LABEL = "DOWNTOWN & BROOKLYN"

# How often to refresh arrival data, in seconds
REFRESH_INTERVAL_SECONDS = 30

# Maximum number of upcoming arrivals to display
MAX_ARRIVALS = 2

# HTTP request timeout when fetching the feed, in seconds
REQUEST_TIMEOUT_SECONDS = 10

# --- LED matrix hardware (rpi-rgb-led-matrix RGBMatrixOptions) ---

# 6x Adafruit 64x32 panels (product 5036), wired as a single serpentine
# (U-shaped) chain off the Bonnet's one output, folded into a 192x64 display
# by the "U-mapper" pixel mapper. The Bonnet only has one chain output, so
# this is NOT 2 parallel chains. Confirmed physical order: bonnet ->
# bottom-right -> bottom-middle -> bottom-left -> top-left -> top-middle ->
# top-right.
PANEL_ROWS = 32
PANEL_COLS = 64
CHAIN_LENGTH = 6
PARALLEL_CHAINS = 1

# Folds the single 6-panel chain into 2 physical rows of 3.
PIXEL_MAPPER = "U-mapper"

# Adafruit RGB Matrix Bonnet (product 3211). "adafruit-hat-pwm" needs a
# soldered GPIO4-GPIO18 jumper mod that hasn't been done on this board --
# using it produced no output at all. Stick with plain "adafruit-hat".
HARDWARE_MAPPING = "adafruit-hat"

# These panels show yellow as purple with the default "RGB" order -- a known
# manufacturing variance where green/blue data lines are swapped internally.
# "RBG" compensates in software; reseating cables didn't fix it because it
# isn't a connection problem.
LED_RGB_SEQUENCE = "RBG"

# Raised from 2: the full 6-panel chain showed clean data near the bonnet
# end degrading to corrupted/blank further down the chain, while each half
# worked perfectly as a standalone 3-panel chain regardless of which cables
# were used -- the signature of insufficient timing margin for a longer
# chain on the Pi Zero 2 W, not a bad cable or panel.
GPIO_SLOWDOWN = 4

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
