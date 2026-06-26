"""
Question 2: Analyze MBTA subway routes for stops and transfer stops.
 
This module analyzes all subway routes to find:
1. Route(s) with the maximum number of stops
2. Route(s) with the minimum number of stops
3. Stops that have two or more routes connect to it
"""

from api import MBTAClient

def run_question_2(silent=False):
    """
    Main function to analyze subway routes and stops.
    
    Orchestrates the complete analysis:
    1. Fetches all subway routes from API
    2. Builds mappings of routes to stops and stops to routes
    3. Calculates stop counts per route
    4. Finds and displays routes with max/min stops
    5. Finds and displays stops that have two or more routes connect to it
    
    Returns:
        dict: routes_stops mapping for use in question 3
    """

    # Initialize API client
    client = MBTAClient()
    params = {"filter[type]": "0,1"}
    routes = client.get_routes(params)
    
    # Build routes_stops and stop_routes mappings for analysis
    # routes_stops: {route_id: {"name": route_name, "stops": [stops]}}
    # stop_routes: {stop_id: {"name": stop_name, "routes": [route_names]}}
    routes_stops, stop_routes = build_routes_stops_mapping(client, routes)
    
    # Part 1 & 2: Find routes with max/min stops
    # Calculate how many stops each route has
    stop_counts = calculate_stop_counts(routes_stops)

    # Find all routes with max stops and all routes with min stops
    # (Multiple routes can have same count)
    routes_with_max_stops, routes_with_min_stops = find_max_min_routes(stop_counts, routes_stops)

    # Display results for part 1 & 2
    # Only print if not silent
    if not silent:
        print_max_min_routes(routes_with_max_stops, routes_with_min_stops)
    
    # Part 3: Find stops that connect 2+ routes
    stops_with_2_or_more_than_2_routes = find_transfer_stops(stop_routes)
    
    # Display stops that connect 2+ routes along with relevant route names
    # Only print if not silent
    if not silent:
        print_transfer_stops(stops_with_2_or_more_than_2_routes)
    
    # Return routes_stops for use in question 3 (pathfinding)
    return routes_stops
 
 
def build_routes_stops_mapping(client, routes):
    """
    Build mappings between routes and stops from API data.
    
    Creates two dictionaries:
    - routes_stops: routes mapped to their stops
    - stop_routes: stops mapped to their routes
    
    Args:
        client (MBTAClient): API client for fetching stop data
        routes (list): List of route objects from MBTA API
    
    Returns:
        tuple: (routes_stops, stop_routes) dictionaries
               - routes_stops: {route_id: {"name": route_name, "stops": [stops]}}
               - stop_routes: {stop_id: {"name": stop_name, "routes": [route_names]}}
    """

    # {route_id: {"name": route_name, "stops": [stops]}}
    routes_stops = {}
    # {stop_id: {"name": stop_name, "routes": [route_names]}}
    stop_routes = {}
    
    # Process each route
    for route in routes:
        # Safely extract route ID and name
        route_id = route.get("id")
        if not route_id:
            continue
        attributes = route.get("attributes", {})
        route_name = attributes.get("long_name")
        if not route_name:
            continue
        # Fetch all stops for this route from API
        stops = client.get_stops_for_route(route_id)
        # Store route information with its stops
        routes_stops[route_id] = {
            "name": route_name,
            "stops": stops
        }
        
        # Build stop_routes mapping
        for stop in stops:
            # Safely extract stop ID and name
            stop_id = stop.get("id")
            if not stop_id:
                continue
            stop_attributes = stop.get("attributes", {})
            stop_name = stop_attributes.get("name")
            if not stop_name:
                continue

            # Initialize stop entry if not seen before
            if stop_id not in stop_routes:
                stop_routes[stop_id] = {
                    "name": stop_name,
                    "routes": [] # List of route names serving this stop
                }
            # Add this route_name to the stop's list of routes
            stop_routes[stop_id]["routes"].append(route_name)
    
    return routes_stops, stop_routes
 
 
