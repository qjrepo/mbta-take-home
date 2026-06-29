"""
Question 3: Find a route between two subway stops.
 
This module finds a path between two stops using BFS (Breadth-First Search).
It lets users enter a from and to stop, then displays which subway routes to take.
"""


from collections import deque

def run_question_3(routes_stops):
    """
    Main function to find and display path between two subway stops.
    
    Orchestrates the complete pathfinding process:
    1. Builds lookup dictionaries for efficient route/stop navigation
    2. Prompts user for start and end stops
    3. Runs BFS to find optimal route(s)
    4. Displays result or error message
    
    Args:
        routes_stops (dict): Route data from question 2
                            {route_id: {"name": route_name, "stops": [stops]}}
    
    Note:
        Builds 4 lookup dictionaries to support efficient BFS:
        - route_id_to_stops_id: Maps route IDs to their stop lists
        - stop_id_to_routes_id: Maps stops to their available routes
        - route_id_to_name: Maps route IDs to routes long names
        - stop_id_to_name_address: Maps stops to their names and addresses
    """
    # {route_id :[stop_ids]}
    # Maps each route to list of stops it serves
    route_id_to_stops_id = {}

    #{stop_id: [routes_id]}
    # Maps each stop to list of routes that serve it
    stop_id_to_routes_id = {}

    #route_id to route_name mapping
    route_id_to_name = {}

    # stop_id: to stop info including address
    # there might be multiple addresses with the same stop name
    # {stop_id: {name: Wonderland, address: 1300 North Shore Rd, Revere, MA 02151}}
    stop_id_to_name_address = {}

    # Process each route and build all lookup dictionaries
    for route_id, route_info in routes_stops.items():
        route_name = route_info["name"]
        route_id_to_name[route_id] = route_name

        # Initialize list to store this route's stops
        stop_ids = []

        # Process each stop in this route
        for stop in route_info["stops"]:
            stop_id = stop.get("id")
            # Skip stops without valid IDs
            if not stop_id:
                continue

            if stop_id not in stop_id_to_name_address:
                # Safely access nested attributes with defaults
                attributes = stop.get("attributes", {})
                stop_name = attributes.get("name")
                stop_address = attributes.get("address")
                if not stop_name or not stop_address:
                    continue

                stop_id_to_name_address[stop_id] = {
                    "name": stop_name, 
                    "address": stop_address
                }

            # Add stop to current route's stop list
            stop_ids.append(stop_id)
            if stop_id not in stop_id_to_routes_id:
                stop_id_to_routes_id[stop_id] = []
            stop_id_to_routes_id[stop_id].append(route_id)
        
        route_id_to_stops_id[route_id] = stop_ids

    
    # Get user input for start and end stops, getting ids here bc there could be same stop names on different routes
    # Prompt separately to handle stops with multiple addresses
    from_id = get_stop_id_user(stop_id_to_name_address, "from")
    to_id = get_stop_id_user(stop_id_to_name_address, "to")

    # Check if start and end are the same
    if from_id == to_id:
        print("Same stop. No need to take the train.")
    else:
        # Find route(s) using BFS algorithm
        routes_found = bfs_find_routes(from_id, to_id, stop_id_to_routes_id, route_id_to_stops_id)
         # Check if a path exists
        if not routes_found:
            print("No route found")
        else:
            # Get names of start and end stops for display
            from_id_name = stop_id_to_name_address[from_id]["name"]
            to_id_name = stop_id_to_name_address[to_id]["name"]

            # Convert route IDs to route names for display
            routes_names = []

            for id in routes_found:
                routes_names.append(route_id_to_name[id])

            # Format as comma-separated string
            routes_names_str = ", ".join(routes_names)
            # Display result to user
            print(f"From {from_id_name} To {to_id_name} -> {routes_names_str}")


def get_stop_id_user(stop_id_to_name_address, direction):
    """
    Prompt user for a stop name and return its ID.
    
    Handles:
    - Case-insensitive matching
    - Multiple stops with same name (different addresses)
    - Invalid input retry logic
    
    Args:
        stop_id_to_name_address (dict): {stop_id: {"name": stop_name, "address": stop_address}}
        direction (str): "from" or "to" for prompt context
    
    Returns:
        str: Stop ID selected by user
    
    Note:
        Loops until valid input received. Handles multiple matches by displaying
        addresses for user to choose.
    """
    while True:
        # Prompt user for stop name
        name = input(f"Where you want to travel {direction}: ").strip()
        match = []

        # Search for all stops matching user input (case-insensitive)
        for stop_id, stop_info in stop_id_to_name_address.items():
            stop_name = stop_info["name"]
            stop_addr = stop_info["address"]
            if name.lower() == stop_name.lower():
                match.append((stop_id, stop_addr))

        # Handle no matches found
        if not match:
            print("Stop not found. Please try again.")
            continue

         # Handle single match - return immediately
        if len(match) == 1:
            return match[0][0]
        
        # Handle multiple matches - let user choose by address
        print(f"\nMultiple '{name}' stops found:")

        for i, (_, addr) in enumerate(match):
            print(f"{i}: {name}")
            print(f"Address: {addr}\n")

         # Get user's selection
        try:
            num_choice = int(input("Pick one number from above: "))
            # Validate selection is in range
            if num_choice < 0 or num_choice >= len(match):
                print("Option doesn't exist. Please try again.")
            else:
                # Return selected stop's ID
                return match[num_choice][0]
        except ValueError:
            print("Invalid input. Please enter an integer")


def bfs_find_routes(start_id, end_id, stop_id_to_routes_id, route_id_to_stops_id):
    """
    Find a path between two stops using Breadth-First Search (BFS).
    
    Algorithm:
    1. Start at source stop, explore all reachable stops via available routes
    2. For each stop, find all routes that serve it
    3. For each route, find all next stops on that route
    4. If moving to a new route, add current route to route list
    5. If continuing on same route, keep route list unchanged
    6. Stop when destination reached
    
    Args:
        start_id (str): Starting stop ID
        end_id (str): Destination stop ID
        stop_id_to_routes_id (dict): {stop_id: [route_ids]} - stops to routes mapping
        route_id_to_stops_id (dict): {route_id: [stop_ids]} - routes to stops mapping
    
    Returns:
        list: Route IDs to take (in order)
              Empty list if no path exists
    
    Note:
        BFS Queue stores tuples: (current_stop_id, [route_ids_used_so_far])
        If already on a route and it continues to next stop,
        don't add route again (stay on same route).
    """
    # Initialize BFS queue with start stop and empty route list
    # Each item: (current_stop_id, [route_ids_taken])
    queue = deque([(start_id, [])])
    # Track visited stops to avoid cycles
    visited = {start_id}
    # Stores route sequence if destination found
    routes_found = []
    
    # BFS traversal loop
    while queue:
        # Dequeue stop and routes used to reach it
        stop, routes_used = queue.popleft()
        # Check if we reached destination
        if stop == end_id:
            routes_found = routes_used
            break
        # Find all routes serving current stop
        # These are transfer options at this stop
        for route in stop_id_to_routes_id[stop]:
            # Iterate over all stops on this route
            for next_stop in route_id_to_stops_id[route]:
                # Only visit unvisited stops
                if next_stop not in visited:
                    # Check if we're already on this route
                    if routes_used and routes_used[-1] == route:
                        # Already on this route, continue without adding it again
                        queue.append((next_stop, routes_used))
                    else:
                        # New route, add it to route sequence
                        queue.append((next_stop, routes_used + [route]))
                    # Mark stop as visited
                    visited.add(next_stop)
         
    return routes_found