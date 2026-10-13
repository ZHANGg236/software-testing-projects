from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class ProductPage(BasePage):
    PRODUCT_CARD = (By.CSS_SELECTOR, '[data-testid="product-card"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[data-testid="product-name"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-testid="search-input"]')
    CATEGORY_SELECT = (By.CSS_SELECTOR, '[data-testid="category-select"]')
    CART_BUTTON = (By.CSS_SELECTOR, '[data-testid="cart-button"]')
    CART_COUNT = (By.CSS_SELECTOR, '[data-testid="cart-count"]')
    EMPTY_RESULT = (By.CSS_SELECTOR, '[data-testid="empty-result"]')

    def open_home(self):
        self.open("/")
        self.find(self.PRODUCT_CARD)
        return self

    def add_product(self, sku: str):
        locator = (By.CSS_SELECTOR, f'[data-testid="add-to-cart-{sku}"]')
        self.click(locator)
        return self

    def search(self, keyword: str):
        self.type(self.SEARCH_INPUT, keyword)
        return self

    def select_category(self, category: str):
        from selenium.webdriver.support.ui import Select

        element = self.find(self.CATEGORY_SELECT)
        Select(element).select_by_visible_text(category)
        return self

    def product_names(self) -> list[str]:
        elements = self.driver.find_elements(*self.PRODUCT_NAME)
        return [element.text.strip() for element in elements]

    def product_count(self) -> int:
        return len(self.driver.find_elements(*self.PRODUCT_CARD))

    def cart_count(self) -> int:
        return int(self.text_of(self.CART_COUNT))

    def open_cart(self):
        self.click(self.CART_BUTTON)
        return self

    def is_empty_result_visible(self) -> bool:
        return self.is_visible(self.EMPTY_RESULT)
