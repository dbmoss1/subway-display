# NYC Subway Arrival Display — Q Train @ 96th St

A DIY LED matrix display showing live downtown Q train arrivals at 96th St
(toward Coney Island–Stillwell Av), built on a Raspberry Pi Zero 2 W.

## Hardware

- Raspberry Pi Zero 2 W
- microSD card (8GB+) for the Pi's OS
- microSD-to-SD (or microSD-to-USB) adapter, for flashing the card from a laptop without a built-in microSD slot
- 4x Adafruit 64x32 RGB LED Matrix panels, 2.5mm pitch ([product 5036](https://www.adafruit.com/product/5036)), chained into a single 256x32 pixel display
- Adafruit RGB Matrix Bonnet ([product 3211](https://www.adafruit.com/product/3211))
- 2x 5V 4A power supplies (matrices draw significant current at full brightness)
- 2x Female DC Power Adapters, 2.1mm jack to screw terminal block ([product 368](https://www.adafruit.com/product/368)) — each panel's power cable ends in bare wire, and each screw terminal can take 2 panels' wires, letting one supply feed 2 panels
- GPIO header for the Pi (its 40 GPIO holes ship unpopulated) — either a solderless "hammer header" + jig kit ([product 3413](https://www.adafruit.com/product/3413)), or a standard 2x20 male header + your own soldering iron
- Something to physically mount/align the 4 panels in a single flush row (frame, backing board, or brackets — not yet decided)

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
