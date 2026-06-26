# MBTA Transit Analysis
 
A Python program that analyzes MBTA subway routes and finds paths between stops.
 
## What it does
 
1. **Lists all subway routes** - Shows all light rail and heavy rail routes
2. **Analyzes routes** - Finds routes with most/least stops and transfer points
3. **Path finding** - Finds subway route(s) between two stops using BFS
## Setup
 
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate
 
# Install dependencies
pip3 install -r requirements.txt
 
# Optional: Add API key to .env
echo "MBTA_API_KEY=your_key" > .env
```
 
## Run
 
```bash
# Run all questions
python3 main.py

# Run specific question
python3 main.py question1  # Question 1 only
python3 main.py question2  # Question 2 only
python3 main.py question3  # Question 2 + 3, 2 silent
```
 
## Run tests
 
```bash
python3 -m pytest tests/ -v
```
 
## Project structure
 
```
mbta-take-home/
├── api/mbta_client.py        # API client
├── questions/
│   ├── question1.py          # List routes
│   ├── question2.py          # Analyze routes
│   └── question3.py          # Find path
├── tests/                     # 36 tests
├── main.py                    # Entry point
└── requirements.txt
```
 
## Technologies
 
- Python 3.9+
- requests (HTTP client)
- pytest (testing)
 