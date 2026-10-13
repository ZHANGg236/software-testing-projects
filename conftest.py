import re
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

from config import DEFAULT_TIMEOUT, EDGE_DRIVER_PATH, HEADLESS, SCREENSHOT_DIR, WEB_ROOT


def _safe_filename(name: str) -> str:
    """把 pytest 转义出来的 \\uXXXX 还原成汉字，并清洗 Windows 非法字符。"""
    # 1) 把字面量 \u6b63 还原成 正
    name = re.sub(
        r"\\u([0-9a-fA-F]{4})",
        lambda m: chr(int(m.group(1), 16)),
        name,
    )
    # 2) 替换 Windows 文件名非法字符
    name = re.sub(r'[\\/:*?"<>|\r\n\t]+', "_", name)
    # 3) 去掉首尾空白和点，限制长度
    name = name.strip(" ._")
    return name[:150] or "screenshot"


class QuietHttpHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return


@pytest.fixture(scope="session")
def base_url():
    handler = partial(QuietHttpHandler, directory=str(WEB_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{server.server_port}"
    yield url

    server.shutdown()
    server.server_close()
    thread.join(timeout=3)


@pytest.fixture
def driver(request):
    options = EdgeOptions()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if HEADLESS:
        options.add_argument("--headless=new")

    service = EdgeService(executable_path=EDGE_DRIVER_PATH) if EDGE_DRIVER_PATH else EdgeService()
    browser = webdriver.Edge(service=service, options=options)
    browser.set_page_load_timeout(DEFAULT_TIMEOUT + 10)
    browser.implicitly_wait(0)

    yield browser

    try:
        rep = getattr(request.node, "rep_call", None)
        if rep is not None and rep.failed:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            filename = _safe_filename(request.node.name)
            screenshot_path = SCREENSHOT_DIR / f"{filename}.png"

            try:
                browser.save_screenshot(str(screenshot_path))
                allure.attach.file(
                    str(screenshot_path),
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as exc:
                print(f"[conftest] 保存失败截图出错: {exc}")
                print(f"[conftest] 目标路径: {screenshot_path}")
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
