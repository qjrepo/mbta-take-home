# AI Prompts
 
I used AI to assist with test generation and documentation during this assessment. Below are the prompts and how I used the output.
 
---
 
## 1. Test Generation
 
I used AI to generate comprehensive pytest tests for all five modules. Here are the prompts I used:
 
### Prompt 1: Main Module Tests
```
I have a main orchestration function that runs three questions in sequence.
Can you write pytest tests covering:
- All three questions are called in order when question=None
- Question 2 result is passed to Question 3
- Error handling when RuntimeError occurs
- Question 3 doesn't run if Question 2 fails
Use mocks for the question functions to isolate main() logic.
```
 
**How I used it:**
- Verified tests matched my actual implementation
- Reviewed error handling logic and the mocking patterns
---
 
### Prompt 2: MBTA API Client Tests
```
I have an MBTA API client class that handles HTTP requests and error handling. 
Can you help me write comprehensive pytest tests that cover:
- Successful API responses with JSON parsing
- API key initialization (with and without key)
- ConnectionError, Timeout, HTTPError scenarios
- Invalid JSON response handling
- The get_routes() and get_stops_for_route() wrapper methods
Use mocking to avoid real API calls.
```
 
**How I used it:**
- Verified error messages matched my actual RuntimeError implementation
- Confirmed mock return values matched actual API response structure
---
 
### Prompt 3: Question 1 Tests
```
Write pytest tests for question1 functions:
- get_subway_route_names() with valid routes, empty results, and missing/invalid attributes
- run_question_1() - test that it prints routes correctly, calls helper function, and handles API errors
Mock the MBTAClient to test logic in isolation.
```
 
**How I used it:**
- Verified test expectations matched my implementation
- Reviewed edge cases for missing attributes and error handling
---
 
### Prompt 4: Question 2 Tests
```
I need tests for all analysis functions in question2:
- build_routes_stops_mapping() - creates routes_stops and stop_routes mappings, handles missing attributes
- calculate_stop_counts() - counts stops per route
- find_max_min_routes() - finds which routes have the most and fewest stops
- find_transfer_stops() - identifies stops serving 2+ routes
- run_question_2() - integration tests for return values and error handling
Include edge cases like missing attributes and empty results.
```
 
**How I used it:**
- Verified the mock data structures matched my routes_stops and stop_routes mappings
- Reviewed test edge cases for missing attributes and empty results
---
 
### Prompt 5: Question 3 Tests
```
Write pytest tests for question3 functions:
- bfs_find_routes() with three scenarios: single-route path, multi-route with transfer, no path exists
- get_stop_id_user() handling: single match, multiple matches (user picks one), invalid input with retry
- run_question_3() testing: same start/end stop, successful pathfinding, no route exists
Mock input() and test with realistic MBTA stop data.
```
 
**How I used it:**
- Verified the tests and reviewed all three BFS scenarios (single-route, transfers, no path)
- Reviewed the input mocking patterns for retry logic and multiple stops with same name
- Verified edge cases for pathfinding output
---
 
## 2. Documentation & Comments
 
I used AI to assist with generating comprehensive docstrings.
 
### Prompt 6: API Client & Main Module Docstrings
```
Generate detailed docstrings for:
 
1. MBTAClient class:
   - Explain the purpose of each method (get(), get_routes(), get_stops_for_route())
   - Document error handling (ConnectionError, Timeout, HTTPError, Invalid JSON response)
   - Explain parameters and return values
   - Add notes about implementation details (API key management, timeout, etc.)
 
2. Main orchestration function:
   - Explain how the three questions flow together
   - Document question interactions (Question2 data passed to Question3)
   - Note error handling strategy
 
Use format with Args, Returns, Note sections.
```
 
**How I used it:**
- Verified all technical details matched my implementation
- Ensured error handling descriptions were accurate
### Prompt 7: Question Module Docstrings
```
Generate comprehensive docstrings for question functions. Use different formats based on function type:
 
For helper/utility functions (with parameters and returns):
- Summary
- Args section
- Returns section  
- Note section (optional, for implementation details)
 
For main orchestration functions (no parameters or simple parameters):
- Clear summary of what the function does
- No rigid structure required—focus on clarity explaining the process
 
Functions to document:
 
Question 1:
- get_subway_route_names() - helper, needs Args/Returns/Note
- run_question_1() - orchestration function
 
Question 2:
- build_routes_stops_mapping() - helper, needs Args/Returns
- calculate_stop_counts() - helper, needs Args/Returns
- find_max_min_routes() - helper, needs Args/Returns
- find_transfer_stops() - helper, needs Args/Returns
- run_question_2() - orchestration function
 
Question 3:
- bfs_find_routes() - helper, needs Args/Returns/Note
- get_stop_id_user() - helper, needs Args/Returns/Note
- run_question_3() - orchestration function
```
 
**How I used it:**
- Reviewed all docstrings for accuracy against the actual code implementation

 