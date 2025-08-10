from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
from utils.logger import setup_logger
from typing import Union, Iterable, Optional
import os

class BasePage:
    """Central base page providing wrapped Playwright actions with logging & resiliency."""

    def __init__(self, page: Page):
        self.page = page
        self.logger = setup_logger(self.__class__.__name__)

    # Navigation
    def goto(self, url: str):
        self.logger.info(f"Navigate: {url}")
        self.page.goto(url)

    def reload(self):
        self.logger.info("Reload page")
        self.page.reload()

    # Locator helpers (role-first, semantic friendly)
    def by_role(self, role: str, name: Optional[str] = None, exact: bool = False) -> Locator:
        self.logger.debug(f"Get by role={role} name={name} exact={exact}")
        return self.page.get_by_role(role, name=name, exact=exact)

    def by_text(self, text: str, exact: bool = False) -> Locator:
        self.logger.debug(f"Get by text='{text}' exact={exact}")
        return self.page.get_by_text(text, exact=exact)

    def by_label(self, text: str, exact: bool = False) -> Locator:
        self.logger.debug(f"Get by label='{text}' exact={exact}")
        return self.page.get_by_label(text, exact=exact)

    def locator(self, selector: str) -> Locator:
        self.logger.debug(f"Create locator: {selector}")
        return self.page.locator(selector)

    # Generic element actions
    def click(self, target: Union[str, Locator], *, force: bool = False):
        loc = self._ensure_locator(target)
        self.logger.info(f"Click: {self._describe(loc)} (force={force})")
        loc.click(force=force)

    def fill(self, target: Union[str, Locator], text: str, *, clear: bool = True):
        loc = self._ensure_locator(target)
        self.logger.info(f"Fill: '{text}' into {self._describe(loc)} (clear={clear})")
        if clear:
            loc.fill("")
        loc.fill(text)

    def type(self, target: Union[str, Locator], text: str, delay: float = 0.0):
        loc = self._ensure_locator(target)
        self.logger.info(f"Type: '{text}' into {self._describe(loc)} delay={delay}")
        loc.type(text, delay=delay)

    def get_text(self, target: Union[str, Locator]) -> str:
        loc = self._ensure_locator(target)
        value = loc.text_content() or ""
        self.logger.debug(f"Text from {self._describe(loc)} => '{value.strip()}'")
        return value.strip()

    def is_visible(self, target: Union[str, Locator]) -> bool:
        loc = self._ensure_locator(target)
        visible = loc.is_visible()
        self.logger.debug(f"Visible? {self._describe(loc)} => {visible}")
        return visible

    def expect_visible(self, target: Union[str, Locator], timeout: int = 10000):
        loc = self._ensure_locator(target)
        self.logger.info(f"Expect visible: {self._describe(loc)} within {timeout}ms")
        expect(loc).to_be_visible(timeout=timeout)
        return loc

    def expect_count(self, target: Union[str, Locator], expected: int, timeout: int = 10000):
        loc = self._ensure_locator(target)
        self.logger.info(f"Expect count={expected} for {self._describe(loc)} within {timeout}ms")
        expect(loc).to_have_count(expected, timeout=timeout)
        return loc

    def screenshot(self, name: str):
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", name)
        self.logger.info(f"Screenshot: {path}")
        self.page.screenshot(path=path, full_page=True)
        return path

    # Internal helpers
    def _ensure_locator(self, target: Union[str, Locator]) -> Locator:
        return target if isinstance(target, Locator) else self.locator(target)

    def _describe(self, locator: Locator) -> str:
        try:
            return locator.to_string()
        except Exception:
            return str(locator)
