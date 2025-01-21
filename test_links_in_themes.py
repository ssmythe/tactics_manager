import os
import requests
from bs4 import BeautifulSoup
import pytest

# Path to the themes.html file
HTML_FILE = "index.html"

# Fixture to parse the HTML file
@pytest.fixture
def parsed_html():
    if not os.path.exists(HTML_FILE):
        raise FileNotFoundError(f"The file {HTML_FILE} does not exist.")
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    return soup

# Test to check all links in the HTML file
@pytest.mark.parametrize("link", [
    pytest.param(a["href"], id=a.text.strip())
    for a in BeautifulSoup(open(HTML_FILE, encoding="utf-8"), "html.parser").find_all("a", href=True)
])
def test_links_exist(link):
    """Test to ensure all links are reachable."""
    response = requests.head(link, allow_redirects=True, timeout=10)
    assert response.status_code == 200, f"Broken link: {link} (Status code: {response.status_code})"
