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
# by the "U-mapper" pixel mapper (see PIXEL_MAPPER below). The Bonnet only
# has one chain output, so this is NOT 2 parallel chains. Confirmed physical
# order: bonnet -> bottom-right -> bottom-middle -> bottom-left -> top-left
# -> top-middle -> top-right.
PANEL_ROWS = 32
PANEL_COLS = 64
CHAIN_LENGTH = 6
PARALLEL_CHAINS = 1

# Folds the single 6-panel chain into 2 physical rows of 3. Plain "U-mapper"
# (no Mirror/Rotate) put the Q bullet on the correct (left) side of a
# working row; adding Rotate:180 moved it to the wrong side without fixing
# anything else, so that was a net loss -- reverted.
#
# UNRESOLVED as of 2026-08-04: the bottom-right/bottom-middle panels
# (chain positions 1-2) display correctly; the next panel (position 3)
# shows corrupted noise; everything after that (positions 4-6) is
# completely dark. This exact failure point held steady across a lot of
# elimination testing -- swapping the cable at that junction, swapping
# which physical panel sits at position 3, GPIO_SLOWDOWN at 2/4/8, and
# BRIGHTNESS at 70 vs 30 all made zero difference. It also happens
# identically whether the chain is 4 panels or the full 6, which rules out
# "chain too long" signal degradation -- it's a fault localized to that one
# junction (between chain position 3 and 4), not a length problem. Not yet
# tested: swapping which panel sits at position 4 (the one right after the
# break) -- see [[project-subway-display]] memory for the fuller diagnostic
# history before re-testing things already ruled out above.
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

# Raise if you see flicker/ghosting on the Pi Zero 2 W; 2-4 is typical
GPIO_SLOWDOWN = 2

# Percent brightness; keep well under 100 given the 2x 5A supplies
BRIGHTNESS = 70

# BDF font bundled with https://github.com/hzeller/rpi-rgb-led-matrix
# Adjust this path to wherever that repo is cloned on the Pi. Used for the
# stop/time text and the bullet's Q, so they all match in size and font.
FONT_DIR = "/home/pi/rpi-rgb-led-matrix/fonts"
LABEL_FONT_FILE = f"{FONT_DIR}/7x13B.bdf"

# Layout, in pixels, of each 16px-tall arrival row
BULLET_DIAMETER = 15
BULLET_CENTER_X = 9
LABEL_X = 22
RIGHT_MARGIN = 4

# Fine-tune nudge (pixels) for the Q's position within the bullet circle,
# on top of its centered/baseline placement in Display._draw_bullet.
BULLET_Q_X_OFFSET = 0  # nudged right then back left 1px 2026-08-05
BULLET_Q_Y_OFFSET = 1  # nudged down 2026-08-05

# The label font's own space glyph is wider than looks right at this scale --
# left too much gap around "&" in DESTINATION_LABEL and between the number
# and "MIN" in the arrival label, enough to crowd the display's fixed width.
# display.py scales the space advance down by this factor instead of using
# the font's native width. 1.0 = font default (the old too-wide look);
# lower = tighter. Nudge this after checking it live on the physical display.
SPACE_WIDTH_SCALE = 0.5

# Extra flat pixel nudge applied on top of SPACE_WIDTH_SCALE above, for
# finer tuning than the scale factor alone can give. Negative = tighter.
SPACE_WIDTH_ADJUST_PX = -1  # trimmed 1px further on 2026-08-05

# Manual kerning nudges (pixels; negative = tighter) for specific adjacent
# character pairs that still look too loose at their normal BDF widths.
# Keyed by (this_char, next_char), checked against consecutive characters
# in any label text drawn via Display._draw_tracked_text. Uppercase because
# DESTINATION_LABEL and the formatted arrival text are both uppercase.
KERNING_ADJUSTMENTS_PX = {
    ("L", "Y"): -1,  # "BROOKLYN" -- tightened 2026-08-05
}
