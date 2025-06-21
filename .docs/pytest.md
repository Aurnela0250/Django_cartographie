TITLE: Defining Global `username` Fixture in Root Conftest
DESCRIPTION: This `conftest.py` snippet defines a global `username` fixture that returns the string 'username'. This fixture is available to all tests within the `tests/` directory and its subfolders unless explicitly overridden.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_60

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def username():
    return 'username'
```

---

TITLE: Running Pytest with Single Marker Selection
DESCRIPTION: This `pytest` command-line example demonstrates how to execute tests marked specifically with 'interface' using the `-m` option. The output shows that only tests marked with `interface` are selected and run, while others are deselected. It also includes the test session summary and failure details for the selected tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_34

LANGUAGE: pytest
CODE:

```
$ pytest -m interface --tb=short
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 4 items / 2 deselected / 2 selected

test_module.py FF                                                    [100%]

================================= FAILURES =================================
__________________________ test_interface_simple ___________________________
test_module.py:4: in test_interface_simple
    assert 0
E   assert 0
__________________________ test_interface_complex __________________________
test_module.py:8: in test_interface_complex
    assert 0
E   assert 0
========================= short test summary info ==========================
FAILED test_module.py::test_interface_simple - assert 0
FAILED test_module.py::test_interface_complex - assert 0
===================== 2 failed, 2 deselected in 0.12s ======================
```

---

TITLE: Asserting Expected Exceptions with pytest.raises Context Manager
DESCRIPTION: Demonstrates using `pytest.raises` as a context manager to assert that a specific exception type is raised within a block of code. This is the recommended way to test for expected exceptions in `pytest`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_3

LANGUAGE: python
CODE:

```
import pytest


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

---

TITLE: Executing pytest and Viewing Output (pytest)
DESCRIPTION: This snippet demonstrates running the `pytest` command from the terminal and shows the resulting output. It illustrates how pytest discovers the test file, executes the test function, and provides detailed information upon failure, including the values involved in the failed assertion, without requiring special assertion methods.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/index.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert inc(3) == 5
E       assert 4 == 5
E        +  where 4 = inc(3)

test_sample.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_sample.py::test_answer - assert 4 == 5
============================ 1 failed in 0.12s =============================
```

---

TITLE: Customizing Parametrized Test IDs in pytest (Python)
DESCRIPTION: This Python snippet demonstrates various methods to customize test IDs for parametrized tests using `pytest.mark.parametrize`. It showcases default ID generation (`test_timedistance_v0`), explicit string lists (`test_timedistance_v1`), a custom ID generation function (`test_timedistance_v2`), and using `pytest.param` for individual ID assignment (`test_timedistance_v3`), enhancing test reporting and selection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_4

LANGUAGE: python
CODE:

```
from datetime import datetime, timedelta

import pytest

testdata = [
    (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
    (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
]


@pytest.mark.parametrize("a,b,expected", testdata)
def test_timedistance_v0(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
def test_timedistance_v1(a, b, expected):
    diff = a - b
    assert diff == expected


def idfn(val):
    if isinstance(val, (datetime,)):
        # note this wouldn't show any hours/minutes/seconds
        return val.strftime("%Y%m%d")


@pytest.mark.parametrize("a,b,expected", testdata, ids=idfn)
def test_timedistance_v2(a, b, expected):
    diff = a - b
    assert diff == expected


@pytest.mark.parametrize(
    "a,b,expected",
    [
        pytest.param(
            datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1), id="forward"
        ),
        pytest.param(
            datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1), id="backward"
        )
    ]
)
def test_timedistance_v3(a, b, expected):
    diff = a - b
    assert diff == expected
```

---

TITLE: Defining and Using a Basic Pytest Fixture in Python
DESCRIPTION: This snippet demonstrates how to define a basic pytest fixture (`fruit_bowl`) and how a test function (`test_fruit_salad`) requests and uses it. It includes custom classes (`Fruit`, `FruitSalad`) to illustrate a practical scenario where the fixture provides initial data (a list of `Fruit` objects) for the test to operate on, ensuring a consistent setup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_0

LANGUAGE: python
CODE:

```
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)
```

---

TITLE: Running a Specific Test Method in a Class (Bash)
DESCRIPTION: This command targets and executes a single, specific test method located within a particular class in a module. The full path includes the module, class, and method names, all separated by '::'.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_5

LANGUAGE: bash
CODE:

```
pytest tests/test_mod.py::TestClass::test_method
```

---

TITLE: Running Pytest Tests by Node ID (Method)
DESCRIPTION: This pytest command-line example shows how to execute a single test method by providing its full node ID as a positional argument. The node ID 'test_server.py::TestClass::test_method' precisely targets the desired test, ensuring only that specific method is run.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_4

LANGUAGE: pytest
CODE:

```
$ pytest -v test_server.py::TestClass::test_method
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 1 item

test_server.py::TestClass::test_method PASSED                        [100%]

============================ 1 passed in 0.12s =============================
```

---

TITLE: Parametrizing Tests with pytest.mark.parametrize
DESCRIPTION: This example shows the modern and recommended way to parametrize tests in Pytest using the `@pytest.mark.parametrize` decorator. It allows defining multiple sets of arguments for a single test function, providing better fixture support and readability compared to yield-based generation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_10

LANGUAGE: Python
CODE:

```
@pytest.mark.parametrize("x, y", [(2, 4), (3, 9)])
def test_squared(x, y):
    assert x**x == y
```

---

TITLE: Installing or Updating pytest via pip
DESCRIPTION: This command uses pip to install or upgrade the pytest testing framework to its latest stable version. It is the primary method for setting up pytest in a Python environment, ensuring access to its features for test development.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pip install -U pytest
```

---

TITLE: Creating a Basic Python Test File
DESCRIPTION: This Python code defines a simple function func and a test function test_answer within test_sample.py. It demonstrates the fundamental structure of a pytest test, utilizing a standard assert statement to verify expected behavior.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_2

LANGUAGE: python
CODE:

```
# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
```

---

TITLE: Asserting Function Return Value with Python assert in Pytest
DESCRIPTION: Demonstrates using the standard Python `assert` statement within a `pytest` test function to verify the return value of a function. If the assertion fails, `pytest` provides detailed introspection of the values involved.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_assert1.py
def f():
    return 3


def test_function():
    assert f() == 4
```

---

TITLE: Asserting Specific Contained Exceptions with pytest.RaisesExc (Python)
DESCRIPTION: This snippet shows how to use pytest.RaisesExc within pytest.RaisesGroup to assert more specific details about an exception contained within an ExceptionGroup. Here, it ensures a ValueError is raised with a message matching "foo".
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_10

LANGUAGE: python
CODE:

```
def test_raises_exc():
    with pytest.RaisesGroup(pytest.RaisesExc(ValueError, match="foo")):
        raise ExceptionGroup("", (ValueError("foo")))
```

---

TITLE: Upgrading pytest via pip (Shell)
DESCRIPTION: This command upgrades the pytest package to the latest version available on PyPI using pip. It ensures that the user has the most recent features and bug fixes by performing an in-place update.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/scripts/release.major.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Installing/Upgrading pytest using pip (Shell)
DESCRIPTION: This command installs or upgrades the pytest testing framework using pip, the standard package installer for Python. The '-U' flag ensures that pytest is upgraded to the latest available version if it's already installed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.3.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading Pytest to Latest Version
DESCRIPTION: This command uses pip, the Python package installer, to upgrade the pytest framework to its latest available version. The -U flag ensures an upgrade rather than a fresh install if pytest is already present.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.7.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades or installs the pytest testing framework using pip, Python's package installer. The '-U' flag ensures that pytest is upgraded to the latest available version from PyPI.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.3.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Defining Interdependent Pytest Fixtures
DESCRIPTION: This Python snippet defines an `App` class and an `app` fixture that depends on another fixture, `smtp_connection`. It illustrates how fixtures can consume other fixtures, promoting modularity and reusability in test setups, and how `App` instances are created with the injected `smtp_connection`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_44

LANGUAGE: python
CODE:

```
# content of test_appsetup.py

    import pytest


    class App:
        def __init__(self, smtp_connection):
            self.smtp_connection = smtp_connection


    @pytest.fixture(scope="module")
    def app(smtp_connection):
        return App(smtp_connection)


    def test_smtp_connection_exists(app):
        assert app.smtp_connection
```

---

TITLE: Profiling Test Execution Durations (Bash)
DESCRIPTION: This command displays a list of the 10 slowest test durations that are longer than 1.0 seconds. This feature, updated in pytest version 6.0, helps identify performance bottlenecks. By default, very short durations (<0.005s) are not shown unless '-vv' is passed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_13

LANGUAGE: bash
CODE:

```
pytest --durations=10 --durations-min=1.0
```

---

TITLE: Configuring Project Build System and Metadata with pyproject.toml
DESCRIPTION: This TOML snippet defines the build system requirements using `hatchling` and specifies basic project metadata like `name` and `version` within the `pyproject.toml` file. It's essential for modern Python packaging to ensure proper project setup and distribution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_0

LANGUAGE: toml
CODE:

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "PACKAGENAME"
version = "PACKAGEVERSION"
```

---

TITLE: Correct Usage: Requesting Pytest Fixtures as Dependencies
DESCRIPTION: This snippet demonstrates the correct and recommended way to use a fixture within another fixture in Pytest. By requesting `cell` as a dependency in `full_cell(cell)`, pytest's fixture resolution model is properly utilized, ensuring correct setup and teardown.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_37

LANGUAGE: python
CODE:

```
@pytest.fixture
def cell():
    return ...


@pytest.fixture
def full_cell(cell):
    cell.make_full()
    return cell
```

---

TITLE: Testing Standard Output with pytest capsys Fixture (Python)
DESCRIPTION: Provides an example of a `pytest` test function that uses the `capsys` fixture to capture standard output and standard error. The `readouterr()` method returns the captured output and error streams, allowing assertions against them.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_6

LANGUAGE: python
CODE:

```
def test_output(capsys):
    print("hello")
    out, err = capsys.readouterr()
    assert out == "hello\n"
```

---

TITLE: Upgrading pytest using pip (Python)
DESCRIPTION: This command upgrades the pytest testing framework to its latest version (or a specific release candidate if specified) using the pip package installer. The -U flag ensures that existing installations are upgraded.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.0.0rc1.rst#_snippet_0

LANGUAGE: Python
CODE:

```
pip install -U pytest
```

---

TITLE: Asserting Expected Exceptions with pytest.raises
DESCRIPTION: This Python code uses pytest.raises as a context manager to verify that a function f() raises a SystemExit exception. This pattern is crucial for testing error handling and ensuring that specific exceptions are correctly triggered by code.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_4

LANGUAGE: python
CODE:

```
# content of test_sysexit.py
import pytest

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()
```

---

TITLE: Testing Environment Variables with pytest-monkeypatch (Fixtures)
DESCRIPTION: This example refactors environment variable monkeypatching into pytest fixtures (`mock_env_user`, `mock_env_missing`). This approach promotes reusability and modularity, allowing tests to simply reference the fixtures to set up specific environment states for their execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_8

LANGUAGE: Python
CODE:

```
# contents of our test file e.g. test_code.py
import pytest


@pytest.fixture
def mock_env_user(monkeypatch):
    monkeypatch.setenv("USER", "TestingUser")


@pytest.fixture
def mock_env_missing(monkeypatch):
    monkeypatch.delenv("USER", raising=False)


# notice the tests reference the fixtures for mocks
def test_upper_to_lower(mock_env_user):
    assert get_os_user_lower() == "testinguser"


def test_raise_exception(mock_env_missing):
    with pytest.raises(OSError):
        _ = get_os_user_lower()
```

---

TITLE: Parametrizing a Test Function with pytest.mark.parametrize
DESCRIPTION: This snippet demonstrates how to use the @pytest.mark.parametrize decorator to run a single test function multiple times with different sets of arguments. It defines test_input and expected parameters, allowing the test_eval function to be executed for each provided tuple.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_expectation.py
import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

---

TITLE: Defining a Simple pytest Test Function (Python)
DESCRIPTION: This snippet shows the content of a basic test file (`test_sample.py`) for pytest. It includes a simple function `inc` to be tested and a test function `test_answer` that uses a standard Python `assert` statement to verify the function's behavior. pytest automatically discovers and runs functions prefixed with `test_`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/index.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
```

---

TITLE: Applying Marks to Parametrize Values with pytest.param
DESCRIPTION: This snippet shows the recommended way to apply marks to individual values in `pytest.mark.parametrize` using `pytest.param`. This improves readability and aligns with current pytest architecture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_25

LANGUAGE: python
CODE:

```
@pytest.mark.parametrize(
        "a, b",
        [
            (3, 9),
            pytest.param(6, 36, marks=pytest.mark.xfail(reason="flaky")),
            (10, 100),
            (20, 200),
            (40, 400),
            (50, 500),
        ],
    )
    def test_foo(a, b): ...
```

---

TITLE: Catching ExceptionGroup with pytest.raises in Python
DESCRIPTION: This snippet illustrates how to use `pytest.raises` to assert that a specific code block raises an `ExceptionGroup[Exception]`. The `exc_info` context manager variable will hold the `ExceptionInfo` object, maintaining full typing information for the caught exception group. This approach is crucial for type-safe handling of grouped exceptions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/changelog/13115.improvement.rst#_snippet_0

LANGUAGE: python
CODE:

```
with pytest.raises(ExceptionGroup[Exception]) as exc_info:
    some_function()
```

---

TITLE: Upgrading pytest via pip (Shell)
DESCRIPTION: This command upgrades an existing pytest installation to the latest available version using pip, the Python package installer. It ensures you have the most recent bug fixes and features.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.2.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Pytest Output for Test Class Instance Isolation Demonstration
DESCRIPTION: This snippet shows the `pytest` command execution and its output for the `TestClassDemoInstance`. It demonstrates that `test_one` passes while `test_two` fails because `test_two` receives a fresh instance of the class where `self.value` is still `0`, not `1` as set by `test_one`. This highlights pytest's default behavior of creating a unique class instance for each test method to ensure isolation, while class-level attributes remain shared.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_9

LANGUAGE: pytest
CODE:

```
$ pytest -k TestClassDemoInstance -q
.F                                                                   [100%]
================================= FAILURES =================================
______________________ TestClassDemoInstance.test_two ______________________

self = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>

    def test_two(self):
>       assert self.value == 1
E       assert 0 == 1
E        +  where 0 = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>.value

test_class_demo.py:9: AssertionError
========================= short test summary info ==========================
FAILED test_class_demo.py::TestClassDemoInstance::test_two - assert 0 == 1
1 failed, 1 passed in 0.12s
```

---

TITLE: Defining a Simple Pytest Function in Python
DESCRIPTION: This snippet defines a basic Python function `inc` and a test function `test_answer` designed to be run with pytest. Pytest automatically discovers functions prefixed with `test_` and uses standard `assert` statements for verification. The example demonstrates a failing assertion (`inc(3)` which is 4, asserted to be 5) to showcase pytest's detailed introspection capabilities during test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/README.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 5
```

---

TITLE: Standard Fixture Setup and Teardown with Yield
DESCRIPTION: This snippet shows the recommended way to implement setup and teardown logic within a pytest fixture using the `yield` keyword. This approach leverages the standard fixture mechanism for resource management.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_31

LANGUAGE: python
CODE:

```
@pytest.fixture(scope="module")
    def db_session():
        session = Session.create()
        yield session
        session.close()
```

---

TITLE: Capturing Text File Descriptor Output with capfd
DESCRIPTION: This example shows how to use the `capfd` fixture to capture text output written to file descriptors 1 (stdout) and 2 (stderr). The `readouterr()` method provides the captured output as `text` (string) objects, useful for testing system commands that write to standard file descriptors.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_2

LANGUAGE: python
CODE:

```
def test_system_echo(capfd):
    os.system('echo "hello"')
    captured = capfd.readouterr()
    assert captured.out == "hello\n"
```

---

TITLE: Requesting a Unique Temporary Directory with `tmp_path` Fixture (Python)
DESCRIPTION: This Python test function `test_needsfiles` demonstrates how to request a unique temporary directory using the `tmp_path` built-in fixture. By including `tmp_path` in the function signature, pytest automatically provides a `pathlib.Path` object pointing to a new, isolated temporary directory for each test invocation. This is useful for tests that require creating temporary files or directories without interfering with other tests or the system.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_10

LANGUAGE: python
CODE:

```
# content of test_tmp_path.py
def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0
```

---

TITLE: Defining Fixtures with @pytest.fixture Decorator
DESCRIPTION: This snippet demonstrates the standard and recommended way to define fixtures using the `@pytest.fixture` decorator. This is the modern and supported method for fixture definition in pytest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_27

LANGUAGE: python
CODE:

```
@pytest.fixture
    def data():
        return SomeData()
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades the pytest testing framework to its latest available version using the pip package installer. It ensures you have the most recent bug fixes and features by replacing the existing installation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.2.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Configuring Pytest with pyproject.toml (TOML)
DESCRIPTION: This TOML configuration snippet for `pyproject.toml` uses the `[tool.pytest.ini_options]` table to configure pytest. It specifies a minimum pytest version of 6.0, sets default command-line options (`-ra -q`), and defines test path directories (`tests`, `integration`). This format is intended as a bridge to future TOML-based pytest configurations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/customize.rst#_snippet_2

LANGUAGE: toml
CODE:

```
# pyproject.toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
    "tests",
    "integration",
]
```

---

TITLE: Pytest Fixtures for Web Application Testing with Selenium
DESCRIPTION: This comprehensive set of Python fixtures and a test function demonstrates a safe fixture structure for web application testing. It covers creating a user via an admin API, launching and quitting a Selenium Chrome driver, logging into a web page, and asserting content on a landing page, ensuring all resources are properly cleaned up after the test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_28

LANGUAGE: python
CODE:

```
from uuid import uuid4
from urllib.parse import urljoin

from selenium.webdriver import Chrome
import pytest

from src.utils.pages import LoginPage, LandingPage
from src.utils import AdminApiClient
from src.utils.data_types import User


@pytest.fixture
def admin_client(base_url, admin_credentials):
    return AdminApiClient(base_url, **admin_credentials)


@pytest.fixture
def user(admin_client):
    _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
    admin_client.create_user(_user)
    yield _user
    admin_client.delete_user(_user)


@pytest.fixture
def driver():
    _driver = Chrome()
    yield _driver
    _driver.quit()


@pytest.fixture
def login(driver, base_url, user):
    driver.get(urljoin(base_url, "/login"))
    page = LoginPage(driver)
    page.login(user)


@pytest.fixture
def landing_page(driver, login):
    return LandingPage(driver)


def test_name_on_landing_page_after_login(landing_page, user):
    assert landing_page.header == f"Welcome, {user.name}!"
```

---

TITLE: Configure pytest via pytest.ini
DESCRIPTION: Shows how to set default command line options using the `addopts` setting in a `pytest.ini` configuration file.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_0

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
addopts = -ra -q
```

---

TITLE: Defining a Shared Fixture in conftest.py (Python)
DESCRIPTION: This snippet demonstrates how to define a pytest fixture named 'order' within a `conftest.py` file. Fixtures defined in `conftest.py` are automatically discovered and made available to any tests within the same directory or its subdirectories, facilitating the sharing of setup and teardown logic across multiple test files.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_0

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def order():
    return []
```

---

TITLE: Combining Scoping and Parametrization in pytest Fixtures (pytest-2.3+)
DESCRIPTION: This example demonstrates combining both `scope` and `params` arguments in the `@pytest.fixture` decorator. The `db` fixture is session-scoped and parametrized, meaning it will be invoked twice per session (once for "mysql" and once for "pg"), and all tests requiring `db` will run for both configurations. `request.addfinalizer()` ensures proper cleanup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/funcarg_compare.rst#_snippet_3

LANGUAGE: Python
CODE:

```
@pytest.fixture(scope="session", params=["mysql", "pg"])
def db(request):
    if request.param == "mysql":
        db = MySQL()
    elif request.param == "pg":
        db = PG()
    request.addfinalizer(db.destroy)  # destroy when session is finished
    return db
```

---

TITLE: Setting Specific Logger Level with caplog (Python)
DESCRIPTION: This Python snippet demonstrates how to set the log level for a specific logger (e.g., 'root.baz') using the `caplog` fixture. This allows fine-grained control over which loggers' messages are captured and at what severity level within a test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_8

LANGUAGE: python
CODE:

```
def test_foo(caplog):
        caplog.set_level(logging.CRITICAL, logger="root.baz")
```

---

TITLE: Pytest Fixture Introspection with Request Object (Python)
DESCRIPTION: This snippet illustrates how pytest fixtures can introspect the requesting test context using the `request` object. The `smtp_connection` fixture reads an optional `smtpserver` attribute from the test module, allowing for dynamic configuration of the SMTP server based on the test environment. It also includes a teardown phase to close the connection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_31

LANGUAGE: python
CODE:

```
# content of conftest.py
import smtplib

import pytest


@pytest.fixture(scope="module")
def smtp_connection(request):
    server = getattr(request.module, "smtpserver", "smtp.gmail.com")
    smtp_connection = smtplib.SMTP(server, 587, timeout=5)
    yield smtp_connection
    print(f"finalizing {smtp_connection} ({server})")
    smtp_connection.close()
```

---

TITLE: Stacking Parametrize Decorators in Python
DESCRIPTION: This Python snippet demonstrates how to use multiple `@pytest.mark.parametrize` decorators on a single test function to generate all combinations of the provided arguments. The parameters are exhausted in the order the decorators are stacked.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_7

LANGUAGE: python
CODE:

```
import pytest


@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest version (8.0.2 in this context) using the pip package manager. It ensures you have the most recent bug fixes and features by replacing the old version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.0.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Direct Parametrization of Fixture with @pytest.fixture (pytest-2.3+)
DESCRIPTION: This snippet illustrates how to directly parametrize a fixture using the `params` argument in the `@pytest.fixture` decorator. The fixture factory will be invoked multiple times, once for each parameter value, with `request.param` holding the current value. This simplifies running tests with different configurations without needing `pytest_generate_tests`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/funcarg_compare.rst#_snippet_2

LANGUAGE: Python
CODE:

```
@pytest.fixture(params=["mysql", "pg"])
def db(request): ...  # use request.param
```

---

TITLE: Setting Manual Breakpoints in Pytest (Python)
DESCRIPTION: This Python code snippet demonstrates how to set a manual breakpoint within your test code using the native `pdb.set_trace()` call. Pytest automatically disables its output capture for the duration of the debugger session, resuming it upon exit.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/failures.rst#_snippet_4

LANGUAGE: python
CODE:

```
import pdb;pdb.set_trace()
```

---

TITLE: Parametrizing Pytest Tests for Conditional Exception Handling
DESCRIPTION: This Python snippet illustrates how to write parametrized pytest tests where some test cases are expected to raise exceptions, while others are not. It uses `pytest.mark.parametrize` in conjunction with `pytest.raises` for expected failures and `contextlib.nullcontext` for expected successful outcomes, allowing a single test function to handle both scenarios. Dependencies include `pytest` and `contextlib`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_27

LANGUAGE: python
CODE:

```
from contextlib import nullcontext

import pytest


@pytest.mark.parametrize(
    "example_input,expectation",
    [
        (3, nullcontext(2)),
        (2, nullcontext(3)),
        (1, nullcontext(6)),
        (0, pytest.raises(ZeroDivisionError)),
    ],
)
def test_division(example_input, expectation):
    """Test how much I know division."""
    with expectation as e:
        assert (6 / example_input) == e
```

---

TITLE: End-to-End Login and Landing Page Tests with Pytest Fixtures (Python)
DESCRIPTION: This snippet defines a suite of end-to-end tests for a login and landing page using pytest. It demonstrates the use of class-scoped fixtures for setting up an AdminApiClient, creating/deleting test users, managing a Selenium Chrome driver, and handling the login process. It includes tests for verifying user name in the header, sign-out button visibility, and profile link correctness.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_29

LANGUAGE: python
CODE:

```
# contents of tests/end_to_end/test_login.py
from uuid import uuid4
from urllib.parse import urljoin

from selenium.webdriver import Chrome
import pytest

from src.utils.pages import LoginPage, LandingPage
from src.utils import AdminApiClient
from src.utils.data_types import User


@pytest.fixture(scope="class")
def admin_client(base_url, admin_credentials):
    return AdminApiClient(base_url, **admin_credentials)


@pytest.fixture(scope="class")
def user(admin_client):
    _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
    admin_client.create_user(_user)
    yield _user
    admin_client.delete_user(_user)


@pytest.fixture(scope="class")
def driver():
    _driver = Chrome()
    yield _driver
    _driver.quit()


@pytest.fixture(scope="class")
def landing_page(driver, login):
    return LandingPage(driver)


class TestLandingPageSuccess:
    @pytest.fixture(scope="class", autouse=True)
    def login(self, driver, base_url, user):
        driver.get(urljoin(base_url, "/login"))
        page = LoginPage(driver)
        page.login(user)

    def test_name_in_header(self, landing_page, user):
        assert landing_page.header == f"Welcome, {user.name}!"

    def test_sign_out_button(self, landing_page):
        assert landing_page.sign_out_button.is_displayed()

    def test_profile_link(self, landing_page, user):
        profile_href = urljoin(base_url, f"/profile?id={user.profile_id}")
        assert landing_page.profile_link.get_attribute("href") == profile_href
```

---

TITLE: Executing a Basic pytest Test and Analyzing Output
DESCRIPTION: This command runs pytest, which automatically discovers and executes tests in test_sample.py. The output illustrates a test session, including the failure of test_answer due to an assertion mismatch, showcasing pytest's detailed failure reporting and introspection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_3

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_sample.py F                                                     [100%]

================================= FAILURES =================================
_______________________________ test_answer ________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_sample.py::test_answer - assert 4 == 5
============================ 1 failed in 0.12s =============================
```

---

TITLE: Native Pytest setup_method/teardown_method
DESCRIPTION: This snippet demonstrates the native Pytest way to perform method-level setup and teardown using `setup_method` and `teardown_method`. These methods are preferred over the deprecated Nose-style `setup` and `teardown` for managing resources before and after each test method.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_12

LANGUAGE: Python
CODE:

```
class Test:
    def setup_method(self):
        self.resource = make_resource()

    def teardown_method(self):
        self.resource.close()

    def test_foo(self): ...

    def test_bar(self): ...
```

---

TITLE: Assert Dictionary Equality in Pytest
DESCRIPTION: Illustrates a failed assertion comparing two dictionaries with differing values and extra items. Pytest provides a detailed diff showing differing items and items unique to each dictionary.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_11

LANGUAGE: python
CODE:

```
assert {"a": 0, "b": 1, "c": 0} == {"a": 0, "b": 2, "d": 0}
```

---

TITLE: Defining a Pytest Yield Fixture for Docker Container
DESCRIPTION: This snippet defines a pytest fixture named `docker_container` that uses `yield` to manage the lifecycle of a Docker container. The `scope` is dynamically determined. The `spawn_container()` function is called during setup, and any cleanup code would follow the `yield` statement.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_16

LANGUAGE: Python
CODE:

```
@pytest.fixture(scope=determine_scope)
def docker_container():
    yield spawn_container()
```

---

TITLE: Demonstrating Pytest Fixture Reusability and Isolation in Python
DESCRIPTION: This snippet highlights the reusability of pytest fixtures and their ability to provide isolated environments for each test. It shows two different tests (`test_string`, `test_int`) requesting the same `order` fixture, demonstrating that each test receives its own fresh instance of the fixture's result, preventing test interference and ensuring consistent results.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_4

LANGUAGE: python
CODE:

```
# contents of test_append.py
import pytest


# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]


def test_int(order):
    # Act
    order.append(2)

    # Assert
    assert order == ["a", 2]
```

---

TITLE: Defining a Parametrized Function-Scoped Pytest Fixture (Python)
DESCRIPTION: This Python snippet defines a Pytest fixture named `otherarg` with a 'function' scope and parameters 1 and 2. Similar to `modarg`, `yield` separates setup and teardown. Due to its 'function' scope, this fixture will be set up before and torn down after every test function that uses it, for each parameter.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_48

LANGUAGE: python
CODE:

```
@pytest.fixture(scope="function", params=[1, 2])
def otherarg(request):
    param = request.param
    print("  SETUP otherarg", param)
    yield param
    print("  TEARDOWN otherarg", param)
```

---

TITLE: Grouping Multiple Tests within a Python Class
DESCRIPTION: This Python code defines TestClass containing two test methods, test*one and test_two. pytest automatically discovers methods prefixed with test* within classes prefixed with Test, enabling logical organization of related test cases.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_6

LANGUAGE: python
CODE:

```
# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
```

---

TITLE: Verifying Exact Exception Type with pytest.raises
DESCRIPTION: Explains how to explicitly check for an exact exception type when using `pytest.raises`. While `pytest.raises` matches subclasses, an additional `assert excinfo.type is ExpectedError` is needed to ensure only the precise exception type is raised, preventing false positives from subclasses.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_5

LANGUAGE: python
CODE:

```
def test_foo_not_implemented():
    def foo():
        raise NotImplementedError

    with pytest.raises(RuntimeError) as excinfo:
        foo()
    assert excinfo.type is RuntimeError
```

---

TITLE: Using Metafunc.parametrize for Dynamic Test Generation
DESCRIPTION: This snippet illustrates the recommended `pytest.Metafunc.parametrize` method for dynamically generating tests. This provides a more robust and modern approach compared to `Metafunc.addcall`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_29

LANGUAGE: python
CODE:

```
def pytest_generate_tests(metafunc):
        metafunc.parametrize("i", [1, 2], ids=["1", "2"])
```

---

TITLE: Conditionally Skipping Tests with pytest.mark.skipif (Python)
DESCRIPTION: Demonstrates how to use the pytest.mark.skipif decorator to conditionally skip a test function based on a module's version. This example checks if the first character of 'mymodule.**version**' is '1'. Using a string expression allows pytest to provide more meaningful skip reasons in the test summary.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.2.rst#_snippet_1

LANGUAGE: Python
CODE:

```
import pytest
import mymodule
@pytest.mark.skipif("mymodule.__version__[0] == \"1\"")
def test_function():
    pass
```

---

TITLE: Running Tests by Keyword Expression (Bash)
DESCRIPTION: This command runs tests whose names (including filenames, class names, and function names) match the given case-insensitive string expression. The expression can include Python operators like 'and', 'or', and 'not'. On Windows, it is recommended to use double quotes instead of single quotes for the expression.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_2

LANGUAGE: bash
CODE:

```
pytest -k 'MyClass and not method'
```

---

TITLE: Defining a `cleandir` Fixture for Temporary Directories (Python)
DESCRIPTION: This Python snippet, typically placed in `conftest.py`, defines a `cleandir` fixture. It uses `tempfile.TemporaryDirectory` to create a temporary directory, changes the current working directory (`os.chdir`) to it, yields control to the tests, and then restores the original working directory during teardown. This ensures each test runs in a clean, isolated environment.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_53

LANGUAGE: python
CODE:

```
# content of conftest.py

import os
import tempfile

import pytest


@pytest.fixture
def cleandir():
    with tempfile.TemporaryDirectory() as newpath:
        old_cwd = os.getcwd()
        os.chdir(newpath)
        yield
        os.chdir(old_cwd)
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This command upgrades an existing pytest installation to the specified version (7.1.3 in this context) using the pip package manager. It ensures you have the most recent bug fixes and features by replacing the current version with the latest available.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.1.3.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest version (7.0.1 in this context) using pip, the Python package installer. The --upgrade flag ensures that if pytest is already installed, it will be updated to the specified version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.0.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Defining and Using Dependent Pytest Fixtures in Python
DESCRIPTION: This snippet demonstrates how to define pytest fixtures and how fixtures can depend on other fixtures. It includes a `Fruit` class, a `my_fruit` fixture returning an 'apple' `Fruit` object, and a `fruit_basket` fixture that uses `my_fruit` to create a list. A test function `test_my_fruit_in_basket` then consumes both fixtures to verify the 'apple' is in the basket.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/fixtures.rst#_snippet_0

LANGUAGE: Python
CODE:

```
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket
```

---

TITLE: Testing pytest Plugins with Pytester Fixture (Python)
DESCRIPTION: This snippet illustrates how to use the `pytester` fixture to thoroughly test a custom pytest plugin. It demonstrates creating temporary `conftest.py` and test files using `makeconftest` and `makepyfile`, running the tests with `runpytest`, and asserting the test outcomes using `assert_outcomes`. This specific test verifies the functionality of the `hello` fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_10

LANGUAGE: Python
CODE:

```
def test_hello(pytester):
    """Make sure that our plugin works."""

    # create a temporary conftest.py file
    pytester.makeconftest(
        """
            import pytest

            @pytest.fixture(params=[
                "Brianna",
                "Andreas",
                "Floris",
            ])
            def name(request):
                return request.param
        """
    )

    # create a temporary pytest test file
    pytester.makepyfile(
        """
            def test_hello_default(hello):
                assert hello() == "Hello World!"

            def test_hello_name(hello, name):
                assert hello(name) == "Hello {0}!".format(name)
        """
    )

    # run all tests with pytest
    result = pytester.runpytest()

    # check that all 4 tests passed
    result.assert_outcomes(passed=4)
```

---

TITLE: Direct Scoping of Fixture with @pytest.fixture (pytest-2.3+)
DESCRIPTION: This snippet shows the improved pytest-2.3 fixture mechanism using the `@pytest.fixture` decorator. By directly specifying `scope="session"`, the fixture factory is invoked only once per session, simplifying resource management. `request.addfinalizer()` is used to register a teardown function that runs when the session finishes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/funcarg_compare.rst#_snippet_1

LANGUAGE: Python
CODE:

```
@pytest.fixture(scope="session")
def db(request):
    # factory will only be invoked once per session -
    db = DataBase()
    request.addfinalizer(db.destroy)  # destroy when session is finished
    return db
```

---

TITLE: Getting Help on Command Line Options and Configuration Settings (Bash)
DESCRIPTION: This snippet demonstrates how to use the `pytest -h` command-line option to display help information. It shows available command-line options and configuration file settings registered by installed plugins, providing a comprehensive overview of pytest's configurable aspects.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/customize.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest -h   # prints options _and_ config file settings
```

---

TITLE: Defining Module-Scoped Pytest Fixtures in Python
DESCRIPTION: This conceptual snippet describes how to define a pytest fixture with `scope="module"`. Such a fixture, like `smtp_connection`, is invoked only once per test module, allowing multiple test functions within that module to share the same instance and save setup time for expensive resources.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_10

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture(scope="module")
def smtp_connection():
    # Establish a connection to an SMTP server
    connection = "SMTP_CONNECTION_OBJECT" # Placeholder for actual connection logic
    yield connection
    # Teardown: Close the connection
    # connection.close()
```

---

TITLE: Typing Parameters in Pytest Parametrized Tests
DESCRIPTION: This snippet demonstrates applying type hints to parameters within a pytest parametrized test. Both `input_value` and `expected_output` are typed as `int`, ensuring type safety and clarity for the values provided by `@pytest.mark.parametrize`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/types.rst#_snippet_4

LANGUAGE: python
CODE:

```
@pytest.mark.parametrize("input_value, expected_output", [(1, 2), (5, 6), (10, 11)])
def test_increment(input_value: int, expected_output: int) -> None:
    assert input_value + 1 == expected_output
```

---

TITLE: Using Plain Assertions in pytest (std.utest)
DESCRIPTION: This snippet demonstrates pytest's foundational principle of using standard Python assert statements for test assertions, moving away from verbose assertXYZ APIs. While plain Python asserts provide limited error information, pytest (originally std.utest) enhances them to offer detailed insights into underlying values upon failure, simplifying test writing and debugging.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/history.rst#_snippet_0

LANGUAGE: Python
CODE:

```
assert x == y
```

