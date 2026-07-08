"""Entry point: poll the MTA feed and refresh the LED matrix display every 30s."""

import time

import requests

import config
import fetch_trains
from display import Display


def get_arrival_minutes():
    """Return up to config.MAX_ARRIVALS integer minutes-away, soonest first."""
    raw = fetch_trains.fetch_arrivals()
    return [fetch_trains.format_minutes(m) for m in raw[: config.MAX_ARRIVALS]]


def main():
    display = Display()

    while True:
        try:
            arrivals = get_arrival_minutes()
        except requests.RequestException as exc:
            print(f"Feed request failed: {exc}")
            arrivals = []

        display.render(arrivals)
        time.sleep(config.REFRESH_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down.")
