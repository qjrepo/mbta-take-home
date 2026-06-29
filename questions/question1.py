"""
Question 1: List all MBTA subway routes.
 
This module retrieves and displays all light rail and heavy rail subway routes
from the MBTA API.
"""
"""

DESIGN DECISION: Server-Side Filtering for Subway Routes
 
CHOSEN APPROACH:
Option 2 - Rely on the server API to filter before results are received.
 
Implementation:
    params = {"filter[type]": "0,1"}
    routes = client.get_routes(params)
 
REASONING:
 
I chose server-side API filtering because it is the better software engineering 
choice. It reduces network payload, latency, and local memory usage:
 
1. REDUCES NETWORK PAYLOAD
   - Download only ~10 subway routes instead of 100+ total routes
   - Minimizes data transfer over the network
 
2. REDUCES LATENCY
   - Server-side filtering is faster than downloading and processing locally
   - API is optimized for database-level filtering
 
3. REDUCES LOCAL MEMORY USAGE
   - Client only holds subway route data in memory
   - No need to store unnecessary routes

"""
from api import MBTAClient

def run_question_1():
    """
    Main function to list all MBTA subway routes.
    
    Fetches subway route names from the MBTA API and prints them to stdout.
    Displays routes with a formatted header for readability.
    
    Flow:
    1. Initialize MBTA API client
    2. Fetch filtered subway routes from helper function
    3. Print formatted output with header and separator
    """
    # Initialize API client to communicate with MBTA API
    client = MBTAClient()

    # Get all subway route names (light rail and heavy rail)
    route_names = get_subway_route_names(client)

    # Display results with formatted header
    print("Routes")
    print('-'*40)
    # Iterate through each route name and print on separate line
    for route_name in route_names:
        print(route_name)

def get_subway_route_names(client):
    """
    Fetch and extract all subway route names from MBTA API.
    
    Uses server-side filtering to request only subway routes (Light Rail + Heavy Rail)
    from the API, reducing network payload and improving efficiency.
    
    Args:
        client (MBTAClient): API client for making requests to MBTA.
    
    Returns:
        list: List of subway route long names (strings).
              Example: ["Red Line", "Orange Line", "Blue Line"]
    
    Note:
        Filter types: "0" = light rail, "1" = heavy rail (subway)
        Uses server-side filtering to reduce network payload and latency.
    """

    # Type 0 = Light Rail, Type 1 = Heavy Rail (subway)
    params = {"filter[type]": "0,1"}

    # Fetch routes from MBTA API with filter applied
    # Returns list of route objects with attributes like 'long_name'
    routes = client.get_routes(params)

    # Initialize empty list to store route names
    route_names = []

    # Iterate through each route returned from API
    for route in routes:
        # Safely access nested 'attributes' dict with empty dict as default
        # Prevents KeyError if attributes are missing
        attributes = route.get("attributes", {})

        # Extract 'long_name' from attributes with None as default
        long_name = attributes.get("long_name")

        # Only add routes that have a valid long name
        # Filters out routes with empty or None long_name
        if long_name:
            route_names.append(long_name)

    return route_names