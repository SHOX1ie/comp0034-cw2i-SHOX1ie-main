import requests
from dash.testing.application_runners import import_app
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService


# Test function to check if the server is live
def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to make a HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
    assert response.status_code == 200


# Test function to check the Home page H1 heading text
def test_home_h1textequals(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading text should be "Home"
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Wait for the H1 heading to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text

    # Check the heading has the text we expect
    assert h1_text == "Home"


# Test function to check the Home page access
def test_home_page_access():
    # Define the URL of the home page
    home_page_url = "http://127.0.0.1:8050/"

    # Send a GET request to the home page URL
    response = requests.get(home_page_url)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200, "Failed to access home page URL"


# Test function to check the Undergraduate page access by nav link
def test_nav_link_undergraduate(dash_duo):
    """
    Check the nav link works and leads to the undergraduate page.
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)
    # Time delay
    time.sleep(1)

    # Wait for the navlink to be visible
    dash_duo.wait_for_element("#nav-undergraduate", timeout=4)

    # Click on the navlink
    dash_duo.driver.find_element(By.ID, "nav-undergraduate").click()

    # Time delay
    time.sleep(1)

    # Check the page url includes "Undergraduate"
    dash_duo.wait_for_element("#nav-undergraduate", timeout=4)
    assert "Undergraduate" in dash_duo.driver.current_url


# Test function to check the Home page
def test_select_time_period_dropdown_home(dash_duo):
    """
    GIVEN the home page is loaded
    WHEN the user selects a time period from the dropdown menu
    THEN the corresponding data should be displayed on the page
    """
    # Start the Dash application server
    app = import_app("src.app")
    dash_duo.start_server(app)

    # Wait for the time period dropdown to be visible
    dash_duo.wait_for_element("#time_period_dropdown_h", timeout=4)

    # Select a different time period from the dropdown menu
    dash_duo.select_dcc_dropdown("#time_period_dropdown_h", index=1)  # Select the second time period

    # Wait for the pie chart total element to be present
    dash_duo.wait_for_element("#pie_chart_total", timeout=4)

    # Get the updated data displayed on the page
    updated_data = dash_duo.find_element("#pie_chart_total").text

    # Verify that the displayed data has changed after selecting a different time period
    assert updated_data != ""


# Test function to check the Undergraduate page
def test_select_time_period_dropdown_undergraduate(dash_duo):
    """
    GIVEN the undergraduate page is loaded
    WHEN the user selects a time period from the dropdown menu
    THEN the corresponding data should be displayed on the page
    """
    # Start the Dash application server
    app = import_app("src.app")
    dash_duo.start_server(app)

    # Navigate to the Undergraduate page
    dash_duo.driver.get("http://127.0.0.1:8050/Undergraduate")

    # Wait for the time period dropdown to be visible
    dash_duo.wait_for_element("#time_period_dropdown_u", timeout=4)

    # Select a different time period from the dropdown menu
    dash_duo.select_dcc_dropdown("#time_period_dropdown_u", index=1)  # Select the second time period

    # Wait for the bar chart element to be present
    dash_duo.wait_for_element("#bar_u", timeout=4)

    # Get the updated data displayed on the page
    updated_data = dash_duo.find_element("#bar_u").text

    # Verify that the displayed data has changed after selecting a different time period
    assert updated_data != ""


def test_dropdown_analysis(dash_duo):
    """
    GIVEN the app is running
    WHEN the Analysis page is available
    THEN the dropdown should be visible
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)
    dash_duo.driver.get("http://127.0.0.1:8050/Analysis")
    # To find an element by id you use '#id-name'; to find an element by class use '.class-name'
    dash_duo.wait_for_element("#feature_dropdown", timeout=3)

    # Find the dropdown element by id
    dropdown_input = dash_duo.find_element("#feature_dropdown")
    dropdown_input.send_keys("Age Under 25")
    dash_duo.driver.implicitly_wait(3)

    # Run the app and use Chrome browser, find the element, right click and choose Select, find the element in the
    # Elements console and select 'copy selector'. Pate this as the value of the variable e.g. see css_selector below.
    css_selector = '#line_chart_a > div.js-plotly-plot > div > div > svg:nth-child(3) > g.infolayer > g.g-gtitle > text'
    chart_title = dash_duo.find_element(css_selector)
    assert ("pct_total_age_u25" in chart_title.text), "'pct_total_age_u25' should appear in the chart title"
