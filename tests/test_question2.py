"""Tests for questions.question2"""

import pytest
from unittest.mock import patch, MagicMock
from questions.question2 import (
    run_question_2,
    build_routes_stops_mapping,
    calculate_stop_counts,
    find_max_min_routes,
    find_transfer_stops,
)

class TestBuildRoutesStopsMapping:
    """Tests for build_routes_stops_mapping."""
    
    def test_build_routes_stops_mapping_success(self):
        """Test building routes_stops and stop_routes mappings."""
        mock_client = MagicMock()
        routes = [
            {"id": "Red", "attributes": {"long_name": "Red Line"}},
            {"id": "Blue", "attributes": {"long_name": "Blue Line"}},
        ]
        red_stops = [
            {"id": "place-astao", "attributes": {"name": "Alewife"}},
            {"id": "place-portr", "attributes": {"name": "Porter Square"}},
        ]
        blue_stops = [
            {"id": "place-chncl", "attributes": {"name": "Downtown Crossing"}},
        ]
        mock_client.get_stops_for_route.side_effect = [red_stops, blue_stops]
        
        routes_stops, stop_routes = build_routes_stops_mapping(mock_client, routes)
        
        assert "Red" in routes_stops
        assert "Blue" in routes_stops
        assert routes_stops["Red"]["name"] == "Red Line"
        assert len(routes_stops["Red"]["stops"]) == 2
    
    def test_build_routes_stops_mapping_missing_attributes(self):
        """Test handling missing attributes safely."""
        mock_client = MagicMock()
        routes = [
            {"id": "Red", "attributes": {"long_name": "Red Line"}},
            {"id": "Blue"},  # Missing attributes
        ]
        red_stops = [{"id": "place-astao", "attributes": {"name": "Alewife"}}]
        mock_client.get_stops_for_route.side_effect = [red_stops, []]
        
        routes_stops, stop_routes = build_routes_stops_mapping(mock_client, routes)
        
        # Should only include routes with valid names
        assert "Red" in routes_stops
        assert routes_stops["Red"]["name"] == "Red Line"
        # Blue should be skipped (missing name)
        assert "Blue" not in routes_stops
 
 
class TestCalculateStopCounts:
    """Tests for calculate_stop_counts."""
    
    def test_calculate_stop_counts(self):
        """Test counting stops per route."""
        routes_stops = {
            "Red": {"name": "Red Line", "stops": [
                {"id": "place-astao", "attributes": {"name": "Alewife"}},
                {"id": "place-portr", "attributes": {"name": "Porter Square"}},
            ]},
            "Blue": {"name": "Blue Line", "stops": [
                {"id": "place-chncl", "attributes": {"name": "Downtown Crossing"}},
            ]},
        }
        
        stop_counts = calculate_stop_counts(routes_stops)
        
        assert stop_counts["Red"] == 2
        assert stop_counts["Blue"] == 1
 
 
class TestFindMaxMinRoutes:
    """Tests for find_max_min_routes."""
    
    def test_find_max_min_routes(self):
        """Test finding routes with max and min stops."""
        stop_counts = {"Red": 22, "Blue": 11, "Orange": 22}
        routes_stops = {
            "Red": {"name": "Red Line"},
            "Blue": {"name": "Blue Line"},
            "Orange": {"name": "Orange Line"},
        }
        
        max_routes, min_routes = find_max_min_routes(stop_counts, routes_stops)
        
        assert len(max_routes) == 2  # Red and Orange both have 22
        assert "Blue Line" in min_routes
        assert min_routes["Blue Line"] == 11
 
 
class TestFindTransferStops:
    """Tests for find_transfer_stops."""
    
    def test_find_transfer_stops(self):
        """Test finding stops that connect 2+ routes."""
        stop_routes = {
            "place-chncl": {"name": "Downtown Crossing", "routes": ["Red", "Blue", "Orange"]},
            "place-pktrm": {"name": "Park Street", "routes": ["Red", "Green-B", "Green-C"]},
            "place-astao": {"name": "Alewife", "routes": ["Red"]},
        }
        
        transfer_stops = find_transfer_stops(stop_routes)
        
        assert len(transfer_stops) == 2
        # Downtown Crossing and Park Street have 2+ routes
 
 
class TestRunQuestion2:
    """Tests for run_question_2."""
    
    @patch("questions.question2.MBTAClient")
    @patch("builtins.print")
    def test_run_question_2_returns_routes_stops(self, mock_print, mock_client_class):
        """Test that run_question_2 returns routes_stops dict."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        routes = [
            {"id": "Red", "attributes": {"long_name": "Red Line"}},
        ]
        stops = [
            {"id": "place-astao", "attributes": {"name": "Alewife"}},
            {"id": "place-portr", "attributes": {"name": "Porter Square"}},
        ]
        mock_client.get_routes.return_value = routes
        mock_client.get_stops_for_route.return_value = stops
        
        result = run_question_2(silent=True)
        
        assert isinstance(result, dict)
        assert "Red" in result
    
    @patch("questions.question2.MBTAClient")
    def test_run_question_2_api_error(self, mock_client_class):
        """Test error handling when API fails."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.get_routes.side_effect = RuntimeError("API error")
        
        with pytest.raises(RuntimeError):
            run_question_2(silent=True)
 