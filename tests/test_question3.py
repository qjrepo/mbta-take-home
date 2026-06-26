"""Tests for questions.question3"""

import pytest
from unittest.mock import patch, MagicMock
from questions.question3 import (
    run_question_3,
    bfs_find_routes,
    get_stop_id_user,
)
 
class TestBFSFindRoutes:
    """Tests for bfs_find_routes algorithm."""
    
    def test_bfs_single_route(self):
        """Test BFS on single route."""
        stop_id_to_routes_id = {
            "place-astao": ["Red"],
            "place-portr": ["Red"],
            "place-chncl": ["Red"]
        }
        route_id_to_stops_id = {
            "Red": ["place-astao", "place-portr", "place-chncl"]
        }
        
        result = bfs_find_routes("place-astao", "place-chncl", stop_id_to_routes_id, route_id_to_stops_id)
        
        assert result == ["Red"]
    
    def test_bfs_with_transfer(self):
        """Test BFS with route transfer."""
        stop_id_to_routes_id = {
            "place-astao": ["Red"],
            "place-chncl": ["Red", "Blue"],
            "place-pktrm": ["Blue"]
        }
        route_id_to_stops_id = {
            "Red": ["place-astao", "place-chncl"],
            "Blue": ["place-chncl", "place-pktrm"]
        }
        
        result = bfs_find_routes("place-astao", "place-pktrm", stop_id_to_routes_id, route_id_to_stops_id)
        
        assert result == ["Red", "Blue"]
    
    def test_bfs_no_path(self):
        """Test BFS when no path exists."""
        stop_id_to_routes_id = {
            "place-astao": ["Red"],
            "place-chncl": ["Red"],
            "place-pktrm": ["Blue"],
        }
        route_id_to_stops_id = {
            "Red": ["place-astao", "place-chncl"],
            "Blue": ["place-pktrm"],
        }
        
        result = bfs_find_routes("place-astao", "place-pktrm", stop_id_to_routes_id, route_id_to_stops_id)
        
        assert result == []
 
 
class TestGetStopIdUser:
    """Tests for get_stop_id_user."""
    
    @patch("builtins.input", return_value="Alewife")
    def test_get_stop_id_single_match(self, mock_input):
        """Test when single stop matches."""
        stop_id_to_name_address = {
            "place-astao": {"name": "Alewife", "address": "1282 Massachusetts Ave"},
            "place-pktrm": {"name": "Park Street", "address": "68 Park St"}
        }
        
        result = get_stop_id_user(stop_id_to_name_address, "from")
        
        assert result == "place-astao"
    
    @patch("builtins.input", side_effect=["Downtown Crossing", "0"])
    @patch("builtins.print")
    def test_get_stop_id_multiple_matches(self, mock_print, mock_input):
        """Test when multiple stops have same name."""
        stop_id_to_name_address = {
            "place-chncl": {"name": "Downtown Crossing", "address": "Winter St"},
            "place-dwnxg": {"name": "Downtown Crossing", "address": "State St"}
        }
        
        result = get_stop_id_user(stop_id_to_name_address, "from")
        
        assert result == "place-chncl"
    
    @patch("builtins.input", side_effect=["InvalidStop", "Alewife", "0"])
    @patch("builtins.print")
    def test_get_stop_id_retry_on_not_found(self, mock_print, mock_input):
        """Test retry when stop not found."""
        stop_id_to_name_address = {
            "place-astao": {"name": "Alewife", "address": "1282 Massachusetts Ave"}
        }
        
        result = get_stop_id_user(stop_id_to_name_address, "from")
        
        assert result == "place-astao"
 
 
class TestRunQuestion3:
    """Tests for run_question_3."""
    
    @patch("questions.question3.get_stop_id_user")
    @patch("builtins.print")
    def test_run_question_3_same_stop(self, mock_print, mock_get_stop_id):
        """Test when start and end stops are same."""
        mock_get_stop_id.side_effect = ["place-astao", "place-astao"]
        
        routes_stops = {
            "Red": {
                "name": "Red Line",
                "stops": [
                    {"id": "place-astao", "attributes": {"name": "Alewife", "address": "1282 Massachusetts Ave"}}
                ]
            }
        }
        
        run_question_3(routes_stops)
        
        printed = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Same stop" in str(p) for p in printed)
    
    @patch("questions.question3.get_stop_id_user")
    @patch("builtins.print")
    def test_run_question_3_with_route(self, mock_print, mock_get_stop_id):
        """Test pathfinding with route found."""
        mock_get_stop_id.side_effect = ["place-astao", "place-chncl"]
        
        routes_stops = {
            "Red": {
                "name": "Red Line",
                "stops": [
                    {"id": "place-astao", "attributes": {"name": "Alewife", "address": "1282 Massachusetts Ave"}},
                    {"id": "place-chncl", "attributes": {"name": "Downtown Crossing", "address": "Winter St"}}
                ]
            }
        }
        
        run_question_3(routes_stops)
        
        printed = [str(call[0][0]) for call in mock_print.call_args_list]
        output = " ".join(printed)
        assert "Alewife" in output and "Downtown Crossing" in output
    
    @patch("questions.question3.get_stop_id_user")
    @patch("builtins.print")
    def test_run_question_3_no_route(self, mock_print, mock_get_stop_id):
        """Test when no route exists between stops."""
        mock_get_stop_id.side_effect = ["place-astao", "place-pktrm"]
        
        routes_stops = {
            "Red": {
                "name": "Red Line",
                "stops": [
                    {"id": "place-astao", "attributes": {"name": "Alewife", "address": "1282 Massachusetts Ave"}}
                ]
            },
            "Blue": {
                "name": "Blue Line",
                "stops": [
                    {"id": "place-pktrm", "attributes": {"name": "Park Street", "address": "68 Park St"}}
                ]
            }
        }
        
        run_question_3(routes_stops)
        
        printed = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("No route" in str(p) for p in printed)
 