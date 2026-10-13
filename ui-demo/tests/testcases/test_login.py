import allure
import pytest

from config import DATA_DIR
from tests.pages.login_page import LoginPage
from utils.data_loader import load_yaml


LOGIN_CASES = load_yaml(DATA_DIR / "login_data.yaml")["login_cases"]


@allure.epic("云选商城 UI 自动化")
@allure.feature("登录模块")
@pytest.mark.smoke
@pytest.mark.parametrize(
    "case",
    LOGIN_CASES,
    ids=[case["case_name"] for case in LOGIN_CASES],
)
def test_login(driver, base_url, case):
    """使用 YAML 中的数据验证正确和错误账号的登录结果。"""
    login_page = LoginPage(driver, base_url).open()

    with allure.step("打开登录窗口"):
        login_page.open_login()

    with allure.step(f"输入账号 {case['username']} 并提交"):
        login_page.login(case["username"], case["password"])

    if case["expected_success"]:
        with allure.step("校验登录成功"):
            assert login_page.is_logged_in(), (
                f"预期登录成功并显示用户信息，实际没有显示；"
                f"用例={case['case_name']}"
            )
            actual_user = login_page.current_user()
            assert actual_user == case["expected_message"], (
                f"登录用户不一致，实际值={actual_user!r}，预期值={case['expected_message']!r}"
            )
        return

    with allure.step("校验错误提示"):
        actual_message = login_page.error_message()
        assert actual_message == case["expected_message"], (
            f"错误提示不一致，实际值={actual_message!r}，预期值={case['expected_message']!r}"
        )
