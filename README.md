# COMP0034 2023/24 Coursework 2 starter repostitory (Dash App)

## Set-up
1. Create and activate a virtual environment in the project folder e.g.
    - MacOS: `python3 -m venv .venv` then `source .venv/bin/activate`
    - Windows: `py -m venv .venv` then `.venv\Scripts\activate`

2. Check `pip` is the latest versions: `pip install --upgrade pip`

3. Install the requirements. 
    - e.g. `pip install -r requirements.txt`

4. Install the paralympics app code e.g. `pip install -e .`

## Running the apps in the src directory
- Run the `app.py` file using Python.
    - e.g.: `python src/app.py`. 
    The Dash app should now be running on your localhost. Open a web browser and enter the URL provided in the terminal to view the app.
    This Dash app contains 4 pages: Home, Undergraduate, Postgraduate and Analysis. Each of them contains interactive charts.

## Running the tests in the tests directory
- Execute the tests with pytest when the server is running:
    - e.g.: `pytest`
    The test runner will discover and execute all test functions defined in the `tests` directory.
