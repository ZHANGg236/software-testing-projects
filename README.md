# 云选商城 UI 自动化练习

这是我在学习 Selenium 和 pytest 时整理的一个 UI 自动化练习。外部网站经常会改版，测试数据也不方便控制，所以我写了一个简单的本地电商页面，把登录、商品搜索、购物车和订单结算这几个流程固定下来，再用 Selenium 做页面自动化。

页面和测试代码都放在这个项目里，运行时不需要连接真实后端或数据库。目前实现的内容包括：

- 使用 Selenium 驱动 Edge，对页面元素进行操作和校验。
- 使用 pytest 组织测试用例。
- 把常用页面操作封装到 Page Object 中。
- 把账号、商品组合等测试数据放到 YAML 文件。
- 执行完成后生成 Allure 报告，用例失败时保存截图。

## 一、测试流程

本地页面包含 4 个主要流程：

1. 登录：正确账号登录成功，错误账号显示提示。
2. 搜索：按商品名称搜索，展示搜索结果或空结果提示。
3. 购物车：加入商品、重复加入商品、校验数量与合计金额。
4. 结算：登录后加入多个商品，提交订单并校验购物车清空。

测试账号：

```text
用户名：student
密码：123456
```

## 二、目录结构

```text
ui-automation-demo/
├─ web/                         # 本地电商练习页面
│  ├─ assets/products/          # 商品图片
│  ├─ css/
│  ├─ js/
│  └─ index.html
├─ tests/
│  ├─ pages/                    # Page Object 页面对象
│  │  ├─ base_page.py           # 公共定位、点击、输入、等待
│  │  ├─ login_page.py
│  │  ├─ product_page.py
│  │  └─ cart_page.py
│  └─ testcases/                # 测试用例
│     ├─ test_login.py
│     ├─ test_product_search.py
│     └─ test_cart.py
├─ data/
│  ├─ login_data.yaml           # 登录测试数据
│  └─ shopping_data.yaml        # 搜索、购物车、结算测试数据
├─ utils/
│  └─ data_loader.py            # YAML 读取工具
├─ config.py                    # 路径、浏览器等待时间等配置
├─ conftest.py                  # 本地服务、浏览器和失败截图 fixture
├─ pytest.ini                   # pytest 与 Allure 配置
├─ requirements.txt
├─ run_tests.ps1
├─ run_allure_report.ps1
└─ run_allure_report.bat
```

## 三、环境准备

当前电脑已安装 Python 3.13、Microsoft Edge 以及匹配的 EdgeDriver。打开 PowerShell，进入项目目录：

```powershell
cd C:\Users\31505\Desktop\ui-automation-demo
```

第一次运行需要创建虚拟环境并安装依赖。当前电脑的系统 `py` 启动器指向了一个已不存在的 Python 路径，因此下面使用 Mock 项目中可正常运行的 Python 来创建独立虚拟环境：

```powershell
C:\Users\31505\Desktop\Mock\.venv\Scripts\python.exe -m venv --copies .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

如果 PowerShell 不允许执行激活脚本，可以不激活虚拟环境，直接使用：

```powershell
C:\Users\31505\Desktop\Mock\.venv\Scripts\python.exe -m venv --copies .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 四、执行测试

项目会自动启动本地网页服务，并自动打开 Edge 浏览器执行测试，不需要手动启动网页。

直接执行：

```powershell
.\.venv\Scripts\python.exe -m pytest
```

也可以双击或运行：

```powershell
.\run_tests.ps1
```

默认使用无界面模式。如果想看着浏览器执行，先设置：

```powershell
$env:HEADLESS="false"
.\.venv\Scripts\python.exe -m pytest
```

pytest 的结果会同时写入 `allure-results`。

## 五、查看 Allure 报告

生成并打开报告：

```powershell
.\run_allure_report.ps1
```

也可以双击：

```text
run_allure_report.bat
```

脚本会优先读取 `ALLURE_BIN`，其次使用系统 `allure` 命令。如果没有配置系统命令，会自动使用当前电脑此前安装在 Mock 项目下的 Allure CLI。

手动执行方式：

```powershell
C:\Users\31505\Desktop\Mock\tools\allure-cli\node_modules\.bin\allure.cmd generate .\allure-results -o .\allure-report --clean
C:\Users\31505\Desktop\Mock\tools\allure-cli\node_modules\.bin\allure.cmd open .\allure-report
```

Allure 页面本身的部分菜单是英文，但本项目的用例标题、测试步骤和断言信息都是中文。

## 六、核心文件说明

### Page Object

例如 `tests/pages/login_page.py` 只负责页面操作：

```python
def login(self, username: str, password: str):
    self.type(self.USERNAME_INPUT, username)
    self.type(self.PASSWORD_INPUT, password)
    self.click(self.SUBMIT_BUTTON)
```

测试用例不需要关心元素如何定位，只调用 `login()`。

### YAML 数据驱动

例如 `data/login_data.yaml`：

```yaml
login_cases:
  - case_name: 正确账号登录成功
    username: student
    password: "123456"
    expected_success: true
    expected_message: student
```

测试代码通过 `pytest.mark.parametrize` 读取这些数据。后续增加账号场景时，优先修改 YAML，而不是复制测试代码。

### 失败截图

`conftest.py` 会在用例失败时自动保存截图到 `screenshots`，并附加到 Allure 报告。

## 七、实现说明

商品数据和测试账号直接写在 `web/js/app.js` 中，登录状态和购物车使用浏览器 `localStorage` 保存。订单提交只做页面交互和结果展示，没有连接真实的订单接口。

所以这个项目的检查重点是页面操作和结果是否正确，例如登录提示是否显示、搜索到的商品是否一致、购物车数量与金额是否正确。它不包含后端服务和数据库校验。

目前的功能比较简单，后续练习时可以继续补充商品分类、购物车数量修改、重复提交订单、页面加载失败等场景。
