"""Tests for api.mbta_client"""

import pytest
import os
from unittest.mock import patch, MagicMock
from api.mbta_client import MBTAClient


class TestMBTAClient:
    """Tests for MBTAClient."""
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch.dict(os.environ, {"MBTA_API_KEY": "test-key"}):
            client = MBTAClient()
            assert client.api_key == "test-key"
    
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict(os.environ, {}, clear=True):
            client = MBTAClient()
            assert client.api_key is None
    
    @patch("api.mbta_client.requests.get")
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "Red"}]}
        mock_get.return_value = mock_response
        
        client = MBTAClient()
        result = client.get("routes", {"filter[type]": "0,1"})
        
        assert result == {"data": [{"id": "Red"}]}
    
    @patch("api.mbta_client.requests.get")
    def test_get_connection_error(self, mock_get):
        """Test ConnectionError handling."""
        mock_get.side_effect = __import__("requests").ConnectionError()
        
        client = MBTAClient()
        with pytest.raises(RuntimeError, match="Connection failure"):
            client.get("routes")
    
    @patch("api.mbta_client.requests.get")
    def test_get_timeout_error(self, mock_get):
        """Test Timeout error handling."""
        mock_get.side_effect = __import__("requests").Timeout()
        
        client = MBTAClient()
        with pytest.raises(RuntimeError, match="Request timeout"):
            client.get("routes")
    
    @patch("api.mbta_client.requests.get")
    def test_get_http_error(self, mock_get):
        """Test HTTPError handling."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = __import__("requests").HTTPError()
        mock_get.return_value = mock_response
        
        client = MBTAClient()
        with pytest.raises(RuntimeError, match="HTTP error"):
            client.get("routes")
    
    @patch("api.mbta_client.requests.get")
    def test_get_invalid_json_error(self, mock_get):
        """Test invalid JSON response handling."""
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        client = MBTAClient()
        with pytest.raises(RuntimeError, match="Invalid JSON response"):
            client.get("routes")
    
    @patch("api.mbta_client.requests.get")
    def test_get_routes(self, mock_get):
        """Test get_routes method."""
        mock_response = MagicMock()
        routes = [{"id": "Red"}, {"id": "Blue"}]
        mock_response.json.return_value = {"data": routes}
        mock_get.return_value = mock_response
        
        client = MBTAClient()
        result = client.get_routes({})
        
        assert result == routes
    
    @patch("api.mbta_client.requests.get")
    def test_get_stops_for_route(self, mock_get):
        """Test get_stops_for_route method."""
        mock_response = MagicMock()
        stops = [{"id": "stop1"}, {"id": "stop2"}]
        mock_response.json.return_value = {"data": stops}
        mock_get.return_value = mock_response
        
        client = MBTAClient()
        result = client.get_stops_for_route("Red")
        
        assert result == stops