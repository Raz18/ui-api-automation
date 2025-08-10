
import os
import sys
import pytest
from playwright.sync_api import sync_playwright, Playwright, APIRequestContext, Page, Browser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import setup_logger
from config.settings import api_settings, ui_settings, airports
from pathlib import Path

logger = setup_logger("Fixtures")

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=ui_settings.headless, slow_mo=ui_settings.slowmo)
    logger.info(f"Launched Chromium browser headless={ui_settings.headless} slow_mo={ui_settings.slowmo}ms")
    yield browser
    browser.close()
    logger.info("Browser closed")

@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def api_request_context(playwright_instance):
    """A session-scoped fixture for the Playwright APIRequestContext."""
    request_context = playwright_instance.request.new_context(
        base_url=api_settings.base_url,
        timeout=api_settings.timeout,
        extra_http_headers={
            "Accept": "application/json",
            "User-Agent": "ui-api-automation-tests/1.0"
        }
    )
    logger.info(f"Created API request context with base_url={api_settings.base_url}")
    yield request_context
    request_context.dispose()
    logger.info("Disposed API request context")

@pytest.fixture
def airports_test_data():
    """Provide airports configuration for tests."""
    return airports