---

TITLE: Defining a Fixture with @pytest.fixture Decorator (Python)
DESCRIPTION: This snippet demonstrates the modern and recommended way to define a pytest fixture using the `@pytest.fixture()` decorator. The function name, `db`, directly serves as the name under which the resource can be requested as an argument in test functions. This method fully supports scoping and parametrization, offering greater flexibility than older approaches.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/funcarg_compare.rst#_snippet_4

LANGUAGE: Python
CODE:

```
@pytest.fixture()
def db(request): ...
```

---

TITLE: Setting up Project for Pytest Development in Bash
DESCRIPTION: This snippet demonstrates how to navigate into a project repository and install it in editable development mode. This setup creates a symlink, allowing tests to run against local code changes without reinstallation, which is crucial for an efficient development workflow.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/existingtestsuite.rst#_snippet_0

LANGUAGE: bash
CODE:

```
cd <repository>
pip install -e .  # Environment dependent alternatives include
                      # 'python setup.py develop' and 'conda develop'
```

---

TITLE: Managing Resources with Pytest Fixture Factories (Python)
DESCRIPTION: This advanced factory fixture example shows how to manage resources created by the factory function. The `make_customer_record` fixture collects all created `Customer` records and ensures their cleanup (`record.destroy()`) after the test completes, using a `yield` statement to define setup and teardown phases. This pattern is ideal for managing database entries or temporary files.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_37

LANGUAGE: python
CODE:

```
@pytest.fixture
def make_customer_record():
    created_records = []

    def _make_customer_record(name):
        record = models.Customer(name=name, orders=[])
        created_records.append(record)
        return record

    yield _make_customer_record

    for record in created_records:
        record.destroy()


def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```

---

TITLE: Mocking API Response Objects with Monkeypatch (Python)
DESCRIPTION: This test demonstrates how to use `monkeypatch.setattr` to mock the `requests.get` function. It defines a `MockResponse` class with a `json()` method to simulate an API response, allowing tests to run without actual network calls and ensuring predictable test outcomes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_2

LANGUAGE: python
CODE:

```
import requests
import app


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_get_json(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = app.get_json("https://fakeurl")
    assert result["mock_key"] == "mock_response"
```

---

TITLE: Skipping All Tests in a Pytest Module if Import is Missing
DESCRIPTION: This snippet uses `pytest.importorskip` at the module level to skip all tests if a required module, 'pexpect', cannot be imported. This ensures tests relying on 'pexpect' are only run when it's available.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_12

LANGUAGE: python
CODE:

```
pexpect = pytest.importorskip("pexpect")
```

---

TITLE: Running Pytest with Marker Expression (-m)
DESCRIPTION: This snippet illustrates running `pytest` using the `-m` option to select tests explicitly marked with 'linux'. It shows that only tests matching the marker expression are collected and run, while others are deselected, providing a way to restrict test execution to specific marked tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_31

LANGUAGE: shell
CODE:

```
$ pytest -m linux
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 4 items / 3 deselected / 1 selected

test_plat.py .                                                       [100%]

===================== 1 passed, 3 deselected in 0.12s ======================
```

---

TITLE: Parametrizing All Tests in a Module with pytestmark
DESCRIPTION: This snippet demonstrates how to apply parametrization to all tests within an entire module by assigning the pytest.mark.parametrize decorator to the global pytestmark variable. This ensures that every test function and method in the module will run with the specified parameter sets.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_4

LANGUAGE: python
CODE:

```
import pytest

pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])


class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected
```

---

TITLE: Running Pytest with Session Fixture and Observing Output
DESCRIPTION: This snippet shows the command to execute the `pytest` tests (`pytest -q -s test_module.py`) and the expected console output. The `-q` flag provides quiet output, and `-s` disables output capturing, allowing `print` statements to be seen. The output demonstrates the execution order: the session fixture runs first, then the `callme` methods from each test class, followed by the individual test methods, confirming the fixture's pre-test execution capability.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/special.rst#_snippet_2

LANGUAGE: pytest
CODE:

```
$ pytest -q -s test_module.py
callattr_ahead_of_alltests called
callme called!
callme other called
SomeTest callme called
test_method1 called
.test_method2 called
.test other
.test_unit1 method called
.
4 passed in 0.12s
```

---

TITLE: Applying xfail and skip Markers with pytest.mark.parametrize in Python
DESCRIPTION: This Python snippet illustrates how to apply `xfail` and `skipif` markers to individual test instances within a `pytest.mark.parametrize` decorator. It shows how to mark specific parameter sets as `xfail` (with or without a reason) or `skipif` based on a condition, allowing fine-grained control over test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_24

LANGUAGE: python
CODE:

```
import sys

import pytest


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, 2),
        pytest.param(1, 0, marks=pytest.mark.xfail),
        pytest.param(1, 3, marks=pytest.mark.xfail(reason="some bug")),
        (2, 3),
        (3, 4),
        (4, 5),
        pytest.param(
            10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0), reason="py2k")
        ),
    ],
)
def test_increment(n, expected):
    assert n + 1 == expected
```

---

TITLE: Monkeypatching functools.partial with pytest-monkeypatch
DESCRIPTION: This snippet demonstrates how to use `monkeypatch.setattr` within a context manager to temporarily change the value of `functools.partial` for testing purposes. It ensures the change is reverted after the test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_5

LANGUAGE: Python
CODE:

```
import functools


def test_partial(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(functools, "partial", 3)
        assert functools.partial == 3
```

---

TITLE: Implementing Dynamic Parametrization with pytest_generate_tests in Python
DESCRIPTION: This Python snippet, intended for a `conftest.py` file, shows how to dynamically parametrize tests using the `pytest_generate_tests` hook. It defines a new command-line option `--stringinput` and uses it to parametrize any test function that requests the `stringinput` fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_9

LANGUAGE: python
CODE:

```
# content of conftest.py


def pytest_addoption(parser):
    parser.addoption(
        "--stringinput",
        action="append",
        default=[],
        help="list of stringinputs to pass to test functions",
    )


def pytest_generate_tests(metafunc):
    if "stringinput" in metafunc.fixturenames:
        metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))
```

---

TITLE: Running Pytest Tests by Node ID (Class)
DESCRIPTION: This pytest command-line example demonstrates how to run all tests within a specific test class by providing its node ID ('test_server.py::TestClass'). This selects all methods defined within that class for execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_5

LANGUAGE: pytest
CODE:

```
$ pytest -v test_server.py::TestClass
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 1 item

test_server.py::TestClass::test_method PASSED                        [100%]

============================ 1 passed in 0.12s =============================
```

---

TITLE: Sharing Pytest Skipif Markers Across Modules (Python)
DESCRIPTION: This set of snippets demonstrates how to define a `pytest.mark.skipif` marker in one module and then import and reuse it in another test module. This practice promotes consistency and reduces code duplication, especially in larger test suites where the same skip conditions might apply to multiple tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_5

LANGUAGE: python
CODE:

```
# content of test_mymodule.py
import mymodule

minversion = pytest.mark.skipif(
    mymodule.__versioninfo__ < (1, 1), reason="at least mymodule-1.1 required"
)


@minversion
def test_function(): ...
```

LANGUAGE: python
CODE:

```
# test_myothermodule.py
from test_mymodule import minversion


@minversion
def test_anotherfunction(): ...
```

---

TITLE: Skipping Test Function with Pytest Mark Skip Decorator (Python)
DESCRIPTION: This example demonstrates the simplest way to skip a test function using the `pytest.mark.skip` decorator. An optional `reason` parameter can be provided to explain why the test is being skipped, which will appear in the test summary when detailed reporting is enabled.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_1

LANGUAGE: python
CODE:

```
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown(): ...
```

---

TITLE: Requesting Multiple Pytest Fixtures in Python
DESCRIPTION: This example demonstrates how pytest tests and fixtures can request multiple other fixtures. The `order` fixture depends on `first_entry` and `second_entry`, while `test_string` requests both `order` and `expected_list` to perform its assertions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_7

LANGUAGE: Python
CODE:

```
import pytest


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def second_entry():
    return 2


@pytest.fixture
def order(first_entry, second_entry):
    return [first_entry, second_entry]


@pytest.fixture
def expected_list():
    return ["a", 2, 3.0]


def test_string(order, expected_list):
    # Act
    order.append(3.0)

    # Assert
    assert order == expected_list
```

---

TITLE: Configuring Pytest `addopts` in INI
DESCRIPTION: Illustrates how to use the `addopts` configuration option in `pytest.ini` to automatically append command-line arguments to every pytest invocation. This example sets a maximum of 2 failures before exiting and enables reporting of failure information.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_17

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
addopts = --maxfail=2 -rf  # exit after 2 failures, report fail info
```

---

TITLE: Declaring a Session-Scoped Pytest Fixture in Python
DESCRIPTION: This Python snippet illustrates how to change the `smtp_connection` fixture's scope from `module` to `session`. By setting `scope='session'`, the fixture's value will be created only once for the entire test session and shared across all tests, modules, and packages that request it, providing the broadest possible sharing.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_14

LANGUAGE: python
CODE:

```
@pytest.fixture(scope="session")
def smtp_connection():
    # the returned fixture value will be shared for
    # all tests requesting it
    ...
```

---

TITLE: Specifying Required Pytest Plugins (INI)
DESCRIPTION: This configuration sets `required_plugins` to a space-separated list of plugins, including `pytest-django` with a version range, `pytest-html`, and `pytest-xdist` with a minimum version. Pytest will check for the presence of these plugins before running tests, emitting an error if any are not found. Version specifiers can directly follow plugin names.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_50

LANGUAGE: ini
CODE:

```
[pytest]
required_plugins = pytest-django>=3.0.0,<4.0.0 pytest-html pytest-xdist>=1.0.0
```

---

TITLE: Globally Preventing HTTP Requests with Autouse Fixture (Python)
DESCRIPTION: This `autouse` pytest fixture, defined in `conftest.py`, uses `monkeypatch.delattr` to remove the `requests.sessions.Session.request` method. This effectively prevents any HTTP requests from being made by the `requests` library across all tests, ensuring test isolation and preventing unintended external network calls.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_4

LANGUAGE: python
CODE:

```
import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")
```

---

TITLE: Recommended Assertion for Pytest Test Functions
DESCRIPTION: This Python snippet demonstrates the correct way to validate conditions within a pytest test function using an `assert` statement. Instead of returning a boolean, asserting directly ensures that the test fails if the condition is false, aligning with pytest's expected behavior for test outcomes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_8

LANGUAGE: Python
CODE:

```
@pytest.mark.parametrize(
    ["a", "b", "result"],
    [
        [1, 2, 5],
        [2, 3, 8],
        [5, 3, 18],
    ],
)
def test_foo(a, b, result):
    assert foo(a, b) == result
```

---

TITLE: Applying a Single Mark with `pytestmark` (Python)
DESCRIPTION: This snippet demonstrates how to apply a single `pytest` mark to a test module or class. By assigning `pytest.mark.webtest` to the `pytestmark` variable, all tests within that scope will be tagged with the 'webtest' mark, useful for selective test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_13

LANGUAGE: python
CODE:

```
import pytest

pytestmark = pytest.mark.webtest
```

---

TITLE: Sharing Mocked API Responses with Pytest Fixtures (Python)
DESCRIPTION: This example refactors the API response mocking into a pytest fixture named `mock_response`. This allows the mock to be easily shared and reused across multiple tests, promoting cleaner, more organized, and maintainable test code by centralizing the mocking logic.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_3

LANGUAGE: python
CODE:

```
import pytest
import requests
import app


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_json(mock_response):
    result = app.get_json("https://fakeurl")
    assert result["mock_key"] == "mock_response"
```

---

TITLE: Inlining Tests - Application Package Structure (Text)
DESCRIPTION: This snippet illustrates a recommended directory structure for embedding test directories directly within a Python application package. This setup is ideal for distributing tests alongside application modules, maintaining a clear relationship. It shows `pyproject.toml` at the root, a `mypkg` directory with application code, and a nested `tests` directory containing test files, all with `__init__.py` for package recognition.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_6

LANGUAGE: text
CODE:

```
pyproject.toml
[src/]mypkg/
	__init__.py
	app.py
	view.py
	tests/
		__init__.py
		test_app.py
		test_view.py
		...
```

---

TITLE: Add pytest Command Line Option and Fixture (conftest.py)
DESCRIPTION: Shows how to define a custom command line option using `pytest_addoption` and create a fixture (`cmdopt`) in `conftest.py` to make the option's value available to tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_6

LANGUAGE: python
CODE:

```
# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")
```

---

TITLE: Controlling Fixture Order by Scope in pytest (Python)
DESCRIPTION: This snippet demonstrates how pytest executes higher-scoped fixtures (e.g., `session`) before lower-scoped fixtures (e.g., `function` or `class`). The test will pass because the `session`-scoped fixture runs before the `function`-scoped one, ensuring dependencies are met based on scope.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_8

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture(scope="session")
def session_fixture():
    print("session_fixture executed")
    return "session_data"

@pytest.fixture(scope="function")
def function_fixture(session_fixture):
    print(f"function_fixture executed, received: {session_fixture}")
    return "function_data"

def test_order(function_fixture):
    print(f"test_order executed, received: {function_fixture}")
    assert function_fixture == "function_data"
```

---

TITLE: Correcting Sync Test Usage of Async Fixture in Pytest
DESCRIPTION: This snippet demonstrates the recommended approach to allow a synchronous test to depend on an asynchronous fixture. The asynchronous logic is encapsulated within an `inner_fixture` function, which is then called and returned by a synchronous `unawaited_fixture`. This ensures the coroutine is properly handled before being passed to the synchronous test, preventing warnings and unpredictable behavior.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_1

LANGUAGE: python
CODE:

```
import asyncio
import pytest


@pytest.fixture
def unawaited_fixture():
    async def inner_fixture():
        return 1

    return inner_fixture()


def test_foo(unawaited_fixture):
    assert 1 == asyncio.run(unawaited_fixture)
```

---

TITLE: Checking for Contained Exceptions with ExceptionInfo.group_contains() (Python)
DESCRIPTION: This example demonstrates the basic usage of excinfo.group_contains() to check for the presence of a specific exception type within an ExceptionGroup caught by pytest.raises. It also shows how to use the optional match parameter for message validation and how to assert the absence of an exception.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_13

LANGUAGE: python
CODE:

```
def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        raise ExceptionGroup(
            "Group message",
            [
                RuntimeError("Exception 123 raised"),
            ],
        )
    assert excinfo.group_contains(RuntimeError, match=r".* 123 .*")
    assert not excinfo.group_contains(TypeError)
```

---

TITLE: Parametrizing All Tests in a Class with pytest.mark.parametrize
DESCRIPTION: This example shows how to apply the @pytest.mark.parametrize decorator to an entire test class. When applied to a class, all test methods within that class (test_simple_case, test_weird_simple_case) will be executed for each defined set of parameters (n, expected). This is useful for sharing parameter sets across multiple tests related to a common scenario.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_3

LANGUAGE: python
CODE:

```
import pytest


@pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
class TestClass:
    def test_simple_case(self, n, expected):
        assert n + 1 == expected

    def test_weird_simple_case(self, n, expected):
        assert (n * 1) + 1 == expected
```

---

TITLE: Excluding Pytest Tests by Specific Marker
DESCRIPTION: This pytest command-line example shows how to run all tests except those marked with 'webtest' by using the 'not' operator with the '-m' option. The output confirms that 'test_send_http' is deselected, and the remaining tests are executed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_2

LANGUAGE: pytest
CODE:

```
$ pytest -v -m "not webtest"
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 1 deselected / 3 selected

test_server.py::test_something_quick PASSED                          [ 33%]
test_server.py::test_another PASSED                                  [ 66%]
test_server.py::TestClass::test_method PASSED                        [100%]

===================== 3 passed, 1 deselected in 0.12s ======================
```

---

TITLE: Dynamically Generating Test Parameters with pytest_generate_tests (Python)
DESCRIPTION: This `conftest.py` snippet defines two pytest hooks: `pytest_addoption` to introduce a `--all` command-line option, and `pytest_generate_tests` to dynamically parametrize the `param1` fixture. The range of `param1` values (up to 2 or 5) is determined by whether the `--all` option is provided, enabling conditional test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_1

LANGUAGE: python
CODE:

```
def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")


def pytest_generate_tests(metafunc):
    if "param1" in metafunc.fixturenames:
        if metafunc.config.getoption("all"):
            end = 5
        else:
            end = 2
        metafunc.parametrize("param1", range(end))
```

---

TITLE: Registering Custom Markers in pyproject.toml (TOML)
DESCRIPTION: This TOML configuration shows how to register custom markers within the `pyproject.toml` file under the `[tool.pytest.ini_options]` table. Similar to `pytest.ini`, this method registers markers with pytest, allowing for descriptions and avoiding warnings.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/mark.rst#_snippet_1

LANGUAGE: TOML
CODE:

```
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
```

---

TITLE: Applying Marks to Parametrize Values (Deprecated)
DESCRIPTION: This snippet demonstrates the deprecated method of applying marks directly to values within `pytest.mark.parametrize`. This approach was considered hard to read and hindered internal improvements. Users should migrate to `pytest.param` for marking individual parameters.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_24

LANGUAGE: python
CODE:

```
@pytest.mark.parametrize(
        "a, b",
        [
            (3, 9),
            pytest.mark.xfail(reason="flaky")(6, 36),
            (10, 100),
            (20, 200),
            (40, 400),
            (50, 500),
        ],
    )
    def test_foo(a, b): ...
```

---

TITLE: Matching Exception Messages with pytest.raises
DESCRIPTION: Shows how to use the `match` keyword parameter with `pytest.raises` to assert that the string representation of the raised exception matches a given regular expression. This allows for more granular checks on the content of the exception message.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_6

LANGUAGE: python
CODE:

```
import pytest


def myfunc():
    raise ValueError("Exception 123 raised")


def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
```

---

TITLE: Recording All Warnings with pytest.warns in Python
DESCRIPTION: This snippet shows how to record all warnings without asserting a specific type by calling `pytest.warns` with no arguments. The `record` object can then be used to inspect all warnings emitted within the context.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_16

LANGUAGE: python
CODE:

```
with pytest.warns() as record:
    warnings.warn("user", UserWarning)
    warnings.warn("runtime", RuntimeWarning)

assert len(record) == 2
assert str(record[0].message) == "user"
assert str(record[1].message) == "runtime"
```

---

TITLE: Example of Tests Outside Application Code Layout
DESCRIPTION: This text snippet illustrates a recommended project structure where tests reside in a separate `tests/` directory, distinct from the application's source code located in `src/mypkg/`. This separation helps in organizing large projects and allows tests to run against either an installed or an editable version of the package.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_2

LANGUAGE: text
CODE:

```
pyproject.toml
src/
    mypkg/
        __init__.py
        app.py
        view.py
tests/
    test_app.py
    test_view.py
    ...
```

---

TITLE: Defining a Module-Scoped Pytest Fixture in Python
DESCRIPTION: This snippet defines a `pytest` fixture named `smtp_connection` in a `conftest.py` file. The `scope='module'` decorator ensures that a single `smtplib.SMTP` connection instance is created once per module and shared across all tests within that module, optimizing resource usage. It returns an `SMTP` object connected to `smtp.gmail.com` on port 587 with a 5-second timeout.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_11

LANGUAGE: python
CODE:

```
# content of conftest.py
import smtplib

import pytest


@pytest.fixture(scope="module")
def smtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
```

---

TITLE: Conditionally Skipping Test Function with Pytest Mark Skipif (Python)
DESCRIPTION: This example shows how to use the `pytest.mark.skipif` decorator to conditionally skip a test function. The test will be skipped if the provided condition evaluates to `True` during test collection, with the specified reason appearing in the summary when using the `-rs` option.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_4

LANGUAGE: python
CODE:

```
import sys


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_function(): ...
```

---

TITLE: Defining a Parametrized Module-Scoped Pytest Fixture (Python)
DESCRIPTION: This Python snippet defines a Pytest fixture named `modarg` with a 'module' scope and parameters 'mod1' and 'mod2'. The `yield` keyword separates the setup and teardown phases, allowing resources to be initialized before tests and cleaned up afterward. The `request` object provides access to the parameter value for the current test run.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_47

LANGUAGE: python
CODE:

```
@pytest.fixture(scope="module", params=["mod1", "mod2"])
def modarg(request):
    param = request.param
    print("  SETUP modarg", param)
    yield param
    print("  TEARDOWN modarg", param)
```

---

TITLE: Applying a Custom pytest Mark with Arguments (Python)
DESCRIPTION: Demonstrates how to apply a custom `pytest` mark, `timeout`, as a decorator to a test function. This mark is created dynamically and includes positional arguments (10, "slow") and keyword arguments (method="thread"), which can be accessed later via the `Mark` object.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_3

LANGUAGE: python
CODE:

```
@pytest.mark.timeout(10, "slow", method="thread")
def test_function(): ...
```

---

TITLE: Defining a Function with Type Hints in Python
DESCRIPTION: This Python function `get_caption` demonstrates the use of type hints for parameters (`target: int`, `items: list[tuple[int, str]]`) and return value (`-> str`). The type checker can identify a potential bug where the function might implicitly return `None` if `target` is not found in `items`, even if tests achieve full coverage.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/types.rst#_snippet_0

LANGUAGE: python
CODE:

```
def get_caption(target: int, items: list[tuple[int, str]]) -> str:
    for value, caption in items:
        if value == target:
            return caption
```

---

TITLE: Pytest Fixture Caching and Side Effects in Python
DESCRIPTION: This snippet illustrates pytest's fixture caching mechanism, where a fixture is executed only once per test, and its return value is cached. The `append_first` fixture modifies the `order` list, and `test_string_only` observes this modification because both reference the same cached `order` object.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_8

LANGUAGE: Python
CODE:

```
import pytest


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order():
    return []


@pytest.fixture
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]
```

---

TITLE: Invoking PDB on First or N Failures with Pytest (Bash)
DESCRIPTION: These commands combine the `--pdb` option with failure limits to control when the debugger is invoked. `pytest -x --pdb` drops into PDB on the first failure then ends the session, while `pytest --pdb --maxfail=3` invokes PDB for the first three failures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/failures.rst#_snippet_2

LANGUAGE: bash
CODE:

```
pytest -x --pdb   # drop to PDB on first failure, then end test session
pytest --pdb --maxfail=3  # drop to PDB for first three failures
```

---

TITLE: Re-running Only Failed Pytest Tests with --lf
DESCRIPTION: This snippet illustrates the use of the `pytest --lf` (last-failed) option. When executed after an initial run with failures, `pytest` only collects and runs the previously failed tests, effectively 'deselecting' the passing ones. The output confirms that only the two failing tests (`test_num[17]` and `test_num[25]`) are executed, demonstrating the efficiency of this option for focused debugging.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_2

LANGUAGE: pytest
CODE:

```
$ pytest --lf
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items
run-last-failure: rerun previous 2 failures

test_50.py FF                                                        [100%]

================================= FAILURES =================================
_______________________________ test_num[17] _______________________________

i = 17

    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
>           pytest.fail("bad luck")
E           Failed: bad luck

test_50.py:7: Failed
_______________________________ test_num[25] _______________________________

i = 25

    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
>           pytest.fail("bad luck")
E           Failed: bad luck

test_50.py:7: Failed
========================= short test summary info ==========================
FAILED test_50.py::test_num[17] - Failed: bad luck
FAILED test_50.py::test_num[25] - Failed: bad luck
============================ 2 failed in 0.12s =============================
```

---

TITLE: Defining a Test Function with a Fixture in Python
DESCRIPTION: This Python snippet defines a simple test function `test_valid_string` that accepts a `stringinput` fixture. The test asserts that the provided string input consists only of alphabetic characters, serving as a basic example for dynamic parametrization.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_8

LANGUAGE: python
CODE:

```
# content of test_strings.py


def test_valid_string(stringinput):
    assert stringinput.isalpha()
```

---

TITLE: Listing Built-in and Custom Pytest Fixtures (Bash)
DESCRIPTION: This Bash command `pytest --fixtures` is used to list all available pytest fixtures, including both built-in and custom-defined ones. This is a useful command for discovering what resources and setup/teardown mechanisms are available for tests within a pytest project. It helps in understanding the testing environment and identifying potential fixtures to use or override.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_12

LANGUAGE: bash
CODE:

```
pytest --fixtures   # shows builtin and custom fixtures
```

---

TITLE: Parametrizing Pytest Fixtures for Multiple Test Runs (Python)
DESCRIPTION: This snippet demonstrates how to parametrize a `pytest` fixture using the `params` argument. The `smtp_connection` fixture will be instantiated twice, once for each parameter (`"smtp.gmail.com"` and `"mail.python.org"`), causing any dependent tests to run for each parameter value. The `request.param` attribute provides access to the current parameter value.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_38

LANGUAGE: python
CODE:

```
# content of conftest.py
import smtplib

import pytest


@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print(f"finalizing {smtp_connection}")
    smtp_connection.close()
```

---

TITLE: Installing Python Package in Editable Mode using pip
DESCRIPTION: This bash command installs the current Python package in 'editable' mode. This allows developers to modify source code (both application and tests) and immediately see changes reflected without needing to reinstall the package, streamlining the development and testing workflow.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -e .
```

---

TITLE: Running Pytest with Multiple Marker Selection (OR logic)
DESCRIPTION: This `pytest` command-line example illustrates how to run tests that are marked with either 'interface' OR 'event' using the `-m` option with a boolean expression. The output confirms that tests matching either marker are selected and executed, demonstrating the flexibility of marker expressions for test filtering.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_35

LANGUAGE: pytest
CODE:

```
$ pytest -m "interface or event" --tb=short
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 4 items / 1 deselected / 3 selected

test_module.py FFF                                                   [100%]

================================= FAILURES =================================
__________________________ test_interface_simple ___________________________
test_module.py:4: in test_interface_simple
    assert 0
E   assert 0
__________________________ test_interface_complex __________________________
test_module.py:8: in test_interface_complex
    assert 0
E   assert 0
____________________________ test_event_simple _____________________________
test_module.py:12: in test_event_simple
    assert 0
E   assert 0
========================= short test summary info ==========================
FAILED test_module.py::test_interface_simple - assert 0
FAILED test_module.py::test_interface_complex - assert 0
FAILED test_module.py::test_event_simple - assert 0
===================== 3 failed, 1 deselected in 0.12s ======================
```

---

TITLE: Stopping Pytest After N Failures (Bash)
DESCRIPTION: This snippet demonstrates how to configure pytest to stop its execution after a specified number of test failures. Using `-x` halts the session after the very first failure, while `--maxfail=N` allows testing to continue until N failures have occurred.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/failures.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest -x           # stop after first failure
pytest --maxfail=2  # stop after two failures
```

---

TITLE: Testing Email Functionality with Pytest Yield Fixtures
DESCRIPTION: This test file demonstrates how to use pytest `yield` fixtures for setting up and tearing down test resources, specifically for an email sending scenario. It defines fixtures for `mail_admin`, `sending_user`, and `receiving_user`, with cleanup logic placed after the `yield` statement to ensure proper resource release, such as deleting users and clearing mailboxes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_18

LANGUAGE: Python
CODE:

```
# content of test_emaillib.py
from emaillib import Email, MailAdminClient

import pytest


@pytest.fixture
def mail_admin():
    return MailAdminClient()


@pytest.fixture
def sending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    mail_admin.delete_user(user)


@pytest.fixture
def receiving_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    user.clear_mailbox()
    mail_admin.delete_user(user)


def test_email_received(sending_user, receiving_user):
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    assert email in receiving_user.inbox
```

---

TITLE: Monkeypatching Path.home for Consistent Testing (Python)
DESCRIPTION: This snippet demonstrates using `pytest.monkeypatch.setattr` to replace the `Path.home` function with a mock function that always returns a predefined path (`/abc`). This technique is crucial for isolating tests from the actual user's home directory, ensuring consistent and reproducible test results regardless of the execution environment. The patch is automatically reverted after the test completes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_0

LANGUAGE: Python
CODE:

```
# contents of test_module.py with source code and the test
from pathlib import Path


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
```

---

TITLE: Pytest Fixtures for Optional Module Imports (conftest.py)
DESCRIPTION: This `conftest.py` snippet defines session-scoped pytest fixtures (`basemod` and `optmod`) that use `pytest.importorskip` to conditionally import modules. This allows tests to compare different implementations of an API, skipping tests if an implementation is not available.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_20

LANGUAGE: python
CODE:

```
# content of conftest.py

import pytest


@pytest.fixture(scope="session")
def basemod(request):
    return pytest.importorskip("base")


@pytest.fixture(scope="session", params=["opt1", "opt2"])
def optmod(request):
    return pytest.importorskip(request.param)
```

---

TITLE: Accessing Exception Information with pytest.raises
DESCRIPTION: Illustrates how to capture and inspect the actual exception information using `pytest.raises` by assigning the context manager to a variable (`excinfo`). The `excinfo` object provides access to the exception's type, value, and traceback for further assertions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_4

LANGUAGE: python
CODE:

```
def test_recursion_depth():
    with pytest.raises(RuntimeError) as excinfo:

        def f():
            f()

        f()
    assert "maximum recursion" in str(excinfo.value)
```

---

TITLE: Asserting UserWarning with pytest.warns in Python
DESCRIPTION: This snippet demonstrates how to use `pytest.warns` as a context manager to assert that a specific `UserWarning` is raised within the enclosed code block. The test will fail if the expected warning is not emitted.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_12

LANGUAGE: python
CODE:

```
import warnings

import pytest


def test_warning():
    with pytest.warns(UserWarning):
        warnings.warn("my warning", UserWarning)
```

---

TITLE: Running Pytest with Matching Environment (CLI)
DESCRIPTION: This example shows running pytest with the `-E` option set to 'stage1', which matches the environment marker on `test_basic_db_operation`. As a result, the test passes successfully. This confirms that tests marked with `pytest.mark.env` are executed only when the specified environment matches the command-line argument.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_20

LANGUAGE: pytest
CODE:

```
$ pytest -E stage1
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_someenv.py .                                                    [100%]

============================ 1 passed in 0.12s =============================
```

---

TITLE: Pytest Configuration File Search Order (Text)
DESCRIPTION: This text snippet illustrates the hierarchical search order pytest follows to locate configuration files (pytest.ini, pyproject.toml, tox.ini, setup.cfg) and setup.py files. The search starts from the common ancestor directory (path in the example) and proceeds upwards to the root, with specific content requirements for pyproject.toml, tox.ini, and setup.cfg to be considered a match.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/customize.rst#_snippet_6

LANGUAGE: text
CODE:

```
# first look for pytest.ini files
path/pytest.ini
path/pyproject.toml  # must contain a [tool.pytest.ini_options] table to match
path/tox.ini         # must contain [pytest] section to match
path/setup.cfg       # must contain [tool:pytest] section to match
pytest.ini
... # all the way up to the root

# now look for setup.py
path/setup.py
setup.py
... # all the way up to the root
```

---

TITLE: Querying Recorded Warnings with pytest.warns in Python
DESCRIPTION: This example demonstrates how `pytest.warns` returns a list of `warnings.WarningMessage` objects, allowing for detailed inspection of raised warnings. It shows how to check the number of warnings and assert specific message content.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_15

LANGUAGE: python
CODE:

```
with pytest.warns(RuntimeWarning) as record:
    warnings.warn("another warning", RuntimeWarning)

# check that only one warning was raised
assert len(record) == 1
# check that the message matches
assert record[0].message.args[0] == "another warning"
```

---

TITLE: Using `reason` instead of `msg` in pytest.fail/skip/exit
DESCRIPTION: This snippet demonstrates the deprecation of the `msg` keyword argument in `pytest.fail`, `pytest.skip`, and `pytest.exit`. Users should now use the `reason` keyword argument for consistency with `@pytest.mark.skip` and `@pytest.mark.xfail` markers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_15

LANGUAGE: Python
CODE:

```
def test_fail_example():
    # old
    pytest.fail(msg="foo")
    # new
    pytest.fail(reason="bar")


def test_skip_example():
    # old
    pytest.skip(msg="foo")
    # new
    pytest.skip(reason="bar")


def test_exit_example():
    # old
    pytest.exit(msg="foo")
    # new
    pytest.exit(reason="bar")
```

---

TITLE: Typing a Pytest Fixture Function
DESCRIPTION: This snippet shows how to apply type hints to a pytest fixture. The `sample_fixture` is annotated to return an `int`, demonstrating that standard Python typing works seamlessly with pytest fixtures without special considerations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/types.rst#_snippet_2

LANGUAGE: python
CODE:

```
import pytest


@pytest.fixture
def sample_fixture() -> int:
    return 38
```

---

TITLE: Skipping All Test Functions in a Module with Pytestmark (Python)
DESCRIPTION: This snippet shows how to skip all test functions within a module by assigning a `pytest.mark.skipif` marker to the global `pytestmark` variable at the module level. This provides a concise way to apply a skip condition to an entire module, affecting all tests defined within it.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_7

LANGUAGE: python
CODE:

```
# test_module.py
pytestmark = pytest.mark.skipif(...)
```

---

TITLE: Implementing Pytest Fixtures with addfinalizer for Email Testing (Python)
DESCRIPTION: This Python code demonstrates how to use `pytest.fixture` in conjunction with `request.addfinalizer` to ensure proper resource cleanup (e.g., deleting users, clearing mailboxes) after tests. It provides a structured way to manage setup and teardown, offering an alternative to `yield` fixtures for explicit finalization.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_20

LANGUAGE: python
CODE:

```
# content of test_emaillib.py
from emaillib import Email, MailAdminClient

import pytest


@pytest.fixture
def mail_admin():
    return MailAdminClient()


@pytest.fixture
def sending_user(mail_admin):
    user = mail_admin.create_user()
    yield user
    mail_admin.delete_user(user)


@pytest.fixture
def receiving_user(mail_admin, request):
    user = mail_admin.create_user()

    def delete_user():
        mail_admin.delete_user(user)

    request.addfinalizer(delete_user)
    return user


@pytest.fixture
def email(sending_user, receiving_user, request):
    _email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(_email, receiving_user)

    def empty_mailbox():
        receiving_user.clear_mailbox()

    request.addfinalizer(empty_mailbox)
    return _email


def test_email_received(receiving_user, email):
    assert email in receiving_user.inbox
```

---

TITLE: Defining a class-scoped pytest fixture for unittest (Python)
DESCRIPTION: This Python code defines a pytest fixture named `db_class` with a `scope='class'`, meaning it's invoked once per test class. It creates a `DummyDB` instance and attaches it as a `db` attribute to the test class via `request.cls.db`, making the database object available to all test methods within that class. This demonstrates how to integrate pytest's fixture mechanism with `unittest.TestCase`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst#_snippet_1

LANGUAGE: python
CODE:

```
# content of conftest.py

# we define a fixture function below and it will be "used" by
# referencing its name from tests

import pytest


@pytest.fixture(scope="class")
def db_class(request):
    class DummyDB:
        pass

    # set a class attribute on the invoking test context
    request.cls.db = DummyDB()
```

---

TITLE: Defining a Basic Parametrized Test Function (Python)
DESCRIPTION: This Python snippet defines a simple pytest test function `test_compute` that takes a `param1` argument. It includes an assertion that `param1` must be less than 4, serving as a foundational example for subsequent parametrization demonstrations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_0

LANGUAGE: python
CODE:

```
def test_compute(param1):
    assert param1 < 4
```

---

TITLE: Running Failed Pytest Tests First with --ff
DESCRIPTION: This snippet demonstrates the `pytest --ff` (failed-first) option. Unlike `--lf`, this option runs all tests, but prioritizes the execution of previously failed tests before running the rest. The output shows 'FF' for the initial failed tests, followed by dots for the passing tests, illustrating how this option ensures quick feedback on fixes while still running the full test suite.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_3

