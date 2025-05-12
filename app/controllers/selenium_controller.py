from fastapi import APIRouter, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydantic import BaseModel
from typing import Dict, Any
import time

router = APIRouter()

# Selenium grid URL (same as in the Java version)
SELENIUM_GRID_URL = "http://localhost:4444/wd/hub"


def create_driver():
    """Create and configure a remote Chrome WebDriver"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Remote(
            command_executor=SELENIUM_GRID_URL,
            options=options
        )
        driver.implicitly_wait(10)  # Set implicit wait time
        return driver
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create WebDriver: {str(e)}")


@router.post("/navigate")
def navigate_to_url(url: str) -> Dict[str, Any]:
    """
    Navigate to a URL and return the page title
    Equivalent to the navigateToUrl method in SeleniumController.java
    """
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        title = driver.title

        return {
            "status": "success",
            "title": title
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if driver:
            driver.quit()


@router.post("/extract-text")
def extract_text(url: str, css_selector: str) -> Dict[str, Any]:
    """
    Extract text from an element using CSS selector
    Equivalent to the extractText method in SeleniumController.java
    """
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        text = element.text

        return {
            "status": "success",
            "text": text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if driver:
            driver.quit()


@router.post("/click")
def click_element(url: str, css_selector: str) -> Dict[str, Any]:
    """
    Click an element using CSS selector
    Equivalent to the clickElement method in SeleniumController.java
    """
    driver = None
    try:
        driver = create_driver()
        driver.get(url)
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()

        return {
            "status": "success",
            "message": "Element clicked successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    finally:
        if driver:
            driver.quit()