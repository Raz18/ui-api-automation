import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.settings import credentials
from utils.logger import setup_logger

logger = setup_logger("UI_Tests")


@pytest.mark.ui
def test_inventory_page_has_six_items(page: Page):
    logger.info("Starting test: Verify inventory page has six items")
    
    logger.info(f"Logging in with user: {credentials.username}")
    LoginPage(page).open().login(credentials.username, credentials.password)
    logger.info("Successfully logged in to SauceDemo")
    
    inventory = InventoryPage(page)
    logger.info("Navigated to inventory page")
    
    inventory.assert_items_count(6)
    logger.info("Inventory count assertion passed")
    
    names = inventory.get_all_item_names()
    logger.info(f"Retrieved item names: {names}")
    
    actual_count = len(names)
    assert actual_count == 6, f"Expected 6 item names, got {actual_count}"
    logger.info(f"Test passed: Found {actual_count} items as expected")

@pytest.mark.ui
def test_add_single_item_increments_cart(page: Page):
    logger.info("Starting test: Add single item increments cart")
    
    logger.info("Logging in with default credentials")
    LoginPage(page).open().login()  # uses default credentials from settings
    logger.info("Successfully logged in to SauceDemo")
    
    inventory = InventoryPage(page)
    logger.info("Navigated to inventory page")
    
    logger.info("Adding 1 item to cart")
    added = inventory.add_items_to_cart(1)
    logger.info(f"Successfully added {added} item(s) to cart")
    
    assert added == 1, f"Expected to add 1 item, added {added}"
    
    inventory.assert_cart_count(1)
    logger.info(" Test passed: Cart count correctly shows 1 item")


#BONUS TEST
@pytest.mark.ui
def test_add_all_items_results_in_cart_count_six(page: Page):
    logger.info("Starting test: Add all items results in cart count six")
    
    logger.info("Logging in with default credentials")
    LoginPage(page).open().login()
    logger.info("Successfully logged in to SauceDemo")
    
    inventory = InventoryPage(page)
    logger.info("Navigated to inventory page")
    
    logger.info("Verifying initial inventory count")
    inventory.assert_items_count(6)
    logger.info("Confirmed 6 items available in inventory")
    
    logger.info("Adding all items to cart")
    added = inventory.add_all_items_to_cart()
    logger.info(f"Successfully added {added} item(s) to cart")
    
    assert added == 6, f"Expected to add 6 items, added {added}"
    
    inventory.assert_cart_count(6)
    logger.info("Test passed: Cart count correctly shows 6 items (all items added)")