LANGUAGE: pytest
CODE:

```
$ pytest --ff
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 50 items
run-last-failure: rerun previous 2 failures first

test_50.py FF................................................        [100%]

================================= FAILURES =================================
_______________________________ test_num[17] _______________________________

i = 17

    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
>           pytest.fail("bad luck")
E           Failed: bad luck

test_50.py:7: Failed
_______________________________ test_num[25] _______________________________

i = 25

    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
>           pytest.fail("bad luck")
E           Failed: bad luck
```

---

TITLE: Adjusting pytest Output Verbosity (Bash)
DESCRIPTION: Examples of bash commands using flags like `-q` and `-v` to control the verbosity level of pytest's output during test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pytest --quiet          # quiet - less verbose - mode
pytest -q               # quiet - less verbose - mode (shortcut)
pytest -v               # increase verbosity, display individual test names
pytest -vv              # more verbose, display more details from the test output
pytest -vvv             # not a standard , but may be used for even more detail in certain setups
```

---

TITLE: Setting Root Logger Level with caplog (Python)
DESCRIPTION: This Python snippet shows how to change the log level for the root logger within a test using the `caplog` fixture. By calling `caplog.set_level(logging.INFO)`, all log messages at or above the INFO level will be captured for the duration of the test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_7

LANGUAGE: python
CODE:

```
def test_foo(caplog):
        caplog.set_level(logging.INFO)
```

---

TITLE: Demonstrating Test Class Instance Isolation in Pytest (Python)
DESCRIPTION: This Python code defines a test class `TestClassDemoInstance` to illustrate how pytest handles test instances. Each test method (`test_one`, `test_two`) receives a unique instance of the class, ensuring test isolation. The `value` attribute, initialized at the class level, acts as a class attribute, demonstrating that changes to `self.value` in one test do not affect the initial state of `self.value` in another test method within the same class due to instance isolation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_8

LANGUAGE: python
CODE:

```
# content of test_class_demo.py
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1
```

---

TITLE: Marking Individual Parametrized Test Instances
DESCRIPTION: This snippet illustrates how to apply specific pytest marks, such as pytest.mark.xfail, to individual parameter sets within the @pytest.mark.parametrize decorator. By using pytest.param, you can selectively mark certain test instances to behave differently (e.g., expected to fail) without affecting others.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_5

LANGUAGE: python
CODE:

```
# content of test_expectation.py
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
```

---

TITLE: Asserting Expected Exception Groups with pytest.RaisesGroup
DESCRIPTION: Demonstrates the use of `pytest.RaisesGroup` to assert that a `BaseExceptionGroup` or `ExceptionGroup` containing specific exception types is raised. This is useful for testing code that raises multiple exceptions encapsulated within a group.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_7

LANGUAGE: python
CODE:

```
def test_exception_in_group():
    with pytest.RaisesGroup(ValueError):
        raise ExceptionGroup("group msg", [ValueError("value msg")])
    with pytest.RaisesGroup(ValueError, TypeError):
```

---

TITLE: Controlling ExceptionGroup Structure and Unwrapped Exceptions (Python)
DESCRIPTION: This example illustrates how pytest.RaisesGroup handles nested exception groups and unwrapped exceptions. It demonstrates using flatten_subgroups=True to match exceptions within nested groups and allow_unwrapped=True to permit matching a single, unwrapped exception against RaisesGroup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_9

LANGUAGE: python
CODE:

```
def test_structure():
    with pytest.RaisesGroup(pytest.RaisesGroup(ValueError)):
        raise ExceptionGroup("", (ExceptionGroup("", (ValueError(),)),))
    with pytest.RaisesGroup(ValueError, flatten_subgroups=True):
        raise ExceptionGroup("1st group", [ExceptionGroup("2nd group", [ValueError()])])
    with pytest.RaisesGroup(ValueError, allow_unwrapped=True):
        raise ValueError
```

---

TITLE: Ensuring No Warnings are Emitted in Python
DESCRIPTION: This snippet shows how to configure the `warnings` module to treat all warnings as errors within a context, effectively ensuring that no warnings are emitted. If any warning occurs, it will raise an error and fail the test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_20

LANGUAGE: python
CODE:

```
def test_warning():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        ...
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest version (7.4.1 in this context) using the pip package manager. The `--upgrade` flag ensures that pip replaces the current version with the new one, making it a drop-in replacement.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.4.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Running Pytest Tests by Marker Keyword Argument
DESCRIPTION: This pytest command-line example demonstrates how to select tests based on a marker's specific keyword argument value, using the '-m' option with an expression like "device(serial='123')". This allows for fine-grained selection of tests, such as only running 'device' tests with a specific serial number.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_3

LANGUAGE: pytest
CODE:

```
$ pytest -v -m "device(serial='123')"
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 3 deselected / 1 selected

test_server.py::test_something_quick PASSED                          [100%]

===================== 1 passed, 3 deselected in 0.12s ======================
```

---

TITLE: Creating Parameterized Data with Pytest Fixture Factories (Python)
DESCRIPTION: This snippet demonstrates the "factory as fixture" pattern in `pytest`. The `make_customer_record` fixture returns a function (`_make_customer_record`) that can be called multiple times within a single test to generate distinct, parameterized data objects (customer records in this case). This is useful when a fixture's result is needed multiple times.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_36

LANGUAGE: python
CODE:

```
@pytest.fixture
def make_customer_record():
    def _make_customer_record(name):
        return {"name": name, "orders": []}

    return _make_customer_record


def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")
```

---

TITLE: Running Class-Based pytest Tests and Reviewing Results
DESCRIPTION: This command executes pytest on test_class.py, which contains tests grouped within a class. The output shows a mix of passed and failed tests, along with detailed assertion failure information, demonstrating pytest's ability to run and report on class-organized tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_7

LANGUAGE: pytest
CODE:

```
$ pytest -q test_class.py
.F                                                                   [100%]
================================= FAILURES =================================
____________________________ TestClass.test_two ____________________________

self = <test_class.TestClass object at 0xdeadbeef0001>

    def test_two(self):
        x = "hello"
>       assert hasattr(x, "check")
E       AssertionError: assert False
E        +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
========================= short test summary info ==========================
FAILED test_class.py::TestClass::test_two - AssertionError: assert False
1 failed, 1 passed in 0.12s
```

---

TITLE: Configuring pytest pythonpath in pyproject.toml
DESCRIPTION: This TOML snippet configures `pytest` to permanently include the `src` directory in Python's module search path via the `pythonpath` option in `pyproject.toml`. This provides a persistent way for `pytest` to locate and import modules from the `src` layout when an editable install is not used.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_5

LANGUAGE: toml
CODE:

```
[tool.pytest.ini_options]
pythonpath = "src"
```

---

TITLE: Preventing Pytest Class Discovery with **test** (Python)
DESCRIPTION: This Python example shows how to prevent Pytest from discovering a class as a test class, even if its name starts with `Test`. By setting the `__test__` attribute to `False` within the class, Pytest will explicitly ignore it during collection, a feature available since Pytest 2.6.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_20

LANGUAGE: python
CODE:

```
# Will not be discovered as a test
class TestClass:
    __test__ = False
```

---

TITLE: Recommended pytest.raises with pytest.fail for Custom Messages (Python)
DESCRIPTION: Demonstrates the recommended approach for providing custom failure messages with `pytest.raises` after the deprecation of the `message` parameter. Users should now call `pytest.fail` manually within the `with` statement.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_21

LANGUAGE: Python
CODE:

```
with pytest.raises(TimeoutError):
    wait_for(websocket.recv(), 0.5)
    pytest.fail("Client got unexpected message")
```

---

TITLE: Running Tests in a Module (Bash)
DESCRIPTION: This command executes all tests found within a specified Python module file. Pytest will discover functions and classes adhering to its standard test discovery rules within 'test_mod.py'.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest test_mod.py
```

---

TITLE: Defining a pytest Fixture with a Dependency (Python)
DESCRIPTION: Illustrates how one `pytest` fixture (`db_session`) can depend on another fixture (`tmp_path`). The `tmp_path` fixture provides a unique temporary directory, which is then used to create a database file for the `db_session`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_7

LANGUAGE: python
CODE:

```
@pytest.fixture
def db_session(tmp_path):
    fn = tmp_path / "db.file"
    return connect(fn)
```

---

TITLE: Applying Marks and IDs to Parametrized Tests with pytest.param
DESCRIPTION: This Python snippet demonstrates how to use `pytest.param` within a `@pytest.mark.parametrize` decorator to apply specific marks (like `pytest.mark.basic`) or custom test IDs to individual test cases, allowing for more granular control over test execution and reporting.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_25

LANGUAGE: python
CODE:

```
# content of test_pytest_param_example.py
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("3+5", 8),
        pytest.param("1+7", 8, marks=pytest.mark.basic),
        pytest.param("2+4", 6, marks=pytest.mark.basic, id="basic_2+4"),
        pytest.param(
```

---

TITLE: Using Autouse Pytest Fixtures in Python
DESCRIPTION: This example demonstrates an `autouse` fixture (`append_first`), which is automatically invoked for all tests within its scope without explicit request. Both `test_string_only` and `test_string_and_int` are affected by `append_first`'s side effects on the `order` fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_9

LANGUAGE: Python
CODE:

```
import pytest


@pytest.fixture
def first_entry():
    return "a"


@pytest.fixture
def order(first_entry):
    return []


@pytest.fixture(autouse=True)
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(order, first_entry):
    assert order == [first_entry]


def test_string_and_int(order, first_entry):
    order.append(2)
    assert order == [first_entry, 2]
```

---

TITLE: Running Pytest for Package-Aware Test Discovery (Bash)
DESCRIPTION: This `bash` command initiates `pytest` from the `root/` directory. When `pytest` encounters test modules or `conftest.py` files within a Python package structure (indicated by `__init__.py` files), it identifies the package root and prepends it to `sys.path`. This ensures modules are imported with their full package name, preventing naming conflicts and preserving the package context.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/pythonpath.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest root/
```

---

TITLE: Using tmp_path fixture in pytest (Python)
DESCRIPTION: Demonstrates how to use the function-scoped `tmp_path` fixture, a `pathlib.Path` object, to create and manage temporary directories and files within a pytest test function.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/tmp_path.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_tmp_path.py
CONTENT = "content"


def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT, encoding="utf-8")
    assert p.read_text(encoding="utf-8") == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 0
```

---

TITLE: Defining Doctests in Python Docstrings
DESCRIPTION: This Python code snippet shows how to embed a doctest directly within a function's docstring. When `pytest` is run with the `--doctest-modules` option, it will discover and execute this interactive example as a test case.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst#_snippet_3

LANGUAGE: python
CODE:

```
# content of mymodule.py
def something():
    """a doctest in a docstring
    >>> something()
    42
    """
    return 42
```

---

TITLE: Controlling Test Skipping with Command Line Option in Pytest (Python)
DESCRIPTION: Defines a `--runslow` option and a `slow` marker in `conftest.py`. The `pytest_collection_modifyitems` hook is used to iterate through collected tests and add a skip marker to tests marked `slow` unless the `--runslow` option was provided.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_15

LANGUAGE: python
CODE:

```
# content of conftest.py

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```

---

TITLE: Testing Bad Login Credentials with Pytest (Python)
DESCRIPTION: This snippet demonstrates how to test a login scenario with bad credentials using pytest. It defines a `faux_user` fixture that creates a copy of a user with an incorrect password and then uses `pytest.raises` to assert that a `BadCredentialsException` is raised upon attempting to log in with these credentials.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_30

LANGUAGE: python
CODE:

```
class TestLandingPageBadCredentials:
    @pytest.fixture(scope="class")
    def faux_user(self, user):
        _user = deepcopy(user)
        _user.password = "badpass"
        return _user

    def test_raises_bad_credentials_exception(self, login_page, faux_user):
        with pytest.raises(BadCredentialsException):
            login_page.login(faux_user)
```

---

TITLE: Demonstrating Context-Sensitive Set Comparison (Python)
DESCRIPTION: Provides a Python test example demonstrating pytest's ability to offer rich, context-sensitive information for failed assertions, specifically for set comparisons. It highlights how pytest identifies extra or missing items in sets.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_18

LANGUAGE: Python
CODE:

```
# content of test_assert2.py
def test_set_comparison():
    set1 = set("1308")
    set2 = set("8035")
    assert set1 == set2
```

---

TITLE: Deferring Pytest Fixture Setup with `indirect` Parametrization in Python
DESCRIPTION: This `conftest.py` file defines a `pytest_generate_tests` hook and a `db` fixture to demonstrate deferred setup of parametrized resources. The hook parametrizes the `db` fixture with values `d1` and `d2` using `indirect=True`, which tells pytest to pass the values to the `db` fixture for instantiation. The `db` fixture then creates either a `DB1` or `DB2` object based on the requested parameter, ensuring expensive resource setup occurs only when the test runs.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_10

LANGUAGE: python
CODE:

```
# content of conftest.py
import pytest


def pytest_generate_tests(metafunc):
    if "db" in metafunc.fixturenames:
        metafunc.parametrize("db", ["d1", "d2"], indirect=True)


class DB1:
    "one database object"


class DB2:
    "alternative database object"


@pytest.fixture
def db(request):
    if request.param == "d1":
        return DB1()
    elif request.param == "d2":
        return DB2()
    else:
        raise ValueError("invalid internal test config")
```

---

TITLE: Accessing Captured Output with Pytest Fixtures (Python)
DESCRIPTION: This Python test function demonstrates how to programmatically access captured stdout and stderr using the `capsys` fixture. The `readouterr()` method snapshots the output generated up to that point, allowing assertions against `captured.out` and `captured.err`. This enables testing functions that produce console output directly within pytest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-stdout-stderr.rst#_snippet_3

LANGUAGE: python
CODE:

```
def test_myoutput(capsys):  # or use "capfd" for fd-level
    print("hello")
    sys.stderr.write("world\n")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
    assert captured.err == "world\n"
    print("next")
    captured = capsys.readouterr()
    assert captured.out == "next\n"
```

---

TITLE: Chaining Pytest Fixtures (Fixture Dependencies) in Python
DESCRIPTION: This snippet illustrates how one pytest fixture (`order`) can request and utilize another fixture (`first_entry`) as a dependency. It shows how `pytest` resolves these dependencies recursively, providing a structured way to build complex test setups from smaller, reusable components, and then how a test function consumes the final fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_2

LANGUAGE: python
CODE:

```
# contents of test_append.py
import pytest


# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]
```

---

TITLE: Illustrating Pytest Fixture Error Handling and Execution Order in Python
DESCRIPTION: This example showcases pytest's behavior when a fixture raises an exception. It defines a series of dependent fixtures (`order`, `append_first`, `append_second`, `append_third`) that modify a shared list. If an earlier fixture, like `append_first`, fails, pytest will stop executing subsequent fixtures and the test itself, marking the test as an error rather than a failure, indicating it couldn't be attempted.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/fixtures.rst#_snippet_1

LANGUAGE: Python
CODE:

```
import pytest


@pytest.fixture
def order():
    return []


@pytest.fixture
def append_first(order):
    order.append(1)


@pytest.fixture
def append_second(order, append_first):
    order.extend([2])


@pytest.fixture(autouse=True)
def append_third(order, append_second):
    order += [3]


def test_order(order):
    assert order == [1, 2, 3]
```

---

TITLE: Selecting pytest Tests by Keyword (http)
DESCRIPTION: This command demonstrates how to use the -k option in pytest to select tests whose names or parent names contain the substring "http". It runs tests verbosely and shows that test_send_http is selected.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_7

LANGUAGE: pytest
CODE:

```
$ pytest -v -k http  # running with the above defined example module
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 3 deselected / 1 selected

test_server.py::test_send_http PASSED                                [100%]

===================== 1 passed, 3 deselected in 0.12s ======================
```

---

TITLE: Capturing Text Stdout/Stderr with capsys
DESCRIPTION: This example demonstrates using the `capsys` fixture to capture text-based output from `sys.stdout` and `sys.stderr`. The `readouterr()` method returns a `(out, err)` namedtuple, where `out` and `err` are `text` (string) objects, suitable for asserting on standard text console output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_4

LANGUAGE: python
CODE:

```
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This command upgrades an existing pytest installation to the latest version (4.6.9 in this context) using the pip package installer. It ensures you have the most recent bug fixes and features.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.6.9.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command is used to upgrade the pytest testing framework to its latest version available on PyPI. The '-U' flag ensures that the package is upgraded if it's already installed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.3.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Running Pytest with XFAIL
DESCRIPTION: This snippet shows the output of a Pytest run where one test case is marked as 'xfailed' (expected to fail). This is useful for documenting known issues or features that are not yet fully implemented but are expected to fail.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_6

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_expectation.py ..x                                              [100%]

======================= 2 passed, 1 xfailed in 0.12s =======================
```

---

TITLE: Upgrading pytest to 4.6.2 via pip (Shell)
DESCRIPTION: This command is used to upgrade an existing pytest installation to version 4.6.2. The '--upgrade' flag ensures that pip replaces the current version with the specified or latest available version, providing access to the latest bug fixes and improvements.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.6.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades the pytest testing framework to its latest version available on PyPI. The `-U` flag ensures that an existing installation is updated rather than a new one being installed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.4.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command uses the pip package manager to upgrade the pytest testing framework to its latest available version. The -U flag ensures that if pytest is already installed, it will be updated to the newest release.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.6.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Typing a Pytest Fixture that Depends on Another Fixture
DESCRIPTION: This example shows how to type-annotate a pytest fixture that itself depends on another fixture. The `monkeypatch` fixture is typed as `pytest.MonkeyPatch`, and the `mock_env_user` fixture is typed to return `None`, illustrating how type hints propagate through fixture dependencies.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/types.rst#_snippet_5

LANGUAGE: python
CODE:

```
@pytest.fixture
def mock_env_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("USER", "TestingUser")
```

---

TITLE: Asserting on Captured Log Records and Text (Python)
DESCRIPTION: This Python snippet shows how to access captured log messages as `logging.LogRecord` instances (`caplog.records`) and as a single string (`caplog.text`) for assertion purposes. It allows verifying log content, levels, and presence of specific text after a function call.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_11

LANGUAGE: python
CODE:

```
def test_baz(caplog):
        func_under_test()
        for record in caplog.records:
            assert record.levelname != "CRITICAL"
        assert "wally" not in caplog.text
```

---

TITLE: Registering External Pytest Fixtures via pytest_plugins
DESCRIPTION: This snippet shows how to register an external module containing pytest fixtures as a plugin using the `pytest_plugins` variable. By assigning the module path "mylibrary.fixtures" to `pytest_plugins` in a `conftest.py` file, all fixtures and hooks within that module become available to tests in the current directory and its subdirectories. This is a recommended way to reuse fixtures from other projects.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_64

LANGUAGE: Python
CODE:

```
pytest_plugins = "mylibrary.fixtures"
```

---

TITLE: Setting Default Database with Pytest Monkeypatch (Python)
DESCRIPTION: This snippet demonstrates how to use `monkeypatch.setitem` to temporarily modify the `database` key in `app.DEFAULT_CONFIG` to `test_db` for testing purposes. It's typically used within a pytest fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_13

LANGUAGE: Python
CODE:

```
monkeypatch.setitem(app.DEFAULT_CONFIG, "database", "test_db")
```

---

TITLE: Running Tests in a Directory (Bash)
DESCRIPTION: This command instructs pytest to discover and execute all tests located within the specified directory and its subdirectories. Pytest will apply its standard test discovery rules to files and directories within 'testing/'.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pytest testing/
```

---

TITLE: Defining Pytest Test Cases and Fixture (Python)
DESCRIPTION: This Python code defines a series of test functions and a fixture to demonstrate various possible outcomes when running tests with pytest, including passing, failing, skipping, expected failures (xfail), expected passes (xpass), and errors during setup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_7

LANGUAGE: python
CODE:

```
# content of test_example.py
import pytest


@pytest.fixture
def error_fixture():
    assert 0


def test_ok():
    print("ok")


def test_fail():
    assert 0


def test_error(error_fixture):
    pass


def test_skip():
    pytest.skip("skipping this test")


def test_xfail():
    pytest.xfail("xfailing this test")


@pytest.mark.xfail(reason="always xfail")
def test_xpass():
    pass
```

---

TITLE: Assert List Equality in Pytest
DESCRIPTION: Demonstrates a failed assertion comparing two lists that differ by a single element. Pytest provides a specific diff highlighting the index and values that differ.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_9

LANGUAGE: python
CODE:

```
assert [0, 1, 2] == [0, 1, 3]
```

---

TITLE: Applying Marks to Parametrized Fixtures in Pytest
DESCRIPTION: This snippet demonstrates how to use `pytest.param` to apply marks, specifically `pytest.mark.skip`, to individual values within a parametrized fixture. This allows selective skipping of test invocations based on specific fixture parameters, enhancing test control and flexibility.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_42

LANGUAGE: python
CODE:

```
# content of test_fixture_marks.py
import pytest


@pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
def data_set(request):
    return request.param


def test_data(data_set):
    pass
```

---

TITLE: Defining Autouse Pytest Fixture for Unittest Class
DESCRIPTION: This Python code defines an autouse pytest fixture, initdir, within a unittest.TestCase class. It leverages tmp_path and monkeypatch to change the current directory to a temporary one and create a samplefile.ini, automatically setting up a controlled environment for all test methods in the class.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst#_snippet_6

LANGUAGE: python
CODE:

```
import unittest

import pytest


class MyTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initdir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)  # change to pytest-provided temporary directory
        tmp_path.joinpath("samplefile.ini").write_text("# testdata", encoding="utf-8")

    def test_method(self):
        with open("samplefile.ini", encoding="utf-8") as f:
            s = f.read()
        assert "testdata" in s
```

---

TITLE: Customizing Pytest Fixture IDs with `ids` Parameter
DESCRIPTION: This Python code demonstrates how to customize the test IDs generated by `pytest` for parametrized fixtures using the `ids` keyword argument. It shows two methods: providing a list of strings for explicit IDs (e.g., "spam", "ham") or supplying a function that dynamically generates IDs based on the fixture value, returning `None` to fall back to `pytest`'s default ID generation. This allows for more readable and meaningful test identifiers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_40

LANGUAGE: python
CODE:

```
# content of test_ids.py
import pytest


@pytest.fixture(params=[0, 1], ids=["spam", "ham"])
def a(request):
    return request.param


def test_a(a):
    pass


def idfn(fixture_value):
    if fixture_value == 0:
        return "eggs"
    else:
        return None


@pytest.fixture(params=[0, 1], ids=idfn)
def b(request):
    return request.param


def test_b(b):
    pass
```

---

TITLE: Overriding Pytest Fixtures in a Separate Module
DESCRIPTION: This code demonstrates how fixtures are overridden in `test_something_else.py`. It shows a `test_username` function that now expects `parametrized_username` to behave as a parametrized fixture, and another `test_username` that expects `non_parametrized_username` to be a simple, non-parametrized value. This illustrates fixture overriding at the module level.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_63

LANGUAGE: Python
CODE:

```
# content of tests/test_something_else.py
def test_username(parametrized_username):
    assert parametrized_username in ['one', 'two', 'three']

def test_username(non_parametrized_username):
    assert non_parametrized_username == 'username'
```

---

TITLE: Defining 'mid' Autouse Fixture with Plugin Dependency in pytest (tests/subpackage/conftest.py)
DESCRIPTION: This `autouse` pytest fixture, located in `tests/subpackage/conftest.py`, automatically appends 'mid subpackage' to the `order` list. It depends on `order` and `b_fix` (a plugin-provided fixture), showcasing automatic execution and interaction with external plugin fixtures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_6

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture(autouse=True)
def mid(order, b_fix):
    order.append("mid subpackage")
```

---

TITLE: Defining a Custom pytest Fixture with Options (Python)
DESCRIPTION: This example demonstrates how to create a pytest plugin that defines a custom fixture named `hello`. It includes the `pytest_addoption` hook to add a command-line option `--name` and the `hello` fixture itself, which yields a function that returns a greeting based on the option or a provided argument.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_9

LANGUAGE: Python
CODE:

```
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("helloworld")
    group.addoption(
        "--name",
        action="store",
        dest="name",
        default="World",
        help='Default "name" for hello().',
    )


@pytest.fixture
def hello(request):
    name = request.config.getoption("name")

    def _hello(name=None):
        if not name:
            name = request.config.getoption("name")
        return f"Hello {name}!"

    return _hello
```

---

TITLE: Conditionally Skipping All Tests in a Pytest Module
DESCRIPTION: This snippet demonstrates how to skip all tests in a module based on a specific condition, such as the operating system. If the condition `sys.platform == "win32"` is true, all tests in the module will be skipped.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_11

LANGUAGE: python
CODE:

```
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")
```

---

TITLE: Defining Pytest Fixtures and Tests (Initial)
DESCRIPTION: This snippet defines a parametrized `pytest` fixture named `non_parametrized_username` and two test functions. The fixture returns a parameter from its `request` object. The tests demonstrate how fixtures are used, with one test expecting an overridden fixture value and another testing the parametrized fixture's values.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_62

LANGUAGE: Python
CODE:

```
@pytest.fixture(params=['one', 'two', 'three'])
def non_parametrized_username(request):
    return request.param

def test_username(parametrized_username):
    assert parametrized_username == 'overridden-username'

def test_parametrized_username(non_parametrized_username):
    assert non_parametrized_username in ['one', 'two', 'three']
```

---

TITLE: Monkeypatching Dictionary Items with pytest-monkeypatch (Fixtures)
DESCRIPTION: This snippet demonstrates organizing dictionary monkeypatching into pytest fixtures for better modularity and reusability. The `mock_test_user` fixture sets a specific 'user' value in `app.DEFAULT_CONFIG`, allowing tests to easily apply this mock by simply requesting the fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_12

LANGUAGE: Python
CODE:

```
# contents of test_app.py
import pytest

# app.py with the connection string function
import app


# all of the mocks are moved into separated fixtures
@pytest.fixture
def mock_test_user(monkeypatch):
    """Set the DEFAULT_CONFIG user to test_user."""
    monkeypatch.setitem(app.DEFAULT_CONFIG, "user", "test_user")
```

---

TITLE: Asserting Dataclass Equality in Python with Pytest
DESCRIPTION: This test demonstrates asserting equality between two Python dataclass instances. Pytest provides detailed output showing differing attributes upon failure.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_19

LANGUAGE: python
CODE:

```
def test_eq_dataclass(self):
    from dataclasses import dataclass

    @dataclass
    class Foo:
        a: int
        b: str

    left = Foo(1, "b")
    right = Foo(1, "c")
    assert left == right
```

---

TITLE: Defining a Simple API Retrieval Function (Python)
DESCRIPTION: This Python function `get_json` takes a URL, makes an HTTP GET request using the `requests` library, and returns the JSON response. It serves as the target for subsequent monkeypatching examples, demonstrating a common scenario where external dependencies need to be mocked for testing.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_1

LANGUAGE: python
CODE:

```
import requests


def get_json(url):
    """Takes a URL, and returns the JSON."""
    r = requests.get(url)
    return r.json()
```

---

TITLE: Selecting pytest Tests with 'or' Keyword Expression
DESCRIPTION: This command shows how to use the -k option with the "or" operator to select tests that match either "http" or "quick" in their names. It demonstrates combining multiple keyword criteria for test selection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_9

LANGUAGE: pytest
CODE:

```
$ pytest -k "http or quick" -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 2 deselected / 2 selected

test_server.py::test_send_http PASSED                                [ 50%]
test_server.py::test_something_quick PASSED                          [100%]

===================== 2 passed, 2 deselected in 0.12s ======================
```

---

TITLE: Marking Test as XFAIL with ExceptionGroup (Python)
DESCRIPTION: Shows how to use `pytest.mark.xfail` in conjunction with `pytest.RaisesGroup` to check for specific exceptions contained within an `ExceptionGroup`. This allows for precise xfail conditions when dealing with grouped exceptions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_17

LANGUAGE: Python
CODE:

```
def f():
    raise ExceptionGroup("", [IndexError()])


@pytest.mark.xfail(raises=RaisesGroup(IndexError))
def test_f():
    f()
```

---

TITLE: Executing Pytest with Fixture Parametrization (Pytest CLI)
DESCRIPTION: This Pytest CLI command runs tests in verbose mode (`-v`) and displays print statements (`-s`) from `test_module.py`. The output clearly illustrates the setup and teardown order of parametrized fixtures with different scopes, showing how module-scoped fixtures are managed across multiple tests and how function-scoped fixtures are re-initialized for each test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_52

LANGUAGE: pytest
CODE:

```
$ pytest -v -s test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 8 items

test_module.py::test_0[1]   SETUP otherarg 1
  RUN test0 with otherarg 1
PASSED  TEARDOWN otherarg 1

test_module.py::test_0[2]   SETUP otherarg 2
  RUN test0 with otherarg 2
PASSED  TEARDOWN otherarg 2

test_module.py::test_1[mod1]   SETUP modarg mod1
  RUN test1 with modarg mod1
PASSED
test_module.py::test_2[mod1-1]   SETUP otherarg 1
  RUN test2 with otherarg 1 and modarg mod1
PASSED  TEARDOWN otherarg 1

test_module.py::test_2[mod1-2]   SETUP otherarg 2
  RUN test2 with otherarg 2 and modarg mod1
PASSED  TEARDOWN otherarg 2

test_module.py::test_1[mod2]   TEARDOWN modarg mod1
  SETUP modarg mod2
  RUN test1 with modarg mod2
PASSED
test_module.py::test_2[mod2-1]   SETUP otherarg 1
  RUN test2 with otherarg 1 and modarg mod2
PASSED  TEARDOWN otherarg 1

test_module.py::test_2[mod2-2]   SETUP otherarg 2
  RUN test2 with otherarg 2 and modarg mod2
PASSED  TEARDOWN otherarg 2
  TEARDOWN modarg mod2


============================ 8 passed in 0.12s =============================
```

---

TITLE: Custom Failure Messages for Warnings in Python
DESCRIPTION: This snippet shows a pattern for using `pytest.warns` to record warnings, which can then be inspected to produce custom test failure messages if no warnings are issued or other conditions are not met. The `record` object allows post-hoc analysis.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_22

LANGUAGE: python
CODE:

```
def test():
    with pytest.warns(Warning) as record:
        f()
```

---

TITLE: Assert Substring Not In Multiline String in Pytest
DESCRIPTION: Illustrates a failed assertion checking if a substring is NOT present in a multiline string. Pytest shows the multiline string and highlights where the substring was found.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_15

LANGUAGE: python
CODE:

```
text = "some multiline\ntext\nwhich\nincludes foo\nand a\ntail"
assert "foo" not in text
```

---

TITLE: Pytest raises TypeError check (Python)
DESCRIPTION: Attempts to check if a `TypeError` is raised when calling `int()` with a non-integer string 'qwe' using pytest's `raises` helper. This example shows a `ValueError` being raised instead, leading to a test failure.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_25

LANGUAGE: python
CODE:

```
raises(TypeError, int, s)
```

---

TITLE: Applying Individual Pytest Markers with Parametrize in Python
DESCRIPTION: This example shows how to apply a marker to a specific test instance generated by `pytest.mark.parametrize`. While `foo` applies to all instances, `bar` is applied only to the second test case using `pytest.param`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_16

LANGUAGE: Python
CODE:

```
import pytest


@pytest.mark.foo
@pytest.mark.parametrize(
    ("n", "expected"), [(1, 2), pytest.param(1, 3, marks=pytest.mark.bar), (2, 3)]
)
def test_increment(n, expected):
    assert n + 1 == expected
```

---

TITLE: Temporarily Changing Specific Logger Level with caplog (Python)
DESCRIPTION: This Python snippet demonstrates using `caplog.at_level` as a context manager to temporarily change the log level of a specific logger (e.g., 'root.baz'). This provides a convenient way to control logging behavior for particular loggers within a defined scope.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_10

LANGUAGE: python
CODE:

```
def test_bar(caplog):
        with caplog.at_level(logging.CRITICAL, logger="root.baz"):
            pass
```

---

TITLE: Customizing Pytest Naming Conventions in pytest.ini
DESCRIPTION: This `pytest.ini` example shows how to override pytest's default naming conventions for test files, classes, and functions. It configures pytest to look for files matching `check_*.py`, classes starting with `Check`, and functions/methods ending with `_check`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_6

LANGUAGE: ini
CODE:

```
# content of pytest.ini\n# Example 1: have pytest look for \"check\" instead of \"test\"\n[pytest]\npython_files = check_*.py\npython_classes = Check\npython_functions = *_check
```

---

TITLE: Recommended pytest.raises/warns Context Manager Form (Python)
DESCRIPTION: Illustrates the recommended context manager syntax for `pytest.raises` and `pytest.warns`. For cases involving invalid syntax, `exec` is used to execute the string within the context manager, ensuring the error is caught.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_23

LANGUAGE: Python
CODE:

```
with pytest.raises(ZeroDivisionError):
    1 / 0
with pytest.raises(SyntaxError):
    exec("a $ b")  # exec is required for invalid syntax

with pytest.warns(DeprecationWarning):
    my_function()
with pytest.warns(SyntaxWarning):
    exec("assert(1, 2)")  # exec is used to avoid a top-level warning
```

---

TITLE: Testing Environment Variables with pytest-monkeypatch (Direct)
DESCRIPTION: This snippet shows how to test the `get_os_user_lower` function by directly using `monkeypatch.setenv` to set an environment variable and `monkeypatch.delenv` to remove one. It demonstrates testing both the success path (variable set) and the error path (variable missing) without affecting the actual system environment.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_7

LANGUAGE: Python
CODE:

```
# contents of our test file e.g. test_code.py
import pytest


def test_upper_to_lower(monkeypatch):
    """Set the USER env var to assert the behavior."""
    monkeypatch.setenv("USER", "TestingUser")
    assert get_os_user_lower() == "testinguser"


def test_raise_exception(monkeypatch):
    """Remove the USER env var and assert OSError is raised."""
    monkeypatch.delenv("USER", raising=False)

    with pytest.raises(OSError):
        _ = get_os_user_lower()
```

---

TITLE: Configuring pytest to Use importlib Import Mode
DESCRIPTION: This TOML configuration snippet for `pyproject.toml` sets the `pytest` import mode to `importlib`. Using `importlib` is recommended for new projects, especially when employing a `src` layout, as it helps prevent common import-related pitfalls during test discovery and execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_3

LANGUAGE: toml
CODE:

```
[tool.pytest.ini_options]
addopts = [
    "--import-mode=importlib",
]
```

---

TITLE: Pytest Skipif Condition Using Config Value (Boolean) - Python
DESCRIPTION: This snippet shows the modern, preferred way to specify a `skipif` condition using a boolean expression and a mandatory `reason` string. It checks if the `db` configuration value is not set using `pytest.config.getvalue("db")`. This approach offers better encapsulation and allows markers to be freely imported between test modules, unlike string conditions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/historical-notes.rst#_snippet_5

LANGUAGE: Python
CODE:

```
@pytest.mark.skipif(not pytest.config.getvalue("db"), reason="--db was not specified")
def test_function():
    pass
```

---

TITLE: Debugging with Print Statements in Pytest (Python)
DESCRIPTION: This Python code snippet illustrates how print statements can be used for debugging within pytest tests. It defines a `setup_function` that prints a message and two test functions, one passing and one failing. Pytest's default capturing mechanism ensures that only the output related to failing tests is displayed, making it easy to pinpoint issues.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-stdout-stderr.rst#_snippet_1

LANGUAGE: python
CODE:

```
# content of test_module.py


def setup_function(function):
    print("setting up", function)


def test_func1():
    assert True


def test_func2():
    assert False
