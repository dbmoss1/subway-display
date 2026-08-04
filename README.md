# NYC Subway Arrival Display — Q Train @ 96th St

A DIY LED matrix display showing live downtown Q train arrivals at 96th St
(toward Coney Island–Stillwell Av), built on a Raspberry Pi Zero 2 W.

## Hardware

- Raspberry Pi Zero 2 W
- microSD card (8GB+) for the Pi's OS
- microSD-to-SD (or microSD-to-USB) adapter, for flashing the card from a laptop without a built-in microSD slot
- 6x Adafruit 64x32 RGB LED Matrix panels, 2.5mm pitch ([product 5036](https://www.adafruit.com/product/5036)), wired as a single serpentine ("U-shaped") chain off the Bonnet's one output — **done**, actual physical order is bonnet → bottom-right → bottom-middle → bottom-left → top-left → top-middle → top-right, folded into a 192x64 display by the `rpi-rgb-led-matrix` "U-mapper" pixel mapper. The chain visits the bottom row first, then the top row — the opposite of what U-mapper assumes — so `config.PIXEL_MAPPER` also applies a 180-degree rotation (`"U-mapper;Rotate:180"`) to compensate. **Wiring order matters**: the ribbon between rows must land on the same side the first row's chain ends on, or the image scrambles. These panels also have green/blue data lines swapped internally (see `LED_RGB_SEQUENCE` in `config.py`).
- Adafruit RGB Matrix Bonnet ([product 3211](https://www.adafruit.com/product/3211)) — note this board has a single chain output only (no parallel-chain support), which is why the 6 panels must be one folded chain rather than 2 independent chains of 3 — **done**, mounted and attached. Do not use `HARDWARE_MAPPING = "adafruit-hat-pwm"` unless the GPIO4-GPIO18 jumper mod has been soldered onto this board — without it, that mapping produces no output at all.
- Power: one 5V/10A supply ([product 658](https://www.adafruit.com/product/658)) through a 4-way DC splitter ([product 1352](https://www.adafruit.com/product/1352)) — **done**, 3 outputs each feed a pair of panels' bare wires via product-368 screw terminal blocks, 1 output feeds the Pi (via barrel-to-USB adapter), which powers the Bonnet through its GPIO pins. The Pi must be powered from this dedicated supply, not a laptop's USB port — running 6 LED panels' worth of backfed current through a laptop USB port/Pi GPIO pins caused garbled/dark panels that looked like a data or software bug.
- GPIO header for the Pi (its 40 GPIO holes ship unpopulated) — either a solderless "hammer header" + jig kit ([product 3413](https://www.adafruit.com/product/3413)), or a standard 2x20 male header + your own soldering iron — **done**, header mounted and bonnet attached
- Something to physically mount/align the 6 panels in a 2-row x 3-column grid (frame, backing board, or brackets — not yet decided)

## Software

- `config.py` — station/feed configuration
- `fetch_trains.py` — polls the MTA GTFS-realtime feed for the N/Q/R/W lines and
  extracts Q train arrival predictions for a given stop
- `display.py` — renders arrivals onto the LED matrix panels
- `main.py` — ties fetching and rendering together in a refresh loop

No MTA API key is required — the GTFS-realtime feeds are public.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On the Raspberry Pi, `display.py` additionally requires the
[rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) Python
bindings, installed separately per that project's instructions (it's a C++
library with Python bindings, not a pip package). Clone that repo on the Pi
and update `config.FONT_DIR` to point at its `fonts/` directory.

## Usage

Test the feed connection and stop ID without any hardware attached:

```bash
python3 fetch_trains.py
```

Preview the LED layout on the Pi without the fetch loop:

```bash
sudo python3 display.py
```

Run the full display loop (on the Pi, with the bonnet and panels attached):

```bash
sudo python3 main.py
```

(`sudo` is required because the LED matrix library needs direct hardware access.)

## Gotchas

- The feed URL's `nyct/gtfs-nqrw` segment must be percent-encoded as
  `nyct%2Fgtfs-nqrw` — it's a single API Gateway path parameter, not two path
  segments. An unencoded slash returns a misleading 403
  `MissingAuthenticationTokenException` instead of a 404.

## Finding a stop ID

Stop IDs come from the MTA's static GTFS `stops.txt`. For the N/Q/R/W lines,
southbound (downtown) stops end in `S` and northbound (uptown) stops end in
`N`. 96th St downtown is `Q05S`.
