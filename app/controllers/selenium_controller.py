import time
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

router = APIRouter()

# Selenium grid URL
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
    Extract text from an element using CSS selector with validation
    """
    driver = None
    start_time = time.time()

    try:
        driver = create_driver()
        driver.get(url)

        # Check if page loaded correctly
        if "error" in driver.title.lower() or "404" in driver.title.lower():
            return {
                "status": "error",
                "message": f"Page loaded with error title: {driver.title}",
                "execution_time_ms": int((time.time() - start_time) * 1000)
            }

        # Use explicit wait instead of just finding the element
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            text = element.text

            # Validate that we got meaningful content
            if not text or len(text.strip()) == 0:
                return {
                    "status": "warning",
                    "message": "Element found but contains no text",
                    "text": "",
                    "execution_time_ms": int((time.time() - start_time) * 1000)
                }

            return {
                "status": "success",
                "text": text,
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "page_title": driver.title,
                "element_found": True
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Element not found: {str(e)}",
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "page_title": driver.title,
                "element_found": False
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "execution_time_ms": int((time.time() - start_time) * 1000)
        }
    finally:
        if driver:
            driver.quit()

@router.post("/click")
def click_element(url: str, css_selector: str) -> Dict[str, Any]:
    """
    Click an element using CSS selector
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