```

---

TITLE: Defining Pytest Markers in Python Test Functions
DESCRIPTION: This Python code defines several test functions and a test class, demonstrating how to apply custom markers using @pytest.mark.<marker_name> and @pytest.mark.<marker_name>(key=value) decorators. It shows examples of a simple 'webtest' marker and 'device' markers with 'serial' keyword arguments, which can be used later for selective test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_server.py

import pytest


@pytest.mark.webtest
def test_send_http():
    pass  # perform some webtest test for your app


@pytest.mark.device(serial="123")
def test_something_quick():
    pass


@pytest.mark.device(serial="abc")
def test_another():
    pass


class TestClass:
    def test_method(self):
        pass
```

---

TITLE: Marking a Pytest Function as XFAIL with Condition
DESCRIPTION: This snippet shows how to use the `condition` parameter with `@pytest.mark.xfail` to mark a test as expected to fail only if a specific condition (e.g., `sys.platform == "win32"`) is met. A `reason` parameter is also required.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_16

LANGUAGE: python
CODE:

```
@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function(): ...
```

---

TITLE: Running Pytest with Specific Markers and Verbose Output
DESCRIPTION: This snippet demonstrates how to execute pytest tests, filtering them by a specific marker (`basic`) and enabling verbose output. It shows the command-line invocation and the resulting test session summary, including passed, deselected, and xfailed tests. This requires pytest to be installed and tests with the specified markers to be defined.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_26

LANGUAGE: pytest
CODE:

```
$ pytest -v -m basic
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 24 items / 21 deselected / 3 selected

test_pytest_param_example.py::test_eval[1+7-8] PASSED                [ 33%]
test_pytest_param_example.py::test_eval[basic_2+4] PASSED            [ 66%]
test_pytest_param_example.py::test_eval[basic_6*9] XFAIL             [100%]

=============== 2 passed, 21 deselected, 1 xfailed in 0.12s ================
```

---

TITLE: Running Pytest with Fixture Finalizer Plugin
DESCRIPTION: Executes pytest with the `-s` flag (to show print output) on `test_module.py` using the `conftest.py` plugin. The output shows the test session, the print statements from the fixture finalizer triggered by the failing tests, and the detailed error/failure reports for each test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_45

LANGUAGE: bash
CODE:

```
$ pytest -s test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_module.py Esetting up a test failed or skipped test_module.py::test_setup_fails
Fexecuting test failed or skipped test_module.py::test_call_fails
F

================================== ERRORS ==================================
____________________ ERROR at setup of test_setup_fails ____________________

    @pytest.fixture
    def other():
>       assert 0
E       assert 0

test_module.py:7: AssertionError
================================= FAILURES =================================
_____________________________ test_call_fails ______________________________

something = None

    def test_call_fails(something):
>       assert 0
E       assert 0

test_module.py:15: AssertionError
________________________________ test_fail2 ________________________________

    def test_fail2():
>       assert 0
E       assert 0

test_module.py:19: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_call_fails - assert 0
FAILED test_module.py::test_fail2 - assert 0
ERROR test_module.py::test_setup_fails - assert 0
```

---

TITLE: Invoking PDB on Test Failures with Pytest (Bash)
DESCRIPTION: This command line option instructs pytest to automatically drop into the Python debugger (pdb) whenever a test fails or a KeyboardInterrupt is detected. This allows for interactive debugging at the point of failure.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/failures.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pytest --pdb
```

---

TITLE: Applying Warning Filters with pytest.mark.filterwarnings - Python
DESCRIPTION: Shows how to apply a warning filter to a test function using the `filterwarnings` mark. This allows specific warnings to be ignored, always shown, or treated as errors during test execution based on a warning specification string. The filter string defines the action, message pattern, warning category, module, and line number.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_2

LANGUAGE: python
CODE:

```
@pytest.mark.filterwarnings("ignore:.*usage will be deprecated.*:DeprecationWarning")
def test_foo(): ...
```

---

TITLE: Deprecated pytest_cmdline_preparse Hook Replacement in Python
DESCRIPTION: This snippet illustrates the deprecation of the `pytest_cmdline_preparse` hook and its replacement with `pytest_load_initial_conftests` in pytest 7.0 (removed in 8.0). The `pytest_cmdline_preparse` hook was used for pre-parsing command-line arguments, while the new `pytest_load_initial_conftests` hook provides similar functionality with an updated signature, allowing initial configuration and parser access.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_16

LANGUAGE: Python
CODE:

```
def pytest_cmdline_preparse(config: Config, args: List[str]) -> None: ...


# becomes:


def pytest_load_initial_conftests(
    early_config: Config, parser: Parser, args: List[str]
) -> None: ...
```

---

TITLE: Pytest Function Using a Single Fixture (Python)
DESCRIPTION: This Python snippet defines a simple Pytest test function `test_0` that consumes the `otherarg` fixture. The fixture's value is passed as an argument to the test function. This demonstrates the basic mechanism of injecting fixture values into tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_49

LANGUAGE: python
CODE:

```
def test_0(otherarg):
    print("  RUN test0 with otherarg", otherarg)
```

---

TITLE: Clearing Pytest Cache Content - Bash
DESCRIPTION: This command line option instructs pytest to clear all cached test results and values. It is particularly useful in Continuous Integration (CI) environments to ensure isolation and correctness of test runs, preventing issues from stale cache data.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_10

LANGUAGE: bash
CODE:

```
pytest --cache-clear
```

---

TITLE: Understanding Pytest Yield Fixture Teardown Order (Python)
DESCRIPTION: This Python code defines two `pytest` yield fixtures and a test function to illustrate the execution order of teardown code for yield fixtures. It shows that the teardown code for the right-most fixture parameter (the last one listed in the test function's signature) runs first.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_22

LANGUAGE: python
CODE:

```
# content of test_finalizers.py
import pytest


def test_bar(fix_w_yield1, fix_w_yield2):
    print("test_bar")


@pytest.fixture
def fix_w_yield1():
    yield
    print("after_yield_1")


@pytest.fixture
def fix_w_yield2():
    yield
    print("after_yield_2")
```

---

TITLE: Testing Database Initialization with Pytest Fixture in Python
DESCRIPTION: This Python test function `test_db_initialized` demonstrates a basic test that depends on a `db` fixture. It checks the type of the injected `db` object and includes a conditional `pytest.fail` for demonstration purposes when the `db` object is an instance of `DB2`. This snippet highlights how tests consume parametrized fixtures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_9

LANGUAGE: python
CODE:

```
# content of test_backends.py

import pytest


def test_db_initialized(db):
    # a dummy test
    if db.__class__.__name__ == "DB2":
        pytest.fail("deliberately failing for demo purposes")
```

---

TITLE: Applying `usefixtures` at Module Level (Python)
DESCRIPTION: This Python snippet demonstrates how to apply a fixture to all tests within an entire module by assigning `pytest.mark.usefixtures("cleandir")` to the module-level variable `pytestmark`. This is a convenient way to ensure a specific fixture is active for all tests in a file without decorating each test function or class individually.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_57

LANGUAGE: python
CODE:

```
pytestmark = pytest.mark.usefixtures("cleandir")
```

---

TITLE: Skipping Tests Based on Platform Markers in Conftest
DESCRIPTION: This `conftest.py` plugin defines a `pytest_runtest_setup` hook that automatically skips tests if they are marked for a platform different from the current system's platform. It identifies platform-specific markers and uses `pytest.skip` to prevent tests from running on unsupported environments.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_28

LANGUAGE: python
CODE:

```
# content of conftest.py
#
import sys

import pytest

ALL = set("darwin linux win32".split())


def pytest_runtest_setup(item):
    supported_platforms = ALL.intersection(mark.name for mark in item.iter_markers())
    plat = sys.platform
    if supported_platforms and plat not in supported_platforms:
        pytest.skip(f"cannot run on platform {plat}")
```

---

TITLE: Configuring Pytest Parametrization with Scenarios in Python
DESCRIPTION: This Python code demonstrates how to integrate `testscenarios` with pytest's parametrization mechanism. The `pytest_generate_tests` hook dynamically generates test IDs and argument values based on scenarios defined within a test class, allowing tests like `test_demo1` and `test_demo2` to run with different `attribute` values. It requires the `pytest` framework and defines `scenario1` and `scenario2` tuples to provide test data.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_6

LANGUAGE: python
CODE:

```
# content of test_scenarios.py


def pytest_generate_tests(metafunc):
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


scenario1 = ("basic", {"attribute": "value"})
scenario2 = ("advanced", {"attribute": "value2"})


class TestSampleWithScenarios:
    scenarios = [scenario1, scenario2]

    def test_demo1(self, attribute):
        assert isinstance(attribute, str)

    def test_demo2(self, attribute):
        assert isinstance(attribute, str)
```

---

TITLE: Understanding Pytest addfinalizer Teardown Order (Python)
DESCRIPTION: This Python code demonstrates the execution order of functions registered with `request.addfinalizer` within a `pytest` fixture. It shows that finalizers are executed in a first-in-last-out order, meaning the last function registered with `addfinalizer` will be the first one to run during teardown.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_24

LANGUAGE: python
CODE:

```
# content of test_finalizers.py
from functools import partial
import pytest


@pytest.fixture
def fix_w_finalizers(request):
    request.addfinalizer(partial(print, "finalizer_2"))
    request.addfinalizer(partial(print, "finalizer_1"))


def test_bar(fix_w_finalizers):
    print("test_bar")
```

---

TITLE: Imperative Skipping of Test Function with Pytest Skip (Python)
DESCRIPTION: This snippet illustrates how to imperatively skip a test function during its execution or setup by calling the `pytest.skip(reason)` function. This method is particularly useful when the condition for skipping cannot be evaluated at import time and depends on runtime factors or configurations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_2

LANGUAGE: python
CODE:

```
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command uses the pip package installer to upgrade the pytest framework to its latest available version. The -U flag ensures that any previously installed versions are updated.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.0.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades the pytest testing framework to its latest version available on PyPI. The `-U` flag ensures that any existing installation is updated to the newest release.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.6.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This shell command uses the pip package installer to upgrade an existing pytest installation to its latest available version. The '--upgrade' flag ensures that pip replaces the current version with the new one, providing access to recent bug fixes and features.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.2.3.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command upgrades the pytest testing framework to the latest version using pip, the Python package installer. The '-U' flag ensures that existing packages are updated to their newest available versions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.1.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest Package via pip
DESCRIPTION: This command line snippet demonstrates how to upgrade the pytest testing framework to its latest version using the pip package installer. The '-U' flag ensures that any existing installation is updated.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.3.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Apply Custom Marker to Test Function (Python)
DESCRIPTION: Shows how to apply a custom marker (`@pytest.mark.test_id`) with an argument to a test function, which can then be processed by a hook like `pytest_collection_modifyitems` to add data to the JUnit XML report.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_19

LANGUAGE: python
CODE:

```
# content of test_function.py
import pytest


@pytest.mark.test_id(1501)
def test_function():
    assert True
```

---

TITLE: Example Tests with Pytest Markers (Python)
DESCRIPTION: Provides example test functions in `test_module.py`, including one marked with `@pytest.mark.slow`, to be used with the skipping logic defined in the `conftest.py` snippet.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_16

LANGUAGE: python
CODE:

```
# content of test_module.py
import pytest


def test_func_fast():
    pass


@pytest.mark.slow
def test_func_slow():
    pass
```

---

TITLE: Excluding Directories from Pytest Discovery (INI)
DESCRIPTION: Sets directory basename patterns to avoid during test discovery recursion. This helps exclude irrelevant directories like build artifacts, version control folders, or temporary directories from test collection, optimizing test run performance.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_44

LANGUAGE: ini
CODE:

```
[pytest]
norecursedirs = .svn _build tmp*
```

---

TITLE: Applying `usefixtures` Marker to a Test Class (Python)
DESCRIPTION: This Python snippet demonstrates applying the `@pytest.mark.usefixtures("cleandir")` marker to a test class `TestDirectoryInit`. This automatically applies the `cleandir` fixture to every test method within the class, eliminating the need to explicitly pass `cleandir` as an argument to each test function. This is useful when tests don't need direct access to the fixture object but require its setup/teardown effects.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_54

LANGUAGE: python
CODE:

```
# content of test_setenv.py
import os

import pytest


@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w", encoding="utf-8") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
```

---

TITLE: Running Tests by Marker Expression (Bash)
DESCRIPTION: This command runs all tests that have been decorated with the '@pytest.mark.slow' decorator. The '-m' option is used to specify a marker expression, allowing for selective test execution based on defined markers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_7

LANGUAGE: bash
CODE:

```
pytest -m slow
```

---

TITLE: Implementing Pytest Fixture with Cache in Python
DESCRIPTION: This Python snippet shows how to create a pytest fixture (mydata) that utilizes pytestconfig.cache to store and retrieve values across test runs. It demonstrates a pattern for performing an expensive computation only once and caching its result for subsequent invocations, improving test performance.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_5

LANGUAGE: python
CODE:

```
# content of test_caching.py
import pytest


def expensive_computation():
    print("running expensive computation...")


@pytest.fixture
def mydata(pytestconfig):
    val = pytestconfig.cache.get("example/value", None)
    if val is None:
        expensive_computation()
        val = 42
        pytestconfig.cache.set("example/value", val)
    return val


def test_function(mydata):
    assert mydata == 23
```

---

TITLE: Marking a Pytest Function as Expected to Fail (Basic)
DESCRIPTION: This snippet shows the basic usage of the `@pytest.mark.xfail` decorator to mark a test function as expected to fail. The test will still run, but its failure won't cause the test suite to fail, instead reporting as XFAIL.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_13

LANGUAGE: python
CODE:

```
@pytest.mark.xfail
def test_function(): ...
```

---

TITLE: Imperatively Marking a Pytest Function as XFAIL (Conditional)
DESCRIPTION: This snippet demonstrates how to imperatively mark a test as XFAIL from within the test function itself using `pytest.xfail()`. The test will be marked XFAIL if `valid_config()` returns false, and no further code in the test will execute.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_14

LANGUAGE: python
CODE:

```
def test_function():
    if not valid_config():
        pytest.xfail("failing configuration (but should work)")
```

---

TITLE: Controlling Fixture Order by Dependencies in pytest (Python)
DESCRIPTION: This example illustrates how pytest prioritizes fixture execution based on explicit dependencies. If fixture 'A' requests fixture 'B', 'B' will always execute before 'A', ensuring that 'A' has its prerequisites met. This mechanism allows for a clear, linear chain of operations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_9

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def a():
    print("fixture a")
    return "a"

@pytest.fixture
def b(a):
    print("fixture b")
    return "b"

@pytest.fixture
def c(b):
    print("fixture c")
    return "c"

@pytest.fixture
def d():
    print("fixture d")
    return "d"

@pytest.fixture
def e():
    print("fixture e")
    return "e"

@pytest.fixture
def f(e):
    print("fixture f")
    return "f"

@pytest.fixture
def g(f, c):
    print("fixture g")
    return "g"

def test_dependencies(g, d):
    print("test_dependencies executed")
    assert True
```

---

TITLE: Configuring Pytest Log Format in pytest.ini (INI)
DESCRIPTION: This `pytest.ini` configuration demonstrates how to set global log and date formatting options for pytest. Placing these settings in `pytest.ini` allows for consistent logging behavior across test runs without needing to specify command-line arguments every time.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_4

LANGUAGE: ini
CODE:

```
[pytest]
log_format = %(asctime)s %(levelname)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
```

---

TITLE: Applying Filterwarnings to a Module in Pytest
DESCRIPTION: This snippet shows how to apply a warning filter to all tests within a module by setting the `pytestmark` variable. Here, all warnings encountered in this module will be treated as errors. If multiple filters are assigned to `pytestmark` as a list, they follow the traditional `warnings.filterwarnings` ordering (later filters take precedence).
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_8

LANGUAGE: python
CODE:

```
# turns all warnings into errors for this module
pytestmark = pytest.mark.filterwarnings("error")
```

---

TITLE: Using Pytest record_property Fixture (Python)
DESCRIPTION: Demonstrates how to use the `record_property` fixture within a test function to log additional key-value information that will be included in test reports, such as JUnit XML.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_16

LANGUAGE: python
CODE:

```
def test_function(record_property):
    record_property("example_key", 1)
    assert True
```

---

TITLE: Running All Tests in a Class (Bash)
DESCRIPTION: This command executes all test methods defined within a specific test class in a module. The path includes the module file relative to the working directory, followed by '::' and the class name.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_4

LANGUAGE: bash
CODE:

```
pytest tests/test_mod.py::TestClass
```

---

TITLE: Executing Pytest with Explicit Test Paths (Console)
DESCRIPTION: This command `pytest testing doc` explicitly instructs pytest to search for and run tests within the `testing` and `doc` directories. This command demonstrates the equivalent effect of configuring `testpaths = testing doc` in the `pytest.ini` file and then running `pytest` without arguments.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_53

LANGUAGE: console
CODE:

```
pytest testing doc
```

---

TITLE: Configuring Pytest with tox.ini (INI)
DESCRIPTION: This INI configuration snippet for `tox.ini` demonstrates how to embed pytest settings within a tox project's configuration file. It sets the minimum pytest version to 6.0, adds default command-line options (`-ra -q`), and specifies test directories (`tests`, `integration`), provided it contains a `[pytest]` section.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/customize.rst#_snippet_3

LANGUAGE: ini
CODE:

```
# tox.ini
[pytest]
minversion = 6.0
addopts = -ra -q
testpaths =
    tests
    integration
```

---

TITLE: Shorter Monkeypatching with setattr for Modules
DESCRIPTION: Illustrates a concise way to use `monkeypatch.setattr` for replacing functions or classes within modules. This example shows how to mock the `get` function of the `requests` module with a custom function `myfunc`, which is useful for isolating tests from external dependencies.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst#_snippet_2

LANGUAGE: Python
CODE:

```
monkeypatch.setattr("requests.get", myfunc)
```

---

TITLE: Configuring Pytest Output Capturing Methods (Bash)
DESCRIPTION: This snippet demonstrates how to control pytest's output capturing behavior using command-line arguments. It shows options to disable all capturing (`-s`), capture only Python `sys` streams (`--capture=sys`), capture file descriptor level output (`--capture=fd`), or capture `sys` streams while also passing them through (`--capture=tee-sys`). These flags allow fine-grained control over how pytest handles stdout and stderr during test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-stdout-stderr.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest -s                  # disable all capturing
pytest --capture=sys       # replace sys.stdout/stderr with in-mem files
pytest --capture=fd        # also point filedescriptors 1 and 2 to temp file
pytest --capture=tee-sys   # combines 'sys' and '-s', capturing sys.stdout/stderr
                               # and passing it along to the actual sys.stdout/stderr
```

---

TITLE: Temporarily Changing Root Logger Level with caplog (Python)
DESCRIPTION: This Python snippet illustrates using `caplog.at_level` as a context manager to temporarily change the root logger's level within a `with` block. The log level is automatically restored to its previous state upon exiting the block, ensuring isolated log level changes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_9

LANGUAGE: python
CODE:

```
def test_bar(caplog):
        with caplog.at_level(logging.INFO):
            pass
```

---

TITLE: Simplifying pytest.mark.parametrize Argument Naming in Python
DESCRIPTION: This snippet demonstrates the simplified signature for `pytest.mark.parametrize`, which now allows a comma-separated string (e.g., "input,expected") to specify argument names. This new, more concise approach works equivalently to the previous method of providing a tuple of strings for `argnames`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst#_snippet_7

LANGUAGE: Python
CODE:

```
pytest.mark.parametrize("input,expected", [(1,2), (2,3)])
```

LANGUAGE: Python
CODE:

```
pytest.mark.parametrize(("input", "expected"), ...)
```

---

TITLE: Define Pytest Package-Scoped Fixture (Python)
DESCRIPTION: Defines a `db` fixture with `package` scope in `a/conftest.py`. This fixture creates an instance of a simple `DB` class and makes it available to tests within the 'a' package.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_33

LANGUAGE: python
CODE:

```
# content of a/conftest.py
import pytest


class DB:
    pass


@pytest.fixture(scope="package")
def db():
    return DB()
```

---

TITLE: Failing Tests on Captured Warnings with Pytest's `caplog`
DESCRIPTION: This Python snippet demonstrates how to check for and fail a pytest test if any warning messages are captured by the `caplog` fixture during the 'setup' or 'call' phases. It iterates through captured records, filters for warnings based on `levelno`, and uses `pytest.fail` if warnings are present. This ensures tests are strict about unexpected warnings.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_15

LANGUAGE: Python
CODE:

```
for when in ("setup", "call"):
    messages = [
        x.message for x in caplog.get_records(when) if x.levelno == logging.WARNING
    ]
    if messages:
        pytest.fail(f"warning messages encountered during testing: {messages}")
```

---

TITLE: Configuring pytest via INI Files (INI)
DESCRIPTION: This INI configuration block demonstrates how to customize pytest behavior using `setup.cfg` or `tox.ini` files. It shows how to exclude directories from recursion (`norecursedirs`) and add default command-line options (`addopts`) for all test runs, centralizing configuration.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.0.rst#_snippet_3

LANGUAGE: INI
CODE:

```
[pytest]
norecursedirs = .hg data*  # don't ever recurse in such dirs
addopts = -x --pyargs      # add these command line options by default
```

---

TITLE: Executing Pytest with Local conftest.py Hook - Shell
DESCRIPTION: This snippet shows how to execute pytest from the command line to observe the effect of the `pytest_runtest_setup` hook defined in `a/conftest.py`. Running `test_flat.py` (outside 'a' directory) does not trigger the hook, while `a/test_sub.py` (inside 'a' directory) does, demonstrating the scope of local `conftest.py` plugins.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_1

LANGUAGE: Shell
CODE:

```
pytest test_flat.py --capture=no  # will not show "setting up"
```

LANGUAGE: Shell
CODE:

```
pytest a/test_sub.py --capture=no  # will show "setting up"
```

---

TITLE: Pytest Run Output Showing Fixture Scope Errors
DESCRIPTION: The output of running pytest on the example project structure. It shows that tests in directory 'a' fail due to the assertion (but successfully receive the fixture), while the test in directory 'b' errors out because the 'db' fixture is not found.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_37

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 7 items

a/test_db.py F                                                       [ 14%]
a/test_db2.py F                                                      [ 28%]
b/test_error.py E                                                    [ 42%]
test_step.py .Fx.                                                    [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_root ________________________
file /home/sweet/project/b/test_error.py, line 1
  def test_root(db):  # no db here, will error out
E       fixture 'db' not found
>       available fixtures: cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/sweet/project/b/test_error.py:1
================================= FAILURES =================================
_________________________________ test_a1 __________________________________

db = <conftest.DB object at 0xdeadbeef0002>

    def test_a1(db):
>       assert 0, db  # to show value
E       AssertionError: <conftest.DB object at 0xdeadbeef0002>
E       assert 0

a/test_db.py:2: AssertionError
_________________________________ test_a2 __________________________________

db = <conftest.DB object at 0xdeadbeef0002>

    def test_a2(db):
>       assert 0, db  # to show value
E       AssertionError: <conftest.DB object at 0xdeadbeef0002>
E       assert 0

a/test_db2.py:2: AssertionError
____________________ TestUserHandling.test_modification ____________________

self = <test_step.TestUserHandling object at 0xdeadbeef0003>

    def test_modification(self):
>       assert 0
E       assert 0

test_step.py:11: AssertionError
========================= short test summary info ==========================
FAILED a/test_db.py::test_a1 - AssertionError: <conftest.DB object at 0x7...
FAILED a/test_db2.py::test_a2 - AssertionError: <conftest.DB object at 0x...
FAILED test_step.py::TestUserHandling::test_modification - assert 0
ERROR b/test_error.py::test_root
============= 3 failed, 2 passed, 1 xfailed, 1 error in 0.12s ==============
```

---

TITLE: Running pytest in Verbose Mode for Custom Tests
DESCRIPTION: This example illustrates running pytest with the `-v` (verbose) flag. It provides more detailed output, showing individual test items (e.g., `test_simple.yaml::hello` and `test_simple.yaml::ok`) and their pass/fail status, which is useful for debugging custom test collection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/nonpython.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
nonpython $ pytest -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project/nonpython
collecting ... collected 2 items

test_simple.yaml::hello FAILED                                       [ 50%]
test_simple.yaml::ok PASSED                                          [100%]

================================= FAILURES =================================
______________________________ usecase: hello ______________________________
usecase execution failed
   spec failed: 'some': 'other'
   no further details known at this point.
========================= short test summary info ==========================
FAILED test_simple.yaml::hello
======================= 1 failed, 1 passed in 0.12s ========================
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command uses pip, the Python package installer, to upgrade the pytest library to its latest available version. The -U flag ensures that an existing installation is updated rather than just installing if not present.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.2.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Implementing Indirect Fixture Parametrization in Pytest
DESCRIPTION: This Python code demonstrates indirect parametrization in pytest. The fixt fixture receives values from request.param and processes them before passing the result to test_indirect. This allows for more complex setup logic within the fixture at test runtime.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_14

LANGUAGE: python
CODE:

```
import pytest


@pytest.fixture
def fixt(request):
    return request.param * 3


@pytest.mark.parametrize("fixt", ["a", "b"], indirect=True)
def test_indirect(fixt):
    assert len(fixt) == 3
```

---

TITLE: Imperatively Marking a Pytest Function as XFAIL (Performance/Dependency)
DESCRIPTION: This snippet illustrates another use case for imperative `pytest.xfail()`, where a test is marked XFAIL if a condition related to a slow module's performance is met. This allows skipping tests that might hang or take too long under specific circumstances.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_15

LANGUAGE: python
CODE:

```
def test_function2():
    import slow_module

    if slow_module.slow_function():
        pytest.xfail("slow_module taking too long")
```

---

TITLE: Installing and Uninstalling pytest Plugins with pip (Bash)
DESCRIPTION: This snippet demonstrates the command-line usage of pip to install and uninstall pytest plugins. Once installed, pytest automatically discovers and integrates the plugin without further activation steps.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pip install pytest-NAME
pip uninstall pytest-NAME
```

---

TITLE: Running Pytest in CI with Full Output
DESCRIPTION: This snippet demonstrates running the `test_ci.py` file in a simulated CI environment by setting the `CI=true` environment variable. The output shows the full, untruncated short test summary info, illustrating pytest's adapted behavior in CI.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/ci.rst#_snippet_2

LANGUAGE: pytest
CODE:

```
$ export CI=true
$ pytest test_ci.py
...
========================= short test summary info ==========================
FAILED test_backends.py::test_db_initialized[d2] - Failed: deliberately failing
for demo purpose, Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras
facilisis, massa in suscipit dignissim, mauris lacus molestie nisi, quis varius
metus nulla ut ipsum.
```

---

TITLE: Configuring Pytest with pytest.ini (INI)
DESCRIPTION: This INI configuration snippet for `pytest.ini` or `.pytest.ini` sets the minimum pytest version to 6.0, adds default command-line options (`-ra -q`), and defines the directories to search for tests (`tests`, `integration`). This file takes precedence over other configuration files.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/customize.rst#_snippet_1

LANGUAGE: ini
CODE:

```
# pytest.ini or .pytest.ini
[pytest]
minversion = 6.0
addopts = -ra -q
testpaths =
    tests
    integration
```

---

TITLE: Mocking Missing Default User with Pytest Monkeypatch (Python)
DESCRIPTION: This `pytest` fixture uses `monkeypatch.delitem` to remove the `user` key from `app.DEFAULT_CONFIG`. The `raising=False` argument prevents an error if the key is already absent, simulating a scenario where the user configuration is missing.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_14

LANGUAGE: Python
CODE:

```
@pytest.fixture
def mock_missing_default_user(monkeypatch):
    monkeypatch.delitem(app.DEFAULT_CONFIG, "user", raising=False)
```

---

TITLE: Running Pytest Tests by Specific Marker
DESCRIPTION: This pytest command-line example demonstrates how to execute only tests that have been marked with the 'webtest' marker using the '-m' option. The output shows that only 'test_send_http' (marked 'webtest') is selected and run, while others are deselected.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
$ pytest -v -m webtest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 3 deselected / 1 selected

test_server.py::test_send_http PASSED                                [100%]

===================== 1 passed, 3 deselected in 0.12s ======================
```

---

TITLE: Monkeypatching Dictionary Items with pytest-monkeypatch (setitem)
DESCRIPTION: This test demonstrates using `monkeypatch.setitem` to temporarily modify specific keys within the `app.DEFAULT_CONFIG` dictionary. This allows testing the `create_connection_string` function with custom configuration values without altering the original dictionary globally, ensuring isolated test environments.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_10

LANGUAGE: Python
CODE:

```
# contents of test_app.py
# app.py with the connection string function (prior code block)
import app


def test_connection(monkeypatch):
    # Patch the values of DEFAULT_CONFIG to specific
    # testing values only for this test.
    monkeypatch.setitem(app.DEFAULT_CONFIG, "user", "test_user")
    monkeypatch.setitem(app.DEFAULT_CONFIG, "database", "test_db")

    # expected result based on the mocks
    expected = "User Id=test_user; Location=test_db;"

    # the test uses the monkeypatched dictionary settings
    result = app.create_connection_string()
    assert result == expected
```

---

TITLE: Skipping Tests on Missing Import Dependency in Pytest (Module Level)
DESCRIPTION: This snippet demonstrates how to skip a test if a required module, 'docutils', cannot be imported. It uses `pytest.importorskip` at the module level, causing the test to be skipped if the dependency is not met.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_8

LANGUAGE: python
CODE:

```
docutils = pytest.importorskip("docutils")
```

---

TITLE: Registering a Single Pytest Plugin with `pytest_plugins` (Python)
DESCRIPTION: This snippet shows how to register a single additional plugin using the `pytest_plugins` global variable. It can be declared in test modules or `conftest.py` files. The variable can accept a single string representing the plugin module path.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_11

LANGUAGE: Python
CODE:

```
pytest_plugins = "myapp.testsupport.myplugin"
```

---

TITLE: Marking a Pytest Function as XFAIL Without Execution
DESCRIPTION: This snippet demonstrates using the `run=False` parameter with `@pytest.mark.xfail`. This marks the test as XFAIL and reports it as such, but prevents the test function from being executed at all, useful for crashing tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_19

LANGUAGE: python
CODE:

```
@pytest.mark.xfail(run=False)
def test_function(): ...
```

---

TITLE: Getting Pytest Help and Information (Bash)
DESCRIPTION: These commands provide various ways to get help and information about pytest. '--version' shows the installation path, '--fixtures' lists available built-in function arguments, and '-h' or '--help' displays general command-line and configuration options.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_12

LANGUAGE: bash
CODE:

```
pytest --version   # shows where pytest was imported from
pytest --fixtures  # show available builtin function arguments
pytest -h | --help # show help on command line and config file options
```

---

TITLE: Pytest Output for Failed Python Assertion
DESCRIPTION: Illustrates the output generated by `pytest` when a standard Python `assert` statement fails. It shows the detailed traceback, the specific assertion that failed, and the values of the subexpressions involved, aiding in debugging.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
$ pytest test_assert1.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_assert1.py F                                                    [100%]

================================= FAILURES =================================
______________________________ test_function _______________________________

    def test_function():
>       assert f() == 4
E       assert 3 == 4
E        +  where 3 = f()

test_assert1.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_assert1.py::test_function - assert 3 == 4
============================ 1 failed in 0.12s ============================
```

---

TITLE: Enforcing Strict Marker Validation in pytest.ini (INI)
DESCRIPTION: This INI configuration demonstrates how to enforce strict marker validation by adding `--strict-markers` to the `addopts` section in `pytest.ini`. When enabled, any unknown markers applied to tests will trigger an error instead of just a warning, ensuring marker names are correctly used.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/mark.rst#_snippet_3

LANGUAGE: INI
CODE:

```
[pytest]
addopts = --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    serial
```

---

TITLE: Marking a Pytest Function as XFAIL with Reason
DESCRIPTION: This snippet demonstrates using the `reason` parameter with `@pytest.mark.xfail` to provide a clear explanation for why a test is expected to fail. This helps in understanding the context of the XFAIL outcome.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_17

LANGUAGE: python
CODE:

```
@pytest.mark.xfail(reason="known parser issue")
def test_function(): ...
```

---

TITLE: Applying Multiple `usefixtures` Markers (Python)
DESCRIPTION: This Python snippet shows how to apply multiple fixtures to a test function using the `usefixtures` marker. By listing fixture names as separate arguments to `pytest.mark.usefixtures`, both `cleandir` and `anotherfixture` will be set up before `test()` executes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_56

LANGUAGE: python
CODE:

```
@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test(): ...
```

---

TITLE: Registering Custom Markers in pytest.ini (INI)
DESCRIPTION: This INI configuration demonstrates how to register custom markers like 'slow' and 'serial' in your `pytest.ini` file. Registering markers prevents warnings for unknown marks and allows for optional descriptions, making them discoverable by pytest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/mark.rst#_snippet_0

LANGUAGE: INI
CODE:

```
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    serial
```

---

TITLE: Registering Custom pytest Markers in pytest.ini
DESCRIPTION: This INI configuration snippet demonstrates how to register custom test markers (webtest and slow) within the pytest.ini file. Each marker is defined on a new line under the [pytest] section, allowing for clear descriptions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_10

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
markers =
    webtest: mark a test as a webtest.
    slow: mark test as slow.
```

---

TITLE: Accessing Logs from Different Test Stages with caplog (Python)
DESCRIPTION: This Python snippet, within a pytest fixture, demonstrates how to define a fixture that can utilize the `caplog` fixture. The surrounding text indicates that `caplog.get_records(when)` can be used within such fixtures to inspect logs from different test stages (setup, call, teardown), enabling comprehensive log analysis across the test lifecycle.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_14

LANGUAGE: python
CODE:

```
@pytest.fixture
def window(caplog):
        window = create_window()
        yield window
```

---

TITLE: Applying Pytest Markers to a Class in Python
DESCRIPTION: This snippet demonstrates how to apply a pytest marker to an entire test class. All test methods within the `TestClass` will inherit the `webtest` marker, making it equivalent to applying the decorator individually to each test function.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_12

LANGUAGE: Python
CODE:

```
# content of test_mark_classlevel.py
import pytest


@pytest.mark.webtest
class TestClass:
    def test_startup(self):
        pass

    def test_startup_and_more(self):
        pass
```

---

TITLE: Creating Pytest JUnit XML Report (Bash)
DESCRIPTION: Generates a JUnit XML format report file at the specified path using the `--junit-xml` command-line option, suitable for consumption by CI servers like Jenkins.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_13

LANGUAGE: bash
CODE:

```
pytest --junit-xml=path
```

---

TITLE: Configuring Pytest Test File Collection (INI, Multi-line)
DESCRIPTION: This configuration sets `python_files` to include `test_*.py`, `check_*.py`, and `example_*.py`, instructing pytest to consider Python files matching these glob patterns as test modules. This multi-line format achieves the same result as the single-line version, providing an alternative for readability. By default, files matching `test_*.py` and `*_test.py` are considered test modules.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_47

LANGUAGE: ini
CODE:

```
[pytest]
python_files =
    test_*.py
    check_*.py
    example_*.py
```

---

TITLE: Pytest Function Using Multiple Fixtures (Python)
DESCRIPTION: This Python snippet defines `test_2`, a Pytest test function that simultaneously uses both the `otherarg` (function-scoped) and `modarg` (module-scoped) fixtures. This demonstrates how Pytest handles the interaction and ordering of fixtures with different scopes when multiple are required by a single test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_51

LANGUAGE: python
CODE:

```
def test_2(otherarg, modarg):
    print(f"  RUN test2 with otherarg {otherarg} and modarg {modarg}")
```

---

TITLE: Configuring Warning Filters in pyproject.toml (TOML)
DESCRIPTION: This `pyproject.toml` configuration shows an alternative way to set `filterwarnings` using the `[tool.pytest.ini_options]` section. It achieves the same filtering as the `pytest.ini` example, demonstrating how to ignore `UserWarning` and a specific `DeprecationWarning` while turning others into errors.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_4

LANGUAGE: toml
CODE:

```
# pyproject.toml
[tool.pytest.ini_options]
filterwarnings = [
    "error",
    "ignore::UserWarning",
    # note the use of single quote below to denote "raw" strings in TOML
    'ignore:function ham\(\) is deprecated:DeprecationWarning',
]
```

---

TITLE: Recording Test Suite Properties with Pytest Python
DESCRIPTION: This snippet demonstrates how to use the `record_testsuite_property` fixture in pytest to add global information to the root `<testsuite>` tag. It shows how to record properties like 'ARCH' and 'STORAGE_TYPE', which are compatible with `xunit2` JUnit family. This fixture is session-scoped and takes `name` and `value` parameters.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_8

LANGUAGE: python
CODE:

```
def test_foo(record_testsuite_property):
    record_testsuite_property("ARCH", "PPC")
    record_testsuite_property("STORAGE_TYPE", "CEPH")
```

---

TITLE: Configuring Pytest Test Function Collection (INI)
DESCRIPTION: This configuration sets `python_functions` to `*_test`, instructing pytest to collect test functions and methods whose names end with "\_test". By default, pytest collects functions prefixed with "test". This option allows customizing which functions are considered tests, supporting glob-style patterns. This setting does not affect methods within `unittest.TestCase` derived classes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_48

LANGUAGE: ini
CODE:

```
[pytest]
python_functions = *_test
```

---

TITLE: Applying Multiple Custom pytest Marks (Python)
DESCRIPTION: Shows how to apply multiple custom `pytest` marks to a single test function. When iterating over markers, `pytest` processes them from the innermost (closest to the function) to the outermost.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_5

LANGUAGE: python
CODE:

```
@pytest.mark.timeout(10, "slow", method="thread")
@pytest.mark.slow
def test_function(): ...
```

---

TITLE: Running Pytest with Parametrized Fixtures
DESCRIPTION: This snippet shows the output of running `pytest` on `test_module.py`, demonstrating how parametrized fixtures cause tests to execute multiple times for different values. It highlights the detailed failure reports for each parametrized test, including the specific parameter value in the test ID, and the setup/teardown output for fixture finalization. The output indicates that `test_ehlo` and `test_noop` each ran twice, once for `smtp.gmail.com` and once for `mail.python.org`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_39

LANGUAGE: pytest
CODE:

```
$ pytest -q test_module.py
FFFF                                                                 [100%]
================================= FAILURES =================================
________________________ test_ehlo[smtp.gmail.com] _________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0004>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
>       assert 0  # for demo purposes
E       assert 0

test_module.py:7: AssertionError
________________________ test_noop[smtp.gmail.com] _________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0004>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
E       assert 0

test_module.py:13: AssertionError
________________________ test_ehlo[mail.python.org] ________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0005>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
>       assert b"smtp.gmail.com" in msg
E       AssertionError: assert b'smtp.gmail.com' in b'mail.python.org\nPIPELINING\nSIZE 51200000\nETRN\nSTARTTLS\nAUTH DIGEST-MD5 NTLM CRAM-MD5\nENHANCEDSTATUSCODES\n8BITMIME\nDSN\nSMTPUTF8\nCHUNKING'

test_module.py:6: AssertionError
-------------------------- Captured stdout setup ---------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef0004>
________________________ test_noop[mail.python.org] ________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0005>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
E       assert 0

test_module.py:13: AssertionError
------------------------- Captured stdout teardown -------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef0005>
========================= short test summary info ==========================
FAILED test_module.py::test_ehlo[smtp.gmail.com] - assert 0
FAILED test_module.py::test_noop[smtp.gmail.com] - assert 0
FAILED test_module.py::test_ehlo[mail.python.org] - AssertionError: asser...
FAILED test_module.py::test_noop[mail.python.org] - assert 0
4 failed in 0.12s
```

---

TITLE: Pytest Function Using a Module-Scoped Fixture (Python)
DESCRIPTION: This Python snippet defines `test_1`, a Pytest test function that uses the `modarg` fixture. Since `modarg` has a 'module' scope, its setup and teardown will occur only once per module, for each parameter, regardless of how many functions within that module use it.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_50

LANGUAGE: python
CODE:

```
def test_1(modarg):
    print("  RUN test1 with modarg", modarg)
```

---

TITLE: Implementing a Custom Pytest Marker via Plugin in Python
DESCRIPTION: This `conftest.py` snippet demonstrates how to create a custom pytest marker (`env`) and a command-line option (`-E`) to filter tests. It registers the marker and then uses `pytest_runtest_setup` to skip tests if the environment name doesn't match the command-line option.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_17

LANGUAGE: Python
CODE:

```
# content of conftest.py

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "-E",
        action="store",
        metavar="NAME",
        help="only run tests matching the environment NAME.",
    )


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


