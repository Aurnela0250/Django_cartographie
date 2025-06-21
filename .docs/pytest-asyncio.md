TITLE: Defining Asynchronous Tests with pytest-asyncio in Python
DESCRIPTION: This snippet demonstrates how to define an asynchronous test function using the `@pytest.mark.asyncio` decorator. It allows the test to `await` asynchronous operations, such as `library.do_something()`, directly within the test body. This enables seamless testing of `asyncio`-based code within the pytest framework.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/README.rst#_snippet_0

LANGUAGE: python
CODE:

```
@pytest.mark.asyncio
async def test_some_asyncio_code():
    res = await library.do_something()
    assert b"expected result" == res
```

---

TITLE: Testing Asynchronous Code with pytest-asyncio in Python
DESCRIPTION: This snippet demonstrates how to write an asynchronous test function using `pytest-asyncio`. The `@pytest.mark.asyncio` decorator marks the function as an asyncio test, allowing `await` calls within it. It shows a basic test awaiting a library function and asserting its result.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/index.rst#_snippet_0

LANGUAGE: Python
CODE:

```
@pytest.mark.asyncio
async def test_some_asyncio_code():
    res = await library.do_something()
    assert b"expected result" == res
```

---

TITLE: Defining an Async Test Function for Pytest-asyncio (Function Scope)
DESCRIPTION: This Python snippet defines a basic asynchronous test function `test_runs_in_a_loop` that uses `asyncio.sleep`. This function is collected by pytest's Function collector and, by default, runs within an asyncio event loop provided at the function scope, ensuring high isolation.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/concepts.rst#_snippet_0

LANGUAGE: python
CODE:

```
import asyncio

async def test_runs_in_a_loop():
    await asyncio.sleep(0)
    assert True
```

---

