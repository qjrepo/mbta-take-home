"""
MBTA API Client Module
 
Provides MBTAClient for communicating with the MBTA (Massachusetts Bay Transportation Authority)
REST API. Handles HTTP requests, error handling, and API key management.
"""
import requests
import os

class MBTAClient:
    """
    Client for interacting with the MBTA API.
    
    Handles:
    - HTTP GET requests to MBTA endpoints
    - API key authentication via environment variables
    - Error handling for network and HTTP errors
    - JSON response parsing
    
    Attributes:
        BASE_URL (str): Base URL for MBTA API v3
        TIMEOUT (int): Request timeout in seconds
        api_key (str): MBTA API key loaded from environment
    """

    # MBTA API v3 base URL
    BASE_URL = "https://api-v3.mbta.com"

    # Timeout for all requests (10 seconds)
    TIMEOUT = 10

    def __init__(self):
        # Load API key from environment variable
        self.api_key = os.getenv("MBTA_API_KEY")

    def get(self, endpoint, params=None):
        """
        Make a GET request to the MBTA API.
        
        Args:
            endpoint (str): API endpoint (e.g., "routes", "stops")
                           Leading slash is optional
            params (dict): Query parameters for the request
                          Example: {"filter[type]": "0,1"}
                          Will not be modified (params are copied)
        
        Returns:
            dict: Parsed JSON response from API
        
        Raises:
            RuntimeError: On connection failure, timeout, HTTP error, or invalid JSON
        
        Note:
            - API key is automatically added to params if available
            - All requests timeout after 10 seconds
            - Response status is checked (raises on 4xx/5xx)
        """

        # Remove leading slash from endpoint if present (normalize)
        endpoint = endpoint.lstrip("/")
        url = f"{self.BASE_URL}/{endpoint}"

        # Copy params dict to avoid mutating caller's dict
        # Create empty dict if params is None
        params = params.copy() if params else {}

        if self.api_key:
            params["api_key"] = self.api_key
        try:
            # Make GET request with timeout
            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            # Raise exception for 4xx/5xx status codes
            response.raise_for_status()
            # Parse and return JSON response
            return response.json()
        except requests.ConnectionError:
            # Network connectivity issue (DNS, connection refused, etc.)
            raise RuntimeError("Connection failure")
        
        except requests.Timeout:
            # Request took longer than TIMEOUT seconds
            raise RuntimeError("Request timeout")
        
        except requests.HTTPError as e:
            # HTTP error status code (4xx or 5xx)
            raise RuntimeError(f"HTTP error: {e}")
        except ValueError:
            # JSON parsing failed (invalid JSON response)
            raise RuntimeError("Invalid JSON response")
    
    def get_routes(self, params=None):
        """
        Fetch routes from MBTA API.
        
        Args:
            params (dict): Query parameters to filter routes
                Example: {"filter[type]": "0,1"} for subway only
        
        Returns:
            list: List of route objects from API
                Example: [{"id": "Red", "attributes": {...}}, ...]
        Note:
            API response format: {"data": [routes]}
            This method extracts just the "data" list
        """
        data = self.get("routes", params)
        return data.get("data", [])
    
    def get_stops_for_route(self, route_id):
        """
        Fetch all stops for a specific route.
        
        Args:
            route_id (str): Route ID to fetch stops for
                Example: "Red", "Orange", "Blue"
        
        Returns:
            list: List of stop objects on the route
                Empty list if no stops found or API error
                Example: [{"id": "place-astao", "attributes": {...}}, ...]
        Note:
            Uses server-side filtering to reduce network payload
            Returns empty list as default if "data" key missing
        """
        params = {"filter[route]": route_id}
        data = self.get("stops", params)
        return data.get("data", [])