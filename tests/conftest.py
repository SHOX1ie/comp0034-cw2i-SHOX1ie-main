import os
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    """pytest extra command line arguments for running chrome driver

     For GitHub Actions or similar container you need to run it headless.
     When writing the tests and running locally it may be useful to
     see the browser and so you need to see the browser.
    """
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    return options
