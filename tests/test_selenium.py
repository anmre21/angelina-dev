"""Perform a Google search using Selenium and a headless Chrome browser."""
import subprocess
from pathlib import Path
import queue

import selenium
import selenium.webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def test_selenium():
    """Perform a Google search using Selenium and a headless Chrome browser."""

    # Configure Selenium
    #
    # Pro-tip: remove the "headless" option and set a breakpoint.  A Chrome
    # browser window will open, and you can play with it using the developer
    # console.
    options = selenium.webdriver.chrome.options.Options()
    options.add_argument("--headless")

    s=Service(ChromeDriverManager().install())
    driver = selenium.webdriver.Chrome(service=s, options=options)

    # An implicit wait tells WebDriver to poll the DOM for a certain amount of
    # time when trying to find any element (or elements) not immediately
    # available. Once set, the implicit wait lasts for the life of the
    # WebDriver object.
    #
    # https://selenium-python.readthedocs.io/waits.html#implicit-waits
    driver.implicitly_wait(1)

    # Load localhost page
    driver.get("http://127.0.0.1:5000")

    # Find all links
    visited = []
    links = [l.get_attribute("href") for l in 
             driver.find_elements(By.XPATH, "//a[@href]")]
    if not links:
        links = ["http://127.0.0.1:5000/home"]

    while len(links) > 0:
        # Visit next link in the list
        link = links.pop(0)
        # If link is not localhost, skip
        if "http://127.0.0.1:5000/" not in link:
            continue
        # print(f"Testing {link}")
        driver.get(link)

        # Check if page does not exist
        if "404" in str(driver.title):
            print(f"[ERROR] Linked page not found: {link}")
            exit(1)

        # Check if navbar is present (not blank page)
        try:
            driver.find_element(By.CLASS_NAME, "navbar")
        except:
            print(f"[ERROR] Navbar not found, page may be empty: {link}")
            exit(1)

        # If it's a blog post, print title
        if "/blog/" in link:
            try:
                print("Blog post:", driver.find_element(By.TAG_NAME, "h1").text)
            except:
                print(f"[ERROR] Title not found, page may be empty: {link}")
                exit(1)

        # Add more links to list
        visited.append(link)
        new_links = driver.find_elements(By.XPATH, "//a[@href]")
        new_links = set([l.get_attribute("href") for l in new_links])
        new_links = new_links.difference(visited, set(links))
        links.extend(new_links)
        # print(f"Link set = ", links)

    # Cleanup
    driver.quit()


if __name__ == "__main__":
    test_selenium()
