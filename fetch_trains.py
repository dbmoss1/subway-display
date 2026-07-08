"""Fetch live Q train arrival predictions from the MTA GTFS-realtime feed."""

import time
from datetime import datetime

import requests
from google.transit import gtfs_realtime_pb2

import config


def fetch_arrivals(stop_id=config.STOP_ID, route_id=config.ROUTE_ID):
    """Return a sorted list of minutes-until-arrival for the given stop/route.

    Only future arrivals are included; anything already in the past (stale
    feed data) is dropped.
    """
    response = requests.get(config.FEED_URL, timeout=config.REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    now = time.time()
    arrivals = []

    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update
        if trip_update.trip.route_id != route_id:
            continue

        for stop_time_update in trip_update.stop_time_update:
            if stop_time_update.stop_id != stop_id:
                continue

            if stop_time_update.HasField("arrival"):
                event_time = stop_time_update.arrival.time
            elif stop_time_update.HasField("departure"):
                event_time = stop_time_update.departure.time
            else:
                continue

            minutes_away = (event_time - now) / 60
            if minutes_away >= 0:
                arrivals.append(minutes_away)

    arrivals.sort()
    return arrivals


def format_minutes(minutes_away):
    """Round minutes-away into a display-friendly integer, with a floor of 0."""
    return max(0, round(minutes_away))


if __name__ == "__main__":
    print(f"Fetching arrivals for stop {config.STOP_ID} (route {config.ROUTE_ID})...")
    print(f"Feed URL: {config.FEED_URL}")
    print(f"Time: {datetime.now().isoformat()}\n")

    try:
        results = fetch_arrivals()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        raise SystemExit(1)

    if not results:
        print(f"No upcoming arrivals found for stop {config.STOP_ID}.")
        print("Double-check the stop ID against the MTA GTFS static stops.txt.")
    else:
        print(f"Found {len(results)} upcoming arrival(s):")
        for minutes in results[: config.MAX_ARRIVALS]:
            print(f"  {format_minutes(minutes)} min")
