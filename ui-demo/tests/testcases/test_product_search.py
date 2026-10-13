import allure
import pytest

from config import DATA_DIR
from tests.pages.product_page import ProductPage
from utils.data_loader import load_yaml


SEARCH_CASES = load_yaml(DATA_DIR / "shopping_data.yaml")["search_cases"]


@allure.epic("云选商城 UI 自动化")
@allure.feature("商品搜索")
@pytest.mark.regression
@pytest.mark.parametrize(
    "case",
    SEARCH_CASES,
    ids=[case["case_name"] for case in SEARCH_CASES],
)
def test_search_product(driver, base_url, case):
    """验证商品名称搜索和空结果提示。"""
    product_page = ProductPage(driver, base_url).open_home()

    with allure.step(f"搜索关键字: {case['keyword']}"):
        product_page.search(case["keyword"])

    with allure.step("校验搜索结果"):
        actual_names = product_page.product_names()
        assert actual_names == case["expected_names"], (
            f"搜索结果不一致，实际值={actual_names!r}，预期值={case['expected_names']!r}"
        )
        if not case["expected_names"]:
            assert product_page.is_empty_result_visible(), (
                "预期显示空结果提示，实际没有显示"
            )
