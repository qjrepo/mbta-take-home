"""
MBTA Transit Project
 
Main entry point for the MBTA Transit Project
Orchestrates the three questions:
1. List all subway routes
2. Analyze routes for max/min stops and transfer stops
3. Find path between two stops using BFS
"""

from questions import run_question_1, run_question_2,run_question_3

def main():
    """
    Main orchestration function for MBTA transit analysis.
    
    Executes three questions in sequence:
    1. Question 1: Display all subway routes
    2. Question 2: Analyze routes (max/min stops, transfer points)
                   Returns routes_stops mapping for Question 3
    3. Question 3: Find path between two user-selected stops
    
    Error handling:
    - Catches RuntimeError from API failures or invalid data
    - Displays error message
    
    Raises:
        RuntimeError: From any of the questions (API errors, etc.)
    """
    try:
        # Question 1: List all MBTA subway routes (light rail + heavy rail)
        # Fetches and displays route long names
        run_question_1()
        # Question 2: Analyze subway routes
        # Finds: routes with max/min stops, transfer stops
        # Returns: routes_stops mapping for use in Question 3
        routes_stops = run_question_2()
        # Question 3: Find path between two stops
        # Uses BFS to find optimal route(s)
        # Requires routes_stops from Question 2
        run_question_3(routes_stops)
        
    except RuntimeError as e:
        # Catch API errors or data validation errors
        # Display error message to user and exit
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
