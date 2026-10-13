from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class CartPage(BasePage):
    CART_DRAWER = (By.CSS_SELECTOR, '[data-testid="cart-drawer"]')
    CART_ITEM = (By.CSS_SELECTOR, '[data-testid="cart-item"]')
    CART_TOTAL = (By.CSS_SELECTOR, '[data-testid="cart-total"]')
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-testid="checkout-button"]')
    ORDER_SUCCESS = (By.CSS_SELECTOR, '[data-testid="order-success"]')
    ORDER_NO = (By.CSS_SELECTOR, '[data-testid="order-no"]')

    def wait_until_open(self):
        self.find(self.CART_DRAWER)
        return self

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEM))

    def total(self) -> str:
        return self.text_of(self.CART_TOTAL)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self

    def is_order_success_visible(self) -> bool:
        return self.is_visible(self.ORDER_SUCCESS)

    def order_no(self) -> str:
        return self.text_of(self.ORDER_NO)
