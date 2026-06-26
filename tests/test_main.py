"""Tests for main module"""
 
import pytest
from unittest.mock import patch
from main import main
 
 
class TestMain:
    """Tests for main function."""
    
    @patch("main.run_question_3")
    @patch("main.run_question_2")
    @patch("main.run_question_1")
    def test_main_calls_all_questions(self, mock_q1, mock_q2, mock_q3):
        """Test that main calls all three questions in order."""
        mock_q2.return_value = {}
        
        main(None)
        
        mock_q1.assert_called_once()
        mock_q2.assert_called_once()
        mock_q3.assert_called_once()
    
    @patch("main.run_question_3")
    @patch("main.run_question_2")
    def test_main_passes_q2_result_to_q3(self, mock_q2, mock_q3):
        """Test that Q2 result is passed to Q3."""
        routes_stops = {"Red": {"name": "Red Line", "stops": []}}
        mock_q2.return_value = routes_stops
        
        main(None)
        
        mock_q3.assert_called_once_with(routes_stops)
    
    @patch("main.run_question_1")
    @patch("builtins.print")
    def test_main_handles_runtime_error(self, mock_print, mock_q1):
        """Test error handling when RuntimeError occurs."""
        mock_q1.side_effect = RuntimeError("API error")
        
        main(None)
        
        printed = [str(call[0][0]) for call in mock_print.call_args_list]
        assert any("API error" in str(p) for p in printed)
    
    @patch("main.run_question_3")
    @patch("main.run_question_2")
    @patch("main.run_question_1")
    def test_main_q2_error_stops_execution(self, mock_q1, mock_q2, mock_q3):
        """Test that error in Q2 stops Q3 from running."""
        mock_q2.side_effect = RuntimeError("Q2 failed")
        
        main(None)
        
        mock_q3.assert_not_called()
    
    @patch("main.run_question_3")
    @patch("main.run_question_2")
    @patch("main.run_question_1")
    def test_main_completes_without_exception(self, mock_q1, mock_q2, mock_q3):
        """Test that main completes successfully."""
        mock_q2.return_value = {}
        try:
            main(None)
        except Exception as e:
            pytest.fail(f"main() raised {type(e).__name__}: {e}")