def pytest_runtest_setup(item):
    envnames = [mark.args[0] for mark in item.iter_markers(name="env")]
    if envnames:
        if item.config.getoption("-E") not in envnames:
```

---

TITLE: Pytest Test Execution Output with Module-Scoped Fixture
DESCRIPTION: This snippet shows the console output when running `pytest test_module.py`. It demonstrates that both `test_ehlo` and `test_noop` fail due to the `assert 0` statements. Crucially, the traceback confirms that the _same_ `smtp_connection` object instance was passed to both test functions, highlighting the effect of the `module` scope.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_13

LANGUAGE: pytest
CODE:

```
$ pytest test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py FF                                                    [100%]

================================= FAILURES =================================
________________________________ test_ehlo _________________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0001>

    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
>       assert 0  # for demo purposes
E       assert 0

test_module.py:7: AssertionError
________________________________ test_noop _________________________________

smtp_connection = <smtplib.SMTP object at 0xdeadbeef0001>

    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
>       assert 0  # for demo purposes
E       assert 0

test_module.py:13: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_ehlo - assert 0
FAILED test_module.py::test_noop - assert 0
============================ 2 failed in 0.12s =============================
```

---

TITLE: Treating UserWarning as Error via Pytest CLI (Pytest CLI)
DESCRIPTION: This command-line snippet demonstrates how to use the `-W` flag with `error::UserWarning` to configure pytest to treat all `UserWarning` instances as test failures. The output shows the test failing due to the warning being elevated to an error, leading to a test failure.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_2

LANGUAGE: pytest
CODE:

```
$ pytest -q test_show_warnings.py -W error::UserWarning
F                                                                    [100%]
================================= FAILURES =================================
_________________________________ test_one _________________________________

    def test_one():
>       assert api_v1() == 1

test_show_warnings.py:10:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    def api_v1():
>       warnings.warn(UserWarning("api v1, should use functions from v2"))
E       UserWarning: api v1, should use functions from v2

test_show_warnings.py:5: UserWarning
========================= short test summary info ==========================
FAILED test_show_warnings.py::test_one - UserWarning: api v1, should use ...
1 failed in 0.12s
```

---

TITLE: Pytest Module for Comparing Implementations (test_module.py)
DESCRIPTION: This test module defines `test_func1` which uses the `basemod` and `optmod` fixtures to compare the results of different `func1` implementations. It asserts that the rounded results from both implementations are equal.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_23

LANGUAGE: python
CODE:

```
# content of test_module.py


def test_func1(basemod, optmod):
    assert round(basemod.func1(), 3) == round(optmod.func1(), 3)
```

---

TITLE: Profiling Test Durations with pytest --durations
DESCRIPTION: This snippet shows how to run pytest with the `--durations=N` command-line option to report the N slowest test durations. The output lists the specified number of tests ordered by their execution time.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_29

LANGUAGE: pytest
CODE:

```
$ pytest --durations=3
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_some_are_slow.py ...                                            [100%]

=========================== slowest 3 durations ============================
0.30s call     test_some_are_slow.py::test_funcslow2
```

---

TITLE: Defining Parameterized Pytest Failures in Python
DESCRIPTION: This Python code defines a parameterized `pytest` test (`test_num`) that runs 50 times. It intentionally fails when the parameter `i` is 17 or 25, demonstrating how `pytest` identifies and reports specific test failures. This setup is used to simulate a scenario where some tests fail, allowing subsequent examples to show how to re-run only the failed tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_50.py
import pytest


@pytest.mark.parametrize("i", range(50))
def test_num(i):
    if i in (17, 25):
        pytest.fail("bad luck")
```

---

TITLE: Finding Active pytest Plugins (Bash)
DESCRIPTION: This command-line snippet illustrates how to identify all active pytest plugins in your environment. Running `pytest --trace-config` will output an extended test header that lists activated plugins by name, including locally loaded conftest.py files.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst#_snippet_2

LANGUAGE: bash
CODE:

```
pytest --trace-config
```

---

TITLE: Updating Marker Access: `get_marker` to `get_closest_marker` in Pytest Python
DESCRIPTION: This snippet demonstrates how to replace the deprecated `Node.get_marker(name)` with `Node.get_closest_marker(name)` when marks are intended to overwrite each other. The new method ensures that only the most relevant marker is retrieved, simplifying scenarios like overriding a module-level `log_level` with a test-specific one. It returns a `Marker` object from which `args` can be accessed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/historical-notes.rst#_snippet_0

LANGUAGE: python
CODE:

```
# replace this:
marker = item.get_marker("log_level")
if marker:
    level = marker.args[0]

# by this:
marker = item.get_closest_marker("log_level")
if marker:
    level = marker.args[0]
```

---

TITLE: Running pytest and viewing traceback
DESCRIPTION: This snippet shows the output of running a pytest test file (`test_checkconfig.py`) that contains a failing test. It demonstrates the default traceback output when a test fails, including the specific line causing the failure and a summary.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_20

LANGUAGE: pytest
CODE:

```
$ pytest -q test_checkconfig.py
F                                                                    [100%]
================================= FAILURES =================================
______________________________ test_something ______________________________

    def test_something():
>       checkconfig(42)
E       Failed: not configured: 42

test_checkconfig.py:11: Failed
========================= short test summary info ==========================
FAILED test_checkconfig.py::test_something - Failed: not configured: 42
1 failed in 0.12s
```

---

TITLE: Collecting Pytest Scenarios with --collect-only
DESCRIPTION: This command uses pytest's `--collect-only` option to display the test collection process for `test_scenarios.py` without actually running the tests. It shows how pytest expands the parametrized tests, explicitly listing `test_demo1[basic]`, `test_demo2[basic]`, `test_demo1[advanced]`, and `test_demo2[advanced]` as individual test items. This is useful for verifying parametrization setup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_8

LANGUAGE: pytest
CODE:

```
$ pytest --collect-only test_scenarios.py
```

---

TITLE: Configuring Default Fixtures in Pytest INI
DESCRIPTION: This INI configuration snippet for `pytest.ini` demonstrates how to globally apply a fixture named `cleandir` to all tests by default using the `usefixtures` option. This ensures the specified fixture runs before every test without explicit declaration in test functions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_58

LANGUAGE: INI
CODE:

```
# content of pytest.ini
[pytest]
usefixtures = cleandir
```

---

TITLE: Asserting on Log Record Tuples with caplog (Python)
DESCRIPTION: This Python snippet demonstrates using `caplog.record_tuples` to assert that specific messages have been logged with a given logger name, severity, and message. This attribute provides a convenient tuple format `(logger_name, level_number, message)` for concise assertions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_12

LANGUAGE: python
CODE:

```
def test_foo(caplog):
        logging.getLogger().info("boo %s", "arg")

        assert caplog.record_tuples == [("root", logging.INFO, "boo arg")]
```

---

TITLE: Pytest Output for Failed Set Comparison (CLI)
DESCRIPTION: Displays the command-line output from running a pytest test with a failed set comparison. It illustrates the detailed `AssertionError` message provided by pytest, showing 'Extra items' in both the left and right sets.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_19

LANGUAGE: pytest
CODE:

```
$ pytest test_assert2.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_assert2.py F                                                    [100%]

================================= FAILURES =================================
___________________________ test_set_comparison ____________________________

    def test_set_comparison():
        set1 = set("1308")
        set2 = set("8035")
>       assert set1 == set2
E       AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
E
E         Extra items in the left set:
E         '1'
E         Extra items in the right set:
E         '5'
E         Use -v to get more diff

test_assert2.py:4: AssertionError
========================= short test summary info ==========================
FAILED test_assert2.py::test_set_comparison - AssertionError: assert {'0'...
============================ 1 failed in 0.12s =============================
```

---

TITLE: Assert Set Equality in Pytest
DESCRIPTION: Presents a failed assertion comparing two sets. Pytest clearly lists the items that are present in one set but not the other.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_12

LANGUAGE: python
CODE:

```
assert {0, 10, 11, 12} == {0, 20, 21}
```

---

TITLE: Recording Custom Properties for Test Reports with record_property
DESCRIPTION: This example illustrates using the `record_property` fixture to add custom key-value pairs as extra properties to the calling test. These properties become part of the test report (e.g., JUnit XML), providing additional metadata about the test execution. The value is automatically XML-encoded.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_7

LANGUAGE: python
CODE:

```
def test_function(record_property):
    record_property("example_key", 1)
```

---

TITLE: Disabling a pytest Plugin in pytest.ini (INI)
DESCRIPTION: This INI configuration snippet shows how to unconditionally disable a plugin for an entire project by adding the `-p no:NAME` option to the `addopts` setting within the `[pytest]` section of your `pytest.ini` file. This provides a persistent way to manage plugin loading.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst#_snippet_4

LANGUAGE: ini
CODE:

```
[pytest]
addopts = -p no:NAME
```

---

TITLE: Collecting Pytest Backend Tests with --collect-only
DESCRIPTION: This command uses pytest's `--collect-only` option to show the collected tests for `test_backends.py`. It demonstrates that the `test_db_initialized` function will be invoked twice, once for each parametrized `db` fixture instance (`d1` and `d2`), confirming the successful application of indirect parametrization for deferred resource setup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_11

LANGUAGE: pytest
CODE:

```
$ pytest test_backends.py --collect-only
```

---

TITLE: Pytest Output for Parametrized Test Function
DESCRIPTION: This snippet shows the console output from running the parametrized test_eval function. It illustrates how pytest executes each parameter set, indicating successful tests with a dot and failures with an 'F', along with a detailed traceback for the failing case.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 3 items

test_expectation.py ..F                                              [100%]

================================= FAILURES =================================
____________________________ test_eval[6*9-42] _____________________________

test_input = '6*9', expected = 42

    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       AssertionError: assert 54 == 42
E        +  where 54 = eval('6*9')

test_expectation.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_expectation.py::test_eval[6*9-42] - AssertionError: assert 54...
======================= 1 failed, 2 passed in 0.12s ========================
```

---

TITLE: Excluding pytest Tests by Keyword
DESCRIPTION: This command illustrates how to use the -k option with the "not" operator to exclude tests matching a specific keyword. It runs all tests except those containing "send_http", demonstrating the deselection of one test and the selection of others.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_8

LANGUAGE: pytest
CODE:

```
$ pytest -k "not send_http" -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 4 items / 1 deselected / 3 selected

test_server.py::test_something_quick PASSED                          [ 33%]
test_server.py::test_another PASSED                                  [ 66%]
test_server.py::TestClass::test_method PASSED                        [100%]

===================== 3 passed, 1 deselected in 0.12s ======================
```

---

TITLE: Running Pytest with Skipped Tests (CLI)
DESCRIPTION: Shows the command-line execution of pytest using the `-rs` flag to report details on skipped tests, demonstrating that the test marked `slow` is skipped by default when `--runslow` is not used.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_17

LANGUAGE: pytest
CODE:

```
$ pytest -rs    # "-rs" means report details on the little 's'
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py .s                                                    [100%]

========================= short test summary info ==========================
SKIPPED [1] test_module.py:8: need --runslow option to run
======================= 1 passed, 1 skipped in 0.12s =======================
```

---

TITLE: Listing Pytest Built-in Fixtures and Details
DESCRIPTION: This snippet shows the command-line output when listing Pytest's built-in fixtures with verbose details using `pytest --fixtures -v`. It provides an example of the session start information and the format in which fixture documentation is presented, including their source file and a brief description.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_0

LANGUAGE: pytest
CODE:

```
$ pytest  --fixtures -v
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collected 0 items
```

---

TITLE: Loading Multiple pytest Plugins in Python Test Module
DESCRIPTION: This Python code shows how to load multiple pytest plugins by assigning a list of plugin names to the `pytest_plugins` global variable. When the test module or conftest file is loaded, the specified plugins (e.g., `name1`, `name2`) will also be loaded, enabling modular test setups.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_4

LANGUAGE: Python
CODE:

```
pytest_plugins = ["name1", "name2"]
```

---

TITLE: Demonstrating Sync Test with Unawaited Async Fixture in Pytest
DESCRIPTION: This snippet illustrates a deprecated pattern where a synchronous test function attempts to use an asynchronous fixture directly without awaiting it. This can lead to "unawaited coroutine" warnings or unpredictable behavior, especially with fixture caching. The `asyncio.run` call attempts to execute the coroutine returned by the fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_0

LANGUAGE: python
CODE:

```
import asyncio
import pytest


@pytest.fixture
async def unawaited_fixture():
    return 1


def test_foo(unawaited_fixture):
    assert 1 == asyncio.run(unawaited_fixture)
```

---

TITLE: Registering Custom pytest Markers (Python)
DESCRIPTION: This code illustrates how to register custom markers within a pytest plugin using the `pytest_configure` hook. Registering markers ensures they appear in pytest's help text and prevents warnings for unknown marks. It shows examples for both a simple marker and one that accepts arguments.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_7

LANGUAGE: Python
CODE:

```
def pytest_configure(config):
    config.addinivalue_line("markers", "cool_marker: this one is for cool tests.")
    config.addinivalue_line(
        "markers", "mark_with(arg, arg2): this marker takes arguments."
    )
```

---

TITLE: Skipping Tests on Missing Import Dependency with Minimum Version in Pytest
DESCRIPTION: This snippet extends the `pytest.importorskip` usage to include a minimum version check. If 'docutils' is not importable or its version is less than '0.3', the test will be skipped.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_9

LANGUAGE: python
CODE:

```
docutils = pytest.importorskip("docutils", minversion="0.3")
```

---

TITLE: Using a pytest fixture in a unittest.TestCase subclass (Python)
DESCRIPTION: This Python code defines a `unittest.TestCase` subclass, `MyTest`, which integrates the `db_class` pytest fixture using the `@pytest.mark.usefixtures("db_class")` decorator. This ensures the `db` attribute, provided by the fixture, is available to `test_method1` and `test_method2`. The assert statements demonstrate access to `self.db` and are deliberately set to fail for demonstration purposes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst#_snippet_2

LANGUAGE: python
CODE:

```
# content of test_unittest_db.py

import unittest

import pytest


@pytest.mark.usefixtures("db_class")
class MyTest(unittest.TestCase):
    def test_method1(self):
        assert hasattr(self, "db")
        assert 0, self.db  # fail for demo purposes

    def test_method2(self):
        assert 0, self.db  # fail for demo purposes
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command upgrades the pytest testing framework to its latest version using pip, the Python package installer. It ensures users have access to the newest features, bug fixes, and improvements by fetching the updated package from PyPI.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.5.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the specified version (or the latest available) using pip, the Python package installer. It ensures you have the most recent bug fixes and features.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-7.1.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest version available on PyPI using the pip package manager. The '--upgrade' flag ensures that pip replaces the current version with the newest one.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-6.0.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest version (3.2.3 in this context) using the pip package manager. The `--upgrade` flag ensures that pip replaces any older versions with the new one, providing access to the latest bug fixes and features.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.2.3.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command uses the pip package installer to upgrade the pytest testing framework to its latest available version. The '-U' flag ensures that existing packages are upgraded.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.1.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This command upgrades the pytest testing framework to its latest version available on PyPI using the pip package installer. It ensures that any existing pytest installation is replaced or updated to the newer version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.3.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This shell command uses the pip package manager to upgrade an existing pytest installation to the latest version (6.2.3 in this context). The `--upgrade` flag ensures that pip replaces the old version with the new one, rather than just installing if not present.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-6.2.3.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This shell command uses pip, the Python package installer, to upgrade the pytest testing framework to its latest available version. The `-U` flag ensures that the package is upgraded even if it's already installed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.2.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Configuring Pytest Temporary Path Retention Policy (INI)
DESCRIPTION: This configuration sets `tmp_path_retention_policy` to `all`, instructing pytest to retain directories created by the `tmp_path` fixture for all tests, regardless of their outcome. Other policies include `failed` (retains only for errors/failures) and `none` (always removes). The default value is `all`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_55

LANGUAGE: ini
CODE:

```
[pytest]
tmp_path_retention_policy = all
```

---

TITLE: Generating Tests with Yield in Pytest (Deprecated)
DESCRIPTION: This snippet demonstrates an older method of generating multiple test cases using `yield` within a test function. This approach is deprecated and does not properly support fixtures, with `pytest.mark.parametrize` being the recommended alternative.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_9

LANGUAGE: Python
CODE:

```
def check(x, y):
    assert x**x == y


def test_squared():
    yield check, 2, 4
    yield check, 3, 9
```

---

TITLE: Running Pytest Directly on Specific Module
DESCRIPTION: This command executes pytest directly on the 'testing/test_config.py' module within the activated virtual environment, allowing for quick and direct test runs.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst#_snippet_16

LANGUAGE: Shell
CODE:

```
pytest testing/test_config.py
```

---

TITLE: Capturing Binary Stdout/Stderr with capsysbinary
DESCRIPTION: This example demonstrates using the `capsysbinary` fixture to capture byte-based output from `sys.stdout` and `sys.stderr`. The `readouterr()` method returns a `(out, err)` namedtuple, where `out` and `err` are `bytes` objects, allowing assertions on binary output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_1

LANGUAGE: python
CODE:

```
def test_output(capsysbinary):
    print("hello")
    captured = capsysbinary.readouterr()
    assert captured.out == b"hello\n"
```

---

TITLE: Setting JUnit XML Format in pytest.ini
DESCRIPTION: This configuration defines the format of the generated JUnit XML file. The `xunit2` option produces a format compatible with newer Jenkins versions, which is also the default behavior.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_27

LANGUAGE: ini
CODE:

```
[pytest]
junit_family = xunit2
```

---

TITLE: Ensuring At Least One Warning is Issued in Python
DESCRIPTION: This snippet shows how to assert that at least one of a specified set of warning types (e.g., `RuntimeWarning` or `UserWarning`) is issued within a test using `pytest.warns` with a tuple of warning types.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_18

LANGUAGE: python
CODE:

```
def test_warning():
    with pytest.warns((RuntimeWarning, UserWarning)):
        ...
```

---

TITLE: Listing Registered pytest Markers
DESCRIPTION: This command shows how to use pytest --markers to list all registered markers for the current test suite, including both custom-defined markers from pytest.ini and built-in pytest markers like filterwarnings, skip, and skipif.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_11

LANGUAGE: pytest
CODE:

```
$ pytest --markers
@pytest.mark.webtest: mark a test as a webtest.

@pytest.mark.slow: mark test as slow.

@pytest.mark.filterwarnings(warning): add a warning filter to the given test. see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings

@pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.

@pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif
```

---

TITLE: Applying Filterwarnings to a Test Function in Pytest
DESCRIPTION: This snippet demonstrates how to use the `@pytest.mark.filterwarnings` decorator to turn specific warnings into errors for a single test function. In this case, any warning issued during `test_one` will cause the test to fail. Decorators are evaluated in reverse order, so filters from earlier decorators take precedence.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_7

LANGUAGE: python
CODE:

```
@pytest.mark.filterwarnings("error")
def test_one():
    assert api_v1() == 1
```

---

TITLE: Assertion failure in nested function (Python)
DESCRIPTION: Calls `somefunc` with results from `f()` and `g()`. `somefunc` calls `otherfunc(a, b)`, which contains an assertion `assert a == b`. The assertion fails because the values (44 and 43) are not equal.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_32

LANGUAGE: python
CODE:

```
somefunc(f(), g())
```

LANGUAGE: python
CODE:

```
assert a == b
```

---

TITLE: Upgrading pytest to 8.0.1 via pip
DESCRIPTION: This command is used to upgrade an existing pytest installation to version 8.0.1 using pip, the Python package installer. The '--upgrade' flag ensures that pip replaces the current version with the specified or latest available version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.0.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Defining 'mid' Fixture in pytest (tests/subpackage/conftest.py)
DESCRIPTION: This pytest fixture, located in `tests/subpackage/conftest.py`, appends 'mid subpackage' to the `order` list. It exemplifies how fixtures defined in a `conftest.py` file become available to tests within that directory and its subdirectories, establishing a local scope.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_3

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def mid(order):
    order.append("mid subpackage")
```

---

TITLE: Using a Module-Scoped Pytest Fixture in Python Tests
DESCRIPTION: This snippet demonstrates how test functions (`test_ehlo`, `test_noop`) consume the `smtp_connection` fixture. Pytest automatically injects the fixture instance as an argument to the test functions. Both tests use the same `smtp_connection` object, as indicated by the module scope, and include `assert 0` for demonstration purposes to show test failures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_12

LANGUAGE: python
CODE:

```
# content of test_module.py


def test_ehlo(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250
    assert b"smtp.gmail.com" in msg
    assert 0  # for demo purposes


def test_noop(smtp_connection):
    response, msg = smtp_connection.noop()
    assert response == 250
    assert 0  # for demo purposes
```

---

TITLE: Configure pytest via PYTEST_ADDOPTS Environment Variable
DESCRIPTION: Demonstrates setting default command line options using the `PYTEST_ADDOPTS` environment variable in a bash shell.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_1

LANGUAGE: bash
CODE:

```
export PYTEST_ADDOPTS="-v"
```

---

TITLE: Applying Global Fixtures (INI)
DESCRIPTION: Specifies a list of fixtures that will be applied to all test functions in pytest. This configuration is semantically equivalent to applying the `@pytest.mark.usefixtures` marker to every test function.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_58

LANGUAGE: ini
CODE:

```
[pytest]
usefixtures =
    clean_db
```

---

TITLE: Temporarily Disabling Pytest Output Capture in Python
DESCRIPTION: This snippet demonstrates how to temporarily disable output capturing within a pytest test using the `capsys.disabled()` context manager. Output inside the `with` block is sent directly to `sys.stdout` instead of being captured by pytest, while output outside the block remains captured.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-stdout-stderr.rst#_snippet_4

LANGUAGE: Python
CODE:

```
def test_disabling_capturing(capsys):
    print("this output is captured")
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
    print("this output is also captured")
```

---

TITLE: Issuing Warnings with warnings.warn and PytestWarning
DESCRIPTION: This snippet demonstrates the recommended way to issue warnings in pytest using the standard `warnings.warn` function with a `pytest.PytestWarning` instance. This aligns with Python's built-in warning system.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_33

LANGUAGE: python
CODE:

```
warnings.warn(pytest.PytestWarning("some warning"))
```

---

TITLE: Assert Lists of Different Lengths in Pytest
DESCRIPTION: Demonstrates a failed assertion comparing two lists where one is a prefix of the other. Pytest indicates which list is longer and the extra item(s).
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_13

LANGUAGE: python
CODE:

```
assert [1, 2] == [1, 2, 3]
```

---

TITLE: Dynamically Determining Pytest Fixture Scope in Python
DESCRIPTION: This Python function, `determine_scope`, demonstrates how to dynamically set a fixture's scope based on runtime conditions. It accepts `fixture_name` and a `config` object. If the `--keep-containers` command-line option is present, it returns 'session' scope; otherwise, it defaults to 'function' scope. This allows for flexible fixture behavior without code changes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_15

LANGUAGE: python
CODE:

```
def determine_scope(fixture_name, config):
    if config.getoption("--keep-containers", None):
        return "session"
    return "function"
```

---

TITLE: Defining Pytest and Unittest Test Classes with `callme` Methods in Python
DESCRIPTION: This Python code defines multiple test classes (`TestHello`, `TestOther`, `SomeTest`) for `pytest` and `unittest` frameworks in `test_module.py`. Each class includes a `callme` class method, which is designed to be invoked by the session-scoped fixture before any tests in the class run. This demonstrates how test classes can expose hooks for pre-test execution logic, compatible with both `pytest` and standard `unittest` frameworks.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/special.rst#_snippet_1

LANGUAGE: python
CODE:

```
# content of test_module.py


class TestHello:
    @classmethod
    def callme(cls):
        print("callme called!")

    def test_method1(self):
        print("test_method1 called")

    def test_method2(self):
        print("test_method2 called")


class TestOther:
    @classmethod
    def callme(cls):
        print("callme other called")

    def test_other(self):
        print("test other")


# works with unittest as well ...
import unittest


class SomeTest(unittest.TestCase):
    @classmethod
    def callme(self):
        print("SomeTest callme called")

    def test_unit1(self):
        print("test_unit1 method called")
```

---

TITLE: Running Inlined Tests with Pytest --pyargs (Bash)
DESCRIPTION: This command demonstrates how to execute tests organized in an inlined package structure using `pytest` with the `--pyargs` option. `pytest` automatically discovers the `mypkg` installation and collects tests from its associated `tests` directory, simplifying test execution for distributed application packages.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_7

LANGUAGE: bash
CODE:

```
pytest --pyargs mypkg
```

---

TITLE: Defining Pytest Test Search Paths (INI)
DESCRIPTION: This configuration sets `testpaths` to `testing doc`, instructing pytest to search for tests within these directories when no specific paths are provided on the command line. Paths are relative to the root directory and can include shell-style wildcards. This helps speed up test collection and prevents accidental collection of undesired tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_51

LANGUAGE: ini
CODE:

```
[pytest]
testpaths = testing doc
```

---

TITLE: Calling pytest.warns on Functions or Code Strings in Python
DESCRIPTION: This snippet shows the alternative syntax for `pytest.warns`, allowing it to be called directly on a function or a string representing code to be executed. This is useful for asserting warnings from specific callable units.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_14

LANGUAGE: python
CODE:

```
pytest.warns(expected_warning, func, *args, **kwargs)
pytest.warns(expected_warning, "func(*args, **kwargs)")
```

---

TITLE: Marking a Pytest Function as XFAIL with Strict Mode
DESCRIPTION: This snippet shows how to use the `strict=True` parameter with `@pytest.mark.xfail`. When `strict` is true, an 'unexpectedly passing' (XPASS) result for this test will cause the entire test suite to fail, enforcing stricter expectations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_20

LANGUAGE: python
CODE:

```
@pytest.mark.xfail(strict=True)
def test_function(): ...
```

---

TITLE: Configuring Pytest for xunit2 JUnit Family Format
DESCRIPTION: This snippet shows how to configure `pytest.ini` to use the `xunit2` format for JUnit XML reports. This format is an update to the older `xunit1` and is recommended for compatibility with modern CI/CD tools like Jenkins and Azure Pipelines.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_17

LANGUAGE: ini
CODE:

```
[pytest]
junit_family=xunit2
```

---

TITLE: Failing Assertion in Called Function (Python)
DESCRIPTION: Documents a pytest test method that calls another function, where the assertion failure actually occurs within the called function, demonstrating pytest's traceback reporting.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_2

LANGUAGE: Python
CODE:

```
def test_simple_multiline(self):
    otherfunc_multi(42, 6 * 9)

def otherfunc_multi(a, b):
    assert a == b
```

---

TITLE: Failing Multiline String Equality Assertion (Python)
DESCRIPTION: Documents a pytest test method that fails when asserting the equality of two different multiline strings, showing the multiline diff output provided by pytest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_6

LANGUAGE: Python
CODE:

```
def test_eq_multiline_text(self):
    assert "foo\nspam\nbar" == "foo\neggs\nbar"
```

---

TITLE: Ignoring Specific Deprecation Warnings in pytest.ini
DESCRIPTION: This INI configuration snippet illustrates how to ignore specific `DeprecationWarning` messages using the `filterwarnings` option in `pytest.ini`. It uses a regular expression `.*U.*mode is deprecated` to match and suppress warnings related to deprecated 'U' mode usage, particularly useful for third-party library warnings.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_10

LANGUAGE: ini
CODE:

```
[pytest]
filterwarnings =
    ignore:.*U.*mode is deprecated:DeprecationWarning
```

---

TITLE: Applying Warning Filters with pytest.mark.filterwarnings (Python)
DESCRIPTION: This Python code demonstrates using the `@pytest.mark.filterwarnings` decorator to apply warning filters directly to a test function. Here, it ignores any warning message starting with "api v1" for `test_one`, providing fine-grained control over warning behavior at the test item level.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_5

LANGUAGE: python
CODE:

```
import warnings

def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1


@pytest.mark.filterwarnings("ignore:api v1")
def test_one():
    assert api_v1() == 1
```

---

TITLE: Defining Platform-Specific Pytest Tests
DESCRIPTION: This test file demonstrates how to apply platform-specific markers (`pytest.mark.darwin`, `pytest.mark.linux`, `pytest.mark.win32`) to individual test functions. It also includes a test without any platform marker, which is expected to run on all platforms, showcasing the usage with the platform skipping plugin.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_29

LANGUAGE: python
CODE:

```
# content of test_plat.py

import pytest


@pytest.mark.darwin
def test_if_apple_is_evil():
    pass


@pytest.mark.linux
def test_if_linux_works():
    pass


@pytest.mark.win32
def test_if_win32_crashes():
    pass


def test_runs_everywhere():
    pass
```

---

TITLE: Installing/Upgrading pytest via pip (Shell)
DESCRIPTION: This command utilizes pip, the Python package installer, to either install pytest for the first time or upgrade an existing installation to the latest version. The '-U' flag is crucial for ensuring an upgrade rather than just an installation if the package is already present. This is the recommended method for managing pytest installations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.6.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Using tmp_path_factory fixture in pytest (Python)
DESCRIPTION: Illustrates the use of the session-scoped `tmp_path_factory` fixture to create temporary directories or files once per test session, suitable for expensive setup tasks.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/tmp_path.rst#_snippet_2

LANGUAGE: python
CODE:

```
# contents of conftest.py
import pytest


@pytest.fixture(scope="session")
def image_file(tmp_path_factory):
    img = compute_expensive_image()
    fn = tmp_path_factory.mktemp("data") / "img.png"
    img.save(fn)
    return fn


# contents of test_image.py
def test_histogram(image_file):
    img = load_image(image_file)
    # compute and test histogram
```

---

TITLE: Configuring Pytest Truncation Limits (INI)
DESCRIPTION: Sets custom truncation limits for assertion output in pytest. The `truncation_limit_lines` option controls the maximum number of lines, and `truncation_limit_chars` controls the maximum characters.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_11

LANGUAGE: ini
CODE:

```
[pytest]
truncation_limit_lines = 10
truncation_limit_chars = 90
```

---

TITLE: Configuring Pytest Assertion Message Truncation Limit (INI)
DESCRIPTION: This configuration sets `truncation_limit_chars` to `640`, controlling the maximum number of characters for truncating assertion message contents. Setting the value to `0` disables the character limit. Pytest truncates messages by default to prevent large data comparisons from overloading console output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_56

LANGUAGE: ini
CODE:

```
[pytest]
truncation_limit_chars = 640
```

---

TITLE: Configuring Warning Filters in pytest.ini (INI)
DESCRIPTION: This `pytest.ini` configuration demonstrates how to use the `filterwarnings` option to control warning behavior globally. It sets a default action of `error`, then specifically ignores `UserWarning` and a particular `DeprecationWarning` matching a regex.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_3

LANGUAGE: ini
CODE:

```
# pytest.ini
[pytest]
filterwarnings =
    error
    ignore::UserWarning
    ignore:function ham\(\) is deprecated:DeprecationWarning
```

---

TITLE: Running a Specific Test Function (Bash)
DESCRIPTION: This command executes a single, specific test function within a module. The path to the module is provided relative to the working directory, followed by '::' and the name of the test function.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_3

LANGUAGE: bash
CODE:

```
pytest tests/test_mod.py::test_func
```

---

TITLE: Asserting Equality of Attributes from Different Classes in Python with Pytest
DESCRIPTION: This test demonstrates asserting the equality of attributes from instances of two different classes. The pytest failure output shows the values and the instances they belong to.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_24

LANGUAGE: python
CODE:

```
def test_attribute_multiple():
    class Foo:
        b = 1

    class Bar:
        b = 2

    assert Foo().b == Bar().b
```

---

TITLE: Invoking PDB at Test Start with Pytest (Bash)
DESCRIPTION: This command line option forces pytest to invoke the Python debugger (pdb) at the very beginning of every test execution. This is useful for stepping through test setup and execution from the start.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/failures.rst#_snippet_3

LANGUAGE: bash
CODE:

```
pytest --trace
```

---

TITLE: Defining Custom Markers in Pytest (INI)
DESCRIPTION: Allows listing additional markers to whitelist when `--strict-markers` or `--strict` command-line arguments are used. This ensures only defined markers are recognized, preventing future regressions and maintaining test suite integrity.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_42

LANGUAGE: ini
CODE:

```
[pytest]
addopts = --strict-markers
markers =
    slow
    serial
```

---

TITLE: Running Pytest Scenarios from Command Line
DESCRIPTION: This command executes the `test_scenarios.py` file using pytest. It runs all tests defined within `TestSampleWithScenarios` class, applying the `basic` and `advanced` scenarios to `test_demo1` and `test_demo2`, resulting in four collected and passed tests. This demonstrates the successful application of the scenario-based parametrization.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_7

LANGUAGE: pytest
CODE:

```
$ pytest test_scenarios.py
```

---

TITLE: Disabling Pytest's Internal Logging Feature via INI Configuration
DESCRIPTION: This INI configuration snippet demonstrates how to disable pytest's internal logging feature. By adding `addopts=-p no:logging` under the `[pytest]` section in `pytest.ini`, users can prevent conflicts with older plugins like `pytest-catchlog` or manage logging behavior externally. This is useful for maintaining backward compatibility or specific logging setups.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_17

LANGUAGE: INI
CODE:

```
[pytest]
    addopts=-p no:logging
```

---

TITLE: Pytest Output: Running Interdependent Fixture Tests
DESCRIPTION: This output shows the execution of `test_appsetup.py`, demonstrating that the test `test_smtp_connection_exists` runs twice. This is due to the `smtp_connection` fixture being parametrized, and pytest automatically running the dependent `app` fixture and its tests for each parameter, confirming proper dependency resolution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_45

LANGUAGE: pytest
CODE:

```
$ pytest -v test_appsetup.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 2 items

test_appsetup.py::test_smtp_connection_exists[smtp.gmail.com] PASSED [ 50%]
test_appsetup.py::test_smtp_connection_exists[mail.python.org] PASSED [100%]

============================ 2 passed in 0.12s =============================
```

---

TITLE: Invoking pytest from a Python Program (Python)
DESCRIPTION: This Python snippet illustrates how to programmatically invoke pytest within a Python application. The `pytest.main()` function allows passing a list of arguments and plugins, providing flexible control over the test run directly from your code.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.0.rst#_snippet_2

LANGUAGE: Python
CODE:

```
import pytest ; pytest.main(arglist, pluginlist)
```

---

TITLE: Running a Specific Parameterized Test Instance (Bash)
DESCRIPTION: This command executes a specific parameterized instance of a test function. The particular parameters for the instance are specified within square brackets '[]' immediately following the function name.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_6

LANGUAGE: bash
CODE:

```
pytest tests/test_mod.py::test_func[x1,y2]
```

---

TITLE: Invoking Pytest Programmatically with Custom Plugin
DESCRIPTION: This Python example illustrates how to invoke `pytest.main()` and register a custom plugin. The `MyPlugin` class defines a `pytest_sessionfinish` hook, which is executed after the test session completes. The `plugins` argument to `pytest.main` accepts a list of plugin instances.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_19

LANGUAGE: python
CODE:

```
# content of myinvoke.py
import sys

import pytest


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))
```

---

TITLE: Listing Pytest Fixtures (Shell)
DESCRIPTION: This command shows a list of all available fixtures. Fixtures are functions that provide a fixed baseline for tests, ensuring repeatable results.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_64

LANGUAGE: Shell
CODE:

```
pytest --fixtures
```

---

TITLE: Overriding Pytest Configuration via Command Line (Bash)
DESCRIPTION: Demonstrates how to override pytest configuration options directly from the command line using the `-o` or `--override-ini` flag. This allows for dynamic adjustment of settings like `console_output_style` and `cache_dir` without modifying the `pytest.ini` file.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_16

LANGUAGE: bash
CODE:

```
pytest -o console_output_style=classic -o cache_dir=/tmp/mycache
```

---

TITLE: Dynamically Adding Pytest Markers in conftest.py
DESCRIPTION: This Python snippet defines a `pytest_collection_modifyitems` hook in `conftest.py` to dynamically add markers to tests. It iterates through collected test items and applies `pytest.mark.interface` or `pytest.mark.event` based on whether 'interface' or 'event' is present in the test's node ID. This allows for flexible test categorization without explicit `@pytest.mark` decorators in test files.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_33

LANGUAGE: python
CODE:

```
# content of conftest.py