def calculate_stop_counts(routes_stops):
    """
    Calculate the number of stops for each route.
    
    Args:
        routes_stops (dict): Mapping of routes to their stops
    
    Returns:
        dict: {route_id: number_of_stops}
              Example: {"Red": 22, "Orange": 20, "Blue": 21}
    """
    # Initialize dictionary to store stop counts per route
    stop_counts = {}

    # Calculate stop count for each route
    for route_id, route_detail in routes_stops.items():
        # Count the number of stops for this route
        stops_len = len(route_detail["stops"])
        stop_counts[route_id] = stops_len
    return stop_counts
 
 
def find_max_min_routes(stop_counts, routes_stops):
    """
    Find routes with maximum and minimum number of stops.
    
    Identifies all routes tied for most stops and all routes tied for fewest stops.
    There can be multiple routes with the same max/min stop count.
    
    Args:
        stop_counts (dict): {route_id: number_of_stops}
        routes_stops (dict): {route_id: {"name": route_name, "stops": [stops]}}
    
    Returns:
        tuple: (routes_with_max_stops, routes_with_min_stops)
               Each is a dict: {route_name: stop_count}
    """

    # Find the maximum and minimum stop counts across all routes
    max_stops = max(stop_counts.values())
    min_stops = min(stop_counts.values())
    
    # Initialize dictionaries to store routes with max/min stops
    # There could be multiple routes with the same amount of stops
    routes_with_max_stops = {}
    routes_with_min_stops = {}
    
    # Iterate through each route's stop count
    for route_id, stops_num in stop_counts.items():
        # Get the route name for display
        route_name = routes_stops[route_id]["name"]
        # Check if this route has max stops (can be multiple)
        if stops_num == max_stops:
            routes_with_max_stops[route_name] = stops_num
        # Check if this route has min stops (can be multiple)
        if stops_num == min_stops:
            routes_with_min_stops[route_name] = stops_num
    
    return routes_with_max_stops, routes_with_min_stops
 
 
def print_max_min_routes(routes_with_max_stops, routes_with_min_stops):
    """
    Display routes with maximum and minimum stops.
    
    Prints formatted output showing:
    - Route(s) with the most stops
    - Route(s) with the fewest stops
    
    Args:
        routes_with_max_stops (dict): {route_name: stop_count}
        routes_with_min_stops (dict): {route_name: stop_count}
    """

    print("\nRoute(s) with max stops")
    print("-" * 40)
    for route_name, stops_count in routes_with_max_stops.items():
        print(f"{route_name}: {stops_count}")
    
    print("\nRoute(s) with min stops")
    print("-" * 40)
    for route_name, stops_count in routes_with_min_stops.items():
        print(f"{route_name}: {stops_count}")
 
 
def find_transfer_stops(stop_routes):
    """
    Find all stops that serve 2 or more routes (transfer stops).
    
    A transfer stop allows passengers to switch between subway routes.
    Identifies all stops where multiple routes intersect.
    
    Args:
        stop_routes (dict): {stop_id: {"name": stop_name, "routes": [route_names]}}
    
    Returns:
        dict: {(stop_id, stop_name): [route_names]}
              Maps stop tuples to list of routes serving that stop
    """

    # Initialize dictionary to store transfer stops
    # Key: (stop_id, stop_name) tuple for unique identification
    # Value: list of route names serving this stop
    stops_with_2_or_more_than_2_routes = {}
    
    # Iterate through all stops to find transfer stops
    for stop_id, stop_info in stop_routes.items():
        stop_name = stop_info["name"]
        routes = stop_info["routes"]
        routes_num = len(routes)
        # A transfer stop must have 2 or more routes connect to it
        if routes_num >= 2:
            stop_key = (stop_id, stop_name)
            stops_with_2_or_more_than_2_routes[stop_key] = routes
    
    return stops_with_2_or_more_than_2_routes
 
 
def print_transfer_stops(stops_with_2_or_more_than_2_routes):
    """
    Display all transfer stops and the routes they connect.
    
    Shows stops where passengers can transfer between 2 or more subway routes.
    
    Args:
        stops_with_2_or_more_routes (dict): {(stop_id, stop_name): [route_names]}
    """
    print("\nStops that connect two or more subway routes")
    print("-" * 40)
    for stop_key, routes in stops_with_2_or_more_than_2_routes.items():
        routes_format = ", ".join(routes)
        stop_id = stop_key[0]
        stop_name = stop_key[1]
        print(f"({stop_id},{stop_name}): {routes_format}")