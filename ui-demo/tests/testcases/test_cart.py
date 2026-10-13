import allure
import pytest

from config import DATA_DIR
from tests.pages.cart_page import CartPage
from tests.pages.login_page import LoginPage
from tests.pages.product_page import ProductPage
from utils.data_loader import load_yaml


SHOPPING_DATA = load_yaml(DATA_DIR / "shopping_data.yaml")
CART_CASES = SHOPPING_DATA["cart_cases"]
CHECKOUT_CASE = SHOPPING_DATA["checkout_case"]


@allure.epic("云选商城 UI 自动化")
@allure.feature("购物车")
@pytest.mark.smoke
@pytest.mark.parametrize(
    "case",
    CART_CASES,
    ids=[case["case_name"] for case in CART_CASES],
)
def test_add_products_to_cart(driver, base_url, case):
    """验证不同商品组合加入购物车后的数量和金额。"""
    product_page = ProductPage(driver, base_url).open_home()

    with allure.step(f"依次加入商品: {case['products']}"):
        for sku in case["products"]:
            product_page.add_product(sku)

    with allure.step("校验购物车角标数量"):
        actual_cart_count = product_page.cart_count()
        assert actual_cart_count == case["expected_cart_count"], (
            f"购物车角标不一致，实际值={actual_cart_count}，"
            f"预期值={case['expected_cart_count']}"
        )

    with allure.step("打开购物车"):
        product_page.open_cart()
        cart_page = CartPage(driver, base_url).wait_until_open()

    with allure.step("校验购物车条目和合计金额"):
        actual_item_count = cart_page.item_count()
        assert actual_item_count == case["expected_item_count"], (
            f"购物车条目数不一致，实际值={actual_item_count}，"
            f"预期值={case['expected_item_count']}"
        )
        actual_total = cart_page.total()
        assert actual_total == case["expected_total"], (
            f"购物车金额不一致，实际值={actual_total!r}，"
            f"预期值={case['expected_total']!r}"
        )


@allure.epic("云选商城 UI 自动化")
@allure.feature("订单结算")
@pytest.mark.smoke
def test_checkout_flow(driver, base_url):
    """验证登录、加入多个商品、进入购物车并提交订单的完整流程。"""
    case = CHECKOUT_CASE
    login_page = LoginPage(driver, base_url).open()

    with allure.step("使用测试账号登录"):
        login_page.login_as_standard_user()
        assert login_page.is_logged_in(), "登录后应显示当前用户信息"

    product_page = ProductPage(driver, base_url)
    with allure.step("加入结算需要的商品"):
        for sku in case["products"]:
            product_page.add_product(sku)

    with allure.step("校验结算前购物车信息"):
        actual_cart_count = product_page.cart_count()
        assert actual_cart_count == case["expected_cart_count"], (
            f"购物车角标不一致，实际值={actual_cart_count}，"
            f"预期值={case['expected_cart_count']}"
        )
        product_page.open_cart()
        cart_page = CartPage(driver, base_url).wait_until_open()
        actual_total = cart_page.total()
        assert actual_total == case["expected_total"], (
            f"结算金额不一致，实际值={actual_total!r}，预期值={case['expected_total']!r}"
        )

    with allure.step("提交订单"):
        cart_page.checkout()

    with allure.step("校验订单成功提示和购物车清空"):
        assert cart_page.is_order_success_visible(), (
            "预期显示订单提交成功提示，实际没有显示"
        )
        assert cart_page.order_no().startswith("ORD"), (
            f"订单号格式不正确，实际值={cart_page.order_no()!r}"
        )
        assert product_page.cart_count() == 0, (
            f"订单提交后购物车应清空，实际角标={product_page.cart_count()}"
        )
