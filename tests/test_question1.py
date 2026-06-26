"""Tests for questions.question1"""

import pytest
from unittest.mock import patch, MagicMock
from questions.question1 import (run_question_1, get_subway_route_names,)


class TestGetSubwayRouteNames:
    """Tests for get_subway_route_names helper function."""
    
    def test_get_subway_route_names_with_valid_routes(self):
        """Test extracting route names from valid routes."""
        mock_client = MagicMock()
        routes = [
            {"attributes": {"long_name": "Red Line"}},
            {"attributes": {"long_name": "Blue Line"}},
        ]
        mock_client.get_routes.return_value = routes
        
        result = get_subway_route_names(mock_client)
        
        assert result == ["Red Line", "Blue Line"]
    
    def test_get_subway_route_names_with_empty_routes(self):
        """Test with no routes returned."""
        mock_client = MagicMock()
        mock_client.get_routes.return_value = []
        
        result = get_subway_route_names(mock_client)
        
        assert result == []
    
    def test_get_subway_route_names_with_missing_attributes(self):
        """Test handling routes with missing or invalid attributes."""
        mock_client = MagicMock()
        routes = [
            {"attributes": {"long_name": "Red Line"}},
            {"attributes": {}},  # Missing long_name
            {"other_field": "value"},  # Missing attributes
        ]
        mock_client.get_routes.return_value = routes
        
        result = get_subway_route_names(mock_client)
        
        # Should only include valid routes
        assert result == ["Red Line"]


class TestRunQuestion1:
    """Tests for run_question_1."""
    
    @patch("questions.question1.get_subway_route_names")
    @patch("builtins.print")
    def test_run_question_1_prints_routes(self, mock_print, mock_get_names):
        """Test that route names are printed."""
        mock_get_names.return_value = ["Red Line", "Blue Line"]
        
        run_question_1()
        
        printed = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("Red Line" in str(p) for p in printed)
        assert any("Blue Line" in str(p) for p in printed)
    
    @patch("questions.question1.MBTAClient")
    @patch("questions.question1.get_subway_route_names")
    @patch("builtins.print")
    def test_run_question_1_calls_helper(self, mock_print, mock_get_names, mock_client_class):
        """Test that run_question_1 calls get_subway_route_names."""
        mock_get_names.return_value = []
        
        run_question_1()
        
        mock_get_names.assert_called_once()
    
    @patch("questions.question1.get_subway_route_names")
    def test_run_question_1_api_error(self, mock_get_names):
        """Test error handling when API fails."""
        mock_get_names.side_effect = RuntimeError("API error")
        
        with pytest.raises(RuntimeError):
            run_question_1()