import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "interface" in item.nodeid:
            item.add_marker(pytest.mark.interface)
        elif "event" in item.nodeid:
            item.add_marker(pytest.mark.event)
```

---

TITLE: Filtering Warnings in pytest.ini
DESCRIPTION: This setting allows defining a list of filters and actions for matched warnings during the test session. The example demonstrates ignoring `DeprecationWarning` and turning all other warnings into errors.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_25

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
filterwarnings =
    error
    ignore::DeprecationWarning
```

---

TITLE: Function Level Setup/Teardown in Pytest Modules
DESCRIPTION: These functions are used for module-level test functions, invoked around each test function. `setup_function` runs before each test function, and `teardown_function` runs after each. The `function` parameter is optional since pytest-3.0.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst#_snippet_3

LANGUAGE: python
CODE:

```
def setup_function(function):
    """setup any state tied to the execution of the given function.
        Invoked for every test function in the module.
    """


def teardown_function(function):
    """teardown any state that was previously setup with a setup_function
        call.
    """
```

---

TITLE: Failing String Equality Assertion (Python)
DESCRIPTION: Documents a pytest test method that fails when asserting the equality of two different short strings, showing the simple diff output provided by pytest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_4

LANGUAGE: Python
CODE:

```
def test_eq_text(self):
    assert "spam" == "eggs"
```

---

TITLE: Ignoring Files with Glob Patterns in Pytest (Python)
DESCRIPTION: This `conftest.py` snippet demonstrates using `collect_ignore_glob` to ignore files based on Unix shell-style wildcards. It ignores `setup.py` and, when run with Python 3, additionally ignores all files ending with `*_py2.py`, providing flexible file exclusion.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_19

LANGUAGE: python
CODE:

```
# content of conftest.py
import sys

collect_ignore = ["setup.py"]
if sys.version_info[0] > 2:
    collect_ignore_glob = ["*_py2.py"]
```

---

TITLE: Monkeypatching Dictionary Items with pytest-monkeypatch (delitem)
DESCRIPTION: This test illustrates how `monkeypatch.delitem` can be used to temporarily remove a key from a dictionary, specifically `app.DEFAULT_CONFIG`. It verifies that `create_connection_string` correctly raises a `KeyError` when a required configuration key is missing, simulating a broken or incomplete configuration.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_11

LANGUAGE: Python
CODE:

```
# contents of test_app.py
import pytest

# app.py with the connection string function
import app


def test_missing_user(monkeypatch):
    # patch the DEFAULT_CONFIG t be missing the 'user' key
    monkeypatch.delitem(app.DEFAULT_CONFIG, "user", raising=False)

    # Key error expected because a config is not passed, and the
    # default is now missing the 'user' entry.
    with pytest.raises(KeyError):
        _ = app.create_connection_string()
```

---

TITLE: Running Tests by Annotated Marker Expression (Bash)
DESCRIPTION: This command executes tests decorated with an annotated marker, such as '@pytest.mark.slow(phase=1)', where the marker expression includes specific keyword arguments. The entire expression must be enclosed in quotes to be parsed correctly.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_8

LANGUAGE: bash
CODE:

```
pytest -m "slow(phase=1)"
```

---

TITLE: Use Package-Scoped Fixture in Test (Python)
DESCRIPTION: A test function `test_a1` in `a/test_db.py` that depends on the `db` fixture defined in `a/conftest.py`. It asserts 0 to demonstrate the fixture value.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_34

LANGUAGE: python
CODE:

```
# content of a/test_db.py
def test_a1(db):
    assert 0, db  # to show value
```

---

TITLE: Running unittest Packages with pytest (Shell)
DESCRIPTION: This command demonstrates how pytest can be used to run tests defined within an installed `unittest` package. The `--pyargs` option tells pytest to look for tests within the specified Python package, enabling seamless integration with existing unittest suites.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.0.rst#_snippet_4

LANGUAGE: Shell
CODE:

```
py.test --pyargs unittest
```

---

TITLE: Listing Available Pytest Markers (CLI)
DESCRIPTION: This snippet shows the output of `pytest --markers`, which lists all registered markers, including built-in ones like `skip`, `skipif`, `xfail`, `parametrize`, and `usefixtures`, along with their descriptions. This command is useful for discovering available markers and understanding their intended use and parameters.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_21

LANGUAGE: pytest
CODE:

```
$ pytest --markers
@pytest.mark.env(name): mark test to run only on named environment

@pytest.mark.filterwarnings(warning): add a warning filter to the given test. see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings

@pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.

@pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif

@pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None, strict=xfail_strict): mark the test function as an expected failure if any of the conditions evaluate to True. Optionally specify a reason for better reporting and run=False if you don't even want to execute the test function. If only specific exception(s) are expected, you can list them in raises, and if the test fails in other ways, it will be reported as a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail

@pytest.mark.parametrize(argnames, argvalues): call a test function multiple times passing in different arguments in turn. argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function, one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info and examples.

@pytest.mark.usefixtures(fixturename1, fixturename2, ...): mark tests as needing all of the specified fixtures. see https://docs.pytest.org/en/stable/explanation/fixtures.html#usefixtures

@pytest.mark.tryfirst: mark a hook implementation function such that the plugin machinery will try to call it first/as early as possible. DEPRECATED, use @pytest.hookimpl(tryfirst=True) instead.

@pytest.mark.trylast: mark a hook implementation function such that the plugin machinery will try to call it last/as late as possible. DEPRECATED, use @pytest.hookimpl(trylast=True) instead.
```

---

TITLE: Recording Warnings with recwarn Fixture in Python
DESCRIPTION: This example demonstrates using the `recwarn` fixture to record warnings throughout an entire test function. It shows how to access recorded warnings, check their count, pop specific warning types, and inspect their properties like category, message, filename, and line number.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_17

LANGUAGE: python
CODE:

```
import warnings


def test_hello(recwarn):
    warnings.warn("hello", UserWarning)
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert issubclass(w.category, UserWarning)
    assert str(w.message) == "hello"
    assert w.filename
    assert w.lineno
```

---

TITLE: Skipping Entire Module with Pytest Skip (Python)
DESCRIPTION: This code demonstrates how to skip an entire test module by calling `pytest.skip(reason, allow_module_level=True)` at the module level. This is beneficial for modules containing tests that are entirely dependent on specific environmental conditions, such as platform-specific tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_3

LANGUAGE: python
CODE:

```
import sys

import pytest

if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only tests", allow_module_level=True)
```

---

TITLE: Testing Database Connection String Creation (Python)
DESCRIPTION: This test function verifies that `app.create_connection_string()` produces the expected connection string when `mock_test_user` and `mock_test_database` fixtures are applied. It asserts the generated string against a predefined `expected` value.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_15

LANGUAGE: Python
CODE:

```
def test_connection(mock_test_user, mock_test_database):
    expected = "User Id=test_user; Location=test_db;"

    result = app.create_connection_string()
    assert result == expected
```

---

TITLE: Configuring Live Log Format in Pytest (INI)
DESCRIPTION: Sets a `logging`-compatible string used to format live logging messages displayed in the console. This allows customization of the information included in each log entry, such as timestamp, level, and message.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_33

LANGUAGE: ini
CODE:

```
[pytest]
log_cli_format = %(asctime)s %(levelname)s %(message)s
```

---

TITLE: Nose-style setup/teardown Methods in Python (Deprecated)
DESCRIPTION: This code illustrates the use of plain `setup` and `teardown` methods within a test class, which are part of the deprecated Nose support in Pytest. These methods are not pytest-native and should be migrated to `setup_method` and `teardown_method` for proper Pytest integration.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_11

LANGUAGE: Python
CODE:

```
class Test:
    def setup(self):
        self.resource = make_resource()

    def teardown(self):
        self.resource.close()

    def test_foo(self): ...

    def test_bar(self): ...
```

---

TITLE: Applying Multiple Marks with `pytestmark` (Python)
DESCRIPTION: This example shows how to apply multiple `pytest` marks to a test module or class. By assigning a list of marks (e.g., `pytest.mark.integration`, `pytest.mark.slow`) to `pytestmark`, tests can be categorized with multiple tags for more granular filtering.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_14

LANGUAGE: python
CODE:

```
import pytest

pytestmark = [pytest.mark.integration, pytest.mark.slow]
```

---

TITLE: Defining 'inner' Fixture and 'test_order' with Plugin Dependencies in pytest (tests/subpackage/test_subpackage.py)
DESCRIPTION: This snippet from `tests/subpackage/test_subpackage.py` defines the `inner` fixture, which appends 'inner subpackage' to `order` and depends on `order`, `mid`, and `a_fix` (a plugin fixture). The `test_order` function asserts the final execution order, illustrating the complex interplay of local, `conftest.py`, and plugin-provided fixtures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_7

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def inner(order, mid, a_fix):
    order.append("inner subpackage")

def test_order(order, inner):
    assert order == ["b_fix", "mid subpackage", "a_fix", "inner subpackage"]
```

---

TITLE: JUnit XML Output with Test Suite Properties
DESCRIPTION: Shows the structure of the JUnit XML report including a `<properties>` section at the test suite level, containing properties added using the `record_testsuite_property` fixture.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_25

LANGUAGE: xml
CODE:

```
<testsuite name="pytest" errors="0" failures="0" skipped="0" tests="1" time="0.004">
  <properties>
    <property name="ARCH" value="PPC" />
    <property name="STORAGE_TYPE" value="CEPH" />
  </properties>
  <testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
    <properties>
      <property name="test_id" value="1501" />
    </properties>
  </testcase>
</testsuite>
```

---

TITLE: Defining Pytest Hook for Custom Marker Inspection (Python)
DESCRIPTION: This `conftest.py` snippet defines a `pytest_runtest_setup` hook, which is executed before each test. Inside the hook, it iterates through markers named 'my_marker' applied to the current test item and prints them to standard output. This demonstrates how to programmatically inspect and react to custom markers within a pytest plugin or configuration file.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_22

LANGUAGE: python
CODE:

```
# content of conftest.py
import sys


def pytest_runtest_setup(item):
    for marker in item.iter_markers(name="my_marker"):
        print(marker)
        sys.stdout.flush()
```

---

TITLE: Skipping All Test Functions in a Class with Pytest Mark Skipif (Python)
DESCRIPTION: This example illustrates applying the `pytest.mark.skipif` marker to an entire test class. If the condition specified in the decorator is `True`, all test methods within that class will be skipped, preventing their setup and execution, which is useful for platform-specific test classes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_6

LANGUAGE: python
CODE:

```
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls:
    def test_function(self):
        "will not be setup or run under 'win32' platform"
```

---

TITLE: Setting Faulthandler Timeout in pytest.ini
DESCRIPTION: This option configures `pytest` to dump tracebacks of all threads if a test exceeds a specified duration (in seconds), including fixture setup and teardown. It leverages `faulthandler.dump_traceback_later`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_24

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
faulthandler_timeout=5
```

---

TITLE: Disabling Plugin Autoload and Specifying Plugins in pytest.ini (INI)
DESCRIPTION: This INI configuration snippet illustrates how to persistently disable plugin autoloading and define specific plugins to be loaded within the `pytest.ini` file. Adding `--disable-plugin-autoload` and `-p NAME,NAME2` to `addopts` provides project-wide control over plugin behavior.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst#_snippet_7

LANGUAGE: ini
CODE:

```
[pytest]
addopts = --disable-plugin-autoload -p NAME,NAME2
```

---

TITLE: Configuring pytest Traceback Output (Bash)
DESCRIPTION: Examples of bash commands to configure how pytest prints tracebacks, including showing local variables, controlling output capture, and selecting different traceback formats.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest --showlocals     # show local variables in tracebacks
pytest -l               # show local variables (shortcut)
pytest --no-showlocals  # hide local variables (if addopts enables them)

pytest --capture=fd  # default, capture at the file descriptor level
pytest --capture=sys # capture at the sys level
pytest --capture=no  # don't capture
pytest -s            # don't capture (shortcut)
pytest --capture=tee-sys # capture to logs but also output to sys level streams

pytest --tb=auto    # (default) 'long' tracebacks for the first and last
                     # entry, but 'short' style for the other entries
pytest --tb=long    # exhaustive, informative traceback formatting
pytest --tb=short   # shorter traceback format
pytest --tb=line    # only one line per failure
pytest --tb=native  # Python standard library formatting
pytest --tb=no      # no traceback at all
```

---

TITLE: Disabling Plugin Autoload and Specifying Plugins via Command Line (Bash)
DESCRIPTION: This command-line example shows how to disable automatic plugin loading and explicitly specify plugins for a single pytest run. The `--disable-plugin-autoload` flag prevents default loading, and `-p NAME,NAME2` lists the plugins to be activated.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst#_snippet_6

LANGUAGE: bash
CODE:

```
pytest --disable-plugin-autoload -p NAME,NAME2
```

---

TITLE: Viewing Pytest Test Collection Tree (Console)
DESCRIPTION: This console output demonstrates how to use the `--collect-only` option to inspect Pytest's collection tree without actually running any tests. It provides a detailed view of discovered modules, classes, and functions, showing what Pytest would execute.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_12

LANGUAGE: console
CODE:

```
. $ pytest --collect-only pythoncollection.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
configfile: pytest.ini
collected 3 items

<Dir pythoncollection.rst-207>
  <Dir CWD>
    <Module pythoncollection.py>
      <Function test_function>
      <Class TestClass>
        <Function test_method>
        <Function test_anothermethod>

======================== 3 tests collected in 0.12s ========================
```

---

TITLE: Pytest Failure Traceback with PEP 657 Context
DESCRIPTION: This snippet demonstrates a pytest failure traceback using the enhanced `short` or `long` style, which includes partial PEP 657 support. It highlights the exact expressions (`^^^^^^^^^`) causing the `AttributeError` within the `manhattan_distance` function and the assertion, providing precise context for debugging.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/changelog/10224.improvement.rst#_snippet_0

LANGUAGE: pytest
CODE:

```
================================= FAILURES =================================
_______________________ test_gets_correct_tracebacks _______________________

test_tracebacks.py:12: in test_gets_correct_tracebacks
    assert manhattan_distance(p1, p2) == 1
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
test_tracebacks.py:6: in manhattan_distance
    return abs(point_1.x - point_2.x) + abs(point_1.y - point_2.y)
                           ^^^^^^^^^
E   AttributeError: 'NoneType' object has no attribute 'x'
```

---

TITLE: Customizing Pytest Log and Date Format (Bash)
DESCRIPTION: This command demonstrates how to customize the log message format and date format using command-line options. The `--log-format` and `--log-date-format` arguments accept standard Python logging module format strings, allowing for detailed control over log output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_2

LANGUAGE: bash
CODE:

```
pytest --log-format="%(asctime)s %(levelname)s %(message)s" \
            --log-date-format="%Y-%m-%d %H:%M:%S"
```

---

TITLE: Testing Substring Presence with Pytest (Failing)
DESCRIPTION: This Python function demonstrates a pytest test that asserts if a substring is present within a longer string. The failure output shows a simple AssertionError indicating that the substring was not found in the target string.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_6

LANGUAGE: python
CODE:

```
def test_long_text_fail():
    long_text = "Lorem ipsum dolor sit amet " * 10
    assert "hello world" in long_text
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command utilizes the pip package installer to upgrade an existing pytest installation to the latest available version, specifically 8.3.1 in this context. It ensures that users receive the most recent bug fixes and improvements.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.3.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Running Pytest (CLI)
DESCRIPTION: Shows a basic command-line execution of pytest in an empty directory, demonstrating the default output when no tests are collected.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_14

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 0 items

========================== no tests ran in 0.12s ===========================
```

---

TITLE: Overriding 'innermost' Fixture and 'test_order' in pytest (tests/subpackage/test_subpackage.py)
DESCRIPTION: This snippet from `tests/subpackage/test_subpackage.py` defines an `innermost` fixture that overrides a higher-scoped one, appending 'innermost subpackage' to `order`. The `test_order` function asserts the final execution order, demonstrating fixture overriding and scope resolution in subpackages.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_4

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def innermost(order, mid):
    order.append("innermost subpackage")

def test_order(order, top):
    assert order == ["mid subpackage", "innermost subpackage", "top"]
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This command upgrades the pytest testing framework to its latest available version on PyPI using the pip package installer. It's a standard procedure to ensure you have the most recent bug fixes and features.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-6.2.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Passing Data to Pytest Fixtures Using Markers (Python)
DESCRIPTION: This example illustrates how to pass data from a test function to a `pytest` fixture using markers. The `fixt` fixture accesses the `request` object to retrieve data from the `fixt_data` marker applied to `test_fixt`. This allows dynamic configuration of fixtures based on specific test requirements.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_35

LANGUAGE: python
CODE:

```
import pytest


@pytest.fixture
def fixt(request):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        # Handle missing marker in some way...
        data = None
    else:
        data = marker.args[0]

    # Do something with the data
    return data


@pytest.mark.fixt_data(42)
def test_fixt(fixt):
    assert fixt == 42
```

---

TITLE: pytest Command Line Build Order
DESCRIPTION: Illustrates the order in which command line arguments are combined from `pytest.ini`, the `PYTEST_ADDOPTS` environment variable, and explicit command line arguments.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_2

LANGUAGE: text
CODE:

```
<pytest.ini:addopts> $PYTEST_ADDOPTS <extra command-line arguments>
```

---

TITLE: Testing Missing User Configuration Error Handling (Python)
DESCRIPTION: This test ensures that `app.create_connection_string()` raises a `KeyError` when the `user` configuration is missing, as simulated by the `mock_missing_default_user` fixture. It uses `pytest.raises` to assert the exception.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/monkeypatch.rst#_snippet_16

LANGUAGE: Python
CODE:

```
def test_missing_user(mock_missing_default_user):
    with pytest.raises(KeyError):
        _ = app.create_connection_string()
```

---

TITLE: Parametrizing Pytest Test Methods via Class Configuration
DESCRIPTION: This Python code demonstrates how to parametrize test methods within a class using a pytest_generate_tests hook and a class-level params dictionary. The pytest_generate_tests function dynamically generates test arguments based on the params defined for each test method, allowing for flexible and structured parametrization.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_17

LANGUAGE: python
CODE:

```
# content of ./test_parametrize.py
import pytest


def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


class TestClass:
    # a map specifying multiple argument sets for a test method
    params = {
        "test_equals": [dict(a=1, b=2), dict(a=3, b=3)],
        "test_zerodivision": [dict(a=1, b=0)]
    }

    def test_equals(self, a, b):
        assert a == b

    def test_zerodivision(self, a, b):
        with pytest.raises(ZeroDivisionError):
            a / b
```

---

TITLE: Illustrating Pytest's Default Collection of Imported Classes in Python
DESCRIPTION: This snippet demonstrates pytest's default behavior where it collects classes like `Testament` even when imported into a test module (`tests/test_testament.py`) from a production module (`src/domain.py`). This occurs because the class name starts with 'Test', fulfilling pytest's default collection rules. It sets up a scenario to explain why `collect_imported_tests` is needed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/changelog/12749.feature.rst#_snippet_0

LANGUAGE: Python
CODE:

```
# contents of src/domain.py
class Testament: ...


# contents of tests/test_testament.py
from domain import Testament


def test_testament(): ...
```

---

TITLE: Using pytest.set_trace() for Quick Debugging
DESCRIPTION: Highlights `pytest.set_trace()` as a convenient shortcut for invoking the Python debugger. This function directly sets a breakpoint at its call site, simplifying the process of entering an interactive debugging session during test execution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.4.0.rst#_snippet_6

LANGUAGE: Python
CODE:

```
pytest.set_trace()
```

---

TITLE: Installing/Upgrading pytest via pip
DESCRIPTION: This command demonstrates how to install or upgrade the pytest testing framework using pip, the standard package installer for Python. The `-U` flag ensures that the package is updated to the latest available version from PyPI.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.8.6.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Displaying Pytest Command-line Help
DESCRIPTION: Shows all available command-line flags and options for pytest, including general options, test selection filters, debugging tools, and output capture methods. This provides a comprehensive overview of how to customize pytest execution from the command line.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_62

LANGUAGE: bash
CODE:

```
$ pytest --help
usage: pytest [options] [file_or_dir] [file_or_dir] [...]

positional arguments:
  file_or_dir

general:
  -k EXPRESSION         Only run tests which match the given substring
                        expression. An expression is a Python evaluable
                        expression where all names are substring-matched
                        against test names and their parent classes.
                        Example: -k 'test_method or test_other' matches all
                        test functions and classes whose name contains
                        'test_method' or 'test_other', while -k 'not
                        test_method' matches those that don't contain
                        'test_method' in their names. -k 'not test_method
                        and not test_other' will eliminate the matches.
                        Additionally keywords are matched to classes and
                        functions containing extra names in their
                        'extra_keyword_matches' set, as well as functions
                        which have names assigned directly to them. The
                        matching is case-insensitive.
  -m MARKEXPR           Only run tests matching given mark expression. For
                        example: -m 'mark1 and not mark2'.
  --markers             show markers (builtin, plugin and per-project ones).
  -x, --exitfirst       Exit instantly on first error or failed test
  --fixtures, --funcargs
                        Show available fixtures, sorted by plugin appearance
                        (fixtures with leading '_' are only shown with '-v')
  --fixtures-per-test   Show fixtures per test
  --pdb                 Start the interactive Python debugger on errors or
                        KeyboardInterrupt
  --pdbcls=modulename:classname
                        Specify a custom interactive Python debugger for use
                        with --pdb.For example:
                        --pdbcls=IPython.terminal.debugger:TerminalPdb
  --trace               Immediately break when running each test
  --capture=method      Per-test capturing method: one of fd|sys|no|tee-sys
  -s                    Shortcut for --capture=no
  --runxfail            Report the results of xfail tests as if they were
                        not marked
  --lf, --last-failed   Rerun only the tests that failed at the last run (or
                        all if none failed)
  --ff, --failed-first  Run all tests, but run the last failures first. This
                        may re-order tests and thus lead to repeated fixture
```

---

TITLE: Autouse Fixtures Across Multiple Scopes in pytest (Python)
DESCRIPTION: This example highlights the behavior of `autouse` fixtures when multiple scopes are involved. An `autouse` fixture will execute for every test that can reach it, even if not explicitly requested, demonstrating its broad impact within its defined scope and any nested scopes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_11

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture(scope="module", autouse=True)
def c1():
    print("fixture c1 (module-scoped, autouse)")
    return "c1_data"

@pytest.fixture
def f1():
    print("fixture f1")
    return "f1_data"

class TestClassWithC1Request:
    def test_one(self, c1):
        print("TestClassWithC1Request.test_one executed")
        assert c1 == "c1_data"

class TestClassWithoutC1Request:
    def test_two(self):
        print("TestClassWithoutC1Request.test_two executed")
        assert True

    def test_three(self, f1):
        print("TestClassWithoutC1Request.test_three executed")
        assert f1 == "f1_data"
```

---

TITLE: Verifying pytest Installation Version
DESCRIPTION: This command executes pytest with the --version flag to display the currently installed pytest version. It's a critical step post-installation to confirm successful setup and to identify the exact version being used.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/getting-started.rst#_snippet_1

LANGUAGE: bash
CODE:

```
$ pytest --version
```

---

TITLE: Configuring Pytest Last Failed Behavior with Bash
DESCRIPTION: This snippet demonstrates how to use the --last-failed-no-failures option with pytest to control behavior when no tests failed in the previous run. The 'all' option runs the full test suite, while 'none' causes pytest to exit successfully without running any tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_4

LANGUAGE: bash
CODE:

```
pytest --last-failed --last-failed-no-failures all    # runs the full test suite (default behavior)
pytest --last-failed --last-failed-no-failures none   # runs no tests and exits successfully
```

---

TITLE: Installing or Upgrading pytest (Shell)
DESCRIPTION: Instructions for installing or upgrading the pytest testing framework using either pip or easy_install. The '-U' flag ensures that the package is upgraded if it is already installed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

LANGUAGE: Shell
CODE:

```
easy_install -U pytest
```

---

TITLE: Invoking Pytest Programmatically with Explicit Arguments
DESCRIPTION: This snippet demonstrates how to programmatically invoke pytest using `pytest.main()` while explicitly passing command-line options and arguments as a list of strings. In this example, `-x` stops the test run on the first failure, and `mytestdir` specifies the directory to test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_18

LANGUAGE: python
CODE:

```
retcode = pytest.main(["-x", "mytestdir"])
```

---

TITLE: Specifying Minimum Pytest Version (INI)
DESCRIPTION: Specifies the minimal pytest version required for running tests in the project. If the current pytest version installed is below this threshold, pytest will fail, ensuring compatibility and preventing unexpected behavior.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_43

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
minversion = 3.0  # will fail if we run with pytest-2.8
```

---

TITLE: Running Pytest Tests from CLI
DESCRIPTION: This snippet demonstrates how to execute a specific test file using the pytest command-line interface. The `-q` flag enables quiet mode, showing minimal output. It illustrates the successful execution of one test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_27

LANGUAGE: pytest
CODE:

```
$ pytest -q test_emaillib.py
.                                                                    [100%]
1 passed in 0.12s
```

---

TITLE: pytest Test Function Using Command Line Option Fixture (test_sample.py)
DESCRIPTION: Defines a test function that accepts a `cmdopt` fixture, demonstrating how to use a command line option value within a test. The assert 0 is included to show the printed output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_5

LANGUAGE: python
CODE:

```
# content of test_sample.py
def test_answer(cmdopt):
    if cmdopt == "type1":
        print("first")
    elif cmdopt == "type2":
        print("second")
    assert 0  # to see what was printed
```

---

TITLE: Module Level Setup/Teardown in Pytest
DESCRIPTION: These methods are called once for all test functions and classes within a single module. `setup_module` is executed before any tests in the module, and `teardown_module` after all tests in the module have completed. The `module` parameter is optional since pytest-3.0.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst#_snippet_0

LANGUAGE: python
CODE:

```
def setup_module(module):
    """setup any state specific to the execution of the given module."""


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
```

---

TITLE: Disabling Collection of Imported Tests in Pytest (INI)
DESCRIPTION: Configures `collect_imported_tests` to `false` in `pytest.ini`. This setting prevents pytest from collecting test classes or functions that are imported into a test file, ensuring only definitions within the file are considered for test collection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_19

LANGUAGE: ini
CODE:

```
[pytest]
collect_imported_tests = false
```

---

TITLE: Method Level Setup/Teardown in Pytest Classes
DESCRIPTION: These methods are called around each test method invocation within a class. `setup_method` is executed before each test method, and `teardown_method` after each test method. The `method` parameter is optional since pytest-3.0.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/xunit_setup.rst#_snippet_2

LANGUAGE: python
CODE:

```
def setup_method(self, method):
    """setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
    """


def teardown_method(self, method):
    """teardown any state that was previously setup with a setup_method
        call.
    """
```

---

TITLE: Defining 'top' Fixture in pytest (tests/test_top.py)
DESCRIPTION: This pytest fixture, defined in `tests/test_top.py`, appends the string 'top' to the `order` list. It demonstrates a basic fixture definition and its dependency on `order` and `innermost` fixtures for execution order tracking.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_1

LANGUAGE: Python
CODE:

```
@pytest.fixture
def top(order, innermost):
    order.append("top")
```

---

TITLE: Running Pytest and Observing Failures
DESCRIPTION: Executes pytest on `test_module.py` which contains failing tests. The output shows the test session summary, the list of collected items, the progress indicator ('FF' for two failures), detailed failure reports for each test, and a final summary of failed tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_41

LANGUAGE: bash
CODE:

```
$ pytest test_module.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py FF                                                    [100%]

================================= FAILURES =================================
________________________________ test_fail1 ________________________________

tmp_path = PosixPath('PYTEST_TMPDIR/test_fail10')

    def test_fail1(tmp_path):
>       assert 0
E       assert 0

test_module.py:2: AssertionError
________________________________ test_fail2 ________________________________

    def test_fail2():
>       assert 0
E       assert 0

test_module.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_module.py::test_fail1 - assert 0
FAILED test_module.py::test_fail2 - assert 0
============================ 2 failed in 0.12s =============================
```

---

TITLE: Add pytest Command Line Option with Choices (conftest.py)
DESCRIPTION: Modifies the `pytest_addoption` definition to include the `choices` parameter, restricting the allowed values for the `--cmdopt` option and providing basic validation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_9

LANGUAGE: python
CODE:

```
# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt",
        action="store",
        default="type1",
        help="my option: type1 or type2",
        choices=("type1", "type2"),
    )
```

---

TITLE: Testing Global `username` Fixture Usage
DESCRIPTION: This test function `test_username` demonstrates the consumption of the globally defined `username` fixture. It asserts that the value provided by the fixture is 'username', confirming the base fixture's functionality.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_61

LANGUAGE: undefined
CODE:

```
undefined
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades the pytest package to the latest version available on PyPI using the pip package installer. It ensures that the current pytest installation is replaced with the specified version (or the newest if not specified). This is a common prerequisite for using new features or bug fixes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.3.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Configuring Pytest to Discover All Python Files (INI)
DESCRIPTION: This INI configuration instructs Pytest to discover tests from every Python file (`*.py`) in the project. While convenient, this broad setting might include files like `setup.py` that are not intended for testing, requiring further exclusion rules.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_13

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
python_files = *.py
```

---

TITLE: Collecting Parametrized Test IDs with --collect-only (pytest CLI)
DESCRIPTION: This command-line snippet demonstrates using `pytest --collect-only` to inspect the generated test IDs for the `test_time.py` file. It shows how pytest constructs IDs, including those customized by `idfn` or explicit `ids` lists, which is useful for debugging and selecting specific test cases.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_5

LANGUAGE: pytest
CODE:

```
$ pytest test_time.py --collect-only
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 8 items
```

---

TITLE: Loading pytest Plugins via `PYTEST_PLUGINS` (Bash)
DESCRIPTION: This snippet illustrates how to load additional `pytest` plugins using the `PYTEST_PLUGINS` environment variable. Plugins specified as a comma-separated list (e.g., `mymodule.plugin,xdist`) will be automatically loaded at the start of the pytest session, extending its functionality.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_15

LANGUAGE: bash
CODE:

```
export PYTEST_PLUGINS=mymodule.plugin,xdist
```

---

TITLE: Invoking pytest from Python Interpreter (Shell)
DESCRIPTION: This command shows how to run pytest directly using the Python interpreter's module execution feature, available for Python versions 2.5 and above. It's a standard and recommended way to execute installed Python packages from the command line.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.0.0.rst#_snippet_1

LANGUAGE: Shell
CODE:

```
python -m pytest
```

---

TITLE: Unconditionally Skipping All Tests in a Pytest Module
DESCRIPTION: This snippet shows how to skip all tests within a module unconditionally by setting `pytestmark` to `pytest.mark.skip` with a reason. This is useful for work-in-progress modules.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_10

LANGUAGE: python
CODE:

```
pytestmark = pytest.mark.skip("all tests still WIP")
```

---

TITLE: Displaying Detailed Pytest Skip/Xfail/Xpass Information (Bash)
DESCRIPTION: This snippet shows how to use the `-r` option with the `pytest` command to display detailed information about xfailed, xpassed, and skipped tests in the test session summary. This helps in debugging and understanding why certain tests were not run or failed as expected, without cluttering the default output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest -rxXs  # show extra info on xfailed, xpassed, and skipped tests
```

