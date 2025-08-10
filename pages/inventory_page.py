from playwright.sync_api import Page
from pages.base_page import BasePage
from typing import List

class InventoryPage(BasePage):
    """Inventory page object for SauceDemo.

    Uses explicit data-test / id attributes for stable selectors.
    All locator definitions are centralized as class constants for readability & reuse.
    """

    # URL
    URL_FRAGMENT = '/inventory.html'

    # --- Locators (data-test / ids from provided HTML) ---
    INVENTORY_ITEM = '[data-test="inventory-item"]'
    INVENTORY_LIST = '[data-test="inventory-list"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    ITEM_DESC = '[data-test="inventory-item-desc"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    ADD_TO_CART_BTNS = 'button[data-test^="add-to-cart-"]'
    REMOVE_BTNS = 'button[data-test^="remove-"]'
    CART_BADGE = '.shopping_cart_badge'
    CART_LINK = '[data-test="shopping-cart-link"]'
    SORT_SELECT = '[data-test="product-sort-container"]'
    ACTIVE_SORT = '[data-test="active-option"]'
    MENU_BUTTON = '#react-burger-menu-btn'
    RESET_STATE_LINK = '#reset_sidebar_link'

    # --- Element accessors ---
    @property
    def inventory_items(self):
        return self.locator(self.INVENTORY_ITEM)

    @property
    def add_buttons(self):
        return self.locator(self.ADD_TO_CART_BTNS)

    @property
    def cart_badge(self):
        return self.locator(self.CART_BADGE)

    def add_first_item_to_cart(self):
        self.logger.info("Adding first item to cart")
        self.click(self.add_buttons.first)
        return self

    # New generic cart operations
    def add_items_to_cart(self, number: int) -> int:
        """Add a specified number of items (or all available if fewer). Returns count actually added."""
        available = self.add_buttons.count()
        to_add = min(number, available)
        self.logger.info(f"Requested to add {number} items, available add buttons: {available}. Will add {to_add}.")
        added = 0
        for i in range(to_add):
            self.click(self.add_buttons.first)
            added += 1
        self.logger.info(f"Added {added} items to cart")
        return added

    def add_all_items_to_cart(self) -> int:
        """Click all remaining 'Add to cart' buttons until none left. Returns total added."""
        added = 0
        while self.add_buttons.count() > 0:
            self.click(self.add_buttons.first)
            added += 1
        self.logger.info(f"All items added. Total={added}")
        return added

    # Helper getters
    def get_all_item_names(self) -> List[str]:
        names = [el.text_content().strip() for el in self.page.query_selector_all(self.ITEM_NAME)]
        self.logger.info(f"Collected item names: {names}")
        return names

    def get_all_prices(self) -> List[str]:
        prices = [el.text_content().strip() for el in self.page.query_selector_all(self.ITEM_PRICE)]
        self.logger.info(f"Collected item prices: {prices}")
        return prices

    # Assertions / expectations
    def assert_items_count(self, expected: int):
        self.expect_count(self.inventory_items, expected)
        return self

    def assert_cart_count(self, expected: int):
        # If expected is 0, badge may be absent. Handle gracefully.
        if expected == 0:
            visible = self.is_visible(self.CART_BADGE)
            actual = 0 if not visible else int(self.get_text(self.cart_badge))
            assert actual == 0, f"Expected empty cart (0) but badge showed {actual}" 
            self.logger.info("Cart is empty as expected")
            return self
        self.expect_visible(self.cart_badge)
        actual = self.get_text(self.cart_badge)
        assert actual == str(expected), f"Cart badge expected {expected} got {actual}"
        return self
