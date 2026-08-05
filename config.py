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

# TEMPORARY DIAGNOSTIC CHANGE, 2026-08-04: narrowing down where the chain
# breaks. Both halves (bottom 3, top 3) work perfectly standalone; the full
# 6-panel chain fails at the same spot regardless of cable/panel/timing/
# power. Testing 4 panels flat (bonnet -> screen6 -> 5 -> 4 -> 1, screens 2
# and 3 physically disconnected) to see if it's already broken at 4, or
# only breaks at 5/6. REVERT this and DISPLAY_WIDTH/HEIGHT in display.py
# back to the 6-panel/U-mapper setup afterward -- see git log.
PANEL_ROWS = 32
PANEL_COLS = 64
CHAIN_LENGTH = 4
PARALLEL_CHAINS = 1

# Flat 4-panel chain for this test, no fold.
PIXEL_MAPPER = ""

# Adafruit RGB Matrix Bonnet (product 3211). "adafruit-hat-pwm" needs a
# soldered GPIO4-GPIO18 jumper mod that hasn't been done on this board --
# using it produced no output at all. Stick with plain "adafruit-hat".
HARDWARE_MAPPING = "adafruit-hat"

# These panels show yellow as purple with the default "RGB" order -- a known
# manufacturing variance where green/blue data lines are swapped internally.
# "RBG" compensates in software; reseating cables didn't fix it because it
# isn't a connection problem.
LED_RGB_SEQUENCE = "RBG"

# 2/4/8 all made zero visible difference on the 6-panel chain problem, so
# this isn't the fix -- back to the original default.
GPIO_SLOWDOWN = 2

# Back to 70 -- dropping to 30 also made zero difference to the 6-panel
# chain problem, ruling out combined current draw too.
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