---

TITLE: Disabling Specific Loggers in Pytest (Bash)
DESCRIPTION: This command shows how to disable specific loggers during a pytest run using the `--log-disable` option. This argument can be passed multiple times to disable multiple loggers, preventing their messages from being captured and displayed.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_5

LANGUAGE: bash
CODE:

```
pytest --log-disable=main --log-disable=testing
```

---

TITLE: Handling Duplicate Test Module Names with **init**.py (Text)
DESCRIPTION: This snippet illustrates a directory structure workaround for `pytest`'s `prepend` import mode when test modules have identical names. By adding `__init__.py` files to the `tests` directory and its subfolders (`foo`, `bar`), they are treated as Python packages. This allows `pytest` to import `test_view.py` as `tests.foo.test_view` and `tests.bar.test_view`, resolving potential naming conflicts.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_8

LANGUAGE: text
CODE:

```
pyproject.toml
mypkg/
	...
tests/
	__init__.py
	foo/
		__init__.py
		test_view.py
	bar/
		__init__.py
		test_view.py
```

---

TITLE: Configuring Pytest Python Search Path (INI)
DESCRIPTION: This configuration sets `pythonpath` to `src1 src2`, adding these directories to the Python search path (`sys.path`) for the duration of the test session. Paths are relative to the project's root directory. This is similar to the `PYTHONPATH` environment variable, allowing Python to find imported modules within these specified directories.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_49

LANGUAGE: ini
CODE:

```
[pytest]
pythonpath = src1 src2
```

---

TITLE: Recommended Pytest Hook Configuration with hookimpl
DESCRIPTION: This Python code shows the recommended way to configure pytest hooks using the `@pytest.hookimpl` decorator. Hook attributes like `tryfirst` are now passed as keyword arguments to the decorator, providing a more explicit and structured API for hook implementations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_3

LANGUAGE: Python
CODE:

```
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(): ...
```

---

TITLE: Excluding Test Paths with Glob Patterns using `collect_ignore_glob` in Pytest (Python)
DESCRIPTION: This snippet illustrates the use of the `collect_ignore_glob` global variable in `conftest.py` to exclude test directories or modules using Unix shell-style wildcards. It requires a list of strings, where each string can contain glob patterns. The example shows excluding files ending with `_ignore.py`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_10

LANGUAGE: Python
CODE:

```
collect_ignore_glob = ["*_ignore.py"]
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the specified version (or latest available) using the pip package installer. It ensures all dependencies are also updated to compatible versions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.1.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command line snippet demonstrates how to upgrade an existing pytest installation to the latest version using the pip package manager. The `--upgrade` flag ensures that pip replaces the current version with the newest available one.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-5.2.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Defining Tests for Fixture Finalizer Example
DESCRIPTION: Defines tests in `test_module.py` to be used with the `conftest.py` plugin. It includes a fixture `other` that fails during setup, a test `test_setup_fails` that uses this fixture, a test `test_call_fails` that fails during the call phase, and another failing test `test_fail2`, all designed to trigger different failure scenarios.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_44

LANGUAGE: python
CODE:

```
# content of test_module.py

import pytest


@pytest.fixture
def other():
    assert 0


def test_setup_fails(something, other):
    pass


def test_call_fails(something):
    assert 0


def test_fail2():
    assert 0
```

---

TITLE: Initializing 'order' Fixture in pytest (tests/conftest.py)
DESCRIPTION: This pytest fixture, defined in the top-level `tests/conftest.py`, initializes and returns an empty list. This `order` list serves as a shared mutable object across tests and fixtures to track the sequence of fixture execution, crucial for understanding dependency resolution.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/fixtures.rst#_snippet_5

LANGUAGE: Python
CODE:

```
import pytest

@pytest.fixture
def order():
    return []
```

---

TITLE: Verifying Specific Indirect Parametrization Test Run
DESCRIPTION: This snippet shows the successful pytest output when running test_indirect_list.py. It confirms that the test test_indirect[a-b] passed, demonstrating that the indirect parametrization was correctly applied only to the x argument, resulting in x being "aaa" and y being "b".
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_16

LANGUAGE: pytest
CODE:

```
$ pytest -v test_indirect_list.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 1 item

test_indirect_list.py::test_indirect[a-b] PASSED                     [100%]

============================ 1 passed in 0.12s =============================
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command upgrades the pytest package to the latest version available on PyPI using pip, the Python package installer. The -U flag ensures that existing installations are updated to the newest version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.7.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command line instruction uses pip, the Python package installer, to upgrade an existing pytest installation to the latest available version. The '--upgrade' flag ensures that pytest and its dependencies are updated.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.6.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Configuring pytest Plugin Entry Point in pyproject.toml
DESCRIPTION: This TOML configuration defines a `pytest11` entry point in `pyproject.toml`, making the `myproject.pluginmodule` discoverable by pytest. It also includes build system requirements and Pytest framework classifiers for PyPI, ensuring proper packaging and categorization.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_2

LANGUAGE: TOML
CODE:

```
# sample ./pyproject.toml file
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
classifiers = [
    "Framework :: Pytest",
]

[project.entry-points.pytest11]
myproject = "myproject.pluginmodule"
```

---

TITLE: Creating Stash Keys for pytest Items in Python
DESCRIPTION: This snippet shows how to define `pytest.StashKey` instances at the top level of a plugin. These keys provide a type-safe and conflict-free mechanism for storing and retrieving arbitrary data on `pytest.Item` objects, addressing issues that arise from directly assigning private attributes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst#_snippet_11

LANGUAGE: Python
CODE:

```
been_there_key = pytest.StashKey[bool]()
done_that_key = pytest.StashKey[str]()
```

---

TITLE: Applying a Single Pytest Marker at Module Level in Python
DESCRIPTION: This example shows how to apply a single pytest marker to all tests within a module using the `pytestmark` global variable. All tests in this module will be marked as `webtest`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_13

LANGUAGE: Python
CODE:

```
import pytest
pytestmark = pytest.mark.webtest
```

---

TITLE: Running Pytest with -ra Reporting (pytest)
DESCRIPTION: This snippet shows the command `pytest -ra` and its output when run against the example test file. The `-ra` flag instructs pytest to display a short summary report at the end, including all test outcomes except standard passes, highlighting failures, errors, skips, xfails, and xpasses.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_8

LANGUAGE: pytest
CODE:

```
$ pytest -ra
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
================================= XPASSES ==================================
========================= short test summary info ==========================
SKIPPED [1] test_example.py:22: skipping this test
XFAIL test_example.py::test_xfail - reason: xfailing this test
XPASS test_example.py::test_xpass - always xfail
ERROR test_example.py::test_error - assert 0
FAILED test_example.py::test_fail - assert 0
== 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12s ===
```

---

TITLE: Running Tests from Python Packages (Bash)
DESCRIPTION: This command imports the specified Python package (e.g., 'pkg.testing') and then uses its filesystem location to discover and execute tests contained within it. This is useful for running tests in installed packages.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_9

LANGUAGE: bash
CODE:

```
pytest --pyargs pkg.testing
```

---

TITLE: Demonstrating Unsafe Teardown with Single Yield Fixture (Python)
DESCRIPTION: This Python code presents a `pytest` fixture that consolidates multiple setup steps and a single teardown using `yield`. While compact, this approach is less robust; if an exception occurs during any of the setup steps before `yield`, the teardown code will not execute, potentially leading to resource leaks. It highlights the importance of safe teardown practices.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_26

LANGUAGE: python
CODE:

```
# content of test_emaillib.py
from emaillib import Email, MailAdminClient

import pytest


@pytest.fixture
def setup():
    mail_admin = MailAdminClient()
    sending_user = mail_admin.create_user()
    receiving_user = mail_admin.create_user()
    email = Email(subject="Hey!", body="How's it going?")
    sending_user.send_email(email, receiving_user)
    yield receiving_user, email
    receiving_user.clear_mailbox()
    mail_admin.delete_user(sending_user)
    mail_admin.delete_user(receiving_user)


def test_email_received(setup):
    receiving_user, email = setup
    assert email in receiving_user.inbox
```

---

TITLE: Configuring Captured Log Format in Pytest (INI)
DESCRIPTION: Sets a `logging`-compatible string used to format all captured logging messages, regardless of their destination (console or file). This provides a global format for how log entries appear.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_40

LANGUAGE: ini
CODE:

```
[pytest]
log_format = %(asctime)s %(levelname)s %(message)s
```

---

TITLE: Running XFAIL Tests from Pytest Command Line
DESCRIPTION: This snippet shows the command-line option `--runxfail` for Pytest. When used, tests marked as XFAIL will be executed and reported as regular tests, ignoring their XFAIL status.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_22

LANGUAGE: bash
CODE:

```
pytest --runxfail
```

---

TITLE: Enabling the pytest Pytester Plugin (Python)
DESCRIPTION: This snippet shows how to enable the `pytester` plugin, which is essential for writing tests for pytest plugin code. By adding `pytester` to the `pytest_plugins` list in a `conftest.py` file, the `pytester` fixture becomes available for use in tests. Alternatively, it can be enabled via the command line using `-p pytester`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_8

LANGUAGE: Python
CODE:

```
# content of conftest.py

pytest_plugins = ["pytester"]
```

---

TITLE: Verifying `usefixtures` Application (Pytest CLI)
DESCRIPTION: This Pytest CLI command runs tests in quiet mode (`-q`). The output `..` followed by `2 passed` confirms that both test methods within `TestDirectoryInit` were executed successfully, implying that the `cleandir` fixture was correctly applied via the `usefixtures` marker, ensuring a clean directory for each test.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_55

LANGUAGE: pytest
CODE:

```
$ pytest -q
..                                                                   [100%]
2 passed in 0.12s
```

---

TITLE: Running Pytest with Slow Tests Included (CLI)
DESCRIPTION: Shows the command-line execution of pytest with the `--runslow` option, demonstrating that the test marked `slow` is now executed instead of being skipped.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_18

LANGUAGE: pytest
CODE:

```
$ pytest --runslow
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 2 items

test_module.py ..                                                    [100%]

============================ 2 passed in 0.12s =============================
```

---

TITLE: Installing Tox Test Runner
DESCRIPTION: This command installs `tox` using pip. Tox is a command-line tool that automates testing in isolated virtual environments, ensuring consistent test execution across different Python versions and dependencies.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst#_snippet_11

LANGUAGE: Shell
CODE:

```
pip install tox
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades the pytest package to its latest version (3.6.4 as per the announcement) using pip, the Python package installer. The '--upgrade' flag ensures that if pytest is already installed, it will be updated to the specified or latest available version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.6.4.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Marking a Pytest Function as XFAIL with Expected Exception
DESCRIPTION: This snippet shows how to use the `raises` parameter with `@pytest.mark.xfail` to specify the expected exception type(s) for a test to be marked XFAIL. If the test fails with a different exception, it will be reported as a regular failure.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_18

LANGUAGE: python
CODE:

```
@pytest.mark.xfail(raises=RuntimeError)
def test_function(): ...
```

---

TITLE: Defining Pytest Environment Marker in Test File (Python)
DESCRIPTION: This snippet shows how to define an environment-specific marker using `@pytest.mark.env` on a test function. The test `test_basic_db_operation` is marked to run only when the environment is 'stage1'. This helps in organizing tests that are relevant only to specific deployment stages or configurations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_18

LANGUAGE: python
CODE:

```
# content of test_someenv.py

import pytest


@pytest.mark.env("stage1")
def test_basic_db_operation():
    pass
```

---

TITLE: Enabling Pytester Fixture in Pytest
DESCRIPTION: This snippet demonstrates how to enable the `pytester` fixture in a pytest project. By adding `pytest_plugins = "pytester"` to the topmost `conftest.py` file, the `pytester` instance becomes available, providing an isolated directory and utilities for testing pytest itself.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_8

LANGUAGE: Python
CODE:

```
pytest_plugins = "pytester"
```

---

TITLE: Applying Indirect Parametrization to Specific Arguments in Pytest
DESCRIPTION: This Python example illustrates how to apply indirect parametrization to only specific arguments when multiple arguments are used. The indirect=["x"] parameter ensures that only the x fixture processes its value via request.param, while y receives its value directly.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_15

LANGUAGE: python
CODE:

```
# content of test_indirect_list.py

import pytest


@pytest.fixture(scope="function")
def x(request):
    return request.param * 3


@pytest.fixture(scope="function")
def y(request):
    return request.param * 2


@pytest.mark.parametrize("x, y", [("a", "b")], indirect=["x"])
def test_indirect(x, y):
    assert x == "aaa"
    assert y == "b"
```

---

TITLE: Configuring Pytest Test File Collection (INI, Single Line)
DESCRIPTION: This configuration sets `python_files` to `test_*.py check_*.py example_*.py`, instructing pytest to consider Python files matching these glob patterns as test modules. Multiple patterns are separated by spaces. By default, files matching `test_*.py` and `*_test.py` are considered test modules.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_46

LANGUAGE: ini
CODE:

```
[pytest]
python_files = test_*.py check_*.py example_*.py
```

---

TITLE: Configuring Pytest Test Class Collection (INI)
DESCRIPTION: This configuration sets `python_classes` to `*Suite`, instructing pytest to collect tests from classes whose names end with "Suite". By default, pytest collects classes prefixed with "Test". This option allows customizing which classes are considered for test collection, supporting glob-style patterns. `unittest.TestCase` derived classes are always collected regardless of this option.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_45

LANGUAGE: ini
CODE:

```
[pytest]
python_classes = *Suite
```

---

TITLE: Declaring a Custom Pytest Hook in Python
DESCRIPTION: This snippet demonstrates how to declare a new pytest hook. Hooks are defined as do-nothing functions starting with `pytest_` and include documentation describing their purpose and expected return values. This specific hook receives the `config` object.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst#_snippet_3

LANGUAGE: Python
CODE:

```
def pytest_my_hook(config):
    """
    Receives the pytest config and does things with it
    """
```

---

TITLE: Configuring pytest to Permanently Enable Docstring Doctests
DESCRIPTION: This INI configuration snippet shows how to permanently enable the `--doctest-modules` option for `pytest` within the `pytest.ini` file. By adding `addopts = --doctest-modules` under the `[pytest]` section, doctests in docstrings will always be collected without needing to specify the option on the command line.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst#_snippet_5

LANGUAGE: ini
CODE:

```
# content of pytest.ini
[pytest]
addopts = --doctest-modules
```

---

TITLE: Running Pytest for Standalone Test Module Discovery (Bash)
DESCRIPTION: This `bash` command executes `pytest` from the `root/` directory. For test modules or `conftest.py` files not part of a Python package (i.e., lacking `__init__.py` in their directory), `pytest` adds their immediate directory to `sys.path`. This imports them directly by their filename, which means modules with identical names across different standalone directories will clash in the global import namespace.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/pythonpath.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pytest root/
```

---

TITLE: Defining a Pytest Session-Scoped Fixture in Python
DESCRIPTION: This Python snippet defines a `pytest` session-scoped fixture named `callattr_ahead_of_alltests` in `conftest.py`. Configured with `autouse=True`, it automatically runs once per test session before any tests. It iterates through all collected test items, identifies their parent test classes, and if a class defines a `callme` method, it invokes that method. This allows for pre-test setup or inspection across all test classes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/special.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of conftest.py

import pytest


@pytest.fixture(scope="session", autouse=True)
def callattr_ahead_of_alltests(request):
    print("callattr_ahead_of_alltests called")
    seen = {None}
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        if cls not in seen:
            if hasattr(cls.obj, "callme"):
                cls.obj.callme()
            seen.add(cls)
```

---

TITLE: Running Multiple Pytest Tests by Node ID
DESCRIPTION: This pytest command-line example illustrates how to execute multiple specific tests by listing their node IDs as positional arguments. This allows for running a combination of individual test functions and entire test classes in a single command.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_6

LANGUAGE: pytest
CODE:

```
$ pytest -v test_server.py::TestClass test_server.py::test_send_http
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
cachedir: .pytest_cache
rootdir: /home/sweet/project
collecting ... collected 2 items

test_server.py::TestClass::test_method PASSED                        [ 50%]
test_server.py::test_send_http PASSED                                [100%]
```

---

TITLE: Deactivating a pytest Plugin via Command Line (Bash)
DESCRIPTION: This bash command demonstrates how to prevent a specific plugin from loading or unregister it for the current pytest run. The `-p no:NAME` option ensures that the named plugin will not be activated, even if subsequently requested.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/plugins.rst#_snippet_3

LANGUAGE: bash
CODE:

```
pytest -p no:NAME
```

---

TITLE: Marking Test as XFAIL with Specific Exception (Python)
DESCRIPTION: Illustrates how to use `pytest.mark.xfail` with the `raises` parameter. This ensures that a test is only marked as 'xfail' if it fails by raising the specified exception (or a subclass), providing more specific documentation for known bugs.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_16

LANGUAGE: Python
CODE:

```
def f():
    raise IndexError()


@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()
```

---

TITLE: Deprecating `pytest.main()` with String Arguments in Pytest
DESCRIPTION: This snippet highlights the deprecation of passing a single command-line string to `pytest.main()` in Pytest 4.0. It recommends passing a list of arguments instead (e.g., `["-v", "-s"]`) to ensure portable interpretation of command-line options across different shells.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_35

LANGUAGE: python
CODE:

```
pytest.main("-v -s")
```

LANGUAGE: python
CODE:

```
pytest.main(["-v", "-s"])
```

---

TITLE: Running Pytest with -rpP flags (pytest)
DESCRIPTION: Demonstrates running pytest with the `-r pP` flags to show passing tests and passing tests with captured output. The output includes test summary, errors, failures, and passes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_10

LANGUAGE: bash
CODE:

```
$ pytest -rpP
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
================================= FAILURES =================================
________________________________ test_fail _________________________________

    def test_fail():
>       assert 0
E       assert 0

test_example.py:14: AssertionError
================================== PASSES ==================================
_________________________________ test_ok __________________________________
--------------------------- Captured stdout call ---------------------------
ok
========================= short test summary info ==========================
PASSED test_example.py::test_ok
== 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12s ===
```

---

TITLE: Running Pytest with -rfs Reporting (pytest)
DESCRIPTION: This snippet demonstrates using the `pytest -rfs` command. The `-rfs` flag filters the short summary report to show only failed (`f`) and skipped (`s`) test outcomes, illustrating how multiple characters can be combined with the `-r` option.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_9

LANGUAGE: pytest
CODE:

```
$ pytest -rfs
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 6 items

test_example.py .FEsxX                                               [100%]

================================== ERRORS ==================================
_______________________ ERROR at setup of test_error _______________________

    @pytest.fixture
    def error_fixture():
>       assert 0
E       assert 0

test_example.py:6: AssertionError
```

---

TITLE: Excluding Test Paths with `collect_ignore` in Pytest (Python)
DESCRIPTION: This snippet demonstrates how to use the `collect_ignore` global variable in `conftest.py` files to exclude specific test directories or modules from collection. It expects a list of string paths, `pathlib.Path` objects, or any `os.PathLike` objects. The example shows excluding `setup.py`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_9

LANGUAGE: Python
CODE:

```
collect_ignore = ["setup.py"]
```

---

TITLE: Clearing Captured Log Records with caplog (Python)
DESCRIPTION: This Python snippet shows how to clear previously captured log records using `caplog.clear()`. This is useful when you need to isolate log capturing to specific parts of a test, ensuring that assertions only apply to logs generated after the clear operation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_13

LANGUAGE: python
CODE:

```
def test_something_with_clearing_records(caplog):
        some_method_that_creates_log_records()
        caplog.clear()
        your_test_method()
        assert ["Foo"] == [rec.message for rec in caplog.records]
```

---

TITLE: Invoking pytest with specific directories (Bash)
DESCRIPTION: This Bash command demonstrates how to invoke pytest, specifying multiple directories (path/to/testdir and path/other/) from which to collect tests. Pytest will determine a common ancestor directory (path in this example) as the rootdir for configuration file searching.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/customize.rst#_snippet_5

LANGUAGE: bash
CODE:

```
pytest path/to/testdir path/other/
```

---

TITLE: Installing/Upgrading pytest via pip (Bash)
DESCRIPTION: This command upgrades or installs the pytest testing framework using pip, the Python package installer. The `-U` flag ensures that the package is upgraded to the latest version available on PyPI, or installed if not already present.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-2.9.1.rst#_snippet_0

LANGUAGE: Bash
CODE:

```
pip install -U pytest
```

---

TITLE: Observing Pytest addfinalizer Teardown Order (Pytest Shell)
DESCRIPTION: This shell command executes the `test_finalizers.py` file to observe the output of `addfinalizer` calls. The output confirms that `finalizer_1` is printed before `finalizer_2`, illustrating the first-in-last-out execution order for functions registered via `request.addfinalizer`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_25

LANGUAGE: pytest
CODE:

```
$ pytest -s test_finalizers.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_finalizers.py test_bar
.finalizer_1
finalizer_2


============================ 1 passed in 0.12s =============================
```

---

TITLE: Default pytest Output for Failing Tests (Console)
DESCRIPTION: Example console output from running pytest on the `test_verbosity_example.py` file without extra verbosity flags, showing the summary line, failure details, and assertion errors.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_3

LANGUAGE: console
CODE:

```
$ pytest --no-header
=========================== test session starts ============================
collected 4 items

test_verbosity_example.py .FFF                                       [100%]

================================= FAILURES =================================
_____________________________ test_words_fail ______________________________

    def test_words_fail():
        fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
        fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
>       assert fruits1 == fruits2
E       AssertionError: assert ['banana', 'a...elon', 'kiwi'] == ['banana', 'a...elon', 'kiwi']
E
E         At index 2 diff: 'grapes' != 'orange'
E         Use -v to get more diff

test_verbosity_example.py:8: AssertionError
____________________________ test_numbers_fail _____________________________

    def test_numbers_fail():
        number_to_text1 = {str(x): x for x in range(5)}
        number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
>       assert number_to_text1 == number_to_text2
E       AssertionError: assert {'0': 0, '1':..., '3': 3, ...} == {'0': 0, '10'...'30': 30, ...}
E
E         Omitting 1 identical items, use -vv to show
E         Left contains 4 more items:
E         {'1': 1, '2': 2, '3': 3, '4': 4}
E         Right contains 4 more items:
E         {'10': 10, '20': 20, '30': 30, '40': 40}
E         Use -v to get more diff

test_verbosity_example.py:14: AssertionError
___________________________ test_long_text_fail ____________________________

    def test_long_text_fail():
        long_text = "Lorem ipsum dolor sit amet " * 10
>       assert "hello world" in long_text
```

---

TITLE: Pytest raises OSError check (Python)
DESCRIPTION: Attempts to check if an `OSError` is raised when calling `int()` with a valid integer string '3' using pytest's `raises` helper. This example shows a test failure because no exception is raised, contrary to the expectation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_26

LANGUAGE: python
CODE:

```
raises(OSError, int, "3")
```

---

TITLE: Default Pytest Log Output Format
DESCRIPTION: This output snippet illustrates the default format for captured log messages, stdout, and stderr when tests fail in pytest. Each log message includes the module, line number, log level, and the message itself.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
----------------------- Captured stdlog call ----------------------
test_reporting.py    26 WARNING  text going to logger
----------------------- Captured stdout call ----------------------
text going to stdout
----------------------- Captured stderr call ----------------------
text going to stderr
==================== 2 failed in 0.02 seconds =====================
```

---

TITLE: Testing assertion with custom repr in pytest
DESCRIPTION: This test defines a class `JSON` with a custom `__repr__` method and an attribute `a=1`. It asserts that an instance's `a` attribute equals `b=2`, using the instance itself as the custom failure message. The assertion failed because 1 is not equal to 2, and the custom `__repr__` is shown in the failure output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_43

LANGUAGE: python
CODE:

```
def test_custom_repr(self):
    class JSON:
        a = 1

        def __repr__(self):
            return "This is JSON\n{\n  'foo': 'bar'\n}"

    a = JSON()
    b = 2
    assert a.a == b, a
```

---

TITLE: Second Pytest Run with Cached Fixture Output
DESCRIPTION: This snippet shows the output of a subsequent pytest run after the initial execution. The expensive_computation() is not printed, confirming that the mydata value was successfully retrieved from the pytest cache, demonstrating the persistence of cached data.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/cache.rst#_snippet_7

LANGUAGE: bash
CODE:

```
$ pytest -q
F                                                                    [100%]
================================= FAILURES =================================
______________________________ test_function _______________________________

mydata = 42

    def test_function(mydata):
>       assert mydata == 23
E       assert 42 == 23

test_caching.py:19: AssertionError
========================= short test summary info ==========================
FAILED test_caching.py::test_function - assert 42 == 23
1 failed in 0.12s
```

---

TITLE: Ensuring Only Specific Warnings are Issued in Python
DESCRIPTION: This example demonstrates how to use the `recwarn` fixture to ensure that only a specific warning (e.g., `UserWarning`) is issued during a test. It checks the total count of warnings and then pops the expected warning to verify its type.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_19

LANGUAGE: python
CODE:

```
def test_warning(recwarn):
    ...
    assert len(recwarn) == 1
    user_warning = recwarn.pop(UserWarning)
    assert issubclass(user_warning.category, UserWarning)
```

---

TITLE: Collecting Pytest Test IDs with `--collect-only`
DESCRIPTION: This snippet shows the output of running `pytest` with the `--collect-only` flag, which lists all discovered tests and their generated IDs without executing them. It specifically illustrates how `pytest` constructs test IDs for parametrized functions, such as `test_showhelo[smtp.gmail.com]` and `test_showhelo[mail.python.org]`, making it useful for verifying test collection and understanding the generated identifiers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_41

LANGUAGE: pytest
CODE:

```
$ pytest --collect-only
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 12 items

<Dir fixtures.rst-227>
  <Module test_anothersmtp.py>
    <Function test_showhelo[smtp.gmail.com]>
    <Function test_showhelo[mail.python.org]>
```

---

TITLE: Executing Pytest with Default Test Paths (Console)
DESCRIPTION: This command `pytest` executes pytest without any specific directories or files, relying on the `testpaths` configuration in the `pytest.ini` file. If `testpaths` is set to `testing doc`, this command will have the same effect as `pytest testing doc`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_52

LANGUAGE: console
CODE:

```
pytest
```

---

TITLE: Use Package-Scoped Fixture in Another Test (Python)
DESCRIPTION: Another test function `test_a2` in `a/test_db2.py` that also depends on the `db` fixture from `a/conftest.py`. It similarly asserts 0 to show the fixture value.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_35

LANGUAGE: python
CODE:

```
# content of a/test_db2.py
def test_a2(db):
    assert 0, db  # to show value
```

---

TITLE: Testing assertion with custom message in pytest
DESCRIPTION: This test defines a class `A` with attribute `a=1` and a variable `b=2`. It asserts that `A.a` equals `b` and provides a custom failure message. The assertion failed because 1 is not equal to 2.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_41

LANGUAGE: python
CODE:

```
def test_single_line(self):
    class A:
        a = 1

    b = 2
    assert A.a == b, "A.a appears not to be b"
```

---

TITLE: Manual Simulation of Chained Pytest Fixture Execution in Python
DESCRIPTION: This snippet demonstrates the manual execution flow when fixtures depend on other fixtures. It explicitly calls `first_entry` to get its result, then uses that result to call `order`, and finally passes the `order`'s result to `test_string`, mirroring pytest's dependency resolution for nested fixtures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_3

LANGUAGE: python
CODE:

```
def first_entry():
    return "a"


def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]


entry = first_entry()
the_list = order(first_entry=entry)
test_string(order=the_list)
```

---

TITLE: Applying Multiple Pytest Markers at Module Level in Python
DESCRIPTION: This example demonstrates how to apply multiple pytest markers to all tests within a module by assigning a list of markers to the `pytestmark` global variable. All tests in this module will be marked as both `webtest` and `slowtest`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_14

LANGUAGE: Python
CODE:

```
pytestmark = [pytest.mark.webtest, pytest.mark.slowtest]
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This command line instruction uses the pip package manager to upgrade an existing pytest installation to the specified version (3.2.2 in this context). The '--upgrade' flag ensures that pytest is updated to its latest available version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.2.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Matching Warning Messages with pytest.warns in Python
DESCRIPTION: These examples illustrate how to use the `match` keyword argument with `pytest.warns` to assert that a warning's message matches a given text or regular expression. It also shows how to escape literal strings for exact matching.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_13

LANGUAGE: python
CODE:

```
with warns(UserWarning, match="must be 0 or None"):
    warnings.warn("value must be 0 or None", UserWarning)

with warns(UserWarning, match=r"must be \d+$"):
    warnings.warn("value must be 42", UserWarning)

with warns(UserWarning, match=r"must be \d+$"):
    warnings.warn("this is not here", UserWarning)

with warns(UserWarning, match=re.escape("issue with foo() func")):
    warnings.warn("issue with foo() func")
```

---

TITLE: Applying Multiple Warning Filters with pytest.mark.filterwarnings (Python)
DESCRIPTION: This Python snippet illustrates how to apply multiple `@pytest.mark.filterwarnings` decorators to a single test item. In this example, it specifically ignores warnings starting with "api v1" while implicitly allowing other warnings to be treated as errors based on other configurations.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_6

LANGUAGE: python
CODE:

```
# Ignore "api v1" warnings, but fail on all other warnings
@pytest.mark.filterwarnings("ignore:api v1")
```

---

TITLE: Configuring SMTP Server URL in Pytest Module (Python)
DESCRIPTION: This snippet demonstrates how to configure an SMTP server URL (`smtpserver`) at the module level in a `pytest` test file. The `smtp_connection` fixture automatically picks up this variable, allowing tests like `test_showhelo` to use the specified server. The test intentionally asserts `0` to show the `helo()` output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_33

LANGUAGE: python
CODE:

```
# content of test_anothersmtp.py

smtpserver = "mail.python.org"  # will be read by smtp fixture


def test_showhelo(smtp_connection):
    assert 0, smtp_connection.helo()
```

---

TITLE: Implementing `pytest_collection_modifyitems` Hook in Python
DESCRIPTION: This snippet demonstrates a basic implementation of the `pytest_collection_modifyitems` hook. This hook is called after test item collection is complete, allowing modification of the `items` list. Pytest dynamically prunes arguments, passing only those listed in the function signature, ensuring future compatibility.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst#_snippet_0

LANGUAGE: python
CODE:

```
def pytest_collection_modifyitems(config, items):
    # called after collection is completed
    # you can modify the ``items`` list
    ...
```

---

TITLE: Utilizing Injected Namespace Objects in Doctests (Python)
DESCRIPTION: Shows how an object (e.g., `np` from `numpy`) injected into the `doctest_namespace` can be directly used within a Python doctest. This demonstrates the practical application of the `doctest_namespace` fixture for providing common utilities or context to doctests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst#_snippet_13

LANGUAGE: python
CODE:

```
# content of numpy.py
def arange():
    """
    >>> a = np.arange(10)
    >>> len(a)
    10
    """
```

---

TITLE: Deferring pytest Hook Implementation in Python
DESCRIPTION: This snippet demonstrates how to defer the registration of pytest hook functions to a separate plugin class. This approach allows for conditional hook installation, ensuring that hooks are only registered if their dependent plugins (e.g., 'xdist') are present, thus preventing validation errors for users without optional dependencies.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst#_snippet_10

LANGUAGE: Python
CODE:

```
# contents of myplugin.py


class DeferPlugin:
    """Simple plugin to defer pytest-xdist hook functions."""

    def pytest_testnodedown(self, node, error):
        """standard xdist hook function."""


def pytest_configure(config):
    if config.pluginmanager.hasplugin("xdist"):
        config.pluginmanager.register(DeferPlugin())
```

---

TITLE: Defining Local pytest_runtest_setup Hook in conftest.py - Python
DESCRIPTION: This snippet demonstrates how to implement the `pytest_runtest_setup` hook within a `conftest.py` file to apply specific setup logic only to tests within its directory and subdirectories. The hook is called for each test item, allowing for directory-specific test preparation.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_0

LANGUAGE: Python
CODE:

```
def pytest_runtest_setup(item):
    # called for running each test in 'a' directory
    print("setting up", item)
```

LANGUAGE: Python
CODE:

```
def test_sub():
    pass
```

LANGUAGE: Python
CODE:

```
def test_flat():
    pass
```

---

TITLE: Pytest Test Function for Fixture Parametrization Demo
DESCRIPTION: This Python test function test_db_initialized is used in conjunction with pytest fixtures. It takes a db object and conditionally calls pytest.fail() if the db object's class name is "DB2", serving as a demonstration of how parametrized fixtures can influence test outcomes.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_13

LANGUAGE: python
CODE:

```
def test_db_initialized(db):
    # a dummy test
    if db.__class__.__name__ == "DB2":
        pytest.fail("deliberately failing for demo purposes")
```

---

TITLE: Demonstrating Automatic Warning Capture in Pytest (Python)
DESCRIPTION: This Python code defines a function `api_v1` that issues a `UserWarning` and a test function `test_one` that calls `api_v1`. When executed with pytest, this snippet demonstrates how pytest automatically captures and displays warnings at the end of the test session.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_0

LANGUAGE: python
CODE:

```
# content of test_show_warnings.py
import warnings

def api_v1():
    warnings.warn(UserWarning("api v1, should use functions from v2"))
    return 1

def test_one():
    assert api_v1() == 1
```

---

TITLE: Pytest Collection Output with Ignored Paths
DESCRIPTION: This output demonstrates the result of running pytest with specific paths ignored using the `--ignore` option. It shows that `test_foobar_03.py` and all tests under `tests/hello/` are not collected, resulting in only 5 collected items.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_1

LANGUAGE: pytest
CODE:

```
=========================== test session starts ============================\nplatform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y\nrootdir: $REGENDOC_TMPDIR, inifile:\ncollected 5 items\n\ntests/example/test_example_01.py .                                   [ 20%]\ntests/example/test_example_02.py .                                   [ 40%]\ntests/example/test_example_03.py .                                   [ 60%]\ntests/foobar/test_foobar_01.py .                                     [ 80%]\ntests/foobar/test_foobar_02.py .                                     [100%]\n\n========================= 5 passed in 0.02 seconds =========================
```

---

TITLE: Running Pytest with Mismatched Environment (CLI)
DESCRIPTION: This command-line example demonstrates invoking pytest with the `-E` option, specifying 'stage2' as the environment. Since the `test_basic_db_operation` is marked for 'stage1', pytest skips the test, indicating that the required environment was not met. This highlights pytest's ability to conditionally execute tests based on environment markers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_19

LANGUAGE: pytest
CODE:

```
$ pytest -E stage2
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_someenv.py s                                                    [100%]

============================ 1 skipped in 0.12s ============================
```

---

TITLE: Adding Single Line Info to pytest Report Header in Python
DESCRIPTION: This Python code, intended for `conftest.py`, defines the `pytest_report_header` hook. It returns a single string, which pytest will add as a line in the test session header output.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_23

LANGUAGE: python
CODE:

```
# content of conftest.py


def pytest_report_header(config):
    return "project deps: mylib-1.1"