TITLE: Installing pytest-asyncio via pip in Bash
DESCRIPTION: This command demonstrates the standard method for installing the `pytest-asyncio` plugin using the `pip` package manager. Executing this command will download and install the necessary packages, making the plugin available for use with pytest. This is the primary prerequisite for utilizing `pytest-asyncio`'s features.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
$ pip install pytest-asyncio
```

---

TITLE: Configuring Default Event Loop Scope in pyproject.toml (TOML)
DESCRIPTION: This snippet illustrates how to configure the default event loop scope for pytest-asyncio tests to 'session' within the pyproject.toml file. Using the [tool.pytest.ini_options] section, it applies a session-scoped event loop globally for all asynchronous tests, aligning with modern Python project configuration practices.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_test_loop.rst#_snippet_1

LANGUAGE: toml
CODE:

```
[tool.pytest.ini_options]
asyncio_default_test_loop_scope = "session"
```

---

TITLE: Setting asyncio_mode via Command-Line (Bash)
DESCRIPTION: This snippet shows how to override or set the `asyncio_mode` using the `--asyncio-mode` command-line option when running pytest. Command-line options take precedence over settings in the configuration file. The `strict` mode is the default if no mode is specified.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/reference/configuration.rst#_snippet_1

LANGUAGE: bash
CODE:

```
$ pytest tests --asyncio-mode=strict
```

---

TITLE: Configuring Default Asyncio Fixture Loop Scope in pyproject.toml
DESCRIPTION: This snippet shows how to configure the default event loop scope for asynchronous fixtures to 'session' within the `pyproject.toml` file. It uses the `[tool.pytest.ini_options]` section to apply the setting globally.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_fixture_loop.rst#_snippet_1

LANGUAGE: toml
CODE:

```
[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "session"
```

---

TITLE: Configuring Async Tests for Module-Scoped Event Loop in Pytest-asyncio
DESCRIPTION: This Python example demonstrates how to configure multiple asynchronous tests (`test_first_in_module_loop`, `test_second_in_module_loop`) to share an asyncio event loop provided by the Module collector. By applying `@pytest_asyncio.mark.asyncio(loop_scope='module')`, these tests run in the same loop, which is recommended for neighboring tests to improve readability and maintainability.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/concepts.rst#_snippet_1

LANGUAGE: python
CODE:

```
import asyncio
import pytest_asyncio

@pytest_asyncio.mark.asyncio(loop_scope='module')
async def test_first_in_module_loop():
    await asyncio.sleep(0)
    assert True

@pytest_asyncio.mark.asyncio(loop_scope='module')
async def test_second_in_module_loop():
    await asyncio.sleep(0)
    assert True
```

---

TITLE: Setting Pytest-asyncio Discovery Mode via TOML Configuration
DESCRIPTION: This TOML snippet shows how to configure the `asyncio_mode` for pytest-asyncio within the `pytest.ini_options` section of a `pyproject.toml` file. Users can set the mode to either 'auto' or 'strict' to control how pytest-asyncio discovers and handles asynchronous test functions and fixtures, influencing its coexistence with other async testing plugins.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/concepts.rst#_snippet_2

LANGUAGE: toml
CODE:

```
[tool.pytest.ini_options]
asyncio_mode = "auto" # or "strict"
```

---

TITLE: Configuring Default Event Loop Scope in pytest.ini (INI)
DESCRIPTION: This snippet demonstrates how to set the default event loop scope for pytest-asyncio tests to 'session' using the pytest.ini configuration file. This ensures all asynchronous tests, by default, share a single event loop throughout the test session, which can be beneficial for performance or specific testing scenarios.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_test_loop.rst#_snippet_0

LANGUAGE: ini
CODE:

```
[pytest]
asyncio_default_test_loop_scope = session
```

---

TITLE: Configuring Default Asyncio Fixture Loop Scope in pytest.ini
DESCRIPTION: This snippet demonstrates how to set the default event loop scope for all asynchronous fixtures to 'session' using the `pytest.ini` configuration file. This ensures that all async fixtures share a single event loop for the entire test session.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_fixture_loop.rst#_snippet_0

LANGUAGE: ini
CODE:

```
[pytest]
asyncio_default_fixture_loop_scope = session
```

---

TITLE: Applying Class-Scoped Event Loop to Async Tests (Python)
DESCRIPTION: This snippet demonstrates how to configure all asynchronous tests within a class to run in the same event loop using the `pytest.mark.asyncio(loop_scope="class")` decorator. This is useful for scenarios where tests share resources or state that depend on a single event loop instance, ensuring consistent behavior across related tests.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/run_class_tests_in_same_loop.rst#_snippet_0

LANGUAGE: python
CODE:

```
import pytest
import asyncio

@pytest.mark.asyncio(loop_scope="class")
class TestClassLoopScope:
    async def test_example_one(self):
        # This test runs in the class-scoped event loop
        await asyncio.sleep(0.001)
        assert True

    async def test_example_two(self):
        # This test also runs in the same class-scoped event loop
        await asyncio.sleep(0.001)
        assert True
```

---

TITLE: Configuring asyncio_mode in pytest.ini (INI)
DESCRIPTION: This snippet demonstrates how to set the `asyncio_mode` configuration option within the `pytest.ini` file. This setting determines the behavior of pytest-asyncio, with `auto` being one of the possible values. If not specified, the mode defaults to `strict`.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/reference/configuration.rst#_snippet_0

LANGUAGE: ini
CODE:

```
[pytest]
asyncio_mode = auto
```

---

TITLE: Configuring uvloop Event Loop Policy for Pytest
DESCRIPTION: This snippet defines a pytest fixture named 'event_loop_policy' with a session scope. It returns an instance of 'uvloop.EventLoopPolicy', effectively replacing the default asyncio event loop policy for all asynchronous tests within the session. This allows tests to run using uvloop for improved performance.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/uvloop.rst#_snippet_0

LANGUAGE: Python
CODE:

```
import pytest
import uvloop


@pytest.fixture(scope="session")
def event_loop_policy():
    return uvloop.EventLoopPolicy()
```

---

TITLE: Configuring Default Event Loop Scope in setup.cfg (INI)
DESCRIPTION: This snippet shows how to set the default event loop scope for pytest-asyncio tests to 'session' using the setup.cfg configuration file. By placing the setting under [tool:pytest], it ensures that all asynchronous tests default to a session-scoped event loop, providing consistent behavior across the test suite.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_test_loop.rst#_snippet_2

LANGUAGE: ini
CODE:

```
[tool:pytest]
asyncio_default_test_loop_scope = session
```

---

TITLE: Using unused_tcp_port_factory in Python
DESCRIPTION: Demonstrates how to use the `unused_tcp_port_factory` fixture to obtain multiple unique, unused TCP ports within a single test function. This is particularly useful when a test requires binding several temporary test servers, ensuring each uses a distinct available port.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/reference/fixtures/index.rst#_snippet_0

LANGUAGE: python
CODE:

```
def a_test(unused_tcp_port_factory):
    _port1, _port2 = unused_tcp_port_factory(), unused_tcp_port_factory()
```

---

TITLE: Configuring Default Asyncio Fixture Loop Scope in setup.cfg
DESCRIPTION: This snippet illustrates how to set the default event loop scope for all asynchronous fixtures to 'session' using the `setup.cfg` configuration file. The setting is placed under the `[tool:pytest]` section.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/change_default_fixture_loop.rst#_snippet_2

LANGUAGE: ini
CODE:

```
[tool:pytest]
asyncio_default_fixture_loop_scope = session
```

---

TITLE: Setting Default Async Fixture Loop Scope in Pytest Configuration
DESCRIPTION: To resolve deprecation warnings, set the `asyncio_default_fixture_loop_scope` configuration option to `function` in your pytest configuration file (e.g., `pytest.ini` or `pyproject.toml`) if it's not already defined.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/migrate_from_0_23.rst#_snippet_1

LANGUAGE: INI
CODE:

```
asyncio_default_fixture_loop_scope = function
```

---

TITLE: Migrating Pytest Async Fixture Scope in Python
DESCRIPTION: This snippet illustrates how to update async fixture definitions by explicitly setting `loop_scope` alongside `scope`. Previously, `scope` was used directly; now, `loop_scope` must be specified, typically matching the `scope` value.
SOURCE: https://github.com/pytest-dev/pytest-asyncio/blob/main/docs/how-to-guides/migrate_from_0_23.rst#_snippet_0

LANGUAGE: Python
CODE:

```
@pytest.fixture(scope="…")
```

LANGUAGE: Python
CODE:

```
@pytest_asyncio.fixture(scope="…")
```

LANGUAGE: Python
CODE:

```
@pytest_asyncio.fixture(loop_scope="…", scope="…")
```
