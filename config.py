"""Configuration for the Q train arrival display."""

# MTA GTFS-realtime feed for the N/Q/R/W lines (no API key required)
FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-nqrw"

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