```

---

TITLE: Running unittest-style tests with pytest (Bash)
DESCRIPTION: This command demonstrates how to execute unittest-style test suites using the pytest test runner from the command line. Pytest automatically discovers and runs `unittest.TestCase` subclasses and their `test` methods within `test_*.py` or `*_test.py` files.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pytest tests
```

---

TITLE: Add Test Suite Properties using record_testsuite_property (Python)
DESCRIPTION: Demonstrates how to use a session-scoped fixture with the `record_testsuite_property` fixture to add properties that apply to the entire test suite, appearing under a `<properties>` tag at the suite level in the JUnit XML report.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_24

LANGUAGE: python
CODE:

```
import pytest


@pytest.fixture(scope="session", autouse=True)
def log_global_env_facts(record_testsuite_property):
    record_testsuite_property("ARCH", "PPC")
    record_testsuite_property("STORAGE_TYPE", "CEPH")


class TestMe:
    def test_foo(self):
        assert True
```

---

TITLE: Executing unittest with pytest and observing output (Pytest CLI)
DESCRIPTION: This command demonstrates running the `test_unittest_db.py` file, which contains a `unittest.TestCase` subclass integrated with a pytest fixture. The output shows the session start, indicating pytest is acting as the test runner, and would typically display test results and tracebacks for the deliberately failing assertions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst#_snippet_3

LANGUAGE: pytest
CODE:

```
$ pytest test_unittest_db.py
=========================== test session starts ============================
```

---

TITLE: Accessing Pytest Configuration with pytestconfig
DESCRIPTION: This example demonstrates how to use the session-scoped `pytestconfig` fixture to access the current `pytest.Config` object. It allows tests to query configuration details, such as verbosity level, to adapt test behavior based on the Pytest execution environment.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/builtin.rst#_snippet_6

LANGUAGE: python
CODE:

```
def test_foo(pytestconfig):
    if pytestconfig.get_verbosity() > 0:
        ...
```

---

TITLE: Setting Captured Log Level in Pytest (INI)
DESCRIPTION: Defines the minimum log message level that should be captured by pytest's logging system. Messages with a level lower than the specified one will be ignored across all logging facilities. Both integer values and level names are accepted.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_41

LANGUAGE: ini
CODE:

```
[pytest]
log_level = INFO
```

---

TITLE: Enabling Live Logging in pytest.ini
DESCRIPTION: This option enables the display of log messages directly during the test run, also known as 'live logging'. Setting it to `True` activates this feature, which is `False` by default.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_32

LANGUAGE: ini
CODE:

```
[pytest]
log_cli = True
```

---

TITLE: Defining Custom Class for Pytest Assertion Comparison - Python
DESCRIPTION: This Python snippet defines a `Foo` class with a custom `__eq__` method to demonstrate how pytest's assertion introspection can be extended. It also includes a `test_compare` function that asserts equality between `Foo` instances, which will fail and trigger custom comparison reporting if configured.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_21

LANGUAGE: python
CODE:

```
class Foo:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val


def test_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    assert f1 == f2
```

---

TITLE: Detecting if Running within pytest in Python
DESCRIPTION: This Python snippet shows how to check if your application code is being executed by pytest by inspecting the environment variable `PYTEST_VERSION`. It allows conditional logic based on whether the code is run in a test environment.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_22

LANGUAGE: python
CODE:

```
import os


if os.environ.get("PYTEST_VERSION") is not None:
    # Things you want to to do if your code is called by pytest.
    ...
else:
    # Things you want to to do if your code is not called by pytest.
    ...
```

---

TITLE: Running Pytest with Module-Level SMTP Configuration (Pytest CLI)
DESCRIPTION: This snippet shows the command-line execution of the previous Python test file using `pytest`. It demonstrates how `pytest` runs the test, captures the assertion error, and displays the output from the `smtp_connection.helo()` call, confirming the fixture picked up the `smtpserver` value. The `-qq --tb=short` flags reduce verbosity.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_34

LANGUAGE: pytest
CODE:

```
$ pytest -qq --tb=short test_anothersmtp.py
F                                                                    [100%]
================================= FAILURES =================================
______________________________ test_showhelo _______________________________
test_anothersmtp.py:6: in test_showhelo
    assert 0, smtp_connection.helo()
E   AssertionError: (250, b'mail.python.org')
E   assert 0
------------------------- Captured stdout teardown -------------------------
finalizing <smtplib.SMTP object at 0xdeadbeef0003> (mail.python.org)
========================= short test summary info ==========================
FAILED test_anothersmtp.py::test_showhelo - AssertionError: (250, b'mail....
```

---

TITLE: Running Pytest Tests from Python Packages (Bash)
DESCRIPTION: This command-line example shows how to use the `--pyargs` option with Pytest. This option allows Pytest to interpret command-line arguments as Python package names, derive their file system path, and then run tests within those packages, such as `unittest2.test.test_skipping`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_10

LANGUAGE: bash
CODE:

```
pytest --pyargs unittest2.test.test_skipping -q
```

---

TITLE: Asserting Deprecation Warning with pytest.deprecated_call
DESCRIPTION: This Python snippet demonstrates how to use `pytest.deprecated_call()` to assert that a specific function call triggers a `DeprecationWarning` or `PendingDeprecationWarning`. The test will fail if `myfunction(17)` does not issue the expected deprecation warning, ensuring that deprecated code paths are correctly identified.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_11

LANGUAGE: python
CODE:

```
import pytest


def test_myfunction_deprecated():
    with pytest.deprecated_call():
        myfunction(17)
```

---

TITLE: Running Pytest Tests with Debugger via Tox
DESCRIPTION: This command runs tests on Python 3.9 using 'tox' and passes the '--pdb' option directly to pytest, allowing entry into the Python debugger on test failure.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/CONTRIBUTING.rst#_snippet_13

LANGUAGE: Shell
CODE:

```
tox -e py39 -- --pdb
```

---

TITLE: Configuring Pytest for Multiple Python File Patterns (INI)
DESCRIPTION: This INI configuration demonstrates how to instruct Pytest to discover test files matching multiple glob patterns. By adding a space between patterns in the `python_files` option, Pytest will look for files like `test_*.py` and `example_*.py`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_9

LANGUAGE: ini
CODE:

```
# Example 2: have pytest look for files with "test" and "example"
# content of pytest.ini
[pytest]
python_files = test_*.py example_*.py
```

---

TITLE: Registering Multiple Pytest Plugins with `pytest_plugins` (Python)
DESCRIPTION: This snippet demonstrates how to register multiple additional plugins using the `pytest_plugins` global variable. It can be declared in test modules or `conftest.py` files. The variable can accept a sequence (e.g., tuple or list) of strings, where each string represents a plugin module path.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_12

LANGUAGE: Python
CODE:

```
pytest_plugins = ("myapp.testsupport.tools", "myapp.testsupport.regression")
```

---

TITLE: Inspecting pytest Collection Tree for Custom Tests
DESCRIPTION: This snippet demonstrates using `pytest --collect-only` to view the test collection tree. It shows how pytest identifies and structures custom test items (e.g., `YamlFile`, `YamlItem`) from a YAML file, which is crucial for understanding and debugging custom test collection logic.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/nonpython.rst#_snippet_2

LANGUAGE: pytest
CODE:

```
nonpython $ pytest --collect-only
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
rootdir: /home/sweet/project/nonpython
collected 2 items

<Package nonpython>
  <YamlFile test_simple.yaml>
    <YamlItem hello>
    <YamlItem ok>

======================== 2 tests collected in 0.12s ========================
```

---

TITLE: Running Pytest and Observing Collection Warning
DESCRIPTION: This snippet shows the command-line execution of pytest against the `test_pytest_warnings.py` file and its output. It demonstrates how pytest emits a `PytestCollectionWarning` because the 'Test' class has an `__init__` constructor, preventing its collection.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_24

LANGUAGE: bash
CODE:

```
$ pytest test_pytest_warnings.py -q

============================= warnings summary =============================
test_pytest_warnings.py:1
  /home/sweet/project/test_pytest_warnings.py:1: PytestCollectionWarning: cannot collect test class 'Test' because it has a __init__ constructor (from: test_pytest_warnings.py)
    class Test:

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1 warning in 0.12s
```

---

TITLE: Configuring Log File Format in Pytest (INI)
DESCRIPTION: Sets a `logging`-compatible string used to format log messages that are redirected to the specified logging file. This allows for detailed control over the structure and content of log entries written to the file.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_38

LANGUAGE: ini
CODE:

```
[pytest]
log_file_format = %(asctime)s %(levelname)s %(message)s
```

---

TITLE: Running Pytest with Multiple Fixtures Parametrization (Skipped Tests)
DESCRIPTION: This command-line output demonstrates running pytest with tests parametrized by multiple fixtures. It shows that tests are skipped if required Python interpreters are not found, indicating how pytest handles unavailable dependencies in parametrized scenarios.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_19

LANGUAGE: pytest
CODE:

```
. $ pytest -rs -q multipython.py
sssssssssssssssssssssssssss                                          [100%]
========================= short test summary info ==========================
SKIPPED [9] multipython.py:67: 'python3.9' not found
SKIPPED [9] multipython.py:67: 'python3.10' not found
SKIPPED [9] multipython.py:67: 'python3.11' not found
27 skipped in 0.12s
```

---

TITLE: Testing List Equality with Pytest (Failing)
DESCRIPTION: This Python function demonstrates a pytest test that asserts equality between two lists with different elements. The expected output shows the detailed diff provided by pytest upon failure, highlighting the differing elements and their positions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_4

LANGUAGE: python
CODE:

```
def test_words_fail():
    fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
    fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    assert fruits1 == fruits2
```

---

TITLE: Testing Dictionary Equality with Pytest (Failing)
DESCRIPTION: This Python function shows a pytest test that asserts equality between two dictionaries with different keys and values. The failure output illustrates how pytest provides a detailed diff for dictionaries, showing common items and items unique to each dictionary.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_5

LANGUAGE: python
CODE:

```
def test_numbers_fail():
    number_to_text1 = {str(x): x for x in range(5)}
    number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    assert number_to_text1 == number_to_text2
```

---

TITLE: Setting Live Log Level in Pytest (INI)
DESCRIPTION: Defines the minimum log message level that should be captured and displayed for live logging in the console. Messages with a level lower than the specified one will be ignored. Both integer values and level names (e.g., INFO, DEBUG) are accepted.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_34

LANGUAGE: ini
CODE:

```
[pytest]
log_cli_level = INFO
```

---

TITLE: Implementing Pytest Incremental Testing Hooks (Python)
DESCRIPTION: This `conftest.py` file defines pytest hooks to enable incremental testing. The `pytest_runtest_makereport` hook records failures for tests marked 'incremental', storing the class name and parametrize index. The `pytest_runtest_setup` hook checks this history before running a test; if a previous test in the same marked class and parametrize group failed, it marks the current test as an expected failure (xfail).
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_30

LANGUAGE: python
CODE:

```
# content of conftest.py

from typing import Dict, Tuple

import pytest

# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None:
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail(f"previous test failed ({test_name})")

```

---

TITLE: Asserting Class Attribute Value on New Instance in Python with Pytest
DESCRIPTION: This test demonstrates asserting the value of a class attribute immediately after creating a new instance. The pytest failure output shows the actual value and the instance it came from.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_22

LANGUAGE: python
CODE:

```
def test_attribute_instance():
    class Foo:
        b = 1

    assert Foo().b == 2
```

---

TITLE: Accessing pytest Mark Attributes (Python)
DESCRIPTION: Illustrates how the arguments and keyword arguments passed to a custom `pytest` mark are stored and can be accessed from the `Mark` object. `mark.args` holds positional arguments as a tuple, and `mark.kwargs` holds keyword arguments as a dictionary.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_4

LANGUAGE: python
CODE:

```
mark.args == (10, "slow")
mark.kwargs == {"method": "thread"}
```

---

TITLE: Example Doctest in a Text File
DESCRIPTION: This snippet illustrates a basic doctest embedded within a plain text file named `test_example.txt`. It shows a simple Python interactive session (`>>> x = 3` and `>>> x`) that `pytest` will automatically discover and execute as a test case.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst#_snippet_1

LANGUAGE: text
CODE:

```
# content of test_example.txt

hello this is a doctest
>>> x = 3
>>> x
3
```

---

TITLE: Executing Pytest with SMTP Fixture (Pytest CLI)
DESCRIPTION: This snippet shows a command-line execution of pytest to demonstrate the `smtp_connection` fixture in action. It runs tests in `test_module.py` with quiet output and no traceback, confirming the fixture's finalization message.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/fixtures.rst#_snippet_32

LANGUAGE: pytest
CODE:

```
$ pytest -s -q --tb=no test_module.py
FFfinalizing <smtplib.SMTP object at 0xdeadbeef0002> (smtp.gmail.com)
```

---

TITLE: Adding a Custom Message to Python Assertions
DESCRIPTION: Shows how to include a custom message with a standard Python `assert` statement. This message is printed alongside the assertion introspection in the traceback when the assertion fails, providing additional context for debugging.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_2

LANGUAGE: python
CODE:

```
assert a % 2 == 0, "value was odd, should be even"
```

---

TITLE: Configuring norecursedirs in pytest.ini
DESCRIPTION: This INI configuration snippet demonstrates how to use the `norecursedirs` option in `pytest.ini` to prevent pytest from recursing into specified directories during test collection, such as version control or build directories.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_5

LANGUAGE: ini
CODE:

```
# content of pytest.ini\n[pytest]\nnorecursedirs = .svn _build tmp*
```

---

TITLE: Attempt to Use Unavailable Fixture (Python)
DESCRIPTION: A test function `test_root` in `b/test_error.py`, located in a different directory ('b'), attempts to use the `db` fixture defined in directory 'a'. This is expected to fail because the fixture is not visible in this scope.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_36

LANGUAGE: python
CODE:

```
# content of b/test_error.py
def test_root(db):  # no db here, will error out
    pass
```

---

TITLE: Forcing xfail Tests to Run and Report in pytest
DESCRIPTION: This snippet demonstrates how to force `xfail` marked tests to run and report their status using the `-rx` option with `pytest`. It shows the command line invocation and the resulting output, where all `xfail` tests are explicitly reported as XFAIL, even those with conditions or reasons.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_23

LANGUAGE: pytest
CODE:

```
! pytest -rx xfail_demo.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-1.x.y
cachedir: $PYTHON_PREFIX/.pytest_cache
rootdir: $REGENDOC_TMPDIR/example
collected 7 items

xfail_demo.py xxxxxxx                                                [100%]

========================= short test summary info ==========================
XFAIL xfail_demo.py::test_hello
XFAIL xfail_demo.py::test_hello2
  reason: [NOTRUN]
XFAIL xfail_demo.py::test_hello3
  condition: hasattr(os, 'sep')
XFAIL xfail_demo.py::test_hello4
  bug 110
XFAIL xfail_demo.py::test_hello5
  condition: pytest.__version__[0] != "17"
XFAIL xfail_demo.py::test_hello6
  reason: reason
XFAIL xfail_demo.py::test_hello7
============================ 7 xfailed in 0.12s ============================
```

---

TITLE: Running Pytest with Multiple Dynamic String Inputs
DESCRIPTION: This snippet demonstrates running Pytest with the custom `--stringinput` command-line option, providing two valid string values. The output shows that the test function is executed twice, once for each provided input, and both pass successfully.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/parametrize.rst#_snippet_10

LANGUAGE: pytest
CODE:

```
$ pytest -q --stringinput="hello" --stringinput="world" test_strings.py
..
2 passed in 0.12s
```

---

TITLE: Disabling Captured Content Reporting in Pytest (Bash)
DESCRIPTION: This command demonstrates how to completely disable the reporting of captured content (stdout, stderr, and logs) for failed tests in pytest. The `--show-capture=no` option is useful when you want to suppress verbose output during test failures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/logging.rst#_snippet_6

LANGUAGE: bash
CODE:

```
pytest --show-capture=no
```

---

TITLE: Configuring Assertion Truncation Lines Limit (INI)
DESCRIPTION: Controls the maximum number of lines to truncate assertion message contents in pytest. Setting the value to `0` disables the lines limit. This helps prevent large data comparisons from overloading console output. Pytest automatically disables truncation on CI pipelines.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_57

LANGUAGE: ini
CODE:

```
[pytest]
truncation_limit_lines = 8
```

---

TITLE: Executing Pytest with Autouse Fixture Test Module
DESCRIPTION: This snippet shows the command-line execution of a Python test file containing a unittest.TestCase with an autouse pytest fixture. The output confirms that the test passes, demonstrating the successful application of the initdir fixture before the test method runs.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/unittest.rst#_snippet_7

LANGUAGE: pytest
CODE:

```
$ pytest -q test_unittest_cleandir.py
.                                                                    [100%]
1 passed in 0.12s
```

---

TITLE: Using **tracebackhide** and pytest.fail in Helpers (Python)
DESCRIPTION: Demonstrates how setting `__tracebackhide__ = True` within a helper function (`checkconfig`) prevents that function from appearing in the traceback when `pytest.fail` is called, resulting in cleaner failure output focused on the test function.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_19

LANGUAGE: python
CODE:

```
# content of test_checkconfig.py
import pytest


def checkconfig(x):
    __tracebackhide__ = True
    if not hasattr(x, "config"):
        pytest.fail(f"not configured: {x}")


def test_something():
    checkconfig(42)
```

---

TITLE: Example Dummy setup.py File
DESCRIPTION: This `setup.py` dummy file is designed to raise an exception if imported, demonstrating a common scenario where such files should be excluded from Pytest's test collection. It highlights the need for explicit ignore rules to prevent unintended side effects during test discovery.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_16

LANGUAGE: python
CODE:

```
# content of setup.py
0 / 0  # will raise exception if imported
```

---

TITLE: Running Parametrized Tests with --all Option and Failure (pytest CLI)
DESCRIPTION: This command-line snippet illustrates running the tests with the `--all` option, which expands the `param1` range to include a failing case. The output shows a failure for `test_compute[4]` because `assert 4 < 4` is false, demonstrating the full range execution and how pytest reports specific test failures.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/parametrize.rst#_snippet_3

LANGUAGE: pytest
CODE:

```
$ pytest -q --all
....F
================================= FAILURES =================================
_____________________________ test_compute[4] ______________________________

param1 = 4

    def test_compute(param1):
>       assert param1 < 4
E       assert 4 < 4

test_compute.py:4: AssertionError
========================= short test summary info ==========================
FAILED test_compute.py::test_compute[4] - assert 4 < 4
1 failed, 4 passed in 0.12s
```

---

TITLE: Renaming `record_xml_property` to `record_property` Fixture in Pytest
DESCRIPTION: This snippet demonstrates the renaming of the `record_xml_property` fixture to `record_property` in Pytest. The API remains consistent, allowing other consumers like `pytest-html` to obtain custom test run information by simply updating the fixture name.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_34

LANGUAGE: python
CODE:

```
def test_foo(record_xml_property): ...
```

LANGUAGE: python
CODE:

```
def test_foo(record_property): ...
```

---

TITLE: Disabling Pytest Warning Plugin in pytest.ini
DESCRIPTION: This INI configuration snippet demonstrates how to disable the pytest warning plugin entirely within the `pytest.ini` file. Adding `-p no:warnings` to `addopts` prevents pytest from capturing or displaying any warnings, which can be useful if an external system handles warnings.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/capture-warnings.rst#_snippet_9

LANGUAGE: ini
CODE:

```
[pytest]
addopts = -p no:warnings
```

---

TITLE: Failing Similar String Equality Assertion (Python)
DESCRIPTION: Documents a pytest test method that fails when asserting the equality of two similar short strings, demonstrating how pytest highlights the specific characters that differ.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_5

LANGUAGE: Python
CODE:

```
def test_eq_similar_text(self):
    assert "foo 1 bar" == "foo 2 bar"
```

---

TITLE: Running Pytest with Custom Assertion Output - Pytest CLI
DESCRIPTION: This snippet demonstrates running a pytest test module (`test_foocompare.py`) from the command line. It shows the resulting output, highlighting how custom assertion comparison details (like 'Comparing Foo instances: vals: 1 != 2') are integrated into the failure message.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_22

LANGUAGE: pytest
CODE:

```
$ pytest -q test_foocompare.py
F                                                                    [100%]
================================= FAILURES =================================
_______________________________ test_compare _______________________________

    def test_compare():
        f1 = Foo(1)
        f2 = Foo(2)
>       assert f1 == f2
E       assert Comparing Foo instances:
E            vals: 1 != 2

test_foocompare.py:12: AssertionError
========================= short test summary info ==========================
FAILED test_foocompare.py::test_compare - assert Comparing Foo instances:
1 failed in 0.12s
```

---

TITLE: Running pytest with src Directory in PYTHONPATH
DESCRIPTION: This bash command temporarily adds the `src` directory to Python's module search path (`PYTHONPATH`) before executing `pytest`. This is necessary when not using an editable install and employing a `src` layout, allowing `pytest` to correctly discover and import modules from the local source code.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/explanation/goodpractices.rst#_snippet_4

LANGUAGE: bash
CODE:

```
PYTHONPATH=src pytest
```

---

TITLE: Listing Pytest Markers (Shell)
DESCRIPTION: This command displays a list of all available markers configured in the pytest environment. Markers are used to categorize and filter tests.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_63

LANGUAGE: Shell
CODE:

```
pytest --markers
```

---

TITLE: Raising ValueError directly (Python)
DESCRIPTION: Explicitly raises a `ValueError` with a custom message 'demo error'. This demonstrates a simple test failure caused by an unhandled exception.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_27

LANGUAGE: python
CODE:

```
raise ValueError("demo error")
```

---

TITLE: Using Pytester to Copy and Run Example Tests (Python)
DESCRIPTION: This Python test function `test_plugin` demonstrates the use of `pytester`. It copies an example file named `test_example.py` into the test environment using `pytester.copy_example` and then executes `pytest` with a specific keyword filter using `pytester.runpytest`. The `test_example` function serves as a placeholder for the copied content.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_12

LANGUAGE: python
CODE:

```
# content of test_example.py


def test_plugin(pytester):
    pytester.copy_example("test_example.py")
    pytester.runpytest("-k", "test_example")


def test_example():
    pass
```

---

TITLE: Implement Pytest Report Hook (Python)
DESCRIPTION: Defines a `pytest_runtest_makereport` hook using `@pytest.hookimpl`. This hook is wrapped and runs first (`tryfirst=True`). It intercepts the test report creation, specifically looking for failing test calls (`rep.when == "call" and rep.failed`), and writes information about them to a file named "failures".
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_38

LANGUAGE: python
CODE:

```
# content of conftest.py

import os.path

import pytest


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    rep = yield

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode, encoding="utf-8") as f:
```

---

TITLE: Add/Override XML Attributes using record_xml_attribute (Python)
DESCRIPTION: Shows how to use the `record_xml_attribute` fixture within a test function to add new attributes (like `assertions`) or override existing ones (like `classname`) directly on the `<testcase>` element in the JUnit XML report.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_21

LANGUAGE: python
CODE:

```
def test_function(record_xml_attribute):
    record_xml_attribute("assertions", "REQ-1234")
    record_xml_attribute("classname", "custom_classname")
    print("hello world")
    assert True
```

---

TITLE: Configuring Pytest XFAIL Strict Mode Globally
DESCRIPTION: This snippet demonstrates how to set the `xfail_strict` option in the `pytest.ini` file. Setting `xfail_strict=true` globally makes all XPASS results fail the test suite by default, unless overridden by individual markers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/skipping.rst#_snippet_21

LANGUAGE: ini
CODE:

```
[pytest]
xfail_strict=true
```

---

TITLE: Example of Imported Class in Pytest Test Module (Python)
DESCRIPTION: Provides a Python example demonstrating a class `Testament` defined in `src/domain.py` and then imported into `tests/test_testament.py`. This scenario highlights how pytest, by default, would collect the imported `Testament` class as a test if its name matches test collection rules, even if it's a production class.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_20

LANGUAGE: python
CODE:

```
# contents of src/domain.py
class Testament: ...


# contents of tests/test_testament.py
from domain import Testament


def test_testament(): ...
```

---

TITLE: Python Test File with Custom Naming Conventions
DESCRIPTION: This Python code snippet provides an example of a test file (`check_myapp.py`) structured to comply with custom naming conventions defined in `pytest.ini`, featuring a class named `CheckMyApp` and methods ending with `_check`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_7

LANGUAGE: python
CODE:

```
# content of check_myapp.py\nclass CheckMyApp:\n    def simple_check(self):\n        pass\n\n    def complex_check(self):\n        pass
```

---

TITLE: Example pytest Command Execution
DESCRIPTION: Shows a simple execution of pytest with a specific marker.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_3

LANGUAGE: bash
CODE:

```
pytest -m slow
```

---

TITLE: Viewing pytest Report Header with Custom Info
DESCRIPTION: This snippet shows the output of running pytest after adding a custom header line using the `pytest_report_header` hook. The string returned by the hook is included in the session start information.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/simple.rst#_snippet_24

LANGUAGE: pytest
CODE:

```
$ pytest
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-8.x.y, pluggy-1.x.y
project deps: mylib-1.1
rootdir: /home/sweet/project
collected 0 items

========================== no tests ran in 0.12s ===========================
```

---

TITLE: Programmatically Registering Markers with pytest_configure (Python)
DESCRIPTION: This Python snippet illustrates how to programmatically register a new marker using the `pytest_configure` hook. This method is useful for plugins or complex setups where markers need to be defined dynamically, adding them to pytest's known markers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/mark.rst#_snippet_2

LANGUAGE: Python
CODE:

```
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )
```

---

TITLE: Setting JUnit Suite Name in pytest.ini
DESCRIPTION: This option allows customizing the name of the root test suite XML item within the JUnit report, providing a more descriptive identifier for the test run.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_30

LANGUAGE: ini
CODE:

```
[pytest]
junit_suite_name = my_suite
```

---

TITLE: Applying Multiple Pytest Markers to a Test Function
DESCRIPTION: This Python test file demonstrates how the same marker, 'glob', can be applied multiple times at different scopes: module-level, class-level, and function-level. This setup is used to illustrate how pytest handles and allows reading of stacked markers.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/markers.rst#_snippet_25

LANGUAGE: python
CODE:

```
# content of test_mark_three_times.py
import pytest

pytestmark = pytest.mark.glob("module", x=1)


@pytest.mark.glob("class", x=2)
class TestClass:
    @pytest.mark.glob("function", x=3)
    def test_something(self):
        pass
```

---

TITLE: Using a Mixin for Automatic Pytest Test Collection
DESCRIPTION: This Python snippet defines a `NotATest` mixin class that automatically sets the `__test__` attribute for its subclasses. If `NotATest` is not in the base classes, `__test__` is set to `True`, ensuring the subclass is collected as a test by Pytest. It demonstrates an abstract test class `AbstractTest` and a concrete `RealTest` subclass that will be collected.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/pythoncollection.rst#_snippet_21

LANGUAGE: python
CODE:

```
# Mixin to handle abstract test classes
class NotATest:
    def __init_subclass__(cls):
        cls.__test__ = NotATest not in cls.__bases__


# Abstract test class
class AbstractTest(NotATest):
    pass


# Subclass that will be collected as a test
class RealTest(AbstractTest):
    def test_example(self):
        assert 1 + 1 == 2
```

---

TITLE: Assert Long List Equality in Pytest
DESCRIPTION: Shows a failed assertion comparing two long lists that differ by one element. Pytest truncates the list representation but still indicates the index and values of the differing elements.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_10

LANGUAGE: python
CODE:

```
a = [0] * 100 + [1] + [3] * 100
b = [0] * 100 + [2] + [3] * 100
assert a == b
```

---

TITLE: Skipping Individual Doctest Checks with `doctest: +SKIP` (Python)
DESCRIPTION: Illustrates how to skip a specific check within a Python doctest using the standard `doctest: +SKIP` directive. This allows for selective skipping of problematic or non-deterministic test lines while still executing other checks in the same doctest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/doctest.rst#_snippet_14

LANGUAGE: python
CODE:

```
def test_random(y):
    """
    >>> random.random()  # doctest: +SKIP
    0.156231223

    >>> 1 + 1
    2
    """
```

---

TITLE: Specifying Log File Path in Pytest (INI)
DESCRIPTION: Sets a file name, relative to the current working directory, where log messages should be written. This allows pytest to output all captured log messages to a persistent file in addition to other active logging facilities.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/reference/reference.rst#_snippet_36

LANGUAGE: ini
CODE:

```
[pytest]
log_file = logs/pytest-logs.txt
```

---

TITLE: Loading Single pytest Plugin in Python Test Module
DESCRIPTION: This Python snippet illustrates how to load a single pytest plugin, including internal application modules, by assigning its import path (e.g., `myapp.testsupport.myplugin`) to the `pytest_plugins` global variable. This variable supports recursive loading of plugins, allowing for complex plugin dependencies.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_plugins.rst#_snippet_5

LANGUAGE: Python
CODE:

```
pytest_plugins = "myapp.testsupport.myplugin"
```

---

TITLE: Deprecated pytest.raises with 'message' Parameter (Python)
DESCRIPTION: Illustrates the deprecated use of the `message` parameter in `pytest.raises`, which was often misunderstood to match the exception message. This parameter is being removed, and `pytest.fail` should be used instead for custom failure messages.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/deprecations.rst#_snippet_20

LANGUAGE: Python
CODE:

```
with pytest.raises(TimeoutError, message="Client got unexpected message"):
    wait_for(websocket.recv(), 0.5)
```

---

TITLE: Early Loading Pytest Plugins (Bash)
DESCRIPTION: This command explicitly loads a pytest plugin (internal or external) at invocation time using the '-p' option. The 'name' parameter can be a full module dotted name (e.g., 'myproject.plugins') or an entry-point name (e.g., 'pytest_cov'), which must be importable.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/usage.rst#_snippet_14

LANGUAGE: bash
CODE:

```
pytest -p mypluginmodule
```

---

TITLE: Example pytest File with Failing Tests (Python)
DESCRIPTION: A Python file containing several test functions (`test_ok`, `test_words_fail`, `test_numbers_fail`, `test_long_text_fail`) designed to demonstrate different types of test failures and how pytest reports them.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/output.rst#_snippet_2

LANGUAGE: python
CODE:

```
# content of test_verbosity_example.py
def test_ok():
    pass


def test_words_fail():
    fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
    fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    assert fruits1 == fruits2


def test_numbers_fail():
    number_to_text1 = {str(x): x for x in range(5)}
    number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    assert number_to_text1 == number_to_text2


def test_long_text_fail():
    long_text = "Lorem ipsum dolor sit amet " * 10
    assert "hello world" in long_text
```

---

TITLE: Warning: Pitfalls of ExceptionInfo.group_contains() (Python)
DESCRIPTION: This snippet highlights a critical limitation of ExceptionInfo.group_contains(): it only asserts the presence of a specific exception, not the absence of others. It demonstrates how a test using this method can inadvertently pass even when an unexpected and critical error is also present in the ExceptionGroup.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/assert.rst#_snippet_12

LANGUAGE: python
CODE:

```
class EXTREMELYBADERROR(BaseException):
    """This is a very bad error to miss"""


def test_for_value_error():
    with pytest.raises(ExceptionGroup) as excinfo:
        excs = [ValueError()]
        if very_unlucky():
            excs.append(EXTREMELYBADERROR())
        raise ExceptionGroup("", excs)
    # This passes regardless of if there's other exceptions.
    assert excinfo.group_contains(ValueError)
    # You can't simply list all exceptions you *don't* want to get here.
```

---

TITLE: Storing Data on pytest Item Stash in Python
DESCRIPTION: This snippet illustrates how to store data on a `pytest.Item`'s `stash` attribute using previously defined `StashKey`s within a `pytest_runtest_setup` hook. This allows plugins to associate specific data with a test item that can be accessed later in other hook functions.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/how-to/writing_hook_functions.rst#_snippet_12

LANGUAGE: Python
CODE:

```
def pytest_runtest_setup(item: pytest.Item) -> None:
    item.stash[been_there_key] = True
    item.stash[done_that_key] = "no"
```

---

TITLE: Implementing Custom Directory Collection with pytest_collect_directory Hook (Python)
DESCRIPTION: This Python `conftest.py` plugin defines a `ManifestDirectory` collector that reads a `manifest.json` file to determine which test files to collect within a directory. It uses the `pytest_collect_directory` hook to register this custom collector for directories named 'tests' containing a `manifest.json`. This allows for fine-grained control over test discovery based on a manifest.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/customdirectory.rst#_snippet_0

LANGUAGE: Python
CODE:

```
import pytest
import json

class ManifestDirectory(pytest.Directory):
    def collect(self):
        manifest_path = self.path / "manifest.json"
        if not manifest_path.is_file():
            return []

        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        collected_items = []
        for filename in manifest.get("files", []):
            filepath = self.path / filename
            if filepath.is_file():
                # Use self.session.perform_collection to collect the file
                # This ensures proper handling of modules, packages, etc.
                # and integrates with pytest's internal collection logic.
                # The 'parent' argument is crucial for correct scope.
                collected_items.extend(
                    self.session.perform_collection([filepath], parent=self)
                )
        return collected_items

@pytest.hookimpl(tryfirst=True)
def pytest_collect_directory(path, parent):
    if path.name == "tests" and (path / "manifest.json").is_file():
        return ManifestDirectory.from_parent(parent, path=path)
    return None
```

---

TITLE: Testing assertion within try block in pytest
DESCRIPTION: This test asserts that the variable `x`, initialized to 1, is equal to 0 within a try block. The assertion failed because `x` is 1, not 0.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_40

LANGUAGE: python
CODE:

```
def test_try_finally(self):
    x = 1
    try:
        assert x == 0
```

---

TITLE: Nested string startswith assertion failure (Python)
DESCRIPTION: Calls functions `f()` and `g()` to get strings ('123' and '456') and asserts that the result of `f()` starts with the result of `g()`. The assertion `assert f().startswith(g())` evaluates to `assert False`, causing an `AssertionError`.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/example/reportingdemo.rst#_snippet_36

LANGUAGE: python
CODE:

```
assert f().startswith(g())
```

---

TITLE: Upgrading pytest using pip
DESCRIPTION: This command upgrades an existing pytest installation to the latest version (8.1.2 in this context) using pip, the Python package installer. It ensures you have the most recent bug fixes and features by replacing the current version with the new one.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.1.2.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest to the latest version
DESCRIPTION: This command uses pip, the Python package installer, to upgrade an existing pytest installation to its latest available version. The '--upgrade' flag ensures that if pytest is already installed, it will be updated rather than reinstalled.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.10.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command upgrades the pytest testing framework to the latest version available on PyPI using the pip package installer. The '-U' flag ensures that any existing installation is updated to the newest version.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-8.3.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command line instruction uses the pip package manager to upgrade an existing pytest installation to version 3.7.3 or the latest available. The --upgrade flag ensures that pip replaces the current version with the new one.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.7.3.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest via pip
DESCRIPTION: This command uses pip, the Python package installer, to upgrade the pytest library to its latest available version. The '--upgrade' flag ensures that if pytest is already installed, it will be updated rather than reinstalled.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-4.3.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip (Shell)
DESCRIPTION: This command upgrades an existing pytest installation to the specified version (3.9.1 in this context) using the pip package manager. It ensures you have the most recent bug fixes and features by replacing the current version with the latest available.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.9.1.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install --upgrade pytest
```

---

TITLE: Upgrading pytest using pip in Shell
DESCRIPTION: This command upgrades the pytest testing framework to its latest version using pip, Python's package installer. The '-U' flag ensures that existing packages are upgraded.
SOURCE: https://github.com/pytest-dev/pytest/blob/main/doc/en/announce/release-3.5.0.rst#_snippet_0

LANGUAGE: Shell
CODE:

```
pip install -U pytest
```
