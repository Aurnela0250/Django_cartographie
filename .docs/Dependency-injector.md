TITLE: Configuring and Using Dependency Injector Containers in Python
DESCRIPTION: This Python code demonstrates how to set up and use Dependency Injector's core components: declarative containers, providers, configuration injection, and automatic dependency wiring into Python functions. Dependencies like ApiClient and Service are provided via Singleton and Factory providers, while configuration values are injected from environment variables. The snippet also illustrates how to override providers for testing, requiring dependency_injector and optionally mock for testing. Inputs are environment variables (API_KEY and TIMEOUT); outputs are injected Service instances and controllable execution with overridden dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/index.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    ...


if __name__ == "__main__":
    container = Container()
    container.config.api_key.from_env("API_KEY", required=True)
    container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
    container.wire(modules=[__name__])

    main()  # <-- dependency is injected automatically

    with container.api_client.override(mock.Mock()):
        main()  # <-- overridden dependency is injected automatically

```

---

TITLE: Creating the Main Application Entry Point in Python
DESCRIPTION: Implements the main application module which initializes the containers, loads configuration, and executes the application logic. Shows how to use dependency injection to wire together application components.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-multiple-containers.rst#_snippet_2

LANGUAGE: python
CODE:

```
../../examples/miniapps/application-multiple-containers/example/__main__.py
```

---

TITLE: Checking Container Dependencies in Python Dependency Injector
DESCRIPTION: This code snippet demonstrates how to verify container dependencies using the check_dependencies() method in a Python dependency injection container. It ensures that all dependencies are defined and defaults are set, raising an error if any are missing. The snippet emphasizes the importance of dependency completeness before container usage.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/check_dependencies.rst#_snippet_0

LANGUAGE: python
CODE:

```
import dependency_injector

container = dependency_injector.containers.DynamicContainer()

# Check all dependencies in the container
container.check_dependencies()

# The method raises an error if unresolved dependencies exist; otherwise, proceed
```

---

TITLE: Wiring Container to Modules and Packages Using container.wire() Method in Python
DESCRIPTION: Describes usage of the container.wire() method to enable wiring of container providers into specified modules or packages. Modules can be specified as import strings or already imported module objects. Packages are recursively processed for wiring. Supports relative imports resolved with optional from_package argument. Wiring patches functions and methods with markers to provide injections when called. Functions are injected with keyword arguments by default. Explicit unwiring is supported to revert patching. Wiring usage is shown for testing scenarios with unittest and pytest. Limitations of patching individually imported functions are noted.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_6

LANGUAGE: python
CODE:

```
container.wire(
    modules=[
        "yourapp.module1",
        "yourapp.module2",
    ],
)
```

LANGUAGE: python
CODE:

```
# In module "yourapp.main":

container.wire(
    modules=[
        ".module1",  # Resolved to: "yourapp.module1"
        ".module2",  # Resolved to: "yourapp.module2"
    ],
)
```

LANGUAGE: python
CODE:

```
# In module "yourapp.main":

container.wire(
    modules=[
        ".module1",  # Resolved to: "anotherapp.module1"
        ".module2",  # Resolved to: "anotherapp.module2"
    ],
    from_package="anotherapp",
)
```

LANGUAGE: python
CODE:

```
from yourapp import module1, module2


container = Container()
container.wire(modules=[module1, module2])
```

LANGUAGE: python
CODE:

```
container.wire(
    packages=[
        "yourapp.package1",
        "yourapp.package2",
    ],
)
```

LANGUAGE: python
CODE:

```
@inject
def foo(bar: Bar = Provide[Container.bar]):
    ...


container = Container()
container.wire(modules=[__name__])

foo()  # <--- Argument "bar" is injected
```

LANGUAGE: python
CODE:

```
foo()  # Equivalent to:
foo(bar=container.bar())
```

LANGUAGE: python
CODE:

```
foo(bar=Bar())  # Bar() is injected
```

LANGUAGE: python
CODE:

```
container.unwire()
```

LANGUAGE: python
CODE:

```
import unittest


class SomeTest(unittest.TestCase):

    def setUp(self):
        self.container = Container()
        self.container.wire(modules=["yourapp.module1", "yourapp.module2"])
        self.addCleanup(self.container.unwire)
```

LANGUAGE: python
CODE:

```
import pytest


@pytest.fixture
def container():
    container = Container()
    container.wire(modules=["yourapp.module1", "yourapp.module2"])
    yield container
    container.unwire()
```

---

TITLE: Injecting Dependencies into Modules and Class Attributes Using Provide with String Identifiers in Python
DESCRIPTION: Demonstrates injection of container providers into module-level variables and class attributes using Provide markers with string identifiers. This technique allows avoiding explicit container dependencies in classes or modules by assigning provider injections directly to variables or attribute annotations. Enables seamless injection especially for singleton-like services. Requires dependency-injector wiring.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_5

LANGUAGE: python
CODE:

```
service: Service = Provide["service"]


class Main:

    service: Service = Provide["service"]
```

---

TITLE: Testing FastAPI Endpoint with Dependency Overriding in Python
DESCRIPTION: Demonstrates how to test the FastAPI endpoint defined in `application.py` using `pytest` and `TestClient`. It utilizes the `container.override` context manager to replace the `Service` provided by the container with a `unittest.mock.Mock` object during the test. This allows testing the endpoint's behavior in isolation, verifying that the mocked service method (`process`) is called as expected, without requiring a real Redis instance.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-redis.rst#_snippet_5

LANGUAGE: Python
CODE:

```
"Tests module."

from unittest import mock

import pytest

from fastapi.testclient import TestClient

from .application import app
from .containers import Container
from .services import Service


@pytest.fixture
def client(container: Container) -> TestClient:
    """Test client fixture.

    Args:
        container (Container): Container instance.

    Returns:
        TestClient: Test client instance.
    """
    return TestClient(app)


@pytest.fixture
def container() -> Container:
    """Container fixture.

    Returns:
        Container: Container instance.
    """
    return app.container


def test_main_endpoint(
        client: TestClient,
        container: Container,
):
    """Test main endpoint.

    Args:
        client (TestClient): Test client instance.
        container (Container): Container instance.
    """
    service_mock = mock.AsyncMock(spec=Service)
    service_mock.process.return_value = 'foo'

    with container.service.override(service_mock):
        response = client.get('/')

    assert response.status_code == 200
    # assert response.json() == {'value': 'foo'}
    # service_mock.process.assert_called_once()

```

---

TITLE: Handling Undefined Dependency Error in Python Dependency Injector
DESCRIPTION: This Python code sample illustrates how the Dependency provider raises an error when a dependency is not provided or overridden. It features error handling around an attempt to use an undefined dependency and shows proper exception management for missing dependencies within the Dependency Injector framework. Requires dependency_injector. A correct override or provision of the dependency is necessary to avoid an exception.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/dependency.rst#_snippet_1

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    dependency = providers.Dependency()

container = Container()
try:
    obj = container.dependency()
except Exception as exc:
    print(f"Dependency not provided: {exc}")

```

---

TITLE: Defining Dependency Injection Container with Dependency Injector in Python
DESCRIPTION: Defines a DeclarativeContainer class to configure providers for an API client singleton and a service factory using the Dependency Injector framework. The container uses configuration providers to load parameters such as API key and timeout from environment variables. Dependencies are injected automatically into functions decorated with @inject via wiring. Provider overriding demonstrates how to replace a real API client with a mock for testing. This snippet requires the dependency_injector Python package and assumes ApiClient and Service classes exist. Inputs are environment variables for configuration; outputs are assembled service instances injected at runtime.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/README.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    ...


if __name__ == "__main__":
    container = Container()
    container.config.api_key.from_env("API_KEY", required=True)
    container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
    container.wire(modules=[__name__])

    main()  # <-- dependency is injected automatically

    with container.api_client.override(mock.Mock()):
        main()  # <-- overridden dependency is injected automatically
```

---

TITLE: Injecting Dependencies in FastAPI Handlers Using @inject Decorator in Python
DESCRIPTION: Shows integration of dependency-injector wiring with FastAPI route handlers. The async route function is decorated with @inject and uses the FastAPI Depends combined with Provide to specify dependencies. This example demonstrates combining FastAPI's dependency injection with the wiring feature to seamlessly inject services during request processing. Requires FastAPI and dependency-injector packages along with a properly configured Container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_1

LANGUAGE: python
CODE:

```
app = FastAPI()


@app.api_route("/")
@inject
async def index(service: Annotated[Service, Depends(Provide[Container.service])]):
    value = await service.process()
    return {"result": value}
```

---

TITLE: Injecting Dependencies Using @inject Decorator in Python
DESCRIPTION: Defines use of the @inject decorator from the dependency_injector.wiring module to inject container providers into function or method arguments. The decorator must be the very first decorator to ensure proper wiring and performance. Typical usage decorates functions with @inject and specifies dependencies via default argument values using Provide[Container.provider]. This snippet illustrates basic injection and usage with multiple decorators ensuring @inject is outermost. It requires the dependency-injector package and an existing Container class defining providers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector.wiring import inject, Provide

@inject
def foo(bar: Bar = Provide[Container.bar]):
    ...
```

LANGUAGE: python
CODE:

```
from dependency_injector.wiring import inject, Provide

@decorator_etc
@decorator_2
@decorator_1
@inject
def foo(bar: Bar = Provide[Container.bar]):
    ...
```

---

TITLE: Testing MovieLister Logic with Pytest and Dependency Injector in Python
DESCRIPTION: Implements unit tests for the MovieLister component using pytest and unittest.mock, leveraging Dependency Injector's provider overriding feature to inject a mock finder dependency. Key test functions validate correct filtering by director and year. Prerequisites are pytest and dependency_injector. Inputs are mock movie data; outputs are pytest assertions. Limitations: assumes container and providers are correctly defined elsewhere in the package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_16

LANGUAGE: python
CODE:

```
"""Tests module."""

from unittest import mock

import pytest

from .containers import Container


@pytest.fixture
def container():
    container = Container(
        config={
            "finder": {
                "type": "csv",
                "csv": {
                    "path": "/fake-movies.csv",
                    "delimiter": ",",
                },
                "sqlite": {
                    "path": "/fake-movies.db",
                },
            },
        },
    )
    return container


@pytest.fixture
def finder_mock(container):
    finder_mock = mock.Mock()
    finder_mock.find_all.return_value = [
        container.movie("The 33", 2015, "Patricia Riggen"),
        container.movie("The Jungle Book", 2016, "Jon Favreau"),
    ]

    return finder_mock


def test_movies_directed_by(container, finder_mock):
    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_directed_by("Jon Favreau")

    assert len(movies) == 1
    assert movies[0].title == "The Jungle Book"


def test_movies_released_in(container, finder_mock):
    with container.finder.override(finder_mock):
        lister = container.lister()
        movies = lister.movies_released_in(2015)

    assert len(movies) == 1
    assert movies[0].title == "The 33"
```

---

TITLE: Initializing and Shutting Down Redis Connection Pool in Python
DESCRIPTION: Defines asynchronous functions `init_redis_pool` and `shutdown_redis_pool` within the `redis.py` module to manage an `aioredis` connection pool. `init_redis_pool` creates and returns a Redis pool configured from environment variables, while `shutdown_redis_pool` closes the pool and waits for connections to terminate gracefully. These are intended for use during application startup and shutdown.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-redis.rst#_snippet_1

LANGUAGE: Python
CODE:

```
"Redis module."

import os

import aioredis


async def init_redis_pool() -> aioredis.Redis:
    """Init redis pool.

    Returns:
        aioredis.Redis: Redis pool instance.
    """
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_db = int(os.getenv('REDIS_DB', '0'))
    redis_password = os.getenv('REDIS_PASSWORD')

    return await aioredis.from_url(
        f"redis://{redis_host}:{redis_port}",
        db=redis_db,
        password=redis_password,
        encoding="utf-8",
        decode_responses=True,
    )


async def shutdown_redis_pool(redis: aioredis.Redis):
    """Shutdown redis pool.

    Args:
        redis (aioredis.Redis): Redis pool instance.
    """
    await redis.close()

```

---

TITLE: Handling Asynchronous Injections in Python Providers
DESCRIPTION: This snippet demonstrates how Python providers switch into async mode when they have awaitable dependencies, how they run multiple dependencies concurrently, and how injections are prepared asynchronously. It includes code comments and examples showing the behavior in different scenarios.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/async.rst#_snippet_0

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/async.py
   :language: python
   :emphasize-lines: 26-29
   :lines: 3-
```

---

TITLE: Using String Identifiers for Dependency Injection with Provide Marker in Python
DESCRIPTION: Shows wiring injections via string identifiers matching provider names in the container rather than direct container references. Supports nested containers with dot notation separators. Injection modifiers such as as*int(), as_float(), as*(), required(), invariant(), and provided() can be used to modify or validate the injected values. Also demonstrates special injection of the container instance using the "<container>" identifier. This approach reduces coupling with container classes and can simplify injection in some cases.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_4

LANGUAGE: python
CODE:

```
@inject
def foo(service: UserService = Provide["services.user"]) -> None:
    ...
```

LANGUAGE: python
CODE:

```
from dependency_injector.wiring import (
    inject,
    Provide,
    as_int,
    as_float,
    as_,
    required,
    invariant,
    provided,
)


@inject
def foo(value: int = Provide["config.option", as_int()]) -> None:
    ...


@inject
def foo(value: float = Provide["config.option", as_float()]) -> None:
    ...


@inject
def foo(value: Decimal = Provide["config.option", as_(Decimal)]) -> None:
    ...

@inject
def foo(value: str = Provide["config.option", required()]) -> None:
    ...

@inject
def foo(value: int = Provide["config.option", required().as_int()]) -> None:
    ...


@inject
def foo(value: int = Provide["config.option", invariant("config.switch")]) -> None:
    ...

@inject
def foo(value: int = Provide["service", provided().foo["bar"].call()]) -> None:
    ...
```

LANGUAGE: python
CODE:

```
@inject
def foo(container: Container = Provide["<container>"]) -> None:
    ...
```

---

TITLE: Test Setup with Provider Overriding in Python
DESCRIPTION: Configures tests to override specific dependencies, such as the GitHub client, with mocks using Provider overriding capabilities. This setup allows testing route handlers and business logic in isolation from external services.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/flask-blueprints.rst#_snippet_3

LANGUAGE: python
CODE:

```
# Content of githubnavigator/tests.py
# Overrides dependencies with mocks for testing
from dependency_injector import providers
from githubnavigator.containers import Container

def test_search_repos(monkeypatch):
    container = Container()
    mock_github_client = mock.MagicMock()
    mock_github_client.search_repositories.return_value = [{'name': 'mock-repo'}]
    container.github_service.override(providers.Singleton(lambda: mock_github_client))
    # Additional test setup and assertions

```

---

TITLE: Traditional Dependency Implementation in Python
DESCRIPTION: Shows how dependencies are traditionally implemented in Python with tight coupling. The ApiClient fetches configuration from environment variables, the Service directly creates ApiClient, and the main function creates Service.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/introduction/di_in_python.rst#_snippet_0

LANGUAGE: python
CODE:

```
import os


class ApiClient:

    def __init__(self) -> None:
        self.api_key = os.getenv("API_KEY")  # <-- dependency
        self.timeout = int(os.getenv("TIMEOUT"))  # <-- dependency


class Service:

    def __init__(self) -> None:
        self.api_client = ApiClient()  # <-- dependency


def main() -> None:
    service = Service()  # <-- dependency
    ...


if __name__ == "__main__":
    main()
```

---

TITLE: Creating FastAPI Application with Dependency Injection Wiring in Python
DESCRIPTION: Sets up the FastAPI application in `application.py`. It initializes the `Container`, wires it to the relevant modules (`__name__`), creates a `FastAPI` instance, and adds event handlers to initialize and shut down the Redis pool resource during application startup and shutdown. An endpoint `/` is defined, using the `@inject` decorator to receive an instance of `Service` provided by the container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-redis.rst#_snippet_4

LANGUAGE: Python
CODE:

```
"Application module."

from fastapi import FastAPI, Depends

from dependency_injector.wiring import inject, Provide

from .containers import Container
from .services import Service


@inject
def main(service: Service = Depends(Provide[Container.service])) -> dict:
    """Main endpoint handler.

    Args:
        service (Service): Injected service dependency.

    Returns:
        dict: Response data.
    """
    # value = await service.process()
    # return {'value': value}
    return {}


def create_app() -> FastAPI:
    """Create FastAPI application.

    Returns:
        FastAPI: Application instance.
    """
    container = Container()
    container.wire(modules=[__name__])

    app = FastAPI()
    app.container = container
    app.add_event_handler("startup", container.redis_pool.init)
    app.add_event_handler("shutdown", container.redis_pool.shutdown)
    app.add_api_route("/", main)
    return app


app = create_app()

```

---

TITLE: Using the Singleton Provider in Python for Dependency Injection
DESCRIPTION: This snippet demonstrates the basic usage of the `Singleton` provider in Python's dependency_injector framework. The provider ensures a single instance of an object is created and reused, if dependencies are injected during object creation. It also explains the scope being tied to the container, not global, and how specialization and abstract singletons work similarly to factories.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/singleton.rst#_snippet_0

LANGUAGE: python
CODE:

```
import dependency_injector.providers

# Creating singleton provider instance
singleton_provider = dependency_injector.providers.Singleton(SomeClass)

# Using singleton provider in a container
container = dependency_injector.containers.Container()
container.service = singleton_provider

# Accessing singleton instance
service_instance = container.service()

# Resetting singleton object if needed
singleton_provider.reset()
```

---

TITLE: Context-managed Provider Overrides in Python DeclarativeContainer
DESCRIPTION: This snippet explains using the override_providers() method as a context manager to temporarily override container providers. Providers are substituted within the with-block for testing or runtime flexibility, and the original providers are automatically restored after the block exits, ensuring isolation of overrides.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/declarative.rst#_snippet_5

LANGUAGE: python
CODE:

```
container = Container()

with container.override_providers(foo=mock.Mock(Foo), bar=mock.Mock(Bar)):
    assert isinstance(container.foo(), mock.Mock)
    assert isinstance(container.bar(), mock.Mock)

assert isinstance(container.foo(), Foo)
assert isinstance(container.bar(), Bar)
```

---

TITLE: Configuring Dependency Injector Container for User Services and Database in Python
DESCRIPTION: Defines a declarative Dependency Injector container that wires user service, user repository, and database utility components together. This container centralizes dependency management, allowing configured components to be injected cleanly across the application’s various modules.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_2

LANGUAGE: python
CODE:

```
Contents of webapp/containers.py showing container setup and component wiring
```

---

TITLE: Using Wiring Markers (Provide and Provider) for Dependency Injection in Python
DESCRIPTION: Demonstrates use of wiring markers Provide and Provider to specify injections as default argument values. Provide is typically used to inject instances produced by container providers, while Provider (or Provide with '.provider') can be used to inject the provider itself for manual instantiation. Examples show how to inject factory providers or configuration values with type annotations or without. Dependencies include dependency_injector.providers and dependency_injector.wiring modules.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_3

LANGUAGE: python
CODE:

```
from dependency_injector.providers import Factory
from dependency_injector.wiring import inject, Provide

@inject
def foo(bar_provider: Factory[Bar] = Provide[Container.bar.provider]):
    bar = bar_provider(argument="baz")
    ...
```

LANGUAGE: python
CODE:

```
from dependency_injector.providers import Factory
from dependency_injector.wiring import inject, Provider

@inject
def foo(bar_provider: Factory[Bar] = Provider[Container.bar]):
    bar = bar_provider(argument="baz")
    ...
```

LANGUAGE: python
CODE:

```
@inject
def foo(token: str = Provide[Container.config.api_token]):
    ...

@inject
def foo(timeout: int = Provide[Container.config.timeout.as_(int)]):
    ...

@inject
def foo(baz: Baz = Provide[Container.bar.provided.baz]):
    ...

@inject
def foo(bar: Bar = Provide[Container.subcontainer.bar]):
    ...
```

---

TITLE: Defining FastAPI Endpoints with Injected Services in Python
DESCRIPTION: Implements example API endpoints in the FastAPI framework which depend on a user service injected through Dependency Injector's wiring feature. This module declares routes and leverages dependency injection to decouple endpoint logic from service instantiation, enabling cleaner code and easier testing.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_1

LANGUAGE: python
CODE:

```
Contents of webapp/endpoints.py demonstrating user-related API endpoints and dependency injection
```

---

TITLE: Wiring Dynamically Imported Modules in Python
DESCRIPTION: Demonstrates how to use an import hook to automatically wire containers to dynamically imported modules.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_13

LANGUAGE: python
CODE:

```
import importlib

from dependency_injector.wiring import register_loader_containers

from .containers import Container


if __name__ == "__main__":
    container = Container()
    register_loader_containers(container)  # <--- installs import hook

    module = importlib.import_module("package.module")
    module.foo()
```

---

TITLE: Initializing FastAPI Application Factory Using Python
DESCRIPTION: Defines an application factory function that sets up the Dependency Injector container, wires it with endpoint modules, creates a FastAPI application instance, configures routes, and initializes the database if it does not exist. It serves as the entry point for creating a fully configured web application respecting dependency injection principles.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_0

LANGUAGE: python
CODE:

```
Contents of webapp/application.py (application factory implementation)
```

---

TITLE: Configuring Container Providers for API Client - Python
DESCRIPTION: Enhances the Dependency Injector container by registering configuration and factory providers for the GiphyClient. The Configuration provider loads settings from a YAML file, while the Factory provider instantiates GiphyClient with API key and timeout parameters from the configuration. This setup enables decoupled, flexible dependency management. Requires dependency-injector and a valid config.yml.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_4

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers

from . import giphy


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        timeout=config.giphy.request_timeout,
    )
```

---

TITLE: Defining Dependency Injector Container for Services - Python
DESCRIPTION: Defines a `dependency_injector.containers.DeclarativeContainer` class named `Container`. It configures a `Configuration` provider to load settings, a `Singleton` provider for the `GiphyClient` (dependent on configuration), and a `Factory` provider for the `SearchService` (dependent on the Giphy client). This centralizes dependency management for the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi.rst#_snippet_1

LANGUAGE: python
CODE:

```
# Code included from ../../examples/miniapps/fastapi/giphynavigator/containers.py
```

---

TITLE: Defining the Index Handler with aiohttp - Python
DESCRIPTION: This handler function processes incoming GET requests to the root endpoint. It extracts the 'query' and 'limit' parameters from the request, defaults these if unspecified, and returns a JSON response that includes the query, limit, and an empty list of GIFs. Dependencies include aiohttp.web. Expected input parameters are optional 'query' and 'limit' in the request URL. The handler currently returns a placeholder response with no GIF URLs.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_0

LANGUAGE: python
CODE:

```
"""Handlers module."""

from aiohttp import web


async def index(request: web.Request) -> web.Response:
    query = request.query.get("query", "Dependency Injector")
    limit = int(request.query.get("limit", 10))

    gifs = []

    return web.json_response(
        {
            "query": query,
            "limit": limit,
            "gifs": gifs,
        },
    )
```

---

TITLE: Loading Configuration from Pydantic BaseSettings Object Using Dependency Injector in Python
DESCRIPTION: Shows how to load configuration from a pydantic_settings.BaseSettings object via the from_pydantic method. The Configuration provider calls the model_dump() method of the Pydantic settings object, with optional keyword arguments to customize behavior (e.g., exclude fields). Configuration can also be loaded automatically by passing Pydantic settings instances upon provider declaration. Pydantic-settings or dependency-injector[pydantic2] package required for this functionality. Both Pydantic v1 and v2 are supported for backward compatibility.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_7

LANGUAGE: python
CODE:

```
container.config.from_pydantic(Settings(), exclude={"optional"})
```

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration(pydantic_settings=[Settings()])


if __name__ == "__main__":
    container = Container()  # Config is loaded from Settings()
```

---

TITLE: Implementing Dependency Injection in Python
DESCRIPTION: Demonstrates how to implement dependency injection by modifying classes to accept dependencies as constructor arguments rather than creating them internally, decoupling components and improving testability.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/introduction/di_in_python.rst#_snippet_1

LANGUAGE: python
CODE:

```
import os


class ApiClient:

    def __init__(self, api_key: str, timeout: int) -> None:
        self.api_key = api_key  # <-- dependency is injected
        self.timeout = timeout  # <-- dependency is injected


class Service:

    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client  # <-- dependency is injected


def main(service: Service) -> None:  # <-- dependency is injected
    ...


if __name__ == "__main__":
    main(
        service=Service(
            api_client=ApiClient(
                api_key=os.getenv("API_KEY"),
                timeout=int(os.getenv("TIMEOUT")),
            ),
        ),
    )
```

---

TITLE: Implementing Multiple Containers in Python Dependency Injector
DESCRIPTION: Defines multiple declarative containers for a Python application using Dependency Injector. Includes a main container and packages container that wire together various dependencies including database and AWS S3 clients.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-multiple-containers.rst#_snippet_1

LANGUAGE: python
CODE:

```
../../examples/miniapps/application-multiple-containers/example/containers.py
```

---

TITLE: Performing Dependency Injection in DeclarativeContainer in Python
DESCRIPTION: This snippet shows how to inject dependencies by defining providers within the declarative container. Users create container instances and obtain dependencies by calling provider attributes, supporting automatic injection patterns typical in dependency injection frameworks.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/declarative.rst#_snippet_2

LANGUAGE: python
CODE:

```
container = Container()
foo = container.foo()
bar = container.bar()
```

---

TITLE: Defining User Repository for Data Access Using SQLAlchemy in Python
DESCRIPTION: Implements user data access operations via SQLAlchemy ORM in a repository class. This module abstracts database interactions for the user model, providing query and modification methods to the user service layer.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_4

LANGUAGE: python
CODE:

```
Contents of webapp/repositories.py implementing user repository methods
```

---

TITLE: Defining Dependency Container and Providers in Python
DESCRIPTION: This Python code defines the dependency-injector container using `DeclarativeContainer`. It includes providers for loading configuration from a YAML file and factory providers for creating instances of `GiphyClient` and `SearchService`, injecting dependencies where needed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_10

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers

from . import giphy, services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        timeout=config.giphy.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        giphy_client=giphy_client,
    )
```

---

TITLE: Application Factory in Python for Flask with Dependency Injection
DESCRIPTION: Creates and configures the Flask application, initializes the dependency injection container, applies wiring for blueprints, and sets up routes. This function ensures all dependencies are wired correctly before running the app, enabling modular and testable architecture.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/flask-blueprints.rst#_snippet_2

LANGUAGE: python
CODE:

```
# Content of githubnavigator/application.py
# Creates Flask app, sets up dependency container, wiring, and routes
from flask import Flask
from dependency_injector.wiring import inject, Provide
from githubnavigator.containers import Container
from githubnavigator.blueprints.example import example_bp

def create_app() -> Flask:
    container = Container()
    container.config.from_yaml('config.yml')
    app = Flask(__name__)
    # Wiring dependencies to blueprints
    container.wire(modules=[__name__, 'githubnavigator.blueprints'])
    # Register blueprints
    app.register_blueprint(example_bp)
    return app

```

---

TITLE: Initializing Aiohttp App and Dependency Container in Python
DESCRIPTION: This Python function creates an aiohttp web application and initializes the dependency-injector container. It demonstrates loading the Giphy API key from the 'GIPHY_API_KEY' environment variable and adding application routes.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_6

LANGUAGE: python
CODE:

```
"""Application module."""

from aiohttp import web

from .containers import Container
from . import handlers


def create_app() -> web.Application:
    container = Container()
    container.config.giphy.api_key.from_env("GIPHY_API_KEY")

    app = web.Application()
    app.container = container
    app.add_routes([
        web.get("/", handlers.index),
    ])
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
```

---

TITLE: Overriding Dependency Injector Providers at Runtime in Python
DESCRIPTION: Demonstrates how to override providers in a Dependency Injector container using another container instance at runtime. This approach is useful for replacing service implementations during testing or reconfiguring dependencies for different environments. Providers in the overriding container replace those with the same names in the original container. Requires the dependency_injector package. Inputs are two containers, and outputs are the overridden container state. Limitations include the necessity for provider names to match for successful overriding.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/overriding.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class ApiClient:
    ...

class StubApiClient:
    ...

class Container(containers.DeclarativeContainer):
    api_client = providers.Singleton(ApiClient)

class TestContainer(containers.DeclarativeContainer):
    api_client = providers.Singleton(StubApiClient)

container = Container()
test_container = TestContainer()
container.override(test_container)
container.api_client()  # returns instance of StubApiClient
```

---

TITLE: Creating Custom Decorators with Dependency Injection Using @inject in Python
DESCRIPTION: Defines two example custom decorators that wrap functions and inject dependencies using the @inject decorator inside the wrapper function. Each decorator extracts injected configuration values using Provide and adds these to the decorated function's result. This pattern allows combining arbitrary decorators with dependency-injector wiring by placing @inject inside the inner wrapper, ensuring proper dependency injection. Requires functools and dependency-injector wiring module.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_2

LANGUAGE: python
CODE:

```
def decorator1(func):
    @functools.wraps(func)
    @inject
    def wrapper(value1: int = Provide[Container.config.value1]):
        result = func()
        return result + value1
    return wrapper


def decorator2(func):
    @functools.wraps(func)
    @inject
    def wrapper(value2: int = Provide[Container.config.value2]):
        result = func()
        return result + value2
    return wrapper

@decorator1
@decorator2
def sample():
    ...
```

---

TITLE: Defining Dependency Injection Container in Python
DESCRIPTION: This Python code defines a declarative container using `dependency_injector.containers` and `dependency_injector.providers`. It sets up providers for configuration from a YAML file, an HTTP client session, the Giphy API client, and the search service, making them available for injection throughout the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/aiohttp.rst#_snippet_1

LANGUAGE: python
CODE:

```
"""Containers module."""

import logging.config

import aiohttp
from dependency_injector import containers, providers

from . import giphy, services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )

    http_client = providers.Factory(
        aiohttp.ClientSession,
    )

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        http_client=http_client,
    )

    search_service = providers.Factory(
        services.SearchService,
        giphy_client=giphy_client,
    )

```

---

TITLE: Overriding GiphyClient Dependency in aiohttp Application Test (Python)
DESCRIPTION: This snippet shows how to override the GiphyClient dependency within the application container during testing. It performs an asynchronous GET request to the root endpoint, then asserts the response status code and specific fields in the JSON response, verifying the correct behavior when dependencies are mocked.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_20

LANGUAGE: Python
CODE:

```
    with app.container.giphy_client.override(giphy_client_mock):
        response = await client.get("/")

    assert response.status == 200
    data = await response.json()
    assert data["query"] == app.container.config.default.query()
    assert data["limit"] == app.container.config.default.limit()
```

---

TITLE: Accessing All Aggregated Providers as Dictionary in Python
DESCRIPTION: Shows how to retrieve a dictionary of all aggregated providers using the .providers attribute, which returns a mapping of keys to their corresponding provider instances.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/aggregate.rst#_snippet_3

LANGUAGE: python
CODE:

```
container.config_readers.providers == {
    "yaml": <YAML provider>,
    "json": <JSON provider>,
}
```

---

TITLE: Resetting Singletons in Python Dependency Injector Containers
DESCRIPTION: This snippet demonstrates how to use the .reset_singletons() method to reset all singleton instances within a container. It highlights the direct invocation of .reset_singletons() to clear singletons so that newly requested instances are created instead of cached ones. The snippet requires the Dependency Injector package and a container with singleton providers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/reset_singletons.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    service = providers.Singleton(object)

container = Container()
container.service()
container.reset_singletons()  # Resets all singletons
```

---

TITLE: Environment Variable Interpolation in Configuration Files
DESCRIPTION: Explains syntax and usage for interpolating environment variables within configuration files via the Configuration provider. Variables are represented as ${ENV_NAME} or with defaults as ${ENV_NAME:default}, enabling dynamic substitution during configuration loading. This feature supports INI, YAML, and JSON configuration formats.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_12

LANGUAGE: ini
CODE:

```
section:
  option: ${ENV_NAME}
```

LANGUAGE: ini
CODE:

```
[section]
option = ${ENV_NAME:default}
```

---

TITLE: Using Dependency Injector with Boto3 AWS Clients in Python
DESCRIPTION: This snippet demonstrates leveraging the Dependency Injector framework to manage and inject Boto3 AWS clients, such as S3, SQS, Route53, EC2, and Lambda, in a structured, testable way. It requires the 'boto3' library and 'Dependency Injector' package, and provides modular dependency configurations for AWS services, promoting clean and maintainable code.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/boto3.rst#_snippet_0

LANGUAGE: Python
CODE:

```
import boto3
from dependency_injector import containers, providers

class AwsClients(containers.DeclarativeContainer):
    s3_client = providers.Singleton(boto3.client, 's3')
    sqs_client = providers.Singleton(boto3.client, 'sqs')
    route53_client = providers.Singleton(boto3.client, 'route53')
    ec2_client = providers.Singleton(boto3.client, 'ec2')
    lambda_client = providers.Singleton(boto3.client, 'lambda')

# Usage example:
if __name__ == '__main__':
    container = AwsClients()
    s3 = container.s3_client()
    # Perform operations with the s3 client, e.g., list buckets
    buckets = s3.list_buckets()
    print(buckets)
```

---

TITLE: Implementing Handlers with Dependency Injection in Python
DESCRIPTION: Contains HTTP request handlers in handlers.py that depend on the search service and configuration options. Dependencies are injected using the wiring feature of Dependency Injector, enabling decoupled business logic from framework and infrastructure code. Handlers process REST API requests for searching GIFs and returning JSON responses. The snippet depends on the container's configured providers and Sanic routing.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/sanic.rst#_snippet_1

LANGUAGE: python
CODE:

```
Provided externally in handlers.py via literalinclude directive.
```

---

TITLE: Creating Flask Application Factory with Container Configuration
DESCRIPTION: Defines the create_app function that initializes the Flask application, sets up the container, configures GitHub authentication from environment variables, and registers routes.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_18

LANGUAGE: python
CODE:

```
"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap

from .containers import Container
from . import views


def create_app() -> Flask:
    container = Container()
    container.config.github.auth_token.from_env("GITHUB_TOKEN")

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index)

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
```

---

TITLE: Configuring Dependency Injection Container for FastAPI-Redis App in Python
DESCRIPTION: Defines a `DeclarativeContainer` named `Container` in `containers.py` using `dependency_injector`. It configures a `Resource` provider for the Redis pool, using the `init_redis_pool` function as an initializer and `shutdown_redis_pool` as a finalizer. It also defines a `Factory` provider for the `Service`, automatically injecting the `redis_pool` resource. The container specifies the modules (`.application`, `.endpoints`) where dependency injection wiring should be applied.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-redis.rst#_snippet_3

LANGUAGE: Python
CODE:

```
"Containers module."

from dependency_injector import containers, providers

from . import redis, services


class Container(containers.DeclarativeContainer):
    """Container for dependency injection.

    It wires together the dependencies for the application.
    """

    config = providers.Configuration()

    redis_pool = providers.Resource(
        redis.init_redis_pool,
    )

    service = providers.Factory(
        services.Service,
        redis=redis_pool,
    )

```

---

TITLE: Using ThreadLocalSingleton for Thread-Local Singleton in Python
DESCRIPTION: This snippet describes the usage of `ThreadLocalSingleton` which manages separate singleton instances per thread using thread-locals, perfect for multi-threaded applications requiring thread-specific singletons. It involves declaration and usage within a container context.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/singleton.rst#_snippet_4

LANGUAGE: python
CODE:

```
dependency_injector.providers.ThreadLocalSingleton

thread_local_singleton = dependency_injector.providers.ThreadLocalSingleton(SomeClass)

# Use across different threads, each will have its own singleton instance
container = dependency_injector.containers.Container()
container.thread_local_service = thread_local_singleton
```

---

TITLE: Example: Overriding Providers in Python
DESCRIPTION: Demonstrates overriding providers using `Provider.override()` and context managers in the `dependency-injector` library. It shows replacing a provider's output with another provider or a specific value (mock/stub), useful for testing or adapting configurations for different environments.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/overriding.rst#_snippet_0

LANGUAGE: python
CODE:

```
import unittest
import sqlite3
from dependency_injector import containers, providers


class ApiClient:
    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout

    def get(self) -> dict:
        # Imagine hitting a real API here
        return {'data': f'api_key={self.api_key}, timeout={self.timeout}'}


class Service:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def process(self) -> dict:
        return self.api_client.get()


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )


if __name__ == '__main__':
    container = Container()
    container.config.from_dict({'api_key': 'some-real-key', 'timeout': 10})

    # --- Overriding with another provider --- #

    class StubApiClient(ApiClient):
        def get(self) -> dict:
            return {'data': 'stub'}

    container.api_client.override(
        providers.Singleton(StubApiClient, api_key='stub-key', timeout=1),
    )

    service = container.service()
    data = service.process()
    assert data == {'data': 'stub'}
    assert isinstance(service.api_client, StubApiClient)
    assert service.api_client.api_key == 'stub-key'
    assert service.api_client.timeout == 1

    # --- Overriding with a value --- #

    class MockApiClient:
        def get(self) -> dict:
            return {'data': 'mock'}

    container.api_client.override(MockApiClient())

    service = container.service()
    data = service.process()
    assert data == {'data': 'mock'}
    assert isinstance(service.api_client, MockApiClient)

    # --- Context manager overriding --- #

    class TestApiClient(ApiClient):
        def get(self) -> dict:
            return {'data': 'test'}

    with container.api_client.override(TestApiClient('test-key', 0)):
        service = container.service()
        data = service.process()
        assert data == {'data': 'test'}
        assert isinstance(service.api_client, TestApiClient)

    # --- Overriding is reset --- #

    service = container.service()
    data = service.process()
    assert data == {'data': 'mock'}  # Previous non-context override is restored
    assert isinstance(service.api_client, MockApiClient)

    # --- Resetting the override --- #

    container.api_client.reset_override()

    service = container.service()
    data = service.process()
    assert data == {'data': 'api_key=some-real-key, timeout=10'} # Original provider
    assert isinstance(service.api_client, ApiClient)
    assert service.api_client.api_key == 'some-real-key'
    assert service.api_client.timeout == 10
```

---

TITLE: Overriding Providers at Container Instantiation in Python Dependency Injector
DESCRIPTION: This snippet illustrates overriding container providers by passing alternative implementations during container instance creation. It demonstrates modifying the provider behavior by specifying keyword arguments to substitute existing providers, allowing flexible testing or runtime modification without altering container code.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/declarative.rst#_snippet_3

LANGUAGE: python
CODE:

```
container = Container(foo=mock.Mock(Foo), bar=mock.Mock(Bar))
```

---

TITLE: Testing with Provider Overriding for Dependency Injection in Python
DESCRIPTION: Provides test cases that demonstrate usage of Dependency Injector's provider-overriding feature to replace real repository implementations with mocks. This facilitates isolated testing of services and endpoints without accessing actual databases.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_7

LANGUAGE: python
CODE:

```
Contents of webapp/tests.py highlighting provider overriding in tests at lines 25, 45, 58, 74, 86, and 97
```

---

TITLE: Implementing Scoped Singleton using Reset on Demand in Python
DESCRIPTION: This example illustrates how to implement scope control by resetting a singleton provider manually when needed, thereby creating a scoped singleton where each scope gets a fresh instance. It showcases how to reset the singleton during application runtime for controlled lifetime management.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/singleton.rst#_snippet_5

LANGUAGE: python
CODE:

```
import dependency_injector.providers

service_provider = dependency_injector.providers.Singleton(Service)

# During a particular scope, reset the singleton to create a new instance
service_provider.reset()
```

---

TITLE: Passing Arguments to Nested Underlying Factory Providers (Python)
DESCRIPTION: This snippet exemplifies passing arguments down a nested factory chain using the double-underscore (**) convention in keyword arguments. It allows for selectively targeting arguments to specific underlying providers within an object graph. It depends on Python and dependency_injector, with the nested providers constructed via Factory for each layer and accepts arguments like dependency**arg=value. Limitation: argument delegation only works through the prescribed \_\_ syntax.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_3

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_init_injections_underlying.py
   :language: python
   :lines: 3-
   :emphasize-lines: 44,49

```

---

TITLE: Creating FastAPI Application Instance and Wiring - Python
DESCRIPTION: Provides a factory function (`create_app`) responsible for initializing and configuring the FastAPI application. This involves setting up the Dependency Injector container, loading configuration (e.g., from a YAML file), wiring the container to the endpoints module to enable dependency injection, creating the `FastAPI` app instance, and registering the defined API routes.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi.rst#_snippet_3

LANGUAGE: python
CODE:

```
# Code included from ../../examples/miniapps/fastapi/giphynavigator/application.py
```

---

TITLE: Injecting Container Self using Self Provider in Python
DESCRIPTION: Demonstrates defining a container (`Container`) using `dependency_injector.containers.DeclarativeContainer`. It defines a `Self` provider, named `__self__` using `dependency_injector.providers.Self()`. This `__self__` provider is then injected as the `container` argument into the `Service` factory provider (`providers.Factory`), allowing the `Service` instance to access its parent container. Line 20 (`container=__self__,`) shows the direct injection point. Line 26 (`container=self.__self__,`) shows an alternative attribute reference (commented out in the example). The `Self` provider itself is not listed in `container.providers`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/inject_self.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers


class Service:
    def __init__(self, container):
        self.container = container


class Container(containers.DeclarativeContainer):

    # Define the Self provider. Container can have only one Self provider.
    # Usually you will use name ``__self__``.
    # You can also use different name. When you use different name container
    # will also reference defined ``Self`` provider in ``.__self__`` attribute.
    # Provider ``Self`` is not listed in container ``.providers`` attributes.
    __self__ = providers.Self()

    # Another name also works:
    # _self_ = providers.Self()

    service = providers.Factory(
        Service,
        container=__self__,  # <-- Inject container "self"
    )

    # You can also use reference via attribute:
    # service = providers.Factory(
    #     Service,
    #     container=self.__self__,  # <-- Inject container "self" via attribute reference
    # )


if __name__ == '__main__':
    container = Container()

    service_instance = container.service()

    assert isinstance(service_instance, Service)
    assert service_instance.container is container
```

---

TITLE: Implementing Asynchronous Injections in Python
DESCRIPTION: Demonstrates how to use asynchronous injections with the wiring feature, including resource providers that need initialization.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_11

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    db = providers.Resource(init_async_db_client)

    cache = providers.Resource(init_async_cache_client)


@inject
async def main(
    db: Database = Provide[Container.db],
    cache: Cache = Provide[Container.cache],
):
    ...
```

---

TITLE: Implementing FastAPI Endpoints with Injected Services - Python
DESCRIPTION: Contains FastAPI route definitions (likely using `@app.get()` decorators). It demonstrates using `Dependency Injector`'s wiring mechanism (`@containers.Container.wiring(...)`) to automatically inject the `SearchService` dependency into endpoint functions. It also shows how default values for query parameters can be related to application configuration.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi.rst#_snippet_2

LANGUAGE: python
CODE:

```
# Code included from ../../examples/miniapps/fastapi/giphynavigator/endpoints.py
```

---

TITLE: Managing Multiple Resources with Async and Sync Initializers in Python
DESCRIPTION: Shows how to initialize and shutdown multiple resources (both synchronous and asynchronous) in a container. The container methods must be awaited if at least one resource is asynchronous.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_14

LANGUAGE: python
CODE:

```
import asyncio


class Container(containers.DeclarativeContainer):

    connection1 = providers.Resource(init_async_connection)

    connection2 = providers.Resource(init_sync_connection)


async def main():
    container = Container()
    await container.init_resources()
    await container.shutdown_resources()


if __name__ == "__main__":
    asyncio.run(main())
```

---

TITLE: Defining Main Application Container in Python
DESCRIPTION: Defines the main application container responsible for wiring all components together. It reads configuration, initializes 3rd party clients (like database and S3), instantiates package containers (`UserContainer`, `PhotoContainer`, `AnalyticsContainer`), and injects the required dependencies (clients, repositories) into the respective package containers using provider overrides.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_4

LANGUAGE: python
CODE:

```
# Content of example/containers.py
# Defines the ApplicationContainer, responsible for initializing external resources
# (db, s3 based on config) and wiring package containers together.

import sqlite3
import boto3

from dependency_injector import containers, providers

from .analytics.containers import AnalyticsContainer
from .photo.containers import PhotoContainer
from .user.containers import UserContainer


class ApplicationContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    # Gateways
    database_client = providers.Singleton(
        sqlite3.connect,
        config.database.dsn,
    )

    s3_client = providers.Singleton(
        boto3.client,
        service_name='s3',
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )

    # Packages
    user_package = providers.Container(
        UserContainer,
        db=database_client,
    )

    photo_package = providers.Container(
        PhotoContainer,
        db=database_client,
        s3=s3_client,
    )

    analytics_package = providers.Container(
        AnalyticsContainer,
        user_repository=user_package.repository,
        photo_repository=photo_package.repository,
    )
```

---

TITLE: Testing with Provider Overriding in Django
DESCRIPTION: Test snippets in 'web/tests.py' demonstrate how to override providers, replacing real clients with mocks to facilitate isolated testing. The code employs provider overriding features to inject mock dependencies, ensuring tests are deterministic and independent of external services.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/django.rst#_snippet_4

LANGUAGE: Python
CODE:

```
.. literalinclude:: ../../examples/miniapps/django/web/tests.py
   :language: python
   :emphasize-lines: 39,60
```

---

TITLE: Injecting Dependencies into Flask View Function
DESCRIPTION: Updates the index view function to use dependency injection for obtaining the SearchService instance. This demonstrates how to use the Dependency Injector's wiring feature in a Flask application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_21

LANGUAGE: python
CODE:

```
"""Views module."""

from flask import request, render_template
from dependency_injector.wiring import inject, Provide

from .services import SearchService
from .containers import Container


@inject
def index(search_service: SearchService = Provide[Container.search_service]):
    query = request.args.get("query", "Dependency Injector")
    limit = request.args.get("limit", 10, int)

    repositories = search_service.search_repositories(query, limit)

    return render_template(
        "index.html",
        query=query,
        limit=limit,
        repositories=repositories,
    )
```

---

TITLE: Testing Aiohttp Application with Dependency Overriding in Python
DESCRIPTION: This Python code showcases asynchronous unit tests for the Aiohttp application using `unittest` and `aiohttp.test_utils`. It demonstrates how to use the `override` context manager from the dependency container (`app.container`) to replace the actual `giphy_client` provider with a mock object (`AsyncMock`) during testing, allowing isolated testing of the handler logic.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/aiohttp.rst#_snippet_4

LANGUAGE: python
CODE:

```
"""Tests module."""

import unittest
from unittest.mock import AsyncMock, Mock, patch

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from .application import create_app
from .containers import Container


class ApplicationTestCase(AioHTTPTestCase):

    async def get_application(self):
        """Retrieve web application in test mode."""
        return create_app()

    @unittest_run_loop
    async def test_index(self):
        """Test index page."""
        giphy_client_mock = AsyncMock()
        giphy_client_mock.search.return_value = [{"id": 1}, {"id": 2}]

        with self.app.container.giphy_client.override(giphy_client_mock):
            response = await self.client.request("GET", "/")

        self.assertEqual(response.status, 200)

        response_data = await response.json()
        self.assertEqual(response_data, {
            "query": "cats",
            "gifs": [
                {"id": 1},
                {"id": 2},
            ],
        })

        giphy_client_mock.search.assert_called_once_with("cats", 3)

    @unittest_run_loop
    async def test_index_with_query(self):
        """Test index page with query."""
        giphy_client_mock = AsyncMock()
        giphy_client_mock.search.return_value = [{"id": 1}]

        with self.app.container.giphy_client.override(giphy_client_mock):
            response = await self.client.request("GET", "/?query=dogs")

        self.assertEqual(response.status, 200)

        response_data = await response.json()
        self.assertEqual(response_data, {
            "query": "dogs",
            "gifs": [
                {"id": 1},
            ],
        })

        giphy_client_mock.search.assert_called_once_with("dogs", 3)

    def test_openapi_spec(self):
        """Test openapi spec availability."""
        self.assertTrue(self.app.container.config.giphy.api_key())


if __name__ == "__main__":
    unittest.main()

```

---

TITLE: Provider Delegation with .provider Attribute in dependency_injector (Python)
DESCRIPTION: This snippet demonstrates injecting the provider instance itself instead of its result using the .provider attribute. This is used when an object requires access to a provider for later or conditional use, rather than a ready-made dependency. Requires Python and dependency_injector; .provider is available on all providers. The injected object has direct access to the provider for further operations.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_4

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_delegation.py
   :language: python
   :lines: 3-
   :emphasize-lines: 28

```

---

TITLE: Creating Objects with Factory Provider in dependency_injector (Python)
DESCRIPTION: This snippet demonstrates the initialization of a Factory provider with a class, factory function, or method. The Factory provider injects dependencies into the created object or callable. Dependencies can be other providers or literal values, and are injected every time a new object instance is created. Requires Python and the dependency_injector.providers module; accepts any class or function as the first argument, followed by dependencies as positional or keyword arguments.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_0

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory.py
   :language: python
   :lines: 3-

```

---

TITLE: Creating Dependency Injector Container with GitHub API Client
DESCRIPTION: Defines a container for dependency injection that includes a GitHub client configuration. The container uses Factory and Configuration providers to manage dependencies and application settings.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_15

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers
from github import Github


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    github_client = providers.Factory(
        Github,
        login_or_token=config.github.auth_token,
        timeout=config.github.request_timeout,
    )
```

---

TITLE: Loading Configuration from Environment Variables Using Dependency Injector in Python
DESCRIPTION: Shows how to load configuration options from environment variables using from*env method. Supports type casting via the as* argument to convert string environment variables to desired types (str, float, int). Parameters include the environment variable name, type casting, default values, and whether the variable is required. This method ensures typesafety and allows default fallback values when environment variables are absent.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_9

LANGUAGE: python
CODE:

```
# API_KEY=secret
container.config.api_key.from_env("API_KEY", as_=str, required=True)
assert container.config.api_key() == "secret"

# SAMPLING_RATIO=0.5
container.config.sampling.from_env("SAMPLING_RATIO", as_=float, required=True)
assert container.config.sampling() == 0.5

# TIMEOUT undefined, default is used
container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
assert container.config.timeout() == 5
```

---

TITLE: Argument Passing and Priority in Chained Factories using Dependency Injector
DESCRIPTION: This snippet demonstrates different strategies for passing arguments through nested Factory providers, highlighting how keyword arguments are propagated and how upper-level arguments can override lower-level ones. It also shows how context-provided arguments have the highest priority. These examples are useful for controlling argument precedence in complex factory chains.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/chained-factories.rst#_snippet_1

LANGUAGE: Python
CODE:

```
   # 1. Keyword arguments of upper level factory are added to lower level factory
   chained_dict_factory = providers.Factory(
       providers.Factory(dict, arg1=1),
       arg2=2,
   )
   print(chained_dict_factory())  # prints: {"arg1": 1, "arg2": 2}

   # 2. Keyword arguments of upper level factory have priority
   chained_dict_factory = providers.Factory(
       providers.Factory(dict, arg1=1),
       arg1=2,
   )
   print(chained_dict_factory())  # prints: {"arg1": 2}

   # 3. Keyword arguments provided from context have the most priority
   chained_dict_factory = providers.Factory(
       providers.Factory(dict, arg1=1),
       arg1=2,
   )
   print(chained_dict_factory(arg1=3))  # prints: {"arg1": 3}
```

---

TITLE: Defining a Dependency Injection Container in Python
DESCRIPTION: Reference to the Python code in `example/containers.py`. This file defines a single declarative container using `dependency_injector`. It sets up providers for configuration (read from INI files), AWS Boto3 resources, a database connection, and application services, wiring them together.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-single-container.rst#_snippet_1

LANGUAGE: python
CODE:

```
# Source: examples/miniapps/application-single-container/example/containers.py
# Defines the dependency injection container using dependency_injector.
# Configures providers for settings, AWS, database, and services.
```

---

TITLE: Restricting Provider Types in DynamicContainer (Python)
DESCRIPTION: Shows how to specialize a DynamicContainer by passing the `provider_type` argument during instantiation. This ensures that any provider assigned to the container later must be a subtype of the specified `ServiceProvider`. Assigning an incompatible provider (like `providers.Factory(dict)`) will raise an error.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/specialization.rst#_snippet_1

LANGUAGE: python
CODE:

```
# examples/containers/dynamic_provider_type.py
import abc

from dependency_injector import containers, providers


# Define an abstract base class for specific provider types
class ServiceProvider(providers.Provider):
    __metaclass__ = abc.ABCMeta


# Concrete provider types inheriting from the base
class SingletonServiceProvider(ServiceProvider, providers.Singleton):
    pass


class FactoryServiceProvider(ServiceProvider, providers.Factory):
    pass


# Example service class
class Service:
    pass


# Dynamic container with provider type restriction via argument
container = containers.DynamicContainer(
    provider_type=ServiceProvider,  # Enforce provider type
)

container.provider1 = SingletonServiceProvider(Service)
container.provider2 = FactoryServiceProvider(Service)

# The following assignment would cause a TypeError
# container.other_provider = providers.Factory(dict)


# --- Usage Example (not shown in original emphasis) ---
# assert isinstance(container.provider1, SingletonServiceProvider)
# assert isinstance(container.provider2, FactoryServiceProvider)
```

---

TITLE: Using Non-String Keys or Special String Keys in Aggregate Provider
DESCRIPTION: Demonstrates how to use non-string keys or string keys containing periods and dashes with an Aggregate provider by providing a dictionary as a positional argument.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/aggregate.rst#_snippet_4

LANGUAGE: python
CODE:

```
aggregate = providers.Aggregate({
    SomeClass: providers.Factory(...),
    "key.with.periods": providers.Factory(...),
    "key-with-dashes": providers.Factory(...),
})
```

---

TITLE: Defining Dependency Injection Container in Python
DESCRIPTION: The container setup defines providers and dependencies for the Django application, facilitating modular injection of services throughout the app. It is located in 'githubnavigator/containers.py' and uses Dependency Injector's container class. This setup enables declarative dependency injection, promoting testability and separation of concerns.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/django.rst#_snippet_0

LANGUAGE: Python
CODE:

```
.. literalinclude:: ../../examples/miniapps/django/githubnavigator/containers.py
   :language: python
```

---

TITLE: Declaring Dependency Injection Container with Python
DESCRIPTION: Defines a declarative container in the containers.py file leveraging Dependency Injector to manage application dependencies. This container configures service providers, configuration loading, and wiring to inject dependencies into modules such as handlers. Required dependencies include the Dependency Injector library. The container outputs service instances to be injected throughout the Sanic application, facilitating loose coupling and easier testing.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/sanic.rst#_snippet_0

LANGUAGE: python
CODE:

```
Provided externally in containers.py via literalinclude directive.
```

---

TITLE: Overriding Async Providers with Non-Awaitable Results
DESCRIPTION: This snippet illustrates how asynchronous providers are overridden by non-async providers, with the framework wrapping non-awaitable results into awaitables to maintain async behavior consistency during overrides. The code provides an example using the same include syntax with specific lines emphasized.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/async.rst#_snippet_1

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/async_overriding.py
   :language: python
   :emphasize-lines: 19-24
   :lines: 3-
```

---

TITLE: Defining Dependencies in Dependency Injector Container (Python)
DESCRIPTION: This Python snippet demonstrates defining application component dependencies within a Dependency Injector container using `providers.Factory` and `providers.List`. It shows how an `HttpClient` is created as a factory, and two `HttpMonitor` instances depend on this factory and configuration options. A `Dispatcher` is then configured to receive a list of these monitor instances via `providers.List`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_19

LANGUAGE: python
CODE:

```
           format=config.log.format,
       )

       http_client = providers.Factory(http.HttpClient)

       example_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.example,
       )

       httpbin_monitor = providers.Factory(
           monitors.HttpMonitor,
           http_client=http_client,
           options=config.monitors.httpbin,
       )

       dispatcher = providers.Factory(
           dispatcher.Dispatcher,
           monitors=providers.List(
               example_monitor,
               httpbin_monitor,
           ),
       )
```

---

TITLE: Configuring and Running Main with Dependency Injector in Python
DESCRIPTION: Defines the main CLI application entrypoint using Dependency Injector's wiring capabilities. The code reads provider switch values from environment variables, sets up dependency injection wiring, and executes 'main()' which prints movies by director and year. Requires 'dependency_injector' and appropriate provider configuration. 'MOVIE_FINDER_TYPE' environment variable selects the storage type ('csv' or 'sqlite'); main expects configured containers, listers and finder providers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_13

LANGUAGE: python
CODE:

```
"""Main module."""

from dependency_injector.wiring import Provide, inject

from .listers import MovieLister
from .containers import Container


@inject
def main(lister: MovieLister = Provide[Container.lister]) -> None:
    print("Francis Lawrence movies:")
    for movie in lister.movies_directed_by("Francis Lawrence"):
        print("\t-", movie)

    print("2016 movies:")
    for movie in lister.movies_released_in(2016):
        print("\t-", movie)


if __name__ == "__main__":
    container = Container()
    container.config.finder.type.from_env("MOVIE_FINDER_TYPE")
    container.wire(modules=[sys.modules[__name__]])

    main()
```

---

TITLE: Testing Daemon Components with Pytest and Mocks (Python)
DESCRIPTION: This Python snippet contains unit tests for the monitoring daemon components using pytest and `unittest.mock`. It includes a dataclass for mocking HTTP requests, a pytest fixture to provide a Dependency Injector container configured with mock values, and two async test functions (`test_example_monitor` and `test_dispatcher`) that demonstrate overriding specific providers in the container with mock objects to isolate and test components.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_24

LANGUAGE: python
CODE:

```
さんも
"""Tests module."""

import asyncio
import dataclasses
from unittest import mock

import pytest

from .containers import Container


@dataclasses.dataclass
class RequestStub:
    status: int
    content_length: int


@pytest.fixture
def container():
    return Container(
        config={
            "log": {
                "level": "INFO",
                "formant": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            },
            "monitors": {
                "example": {
                    "method": "GET",
                    "url": "http://fake-example.com",
                    "timeout": 1,
                    "check_every": 1,
                },
                "httpbin": {
                    "method": "GET",
                    "url": "https://fake-httpbin.org/get",
                    "timeout": 1,
                    "check_every": 1,
                },
            },
        }
    )


@pytest.mark.asyncio
async def test_example_monitor(container, caplog):
    caplog.set_level("INFO")

    http_client_mock = mock.AsyncMock()
    http_client_mock.request.return_value = RequestStub(
        status=200,
        content_length=635,
    )

    with container.http_client.override(http_client_mock):
        example_monitor = container.example_monitor()
        await example_monitor.check()

    assert "http://fake-example.com" in caplog.text
    assert "response code: 200" in caplog.text
    assert "content length: 635" in caplog.text


@pytest.mark.asyncio
async def test_dispatcher(container, caplog, event_loop):
    caplog.set_level("INFO")

    example_monitor_mock = mock.AsyncMock()
    httpbin_monitor_mock = mock.AsyncMock()

    with container.override_providers(
            example_monitor=example_monitor_mock,
            httpbin_monitor=httpbin_monitor_mock,
    ):
        dispatcher = container.dispatcher()
        event_loop.create_task(dispatcher.start())
        await asyncio.sleep(0.1)
        dispatcher.stop()

    assert example_monitor_mock.check.called
    assert httpbin_monitor_mock.check.called
```

---

TITLE: Creating the aiohttp Application Factory - Python
DESCRIPTION: This snippet initializes the aiohttp web application and configures routing and dependency injection. It sets up the container, registers the root endpoint with the index handler, and includes a main block to run the app. Prerequisites include aiohttp and dependency-injector, and it expects the handlers and container modules to be correctly implemented. The output is a running aiohttp server exposed on the configured port.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_2

LANGUAGE: python
CODE:

```
"""Application module."""

from aiohttp import web

from .containers import Container
from . import handlers


def create_app() -> web.Application:
    container = Container()

    app = web.Application()
    app.container = container
    app.add_routes([
        web.get("/", handlers.index),
    ])
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
```

---

TITLE: Specifying Mandatory Configuration Sources (Python)
DESCRIPTION: Demonstrates how to mark various configuration sources (YAML file, INI file, dictionary, environment variable) as mandatory using the `required=True` argument in the `from_*` methods. This causes an error to be raised if the specified source does not exist or is undefined.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_16

LANGUAGE: python
CODE:

```
container.config.from_yaml("config.yaml", required=True)
```

LANGUAGE: python
CODE:

```
container.config.from_ini("config.ini", required=True)
```

LANGUAGE: python
CODE:

```
container.config.from_dict(config_dict, required=True)
```

LANGUAGE: python
CODE:

```
container.config.api_key.from_env("API_KEY", required=True)
```

---

TITLE: Providing Default Value for Dependency in Python Dependency Injector
DESCRIPTION: This Python snippet shows how to supply a default value or provider to the Dependency provider using the default argument. If the default is a standard value, the Dependency provider wraps it in an Object provider. This example demonstrates both basic usage and how the provider resolves dependencies to the default when not otherwise overridden. It depends on dependency_injector.providers and works for any type that can be wrapped as an object.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/dependency.rst#_snippet_2

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    dependency = providers.Dependency(default=42)

container = Container()
value = container.dependency()
print(value)  # Output: 42

```

---

TITLE: Aggregating Factory Providers with Non-string Keys with FactoryAggregate (Python)
DESCRIPTION: This snippet explains providing a dictionary to FactoryAggregate to support non-string or special string keys (such as keys containing . or -). It enhances flexibility in mapping classes or complex names to specific factories. Dependencies are as in the main FactoryAggregate usage; constraints include key uniqueness and support for various key types, with dictionary access required for non-standard keys.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_8

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_aggregate_non_string_keys.py
   :language: python
   :lines: 3-
   :emphasize-lines: 30-33,39-40

```

---

TITLE: Demonstrating the Object Provider in Python
DESCRIPTION: This Python example showcases the Object provider from the dependency_injector library. It demonstrates how to create an Object provider initialized with a specific object (e.g., sys.stdout) and retrieve that same object instance using the provider. It depends on the 'dependency_injector' library.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/object.rst#_snippet_0

LANGUAGE: python
CODE:

```
# example based on the description and literalinclude directive

import sys
import dependency_injector.providers as providers

# The Object provider returns the provided object "as is"
stdout_provider = providers.Object(sys.stdout)

# Retrieving the object from the provider
stdout_instance = stdout_provider()

# Verifying that the retrieved instance is the original object
assert stdout_instance is sys.stdout

print(f"Successfully retrieved object: {stdout_instance}")
```

---

TITLE: Configuring Automatic Wiring with DeclarativeContainer in Python
DESCRIPTION: Shows how to define a wiring configuration in a container class to automatically wire modules and packages when the container is instantiated.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_8

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "yourapp.module1",
            "yourapp.module2",
        ],
        packages=[
            "yourapp.package1",
            "yourapp.package2",
        ],
    )

    ...


if __name__ == "__main__":
    container = Container()  # container.wire() is called automatically
    ...
```

---

TITLE: Writing Pytest Tests with Dependency Overriding - Python
DESCRIPTION: This Python snippet contains `pytest` test code for the Flask application's views. It includes a fixture `app` to create and yield the Flask application instance, ensuring the Dependency Injector container is unwired afterwards. The test functions (`test_index`, `test_index_no_results`) demonstrate how to mock external dependencies (specifically the `Github` client) using `unittest.mock` and override the corresponding provider in the Dependency Injector container for testing purposes. Assertions check the response status code and content.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_27

LANGUAGE: python
CODE:

```
"""Tests module."""

from unittest import mock

import pytest
from github import Github
from flask import url_for

from .application import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()


def test_index(client, app):
    github_client_mock = mock.Mock(spec=Github)
    github_client_mock.search_repositories.return_value = [
        mock.Mock(
            html_url="repo1-url",
            name="repo1-name",
            owner=mock.Mock(
                login="owner1-login",
                html_url="owner1-url",
                avatar_url="owner1-avatar-url",
            ),
            get_commits=mock.Mock(return_value=[mock.Mock()]),
        ),
        mock.Mock(
            html_url="repo2-url",
            name="repo2-name",
            owner=mock.Mock(
                login="owner2-login",
                html_url="owner2-url",
                avatar_url="owner2-avatar-url",
            ),
            get_commits=mock.Mock(return_value=[mock.Mock()]),
        ),
    ]

    with app.container.github_client.override(github_client_mock):
        response = client.get(url_for("index"))

    assert response.status_code == 200
    assert b"Results found: 2" in response.data

    assert b"repo1-url" in response.data
    assert b"repo1-name" in response.data
    assert b"owner1-login" in response.data
    assert b"owner1-url" in response.data
    assert b"owner1-avatar-url" in response.data

    assert b"repo2-url" in response.data
    assert b"repo2-name" in response.data
    assert b"owner2-login" in response.data
    assert b"owner2-url" in response.data
    assert b"owner2-avatar-url" in response.data


def test_index_no_results(client, app):
    github_client_mock = mock.Mock(spec=Github)
    github_client_mock.search_repositories.return_value = []

    with app.container.github_client.override(github_client_mock):
        response = client.get(url_for("index"))

    assert response.status_code == 200
    assert b"Results found: 0" in response.data
```

---

TITLE: Defining Analytics Package Container in Python
DESCRIPTION: Defines the container for the 'analytics' package using Dependency Injector. It declares dependencies on the `UserRepository` and `PhotoRepository` from other packages using `providers.Dependency`. It provides an `AnalyticsService` factory that utilizes these repositories, demonstrating inter-package dependency injection.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_3

LANGUAGE: python
CODE:

```
# Content of example/analytics/containers.py
# Defines the AnalyticsContainer, declaring dependencies on 'user_repository'
# and 'photo_repository' from other packages, and providing an AnalyticsService factory.

from dependency_injector import containers, providers

from . import services


class AnalyticsContainer(containers.DeclarativeContainer):

    user_repository = providers.Dependency()
    photo_repository = providers.Dependency()

    service = providers.Factory(
        services.AnalyticsService,
        user_repository=user_repository,
        photo_repository=photo_repository,
    )
```

---

TITLE: Enhanced DI Container with Both Finders
DESCRIPTION: Updates the Container class to support both CSV and SQLite finders, defaulting to the SQLite implementation.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_10

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers

from . import finders, listers, entities


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    movie = providers.Factory(entities.Movie)

    csv_finder = providers.Singleton(
        finders.CsvMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    sqlite_finder = providers.Singleton(
        finders.SqliteMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.sqlite.path,
    )

    lister = providers.Factory(
        listers.MovieLister,
        movie_finder=sqlite_finder,
    )

```

---

TITLE: Creating Aiohttp Application Factory with Dependency Injection in Python
DESCRIPTION: This Python code defines a `create_app` function that acts as an application factory. It initializes the dependency container, wires the container to the `handlers` module to enable automatic dependency injection, creates the `aiohttp.web.Application` instance, and sets up the routes, associating the `/` path with the `index` handler.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/aiohttp.rst#_snippet_3

LANGUAGE: python
CODE:

```
"""Application module."""

from aiohttp import web

from . import handlers
from .containers import Container


def create_app() -> web.Application:
    container = Container()
    container.wire(modules=[handlers])

    app = web.Application()
    app.container = container
    app.add_routes([
        web.get("/", handlers.index),
    ])
    return app

```

---

TITLE: Overriding Strict Mode Behavior with `required=False` (Python)
DESCRIPTION: Shows how to load optional configuration files even when the Configuration provider is in strict mode by explicitly setting `required=False` in the `from_yaml` method call.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_22

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)


if __name__ == "__main__":
    container = Container()

    container.config.from_yaml("config.yml")
    container.config.from_yaml("config.local.yml", required=False)
```

---

TITLE: Resource Subclass without Return Value in Python
DESCRIPTION: Demonstrates a resource subclass implementation that doesn't return a resource object. The shutdown method will still be called with None as the first argument.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_8

LANGUAGE: python
CODE:

```
from dependency_injector import resources


class MyResource(resources.Resource):

    def init(self, argument1=..., argument2=...) -> None:
        # initialization
        ...

    def shutdown(self, _: None) -> None:
        # shutdown
        ...
```

---

TITLE: Build Docker Image using Docker Compose
DESCRIPTION: This command builds the Docker image for the application as defined in the `docker-compose.yml` file. It prepares the container environment needed to run the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
docker compose build
```

---

TITLE: Implementing Aiohttp Handlers with Injected Dependencies in Python
DESCRIPTION: This Python snippet demonstrates Aiohttp request handlers (`index`). Dependencies like the `SearchService` and configuration values (`results_per_page`) are injected into the handler functions using the `@inject` decorator and `Provide` markers from the `dependency_injector.wiring` module. The handler searches for GIFs based on a query parameter and renders a template.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/aiohttp.rst#_snippet_2

LANGUAGE: python
CODE:

```
"""Handlers module."""

from aiohttp import web
from dependency_injector.wiring import inject, Provide

from .containers import Container
from .services import SearchService


@inject
async def index(
        request: web.Request,
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        results_per_page: int = Provide[Container.config.default.results_per_page],
) -> web.Response:
    query = request.query.get("query", default_query)
    gifs = await search_service.search(query, results_per_page)
    return web.json_response({
        "query": query,
        "gifs": gifs,
    })

```

---

TITLE: Implementing `HttpMonitor` for HTTP Availability Checks
DESCRIPTION: Defines an `HttpMonitor` class inheriting from `Monitor`, utilizing `HttpClient` to send GET requests to specified URLs. It records response status, content length, and request duration, logging detailed info. The monitor is instantiated with options dicts containing HTTP method, URL, timeout, and check interval, supporting asynchronous health checks.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_15

LANGUAGE: Python
CODE:

```
"""Monitors module."""

import logging
import time
from typing import Dict, Any

from .http import HttpClient


class Monitor:

    def __init__(self, check_every: int) -> None:
        self.check_every = check_every
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()


class HttpMonitor(Monitor):

    def __init__(
            self,
            http_client: HttpClient,
            options: Dict[str, Any],
    ) -> None:
        self._client = http_client
        self._method = options.pop("method")
        self._url = options.pop("url")
        self._timeout = options.pop("timeout")
        super().__init__(check_every=options.pop("check_every"))

    async def check(self) -> None:
        time_start = time.time()

        response = await self._client.request(
            method=self._method,
            url=self._url,
            timeout=self._timeout,
        )

        time_end = time.time()
        time_took = time_end - time_start

        self.logger.info(
            "Check\n"
            "    %s %s\n"
            "    response code: %s\n"
            "    content length: %s\n"
            "    request took: %s seconds",
            self._method,
            self._url,
            response.status,
            response.content_length,
            round(time_took, 3)
        )
```

---

TITLE: Adding SearchService to Container and Setting Up Wiring
DESCRIPTION: Updates the container to include the SearchService and configures automatic wiring with the views module. This allows for dependency injection into the view functions.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_20

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers
from github import Github

from . import services


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".views"])

    config = providers.Configuration(yaml_files=["config.yml"])

    github_client = providers.Factory(
        Github,
        login_or_token=config.github.auth_token,
        timeout=config.github.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        github_client=github_client,
    )
```

---

TITLE: Implementing Movie Finders with CSV and SQLite Support
DESCRIPTION: Defines abstract MovieFinder interface and two concrete implementations: CsvMovieFinder and SqliteMovieFinder for different data sources.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_9

LANGUAGE: python
CODE:

```
"""Movie finders module."""

import csv
import sqlite3
from typing import Callable, List

from .entities import Movie


class MovieFinder:

    def __init__(self, movie_factory: Callable[..., Movie]) -> None:
        self._movie_factory = movie_factory

    def find_all(self) -> List[Movie]:
        raise NotImplementedError()


class CsvMovieFinder(MovieFinder):

    def __init__(
            self,
            movie_factory: Callable[..., Movie],
            path: str,
            delimiter: str,
    ) -> None:
        self._csv_file_path = path
        self._delimiter = delimiter
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with open(self._csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [self._movie_factory(*row) for row in csv_reader]


class SqliteMovieFinder(MovieFinder):

    def __init__(
            self,
            movie_factory: Callable[..., Movie],
            path: str,
    ) -> None:
        self._database = sqlite3.connect(path)
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with self._database as db:
            rows = db.execute("SELECT title, year, director FROM movies")
            return [self._movie_factory(*row) for row in rows]

```

---

TITLE: Example Test Execution and Coverage Output
DESCRIPTION: Shows the expected console output when running the test command. This includes pytest status information (platform, plugins, number of tests collected and passed) followed by a detailed code coverage report table.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/README.rst#_snippet_4

LANGUAGE: text
CODE:

```
platform linux -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0
rootdir: /code
plugins: cov-6.0.0, anyio-4.7.0
collected 7 items

webapp/tests.py .......                                         [100%]

---------- coverage: platform linux, python 3.10.0-final-0 ----------
Name                     Stmts   Miss  Cover
--------------------------------------------
webapp/__init__.py           0      0   100%
webapp/application.py       12      0   100%
webapp/containers.py        10      0   100%
webapp/database.py          24      8    67%
webapp/endpoints.py         32      0   100%
webapp/models.py            10      1    90%
webapp/repositories.py      36     20    44%
webapp/services.py          16      0   100%
webapp/tests.py             59      0   100%
--------------------------------------------
TOTAL                      199     29    85%
```

---

TITLE: Defining DeclarativeContainer with Providers in Python
DESCRIPTION: This snippet illustrates how to create a declarative container class by subclassing DeclarativeContainer and defining providers as class attributes. This approach requires creating the container instance to access providers properly. It emphasizes that providers should not be accessed or modified on the class-level after instantiation to avoid affecting all container instances.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/declarative.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    foo = providers.Factory(Foo)
    bar = providers.Singleton(Bar)
```

---

TITLE: Specifying Configuration Value Types (Python)
DESCRIPTION: Illustrates how to explicitly specify the data type of a configuration value using helper methods like `.as_int()` and `.as_float()`. This is particularly useful when reading values from INI files or environment variables which are typically strings.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_17

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 19
```

---

TITLE: Resetting Singleton with Full Reset Method in Python
DESCRIPTION: This snippet shows how to perform a full reset of the singleton, including dependent providers, using the `full_reset()` method. It supports the context manager pattern to automatically manage the reset within a defined scope.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/singleton.rst#_snippet_2

LANGUAGE: python
CODE:

```
with container.service.full_reset():
    # All dependent singleton objects are reset here
    pass
```

---

TITLE: Basic Resource Provider Implementation in Python
DESCRIPTION: Demonstrates how to implement a resource provider for thread pool management. The resource provider initializes a thread pool with a specified number of workers and manages its lifecycle.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_0

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    thread_pool = providers.Resource(
        init_thread_pool,
        max_workers=config.max_workers,
    )

    dispatcher = providers.Factory(
        TaskDispatcher,
        executor=thread_pool,
    )
```

---

TITLE: Implementing the Asynchronous Dispatcher for Monitors - Python
DESCRIPTION: Defines the dispatcher.py module, which provides the Dispatcher class to orchestrate and supervise multiple Monitor instances. The Dispatcher schedules and runs monitor checks concurrently using asyncio, and handles graceful shutdown on SIGTERM or SIGINT signals. Key parameters include a list of Monitor objects. Limitations: cancellation and shutdown logic does not handle errors during monitor execution, and requires event loop signal support (not available on Windows).
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_8

LANGUAGE: python
CODE:

```
"""Dispatcher module."""

import asyncio
import logging
import signal
import time
from typing import List

from .monitors import Monitor


class Dispatcher:

    def __init__(self, monitors: List[Monitor]) -> None:
        self._monitors = monitors
        self._monitor_tasks: List[asyncio.Task] = []
        self._logger = logging.getLogger(self.__class__.__name__)
        self._stopping = False

    def run(self) -> None:
        asyncio.run(self.start())

    async def start(self) -> None:
        self._logger.info("Starting up")

        for monitor in self._monitors:
            self._monitor_tasks.append(
                asyncio.create_task(self._run_monitor(monitor)),
            )

        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
        asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)

        await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

        self.stop()

    def stop(self) -> None:
        if self._stopping:
            return

        self._stopping = True

        self._logger.info("Shutting down")
        for task, monitor in zip(self._monitor_tasks, self._monitors):
            task.cancel()
        self._monitor_tasks.clear()
        self._logger.info("Shutdown finished successfully")
```

---

TITLE: Running the Aiohttp Application in Bash
DESCRIPTION: This Bash command executes the application module, starting the aiohttp web server. Ensure you are in the project's root directory and have activated your virtual environment if using one.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_13

LANGUAGE: bash
CODE:

```
python -m giphynavigator.application
```

---

TITLE: Loading Configuration from Python Dictionary Using Dependency Injector in Python
DESCRIPTION: Illustration of loading configuration from an in-memory Python dictionary using from_dict method on the Configuration provider. Enables dynamic programmatic configuration setup without external files.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_8

LANGUAGE: python
CODE:

```
# Example usage (content omitted for brevity)
container.config.from_dict({...})
```

---

TITLE: Listing Django Views with Dependency Injection
DESCRIPTION: The views in 'web/views.py' utilize dependencies such as search services injected via wiring, enabling decoupled and testable request handlers. This code demonstrates how to annotate and wire dependencies into Django views, thus integrating dependency injection with Django's request handling system.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/django.rst#_snippet_2

LANGUAGE: Python
CODE:

```
.. literalinclude:: ../../examples/miniapps/django/web/views.py
   :language: python
```

---

TITLE: Demonstrating Argument Priority in Factory of Factories Pattern
DESCRIPTION: Shows how argument priority works in nested factories. Demonstrates the precedence rules for keyword arguments in upper level factories, lower level factories, and context arguments.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/factory-of-factories.rst#_snippet_1

LANGUAGE: python
CODE:

```
# 1. Keyword arguments of upper level factory are added to lower level factory
factory_of_dict_factories = providers.Factory(
    providers.Factory,
    dict,
    arg1=1,
)
dict_factory = factory_of_dict_factories(arg2=2)
print(dict_factory())  # prints: {"arg1": 1, "arg2": 2}

# 2. Keyword arguments of upper level factory have priority
factory_of_dict_factories = providers.Factory(
    providers.Factory,
    dict,
    arg1=1,
)
dict_factory = factory_of_dict_factories(arg1=2)
print(dict_factory())  # prints: {"arg1": 2}

# 3. Keyword arguments provided from context have the most priority
factory_of_dict_factories = providers.Factory(
    providers.Factory,
    dict,
    arg1=1,
)
dict_factory = factory_of_dict_factories(arg1=2)
print(dict_factory(arg1=3))  # prints: {"arg1": 3}
```

---

TITLE: Container Resource Management in Python
DESCRIPTION: Shows how to initialize and shutdown all resources in a container at once. This pattern is useful for managing multiple resources with a single command.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_1

LANGUAGE: python
CODE:

```
container = Container()
container.init_resources()
container.shutdown_resources()
```

---

TITLE: Running the Python CLI App with Environment Variable
DESCRIPTION: Shows bash commands to run the Python CLI app by setting the 'MOVIE_FINDER_TYPE' environment variable to specify which storage provider ('csv' or 'sqlite') to use. Requires the Python application, and the 'movies' module must be importable as a module. Input is environment variable; output is printed movie lists.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_14

LANGUAGE: bash
CODE:

```
MOVIE_FINDER_TYPE=csv python -m movies
MOVIE_FINDER_TYPE=sqlite python -m movies
```

---

TITLE: Defining and Using Aggregate Provider in Python
DESCRIPTION: Demonstrates how to create and use an Aggregate provider to group different configuration readers under a single access point. The example shows a Container class with YAML and JSON configuration readers aggregated under a config_readers provider.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/aggregate.rst#_snippet_0

LANGUAGE: python
CODE:

```
# Code referenced from the documentation but not directly shown
```

---

TITLE: Implementing User Service Logic in Python
DESCRIPTION: Contains the business logic for user-related operations encapsulated in a service class. This module depends on the user repository to interact with persistent storage and provides higher-level abstractions used by API endpoints.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_3

LANGUAGE: python
CODE:

```
Contents of webapp/services.py with user service implementation
```

---

TITLE: Implementing and Using Selector Provider in Python
DESCRIPTION: This code demonstrates how to instantiate and utilize the Selector provider from the dependency_injector framework. It shows setting up a selector callable, passing provider options as keyword arguments, and delegating work based on dynamic selection keys. Dependencies include the dependency_injector.providers module; the main parameters are the selector callable and provider mappings. The snippet enables flexible provider selection, facilitating polymorphism and configuration-based dependency management.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/selector.rst#_snippet_0

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/selector.py
   :language: python
   :lines: 3-
   :emphasize-lines: 16-20
```

---

TITLE: Configuring Container Wiring for Handlers Module in Python
DESCRIPTION: This Python snippet updates the dependency container definition to include `WiringConfiguration`. This configuration tells the container to automatically inject dependencies into functions and classes decorated with `@inject` within the specified modules, like the 'handlers' module.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_12

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers

from . import giphy, services


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".handlers"])

    config = providers.Configuration(yaml_files=["config.yml"])

    giphy_client = providers.Factory(
        giphy.GiphyClient,
        api_key=config.giphy.api_key,
        timeout=config.giphy.request_timeout,
    )

    search_service = providers.Factory(
        services.SearchService,
        giphy_client=giphy_client,
    )
```

---

TITLE: Implementing Pytest Fixtures and Tests with Mocking in Python
DESCRIPTION: This Python snippet provides example tests for the aiohttp application handler using pytest and unittest.mock. It includes fixtures for setting up the application and test client, and tests that use dependency overriding to mock the `GiphyClient` for isolated testing.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_19

LANGUAGE: python
CODE:

```
"""Tests module."""

from unittest import mock

import pytest

from giphynavigator.application import create_app
from giphynavigator.giphy import GiphyClient


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()


@pytest.fixture
def client(app, aiohttp_client, loop):
    return loop.run_until_complete(aiohttp_client(app))


async def test_index(client, app):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [
            {"url": "https://giphy.com/gif1.gif"},
            {"url": "https://giphy.com/gif2.gif"},
        ],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        response = await client.get(
            "/",
            params={
                "query": "test",
                "limit": 10,
            },
        )

    assert response.status == 200
    data = await response.json()
    assert data == {
        "query": "test",
        "limit": 10,
        "gifs": [
            {"url": "https://giphy.com/gif1.gif"},
            {"url": "https://giphy.com/gif2.gif"},
        ],
    }


async def test_index_no_data(client, app):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [],
    }

    with app.container.giphy_client.override(giphy_client_mock):
        response = await client.get("/")

    assert response.status == 200
    data = await response.json()
    assert data["gifs"] == []


async def test_index_default_params(client, app):
    giphy_client_mock = mock.AsyncMock(spec=GiphyClient)
    giphy_client_mock.search.return_value = {
        "data": [],
    }
```

---

TITLE: Implementing GitHub Search Service with Repository Formatting
DESCRIPTION: Creates a service class for searching GitHub repositories that formats the search results including repository details and latest commit information. This service uses the GitHub API client.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_19

LANGUAGE: python
CODE:

```
"""Services module."""

from github import Github
from github.Repository import Repository
from github.Commit import Commit


class SearchService:
    """Search service performs search on Github."""

    def __init__(self, github_client: Github):
        self._github_client = github_client

    def search_repositories(self, query, limit):
        """Search for repositories and return formatted data."""
        repositories = self._github_client.search_repositories(
            query=query,
            **{"in": "name"},
        )
        return [
            self._format_repo(repository)
            for repository in repositories[:limit]
        ]

    def _format_repo(self, repository: Repository):
        commits = repository.get_commits()
        return {
            "url": repository.html_url,
            "name": repository.name,
            "owner": {
                "login": repository.owner.login,
                "url": repository.owner.html_url,
                "avatar_url": repository.owner.avatar_url,
            },
            "latest_commit": self._format_commit(commits[0]) if commits else {},
        }

    def _format_commit(self, commit: Commit):
        return {
            "sha": commit.sha,
            "url": commit.html_url,
            "message": commit.commit.message,
            "author_name": commit.commit.author.name,
        }
```

---

TITLE: Implementing Factory of Factories Pattern with Python-Dependency-Injector
DESCRIPTION: Creates a base factory that instantiates another factory provider and passes additional arguments. The concrete factory then uses the base factory with extra arguments to create instances.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/factory-of-factories.rst#_snippet_0

LANGUAGE: python
CODE:

```
base_factory = providers.Factory(
    providers.Factory
    SomeClass,
    base_argument=1,
)

concrete_factory = providers.Factory(
    OtherClass,
    instance=base_factory(extra_argument=1),
)


if __name__ == "__main__":
    instance = concrete_factory()
    # Same as: # instance = SomeClass(base_argument=1, extra_argument=2)
```

---

TITLE: Configuring Default Giphy Timeout in YAML
DESCRIPTION: This YAML snippet defines the basic configuration structure for the Giphy API client, including a request timeout setting. This configuration will be loaded by the application's dependency injection container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_5

LANGUAGE: yaml
CODE:

```
giphy:
  request_timeout: 10
```

---

TITLE: Setting Giphy API Key Environment Variable in Bash
DESCRIPTION: This Bash command sets the 'GIPHY_API_KEY' environment variable, which is required by the application to authenticate with the Giphy API. Replace the example key with your actual API key.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_7

LANGUAGE: bash
CODE:

```
export GIPHY_API_KEY=wBJ2wZG7SRqfrU9nPgPiWvORmloDyuL0
```

---

TITLE: Adding `HttpClient` to Dependency Injection Container
DESCRIPTION: Extends the container configuration to include a factory provider for `HttpClient`, enabling dependency injection into monitor classes. This setup allows `HttpMonitor` instances to utilize a shared, configurable HTTP client for performing web requests asynchronously.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_14

LANGUAGE: Python
CODE:

```
"""Containers module."""

import logging
import sys

from dependency_injector import containers, providers

from . import http, dispatcher


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    http_client = providers.Factory(http.HttpClient)

    dispatcher = providers.Factory(
        dispatcher.Dispatcher,
        monitors=providers.List(
            # TODO: add monitors
        ),
    )
```

---

TITLE: Implementing Password Hashing with Callable Provider (Python)
DESCRIPTION: This Python code, included from '../../examples/miniapps/password-hashing/example.py', demonstrates setting up a dependency injection container to provide a password hashing function using the `Callable` provider. It showcases how to configure and utilize the injected callable within an application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/password-hashing.rst#_snippet_0

LANGUAGE: python
CODE:

```
# Source code included from:
# ../../examples/miniapps/password-hashing/example.py
# (Content not available directly in this document)
```

---

TITLE: Loading Configuration from Multiple Sources with Recursive Merge Using Dependency Injector in Python
DESCRIPTION: Illustrates how the Configuration provider supports loading configuration data from multiple sources sequentially, merging them recursively into one combined configuration state. This feature allows layering configuration from base files and environment-specific overrides or local files.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_11

LANGUAGE: python
CODE:

```
# Example usage (content omitted for brevity)
container.config.from_yaml("config.yml")
container.config.from_yaml("config.local.yml")
```

---

TITLE: Application Entry Point with Container Wiring in `__main__.py`
DESCRIPTION: Implements an entry point function `main` that injects the dispatcher from the container and calls its `run()` method. The script initializes the dependency injection container, allocates resources, wires modules for injection, and executes `main`. This setup facilitates decoupling and easy configuration management in an asynchronous environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_11

LANGUAGE: Python
CODE:

```
"""Main module."""

from dependency_injector.wiring import Provide, inject

from .dispatcher import Dispatcher
from .containers import Container


@inject
def main(dispatcher: Dispatcher = Provide[Container.dispatcher]) -> None:
    dispatcher.run()


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
```

---

TITLE: Defining Photo Package Container in Python
DESCRIPTION: Defines the container for the 'photo' package using Dependency Injector. It declares dependencies on a database client ('db') and an AWS S3 client ('s3') using `providers.Dependency`. It provides a `PhotoRepository` factory that requires both external dependencies, encapsulating the package's needs.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_2

LANGUAGE: python
CODE:

```
# Content of example/photo/containers.py
# Defines the PhotoContainer, declaring dependencies on 'db' and 's3'
# and providing a PhotoRepository factory.

from dependency_injector import containers, providers

from . import repositories


class PhotoContainer(containers.DeclarativeContainer):

    db = providers.Dependency()
    s3 = providers.Dependency()

    repository = providers.Factory(
        repositories.PhotoRepository,
        db=db,
        s3=s3,
    )
```

---

TITLE: Defining Application Entry Point in Python
DESCRIPTION: The main execution script (`__main__.py`) for the application. It initializes the `ApplicationContainer`, loads configuration from 'config.ini', wires the container's modules to enable dependency injection, retrieves the `AnalyticsService` from the container, and executes its main logic, demonstrating the application's startup sequence.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_5

LANGUAGE: python
CODE:

```
# Content of example/__main__.py
# Application entry point. Initializes the ApplicationContainer, loads configuration,
# wires dependencies, retrieves the AnalyticsService, and runs the main logic.

from .containers import ApplicationContainer


def main(container: ApplicationContainer): # type: ignore
    # Example usage:
    analytics_service = container.analytics_package.service()
    # result = analytics_service.calculate_stats()
    # print(result)
    print('Application finished.')


if __name__ == '__main__':
    container = ApplicationContainer()
    container.config.from_ini('config.ini')
    # Wire the container to the main module and any other modules where injection is needed.
    container.wire(modules=[__name__])

    main(container=container) # Injected!
```

---

TITLE: Inheriting Declarative Containers in Python
DESCRIPTION: This snippet demonstrates defining a declarative container that inherits from another container class. It shows how inherited providers are accessible alongside newly declared providers, enabling reuse and extension of provider configurations.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/declarative.rst#_snippet_1

LANGUAGE: python
CODE:

```
class BaseContainer(containers.DeclarativeContainer):
    foo = providers.Factory(Foo)

class Container(BaseContainer):
    bar = providers.Singleton(Bar)
```

---

TITLE: Initializing Dependency Injection Container with Logging - Python
DESCRIPTION: Implements the main containers.py module that defines a dependency injection container using the dependency-injector library. It provides a YAML-based configuration provider and a resource provider to configure logging using settings from config.yml. Python dependencies required: dependency-injector, PyYAML. Key parameters include logging settings and the config.yml path; config must contain log.level and log.format fields.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_4

LANGUAGE: python
CODE:

```
"""Containers module."""

import logging
import sys

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )
```

---

TITLE: Creating a Custom Provider Class in Dependency Injector (Python)
DESCRIPTION: This snippet demonstrates how to implement a custom provider by subclassing the Provider class from the dependency_injector.providers module. It includes the necessary overrides: the \_provide() method to define provision logic, the **deepcopy**() method to ensure correct copying behavior using the module's deepcopy mechanism, and the related property to expose internal providers. The **init**() should always call the parent class initializer. The implementation highlights the importance of properly handling arguments, overrides, and copying to ensure reliable IoC integration and maintain expected behaviors when the provider is used or extended.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/custom.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector.providers import Provider, deepcopy

class CustomProvider(Provider):
    __slots__ = ('_args', '_kwargs', '_overrides')

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._args = args
        self._kwargs = kwargs
        self._overrides = []

    def _provide(self, args, kwargs):
        # Provide some object using self._args and self._kwargs
        return (self._args, self._kwargs, args, kwargs)

    def __deepcopy__(self, memo):
        try:
            cls = self.__class__
            copy = cls(*deepcopy(self._args, memo), **deepcopy(self._kwargs, memo))
            copy._copy_overriding(self)
            return copy
        except Exception as error:
            raise error

    @property
    def related(self):
        yield from super().related
        # If this provider stores other providers, yield them here

# Usage example
custom_provider = CustomProvider(1, 2, key='value')
provided = custom_provider()
print(provided)

```

---

TITLE: Fixtures module for creating CSV and SQLite sample data (Python)
DESCRIPTION: Defines sample movie data and functions to generate CSV and SQLite database files used for testing and development. These fixtures ensure reproducible test data for the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_0

LANGUAGE: Python
CODE:

```
"""Fixtures module."""

import csv
import sqlite3
import pathlib


SAMPLE_DATA = [
    ("The Hunger Games: Mockingjay - Part 2", 2015, "Francis Lawrence"),
    ("Rogue One: A Star Wars Story", 2016, "Gareth Edwards"),
    ("The Jungle Book", 2016, "Jon Favreau"),
]

FILE = pathlib.Path(__file__)
DIR = FILE.parent
CSV_FILE = DIR / "movies.csv"
SQLITE_FILE = DIR / "movies.db"


def create_csv(movies_data, path):
    with open(path, "w") as opened_file:
        writer = csv.writer(opened_file)
        for row in movies_data:
            writer.writerow(row)


def create_sqlite(movies_data, path):
    with sqlite3.connect(path) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS movies "
            "(title text, year int, director text)"
        )
        db.execute("DELETE FROM movies")
        db.executemany("INSERT INTO movies VALUES (?,?,?)", movies_data)


def main():
    create_csv(SAMPLE_DATA, CSV_FILE)
    create_sqlite(SAMPLE_DATA, SQLITE_FILE)
    print("OK")


if __name__ == "__main__":
    main()
```

---

TITLE: Creating Sanic Application Factory with Dependency Injection in Python
DESCRIPTION: Constructs the Sanic application instance in application.py by creating and wiring the container with handler modules, setting up routes, and configuring middleware or other application-level settings. This factory pattern allows for centralized app initialization and dependency resolution before the server runs. Dependencies like the container and handlers are utilized here. The snippet requires Sanic and Dependency Injector libraries.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/sanic.rst#_snippet_2

LANGUAGE: python
CODE:

```
Provided externally in application.py via literalinclude directive.
```

---

TITLE: Application Entry Point (**main**.py)
DESCRIPTION: This referenced Python file (`example/__main__.py`) serves as the main execution script. It typically parses command-line arguments, configures the DI container based on the environment (e.g., 'test' or 'prod'), resolves dependencies, and triggers the primary use case. The actual code is external.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/use-cases.rst#_snippet_2

---

TITLE: Asynchronous Function Initializer in Python
DESCRIPTION: Implements a resource provider with an asynchronous function initializer. This is useful for resources that require asynchronous initialization like database connections.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_10

LANGUAGE: python
CODE:

```
async def init_async_resource(argument1=..., argument2=...):
    return await connect()


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        init_resource,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Defining User Package Container in Python
DESCRIPTION: Defines the container for the 'user' package using Dependency Injector. It declares a dependency on a database client using `providers.Dependency` and provides a `UserRepository` that requires this database client. This isolates the package's database dependency, allowing it to be provided externally.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_1

LANGUAGE: python
CODE:

```
# Content of example/user/containers.py
# Defines the UserContainer, declaring a dependency on 'db'
# and providing a UserRepository factory.

from dependency_injector import containers, providers

from . import repositories


class UserContainer(containers.DeclarativeContainer):

    db = providers.Dependency()

    repository = providers.Factory(
        repositories.UserRepository,
        db=db,
    )
```

---

TITLE: Custom YAML Loader Usage with Dependency Injector Configuration Provider in Python
DESCRIPTION: Demonstrates how to use a custom YAML loader by passing the loader argument (e.g., yaml.UnsafeLoader) to the from_yaml method. This allows users to control YAML parsing behavior beyond the default SafeLoader. PyYAML must be installed for YAML loading.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_4

LANGUAGE: python
CODE:

```
import yaml


container.config.from_yaml("config.yml", loader=yaml.UnsafeLoader)
```

---

TITLE: YAML File Example with Environment Variable Interpolation
DESCRIPTION: Example of YAML configuration syntax supporting environment variables. Variables appear as ${ENV_VAR} with optional default values using ${ENV_VAR:default} to enable safe substitution during configuration loading.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_3

LANGUAGE: ini
CODE:

```
section:
  option1: ${ENV_VAR}
  option2: ${ENV_VAR}/path
  option3: ${ENV_VAR:default}
```

---

TITLE: Initializing Container Instance in Django Module
DESCRIPTION: This snippet creates an instance of the dependency container in 'githubnavigator/**init**.py', making it accessible application-wide. It allows the app to leverage the configured providers defined in the container, supporting dependency wiring and injection throughout the Django project.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/django.rst#_snippet_1

LANGUAGE: Python
CODE:

```
.. literalinclude:: ../../examples/miniapps/django/githubnavigator/__init__.py
   :language: python
```

---

TITLE: Configuring Dependency Injection Container with CSV Finder
DESCRIPTION: Updates the Container class to register movie finders and listers with their dependencies, including configuration from a YAML file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_6

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers

from . import finders, listers, entities


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    movie = providers.Factory(entities.Movie)

    csv_finder = providers.Singleton(
        finders.CsvMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    lister = providers.Factory(
        listers.MovieLister,
        movie_finder=csv_finder,
    )

```

---

TITLE: Example Test Execution Output (Bash)
DESCRIPTION: This snippet displays the expected output when running the tests using the provided Docker Compose command. It shows pytest collecting and running the tests, confirming that 2 items were collected and both tests passed ('..'). It also includes the coverage report generated by the `--cov` flag.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_26

LANGUAGE: bash
CODE:

```
platform linux -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0
rootdir: /code
plugins: cov-6.0.0, asyncio-0.24.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 2 items

monitoringdaemon/tests.py ..                                    [100%]

---------- coverage: platform linux, python 3.10.0-final-0 -----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
monitoringdaemon/__init__.py         0      0   100%
monitoringdaemon/__main__.py        11     11     0%
monitoringdaemon/containers.py      11      0   100%
monitoringdaemon/dispatcher.py      45      5    89%
monitoringdaemon/http.py             6      3    50%
monitoringdaemon/monitors.py        23      1    96%
monitoringdaemon/tests.py           35      0   100%
----------------------------------------------------
TOTAL                              131     20    85%
```

---

TITLE: Running the Example Application with Command-line Arguments
DESCRIPTION: Command to run the example application using the Python module with three arguments: an email address, password, and a filename.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-multiple-containers/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
python -m example user@example.com secret photo.jpg
```

---

TITLE: Implementing Aiohttp Handler with Injected Service in Python
DESCRIPTION: This Python function defines an aiohttp request handler using `@inject` and `Provide` from dependency-injector to receive the `SearchService` instance. It retrieves search parameters from the request and uses the injected service to fetch Giphy data.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_11

LANGUAGE: python
CODE:

```
"""Handlers module."""

from aiohttp import web
from dependency_injector.wiring import Provide, inject

from .services import SearchService
from .containers import Container


@inject
async def index(
        request: web.Request,
        search_service: SearchService = Provide[Container.search_service],
) -> web.Response:
    query = request.query.get("query", "Dependency Injector")
    limit = int(request.query.get("limit", 10))

    gifs = await search_service.search(query, limit)

    return web.json_response(
        {
            "query": query,
            "limit": limit,
            "gifs": gifs,
        },
    )
```

---

TITLE: Configuring Application Settings in INI
DESCRIPTION: Provides example configuration settings in INI format (`config.ini`). It includes sections for database connection details (DSN) and AWS credentials (access key ID, secret access key) required by the application container to initialize external services like SQLite and S3.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_6

LANGUAGE: ini
CODE:

```
# Content of config.ini
# Configuration file for the application.

[database]
dsn = :memory:

[aws]
access_key_id = KEY
secret_access_key = SECRET
```

---

TITLE: Implementing Selector Pattern for Dynamic Finder Selection
DESCRIPTION: Enhances the Container with a Selector provider to dynamically choose between CSV and SQLite finders based on configuration.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_12

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers, providers

from . import finders, listers, entities


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    movie = providers.Factory(entities.Movie)

    csv_finder = providers.Singleton(
        finders.CsvMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.csv.path,
        delimiter=config.finder.csv.delimiter,
    )

    sqlite_finder = providers.Singleton(
        finders.SqliteMovieFinder,
        movie_factory=movie.provider,
        path=config.finder.sqlite.path,
    )

    finder = providers.Selector(
        config.finder.type,
        csv=csv_finder,
        sqlite=sqlite_finder,
    )

    lister = providers.Factory(
        listers.MovieLister,
        movie_finder=finder,

```

---

TITLE: Using Generic Provider Type Hinting with Mypy in Python
DESCRIPTION: Illustrates using `providers.Provider[Animal]` as a generic type hint for a provider variable. This informs mypy that the provider will return an instance compatible with the `Animal` type (like `Cat`), allowing for more flexible type checking, especially when passing providers to functions or methods.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/typing_mypy.rst#_snippet_1

LANGUAGE: python
CODE:

```
from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):
    ...


provider: providers.Provider[Animal] = providers.Factory(Cat)


if __name__ == "__main__":
    animal = provider()  # mypy knows that animal is of type "Animal"
```

---

TITLE: Bootstrapping the Monitoring Daemon Application - Python
DESCRIPTION: Provides the application entry point in **main**.py, responsible for creating the DI container, initializing resources (including logging and configuration parsing), and launching the main program logic. No external input is expected, and execution starts if the script is run as **main**. All resource initialization is handled prior to entering main(). Dependencies: the containers.py module must be available.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_6

LANGUAGE: python
CODE:

```
"""Main module."""

from .containers import Container


def main() -> None:
    ...


if __name__ == "__main__":
    container = Container()
    container.init_resources()

    main()
```

---

TITLE: Asynchronous Resource Subclass in Python
DESCRIPTION: Implements an asynchronous resource subclass for managing connection resources. This approach provides explicit async methods for initialization and shutdown.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_12

LANGUAGE: python
CODE:

```
from dependency_injector import resources


class AsyncConnection(resources.AsyncResource):

    async def init(self, argument1=..., argument2=...):
        yield await connect()

    async def shutdown(self, connection):
        await connection.close()


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        AsyncConnection,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Verifying Installed Version of Dependency Injector
DESCRIPTION: This snippet shows how to verify the installed version of Dependency Injector by importing the package and printing its **version** attribute. It helps ensure the correct version is installed, which is crucial for compatibility.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/introduction/installation.rst#_snippet_1

LANGUAGE: bash
CODE:

```
>>> import dependency_injector
>>> dependency_injector.__version__
'4.39.0'
```

---

TITLE: Defining the Monitor Base Class for Periodic Checks - Python
DESCRIPTION: Implements the monitors.py module, which defines the base Monitor class for asynchronous monitoring tasks. Each Monitor has a configurable interval (check_every) and a dedicated logger. Subclasses must implement the async check() method. Python's logging standard library is used for structured logging. Requires Python 3.7+ for async/await syntax.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_7

LANGUAGE: python
CODE:

```
"""Monitors module."""

import logging


class Monitor:

    def __init__(self, check_every: int) -> None:
        self.check_every = check_every
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()
```

---

TITLE: Using Relative Imports in Wiring Configuration in Python
DESCRIPTION: Demonstrates how to use relative imports in wiring configuration, which are resolved relative to the container's module.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_9

LANGUAGE: python
CODE:

```
# In module "yourapp.container":

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
           ".module1",  # Resolved to: "yourapp.module1"
           ".module2",  # Resolved to: "yourapp.module2"
        ],
    )
)


# In module "yourapp.foo.bar.main":

if __name__ == "__main__":
    container = Container()  # wire to "yourapp.module1" and "yourapp.module2"
    ...
```

---

TITLE: Configuration for External Monitoring Settings `config.yml`
DESCRIPTION: Specifies logging level and format, along with monitor parameters such as HTTP method, URL, timeout, and check interval. These settings enable customizable and scalable health checks for external resources like `http://example.com`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_17

LANGUAGE: YAML
CODE:

```
log:
  level: "INFO"
  format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"

monitors:

  example:
    method: "GET"
    url: "http://example.com"
    timeout: 5
    check_every: 5
```

---

TITLE: CSV Movie Finder class for reading movies from a CSV file (Python)
DESCRIPTION: Implements the CsvMovieFinder class inheriting from MovieFinder, responsible for reading movie data from a CSV file using the specified delimiter, and creating Movie instances via a factory function. It encapsulates CSV parsing logic for movie data.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_4

LANGUAGE: Python
CODE:

```
"""Movie finders module."""

import csv
from typing import Callable, List

from .entities import Movie


class MovieFinder:

    def __init__(self, movie_factory: Callable[..., Movie]) -> None:
        self._movie_factory = movie_factory

    def find_all(self) -> List[Movie]:
        raise NotImplementedError()


class CsvMovieFinder(MovieFinder):

    def __init__(
            self,
            movie_factory: Callable[..., Movie],
            path: str,
            delimiter: str,
    ) -> None:
        self._csv_file_path = path
        self._delimiter = delimiter
        super().__init__(movie_factory)

    def find_all(self) -> List[Movie]:
        with open(self._csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self._delimiter)
            return [self._movie_factory(*row) for row in csv_reader]
```

---

TITLE: Configuring Logging Format and Level - YAML
DESCRIPTION: Defines log configuration in YAML format for use by the Python application. The 'level' sets the logging severity (e.g., INFO), and 'format' provides the message layout. This file must be present at config.yml and referenced by the dependency injection setup. Only two fields are specified and both are required by the logging configuration.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_5

LANGUAGE: yaml
CODE:

```
log:
  level: "INFO"
  format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
```

---

TITLE: Main application entry point (Python)
DESCRIPTION: Contains the main function that initializes the dependency injection container and starts the CLI application. Currently, the main() function does nothing but can be extended to run the app.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_2

LANGUAGE: Python
CODE:

```
"""Main module."""

from .containers import Container


def main() -> None:
    ...


if __name__ == "__main__":
    container = Container()

    main()
```

---

TITLE: Injecting Invariant Configuration Options (ItemSelector) (Python)
DESCRIPTION: Shows how to inject different configuration sections based on the value of another configuration option (the 'switch'). This uses the item access syntax `config.options[config.switch]`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_25

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_itemselector.py
   :language: python
   :lines: 3-
   :emphasize-lines: 15,30-31,38
```

---

TITLE: Listing Python Project Dependencies
DESCRIPTION: This text lists the Python packages required for the 'ets-labs/python-dependency-injector' project. It includes libraries for dependency injection (dependency-injector), web framework (fastapi with standard extras, uvicorn ASGI server), configuration/data serialization (pyyaml), database ORM (sqlalchemy), testing (pytest, pytest-cov for coverage), and making HTTP requests (requests). These dependencies are typically installed using a package manager like pip, often from a requirements.txt file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/requirements.txt#_snippet_0

LANGUAGE: Plain Text
CODE:

```
dependency-injector
fastapi[standard]
uvicorn
pyyaml
sqlalchemy
pytest
requests
pytest-cov
```

---

TITLE: Writing Tests with Provider Overriding in Dependency Injector for Python
DESCRIPTION: Demonstrates test cases in tests.py that override the giphy client provider with a mock implementation using Dependency Injector's provider-overriding feature. This method allows isolating external service dependencies to enable reliable and repeatable testing of application logic. The test suite ensures API correctness without relying on live external services. It requires testing libraries, Dependency Injector, and mock dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/sanic.rst#_snippet_3

LANGUAGE: python
CODE:

```
Provided externally in tests.py via literalinclude directive with emphasized lines on mocking and overriding.
```

---

TITLE: Running Tests with Coverage for Django Application
DESCRIPTION: Command to run the unit tests with coverage analysis, showing the test results and the code coverage report for the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/django/README.rst#_snippet_5

LANGUAGE: bash
CODE:

```
coverage run --source='.' manage.py test && coverage report
```

---

TITLE: Function Initializer for Resource Provider in Python
DESCRIPTION: Implements a resource provider using a function initializer. The function can return a resource object or configure a global resource without returning anything.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_3

LANGUAGE: python
CODE:

```
def init_resource(argument1=..., argument2=...):
    return SomeResource()


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        init_resource,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Defining Basic Flask View in Python
DESCRIPTION: Defines a simple Flask view function `index` in `views.py`. This function returns the string "Hello, World!" and serves as the initial endpoint for the web application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_5

LANGUAGE: Python
CODE:

```
"""Views module."""


def index():
    return "Hello, World!"
```

---

TITLE: Updating Handler to Use Configured Defaults in Python
DESCRIPTION: This Python snippet refactors the index handler to fetch default search query and limit values from the injected application configuration instead of hardcoding them. This improves maintainability and configurability.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_16

LANGUAGE: python
CODE:

```
"""Handlers module."""

from aiohttp import web
from dependency_injector.wiring import Provide, inject

from .services import SearchService
from .containers import Container


@inject
async def index(
        request: web.Request,
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        default_limit: int = Provide[Container.config.default.limit.as_int()],
) -> web.Response:
    query = request.query.get("query", default_query)
    limit = int(request.query.get("limit", default_limit))

    gifs = await search_service.search(query, limit)

    return web.json_response(
        {
            "query": query,
            "limit": limit,
            "gifs": gifs,
        },
    )
```

---

TITLE: Extended YAML Configuration for Multiple Data Sources
DESCRIPTION: Updates configuration to include path settings for both CSV and SQLite data sources.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_11

LANGUAGE: yaml
CODE:

```
finder:

  csv:
    path: "data/movies.csv"
    delimiter: ","

  sqlite:
    path: "data/movies.db"

```

---

TITLE: Specializing Factory Providers by Provided Type in dependency_injector (Python)
DESCRIPTION: This snippet shows how to create a Factory provider subclass that only provides instantiations of a specific type using the provided_type class attribute. It ensures type consistency and enforces constraints on the output type of the Factory. Requires subclassing dependency_injector.providers.Factory and setting provided_type. Useful in large codebases or strict type requirements.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_5

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_provided_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-14

```

---

TITLE: Structuring Application Directories in Bash
DESCRIPTION: Shows the directory structure for a Python application using multiple containers. The structure includes the main package, containers, services, configuration, and requirements files.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-multiple-containers.rst#_snippet_0

LANGUAGE: bash
CODE:

```
./
├── example/
│   ├── __init__.py
│   ├── __main__.py
│   ├── containers.py
│   └── services.py
├── config.yml
└── requirements.txt
```

---

TITLE: Declaring and Using Dependency Provider in Python Dependency Injector
DESCRIPTION: This Python snippet demonstrates how to declare a Dependency provider using the instance_of argument to enforce type constraints. It shows the process of specifying expected dependency types and setting up the provider within a Dependency Injector container. The code relies on the dependency_injector.providers module and requires that the referenced class be defined elsewhere. When a dependency is not provided or overridden, attempts to access the provider will raise an error.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/dependency.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class SomeClass:
    ...

class Container(containers.DeclarativeContainer):
    dependency = providers.Dependency(instance_of=SomeClass)

container = Container()
# Attempting to call dependency() without override will raise an error

```

---

TITLE: Creating Flask Application Factory in Python
DESCRIPTION: Defines the `create_app` factory function in `application.py`. This function initializes the `Container`, creates the Flask application instance (`app`), associates the container with the app (`app.container`), maps the root URL ('/') route to the `views.index` function, and returns the configured Flask app object.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_7

LANGUAGE: Python
CODE:

```
"""Application module."""

from flask import Flask

from .containers import Container
from . import views


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index)

    return app
```

---

TITLE: Basic Provider Type Inference with Mypy in Python
DESCRIPTION: Demonstrates how mypy can automatically infer the concrete type (`Cat`) returned by a `dependency_injector.providers.Factory`. When `provider()` is called, mypy correctly identifies the type of the `animal` variable as `Cat` due to the included typing stubs.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/typing_mypy.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import providers


class Animal:
    ...


class Cat(Animal):
    ...


provider = providers.Factory(Cat)


if __name__ == "__main__":
    animal = provider()  # mypy knows that animal is of type "Cat"
```

---

TITLE: Defining Application Directory Structure in Bash
DESCRIPTION: Illustrates the directory structure for the example decoupled application. It shows separate directories for 'user', 'photo', and 'analytics' packages, each containing its own container definition, along with a main application container, entry point (**main**.py), configuration file (config.ini), and requirements.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/decoupled-packages.rst#_snippet_0

LANGUAGE: bash
CODE:

```
./
├── example/
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── containers.py
│   │   └── services.py
│   ├── photo/
│   │   ├── __init__.py
│   │   ├── containers.py
│   │   ├── entities.py
│   │   └── repositories.py
│   ├── user/
│   │   ├── __init__.py
│   │   ├── containers.py
│   │   ├── entities.py
│   │   └── repositories.py
│   ├── __init__.py
│   ├── __main__.py
│   └── containers.py
├── config.ini
└── requirements.txt
```

---

TITLE: Configuring Global Logging with Resource Provider in Python
DESCRIPTION: Shows how to use a resource provider to configure global logging. This example demonstrates a function initializer that doesn't return a value but configures a global resource.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_4

LANGUAGE: python
CODE:

```
import logging.config


class Container(containers.DeclarativeContainer):

    configure_logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )
```

---

TITLE: Adding Default Search Parameters to Config in YAML
DESCRIPTION: This YAML snippet updates the configuration file to include default values for the search query and limit. These values are now available via the dependency injection container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_17

LANGUAGE: yaml
CODE:

```
giphy:
  request_timeout: 10
default:
  query: "Dependency Injector"
  limit: 10
```

---

TITLE: Installing Dependencies using Bash
DESCRIPTION: Command to install the necessary Python packages listed in the `requirements.txt` file using `pip`. This should be run after activating the virtual environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Disabling Environment Variable Interpolation (YAML/Python)
DESCRIPTION: Shows how to disable environment variable interpolation entirely by passing `envs_required=None` when loading configuration. A sample YAML file and a Python snippet demonstrate that the variable placeholder remains unchanged after loading.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_15

LANGUAGE: yaml
CODE:

```
template_string: 'Hello, ${name}!'
```

LANGUAGE: python
CODE:

```
>>> container.config.from_yaml("templates.yml", envs_required=None)
>>> container.config.template_string()
'Hello, ${name}!'
```

---

TITLE: Displaying FastAPI Example File Structure - Bash
DESCRIPTION: Provides the directory structure of the example application, showing the organization of Python modules within the `giphynavigator` package, configuration file (`config.yml`), and dependency requirements file (`requirements.txt`). This structure is typical for small to medium Python projects.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi.rst#_snippet_0

LANGUAGE: bash
CODE:

```
./
├── giphynavigator/
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── endpoints.py
│   ├── giphy.py
│   ├── services.py
│   └── tests.py
├── config.yml
└── requirements.txt
```

---

TITLE: Sample Output of the Python CLI Movie App
DESCRIPTION: Provides sample plain text output from running the movie lister application, showing movies directed by 'Francis Lawrence' and movies released in 2016. Output is purely illustrative and not code to be executed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_15

LANGUAGE: plain
CODE:

```
Francis Lawrence movies:
    - Movie(title='The Hunger Games: Mockingjay - Part 2', year=2015, director='Francis Lawrence')
2016 movies:
    - Movie(title='Rogue One: A Star Wars Story', year=2016, director='Gareth Edwards')
    - Movie(title='The Jungle Book', year=2016, director='Jon Favreau')
```

---

TITLE: Using List Provider with Dependency Injector in Python
DESCRIPTION: Demonstrates how to utilize the List provider from the dependency_injector.providers module to create an injectable list of dependencies. Requires the dependency-injector library to be installed and imported, and the List provider must be imported from dependency_injector.providers. This code constructs a list provider using positional arguments, and does not support keyword arguments due to provider limitations. The expected output is a Python list containing the provided dependencies. Limitations include the lack of keyword argument support and compatibility only with objects provided via positional parameters.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/list.rst#_snippet_0

LANGUAGE: Python
CODE:

```
from dependency_injector import providers

numbers = providers.List(
    1,
    2,
    3,
)

print(numbers())
# Output: [1, 2, 3]
```

---

TITLE: Running Coverage Report for pytest in a Python aiohttp Project
DESCRIPTION: This snippet provides a bash command to execute pytest with coverage measurement on the giphynavigator tests. It shows the command syntax used for running tests with coverage and the expected output indicating how much of the code is covered by tests, aiding in assessing test completeness.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_21

LANGUAGE: bash
CODE:

```
   py.test giphynavigator/tests.py --cov=giphynavigator
```

---

TITLE: Setting Up Configuration for GitHub API
DESCRIPTION: Creates a YAML configuration file for the application that specifies GitHub API settings, particularly the request timeout value. This configuration will be loaded by the container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_16

LANGUAGE: yaml
CODE:

```
github:
  request_timeout: 10
```

---

TITLE: Creating Base HTML Layout with Bootstrap Integration
DESCRIPTION: Defines the base HTML structure (`base.html`) using Jinja2 templating. It includes standard HTML5 boilerplate, responsive viewport meta tag, incorporates Bootstrap CSS and JS via `Bootstrap-Flask` helpers (`bootstrap.load_css()`, `bootstrap.load_js()`), and defines Jinja2 blocks (`head`, `styles`, `title`, `content`, `scripts`) for content extension by child templates.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_12

LANGUAGE: HTML
CODE:

```
<!doctype html>
<html lang="en">
    <head>
        {% block head %}
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        {% block styles %}
            <!-- Bootstrap CSS -->
            {{ bootstrap.load_css() }}
        {% endblock %}

        <title>{% block title %}{% endblock %}</title>
        {% endblock %}
    </head>
    <body>
        <!-- Your page content -->
        {% block content %}{% endblock %}

        {% block scripts %}
            <!-- Optional JavaScript -->
            {{ bootstrap.load_js() }}
        {% endblock %}
    </body>
</html>
```

---

TITLE: Using Closing Marker with Asynchronous Resources in Python
DESCRIPTION: Shows how to use the Closing marker with asynchronous Resource providers to ensure proper cleanup of resources.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_12

LANGUAGE: python
CODE:

```
@inject
async def main(
    db: Database = Closing[Provide[Container.db]],
    cache: Cache = Closing[Provide[Container.cache]],
):
    ...
```

---

TITLE: Python Package Dependencies for AWS Integration
DESCRIPTION: A requirements file listing the dependency-injector package for dependency injection and boto3 for AWS service integration.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/decoupled-packages/requirements.txt#_snippet_0

LANGUAGE: plaintext
CODE:

```
dependency-injector
boto3
```

---

TITLE: Configuring Dict Provider for Dependency Injection in Python
DESCRIPTION: This snippet illustrates how to initialize and use the Dict provider from dependency_injector.providers to inject a dictionary of dependencies in Python. It demonstrates creating a Dict provider using keyword arguments, allowing dependencies to be referenced by their keys when injected. This setup assumes dependency_injector is installed and that the referenced providers (e.g., providers.Factory) are properly configured. The key output is a provider that returns a dictionary mapping keys to constructed dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/dict.rst#_snippet_0

LANGUAGE: python
CODE:

```
from dependency_injector import providers

dict_provider = providers.Dict(
    dependency1=providers.Factory(SomeClass1),
    dependency2=providers.Factory(SomeClass2),
)

```

---

TITLE: Listing Project Dependencies - Bash
DESCRIPTION: This Bash snippet displays the contents of the `requirements.txt` file. It lists the Python packages required for the project, including core dependencies like `dependency-injector`, `flask`, and `pygithub`, as well as testing dependencies like `pytest-flask` and `pytest-cov`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_24

LANGUAGE: bash
CODE:

```
dependency-injector
flask
bootstrap-flask
pygithub
pyyaml
pytest-flask
pytest-cov
```

---

TITLE: Adding a `HttpMonitor` Instance for `http://example.com` in Container
DESCRIPTION: Configures the dependency injection container to include a factory provider `example_monitor` for `HttpMonitor`, passing HTTP method, URL, timeout, and check interval from configuration. This monitor is injected into the dispatcher’s monitor list for periodic health checks on `http://example.com`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_16

LANGUAGE: Python
CODE:

```
"""Containers module."""

import logging
import sys

from dependency_injector import containers, providers

from . import http, monitors, dispatcher


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    http_client = providers.Factory(http.HttpClient)

    example_monitor = providers.Factory(
        monitors.HttpMonitor,
        http_client=http_client,
        options=config.monitors.example,
    )

    dispatcher = providers.Factory(
        dispatcher.Dispatcher,
        monitors=providers.List(
            example_monitor,
        ),
    )
```

---

TITLE: Loading Configuration from YAML File Using Dependency Injector in Python
DESCRIPTION: Shows how to load configuration from a YAML file using the from_yaml method of the Configuration provider. Supports environment variable interpolation within YAML configuration files. Users can specify a custom YAML loader with the loader argument. YAML loading depends on the PyYAML package, which must be installed separately or via the dependency-injector[yaml] extra.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_2

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["./config.yml"])


if __name__ == "__main__":
    container = Container()  # Config is loaded from ./config.yml
```

---

TITLE: Initializing Dict Provider with Non-String and Special Character Keys in Python
DESCRIPTION: This Python snippet shows how to initialize the Dict provider using a dictionary passed as a positional argument, enabling the use of non-string keys and string keys that contain periods or dashes. This approach is necessary when dictionary keys do not conform to standard Python identifier rules. Usage requires the dependency_injector library and pre-defined provider objects for constructing dependencies. The result is a provider that handles diverse keys for flexible dependency injection.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/dict.rst#_snippet_1

LANGUAGE: python
CODE:

```
providers.Dict({
    SomeClass: providers.Factory(...),
    "key.with.periods": providers.Factory(...),
    "key-with-dashes": providers.Factory(...),
})

```

---

TITLE: Specifying Dependency: flake8-pyproject (Python)
DESCRIPTION: Includes 'flake8-pyproject', a plugin that allows flake8 configuration to be read from the pyproject.toml file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_7

LANGUAGE: Python requirements
CODE:

```
flake8-pyproject
```

---

TITLE: Running the Python Dependency Injector Example Application
DESCRIPTION: Command to execute the example application with parameters for user email, authentication token, and photo file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-single-container/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
python -m example user@example.com secret photo.jpg
```

---

TITLE: Loading Configuration from JSON File Using Dependency Injector in Python
DESCRIPTION: Demonstrates loading configuration from a JSON file with from_json method of the Configuration provider. Supports environment variable interpolation inside JSON string values. JSON file paths can also be passed during container provider declaration for automatic loading.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_5

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration(json_files=["./config.json"])


if __name__ == "__main__":
    container = Container()  # Config is loaded from ./config.json
```

---

TITLE: Configuring Logging using INI
DESCRIPTION: Reference to the INI file `logging.ini`. This file configures Python's standard logging framework, defining loggers, handlers, and formatters, typically loaded via `logging.config.fileConfig()`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-single-container.rst#_snippet_5

LANGUAGE: ini
CODE:

```
# Source: examples/miniapps/application-single-container/logging.ini
# Defines logging configuration using standard INI format.
# [loggers]
# keys=root,example
# [handlers]
# keys=consoleHandler
# ...
```

---

TITLE: Running Unit Tests with Coverage Using pytest in Bash
DESCRIPTION: This snippet shows the command to run unit tests for the application using pytest with coverage measurement enabled for the giphynavigator module. The command triggers test discovery and execution, generating a code coverage report to assess test completeness. It requires pytest and pytest-cov to be installed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_5

LANGUAGE: bash
CODE:

```
py.test giphynavigator/tests.py --cov=giphynavigator
```

---

TITLE: Run Flask Development Server - Bash
DESCRIPTION: Sets the necessary environment variables `FLASK_APP` to point to the application entry point and `FLASK_ENV` to 'development' for debugging. It then starts the Flask development server, making the application accessible locally.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
export FLASK_APP=githubnavigator.application
export FLASK_ENV=development
flask run
```

---

TITLE: Example Successful API Response in JSON
DESCRIPTION: This JSON snippet shows the expected response body from a successful request to the application's root endpoint. It includes the query parameters and a list of retrieved Giphy URLs.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_15

LANGUAGE: json
CODE:

```
HTTP/1.1 200 OK
Content-Length: 492
Content-Type: application/json; charset=utf-8
Date: Fri, 09 Oct 2020 01:35:48 GMT
Server: Python/3.10 aiohttp/3.6.2

{
    "gifs": [
        {
            "url": "https://giphy.com/gifs/dollyparton-3xIVVMnZfG3KQ9v4Ye"
        },
        {
            "url": "https://giphy.com/gifs/tennistv-unbelievable-disbelief-cant-believe-UWWJnhHHbpGvZOapEh"
        },
        {
            "url": "https://giphy.com/gifs/discoverychannel-nugget-gold-rush-rick-ness-KGGPIlnC4hr4u2s3pY"
        },
        {
            "url": "https://giphy.com/gifs/soulpancake-wow-work-xUe4HVXTPi0wQ2OAJC"
        },
        {
            "url": "https://giphy.com/gifs/readingrainbow-teamwork-levar-burton-reading-rainbow-3o7qE1EaTWLQGDSabK"
        }
    ],
    "limit": 5,
    "query": "wow,it works"
}
```

---

TITLE: Python Package Dependencies
DESCRIPTION: This snippet lists the required Python packages. It includes 'dependency-injector' (the core library), 'aiohttp' (for asynchronous web tasks), 'pyyaml' (for YAML configuration), and several 'pytest' related packages ('pytest', 'pytest-asyncio', 'pytest-cov') used for testing the project.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/asyncio-daemon/requirements.txt#_snippet_0

LANGUAGE: Configuration
CODE:

```
dependency-injector
aiohttp
pyyaml
pytest
pytest-asyncio
pytest-cov
```

---

TITLE: Specifying Dependency: pyyaml (Python)
DESCRIPTION: Adds 'pyyaml', a YAML parser and emitter for Python. It's used for reading and writing data in the YAML format.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_12

LANGUAGE: Python requirements
CODE:

```
pyyaml
```

---

TITLE: Restricting Provider Types in DeclarativeContainer (Python)
DESCRIPTION: Demonstrates how to specialize a DeclarativeContainer by setting the `provider_type` class attribute. This enforces that all providers defined within the container must be subtypes of the specified `ServiceProvider`. An attempt to define a provider of an incompatible type (like `providers.Factory(dict)`) will result in an error.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/specialization.rst#_snippet_0

LANGUAGE: python
CODE:

```
# examples/containers/declarative_provider_type.py
import abc

from dependency_injector import containers, providers


# Define an abstract base class for specific provider types
class ServiceProvider(providers.Provider):
    __metaclass__ = abc.ABCMeta


# Concrete provider types inheriting from the base
class SingletonServiceProvider(ServiceProvider, providers.Singleton):
    pass


class FactoryServiceProvider(ServiceProvider, providers.Factory):
    pass


# Example service class
class Service:
    pass


# Declarative container with provider type restriction
class Container(containers.DeclarativeContainer):

    provider_type = ServiceProvider  # Enforce provider type

    provider1 = SingletonServiceProvider(Service)
    provider2 = FactoryServiceProvider(Service)

    # The following line, if added, would cause a TypeError
    # other_provider = providers.Factory(dict)


# --- Usage Example (not shown in original emphasis) ---
# container = Container()
# assert isinstance(container.provider1, SingletonServiceProvider)
# assert isinstance(container.provider2, FactoryServiceProvider)
```

---

TITLE: Implementing Callable Provider for Dependency Injection in Python
DESCRIPTION: This code demonstrates how to create and use a Callable provider that manages dependency injection by calling functions, methods, or other callables. The example illustrates the provider's setup and usage, emphasizing its similarity to factory providers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/callable.rst#_snippet_0

LANGUAGE: Python
CODE:

```
import dependency_injector.providers as providers

# Creating a Callable provider that injects dependencies into a function
def my_function(dep):
    print(f"Dependency value: {dep}")

callable_provider = providers.Callable(my_function, dep='Injected Dependency')

# Calling the provider executes the function with injected dependencies
callable_provider()
```

---

TITLE: Creating Coroutine Providers with Dependency Injector in Python
DESCRIPTION: Demonstrates how to define and use a Coroutine provider from the dependency_injector.providers module to create and manage asynchronous functions in Python. Suitable for Python 3.7+ due to its native support for async/await syntax, this snippet ensures injected dependencies are handled similarly to factory providers. Requires dependency-injector and asyncio library. Inputs should be async-compatible, outputs are async coroutine results; loop.run_until_complete() may be needed for Python versions earlier than 3.7.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/coroutine.rst#_snippet_0

LANGUAGE: Python
CODE:

```
# Example from ../../examples/providers/coroutine.py
import asyncio
from dependency_injector import providers, containers

async def example_coroutine(service):
    result = await service.run_async()
    return result

class Service:
    async def run_async(self):
        await asyncio.sleep(1)
        return 'done'

class Container(containers.DeclarativeContainer):
    service = providers.Singleton(Service)
    coroutine = providers.Coroutine(example_coroutine, service)

if __name__ == '__main__':
    container = Container()
    loop = asyncio.get_event_loop()
    # For Python 3.7+
    result = loop.run_until_complete(container.coroutine())
    print(result)

```

---

TITLE: Defining Dependency Injection Containers (containers.py)
DESCRIPTION: This referenced Python file (`example/containers.py`) defines the dependency injection containers using `python-dependency-injector`. It likely includes an `Adapters` container and an `Application` container which uses `DependenciesContainer` to link adapters to use cases, enabling loose coupling. The actual code is external.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/use-cases.rst#_snippet_1

---

TITLE: Specifying Dependency: fastapi (Python)
DESCRIPTION: Adds 'fastapi', a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_14

LANGUAGE: Python requirements
CODE:

```
fastapi
```

---

TITLE: Specifying Dependency: scipy (Python)
DESCRIPTION: Adds 'scipy', a library used for scientific and technical computing. It builds on NumPy and provides modules for optimization, linear algebra, integration, etc.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_17

LANGUAGE: Python requirements
CODE:

```
scipy
```

---

TITLE: Generator Initializer for Resource Provider in Python
DESCRIPTION: Implements a resource provider using a generator function for 2-step initialization and shutdown. The first yield statement marks the end of initialization and can return a resource object.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_5

LANGUAGE: python
CODE:

```
def init_resource(argument1=..., argument2=...):
    resource = SomeResource()  # initialization

    yield resource

    # shutdown
    ...


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        init_resource,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Set Github Personal Access Token - Bash
DESCRIPTION: Sets the `GITHUB_TOKEN` environment variable to a personal access token generated on Github. This token is used by the application to authenticate with the Github API, significantly increasing the hourly request rate limit from 60 to 5000 for authenticated requests.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_4

LANGUAGE: bash
CODE:

```
export GITHUB_TOKEN=<your token>
```

---

TITLE: Creating Search Service File in Bash
DESCRIPTION: This snippet shows the project structure and highlights the creation of a new file, 'services.py', where the SearchService class will be defined. This file will contain the business logic for performing Giphy searches.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_8

LANGUAGE: bash
CODE:

```
./
├── giphynavigator/
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── giphy.py
│   ├── handlers.py
│   └── services.py
├── venv/
├── config.yml
└── requirements.txt
```

---

TITLE: Aggregating Multiple Factory Providers with FactoryAggregate (Python)
DESCRIPTION: This snippet demonstrates the aggregation of multiple factories under a single FactoryAggregate provider. Factories can be registered with string or non-string keys, and the aggregate can be called with a specific key to select the factory at runtime. The aggregation enables modular assembly, dictionary-like provider access, and attribute access to aggregated factories. Dependencies include dependency_injector, with the aggregate pattern facilitating selection by key and extended dictionary operations.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_7

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_aggregate.py
   :language: python
   :lines: 3-
   :emphasize-lines: 33-37,47

```

---

TITLE: Implementing an Async Giphy API Client - Python
DESCRIPTION: Defines an asynchronous GiphyClient class that interacts with the Giphy API using aiohttp. The client is initialized with an API key and request timeout, and exposes a search method to perform GIF searches. Dependencies are aiohttp.ClientSession and an external API key. Input parameters include the search query and result limit. The output is the raw JSON response from the Giphy API, and errors are raised if the response is unsuccessful.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_3

LANGUAGE: python
CODE:

```
"""Giphy client module."""

from aiohttp import ClientSession, ClientTimeout


class GiphyClient:

    API_URL = "https://api.giphy.com/v1"

    def __init__(self, api_key, timeout):
        self._api_key = api_key
        self._timeout = ClientTimeout(timeout)

    async def search(self, query, limit):
        """Make search API call and return result."""
        url = f"{self.API_URL}/gifs/search"
        params = {
            "q": query,
            "api_key": self._api_key,
            "limit": limit,
        }
        async with ClientSession(timeout=self._timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    response.raise_for_status()
                return await response.json()
```

---

TITLE: Installing Requirements from requirements.txt
DESCRIPTION: Command to install the required dependencies for the example application using pip and the requirements.txt file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-multiple-containers/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Creating Virtual Environment Using Bash - Python
DESCRIPTION: Creates a Python virtual environment for dependency isolation using the 'virtualenv' tool and activates it. Required dependency: virtualenv must be installed. 'venv' is the environment folder, and the activation step ensures all subsequent package installations are local to this environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/aiohttp/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
virtualenv venv
. venv/bin/activate
```

---

TITLE: Installing Project Dependencies (Bash)
DESCRIPTION: Uses the `pip` package installer to install Python dependencies listed in the `requirements.txt` file into the currently active virtual environment. This command assumes a `requirements.txt` file exists in the current directory.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/starlette-lifespan/README.rst#_snippet_1

LANGUAGE: Bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Installing Project Dependencies - Bash
DESCRIPTION: This Bash command instructs the user to install the Python packages listed in the `requirements.txt` file using the `pip` package installer.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_25

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Implementing Chained Factories Pattern with Dependency Injector in Python
DESCRIPTION: This snippet illustrates how to create a chain of Factory providers that wraps a class constructor, adding additional arguments through nested factories. It demonstrates wrapping a class with a base factory, then wrapping that factory to inject more arguments, simulating the Chained Factories pattern.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/chained-factories.rst#_snippet_0

LANGUAGE: Python
CODE:

```
   base_factory = providers.Factory(
       SomeClass,
       base_argument=1,
   )

   concrete_factory = providers.Factory(
       base_factory,
       extra_argument=2,
   )


   if __name__ == "__main__":
       instance = concrete_factory()
       # Same as: # instance = SomeClass(base_argument=1, extra_argument=2)
```

---

TITLE: Creating and Activating Python Virtual Environment (Bash)
DESCRIPTION: Provides shell commands to create an isolated Python virtual environment named 'env' using the built-in `venv` module and then activate it for the current shell session. This is a standard prerequisite for managing project dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/starlette-lifespan/README.rst#_snippet_0

LANGUAGE: Bash
CODE:

```
python -m venv env
. env/bin/activate
```

---

TITLE: Running Pytest Unit Tests with Coverage (Bash)
DESCRIPTION: This command executes the unit tests located in `githubnavigator/tests.py` using the `pytest` framework. The `--cov=githubnavigator` flag is used with the `pytest-cov` plugin to measure and report code coverage for the `githubnavigator` package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_8

LANGUAGE: bash
CODE:

```
py.test githubnavigator/tests.py --cov=githubnavigator
```

---

TITLE: Pinning Dependency Injector Version in Requirements Files
DESCRIPTION: This snippet advises on pinning the Dependency Injector version in project dependency files such as pyproject.toml or requirements.txt. It recommends restricting updates to major versions to avoid incompatibility issues in future releases.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/introduction/installation.rst#_snippet_2

LANGUAGE: bash
CODE:

```
dependency-injector>=4.0,<5.0
```

---

TITLE: Setting Up the Dependency Injector Container - Python
DESCRIPTION: This code defines the application's IoC container using the dependency-injector framework. The container is currently empty but serves as the foundation for registering providers and managing dependencies. The class extends DeclarativeContainer. There are no required inputs at this stage, and no constraints other than requiring dependency_injector to be installed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_1

LANGUAGE: python
CODE:

```
"""Containers module."""

from dependency_injector import containers


class Container(containers.DeclarativeContainer):
    ...
```

---

TITLE: Running the Sanic Application with Environment Variable in Bash
DESCRIPTION: This snippet illustrates how to set the required GIPHY_API_KEY environment variable and run the Sanic application via command line. Setting the environment variable ensures the application can authenticate API requests to Giphy. The Sanic command launches the application factory create_app within the giphynavigator.application module, exposing the REST API.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
export GIPHY_API_KEY=wBJ2wZG7SRqfrU9nPgPiWvORmloDyuL0
sanic giphynavigator.application:create_app
```

---

TITLE: Creating a Virtual Environment in Bash
DESCRIPTION: Commands to create and activate a Python virtual environment for isolating the application dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-multiple-containers/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
python3 -m venv venv
. venv/bin/activate
```

---

TITLE: Implementing Movie Lister Class in Python
DESCRIPTION: Defines a MovieLister class that depends on a MovieFinder to retrieve and filter movies by director or release year.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_5

LANGUAGE: python
CODE:

```
"""Movie listers module."""

from .finders import MovieFinder


class MovieLister:

    def __init__(self, movie_finder: MovieFinder):
        self._movie_finder = movie_finder

    def movies_directed_by(self, director):
        return [
            movie for movie in self._movie_finder.find_all()
            if movie.director == director
        ]

    def movies_released_in(self, year):
        return [
            movie for movie in self._movie_finder.find_all()
            if movie.year == year
        ]

```

---

TITLE: Defining Application Configuration - YAML
DESCRIPTION: This YAML snippet shows a sample `config.yml` file used for application configuration. It defines settings like the `request_timeout` for GitHub API calls and default values (`query`, `limit`) that are injected into the Flask views via the Dependency Injector container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_23

LANGUAGE: yaml
CODE:

```
github:
  request_timeout: 10
default:
  query: "Dependency Injector"
  limit: 10
```

---

TITLE: Environment Variable Interpolation Example (INI/Python)
DESCRIPTION: Illustrates how environment variable interpolation happens before parsing. An INI configuration file with an environment variable placeholder is shown before and after interpolation when the variable is undefined. A Python snippet demonstrates that the resulting value after YAML parsing is `None`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_14

LANGUAGE: ini
CODE:

```
section:
  option: ${ENV_NAME}
```

LANGUAGE: ini
CODE:

```
section:
  option:
```

LANGUAGE: python
CODE:

```
assert container.config.section.option() is None
```

---

TITLE: Displaying Flask Application Structure using Bash
DESCRIPTION: This Bash snippet outlines the directory and file structure for the example Flask application (`githubnavigator`). It shows the organization of templates, source files (application, containers, services, views, tests), configuration (`config.yml`), and dependencies (`requirements.txt`).
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/flask.rst#_snippet_0

LANGUAGE: bash
CODE:

```
./
├── githubnavigator/
│   ├── templates
│   │   ├── base.html
│   │   └── index.py
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── services.py
│   ├── tests.py
│   └── views.py
├── config.yml
└── requirements.txt
```

---

TITLE: Example Pytest Test Output
DESCRIPTION: Sample console output generated after running the unit tests with `pytest` and the coverage plugin. It shows the test execution progress (passing tests indicated by '...') and concludes with a coverage summary table, listing the percentage of code covered by tests for each module in the `giphynavigator` package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_6

LANGUAGE: text
CODE:

```
platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
plugins: cov-6.0.0, anyio-4.4.0, asyncio-0.24.0, aiohttp-1.0.5
asyncio: mode=Mode.STRICT, default_loop_scope=None

giphynavigator/tests.py ...                                     [100%]

---------- coverage: platform darwin, python 3.10.0-final-0 ----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
giphynavigator/__init__.py          0      0   100%
giphynavigator/application.py      11      0   100%
giphynavigator/containers.py        7      0   100%
giphynavigator/endpoints.py        20      0   100%
giphynavigator/giphy.py            14      9    36%
giphynavigator/services.py          9      1    89%
giphynavigator/tests.py            37      0   100%
---------------------------------------------------
TOTAL                              98     10    90%
```

---

TITLE: Defining Database Utilities with SQLAlchemy Declarative Base and Session Factory in Python
DESCRIPTION: Sets up the SQLAlchemy declarative base class, engine creation, and session factory encapsulated in a utility class. This module handles low-level database configuration and session management needed throughout the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_6

LANGUAGE: python
CODE:

```
Contents of webapp/database.py defining base, engine, and sessions
```

---

TITLE: Displaying Aiohttp Project Structure in Bash
DESCRIPTION: This Bash snippet shows the directory and file layout for the example Giphy Navigator Aiohttp application. It illustrates the organization of components like containers, handlers, services, configuration, and tests.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/aiohttp.rst#_snippet_0

LANGUAGE: bash
CODE:

```
./
├── giphynavigator/
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── giphy.py
│   ├── handlers.py
│   ├── services.py
│   └── tests.py
├── config.yml
└── requirements.txt
```

---

TITLE: Creating Virtual Environment for Python Dependency Injector Example
DESCRIPTION: Commands to create and activate a Python virtual environment for isolating the application dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-single-container/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
python3 -m venv venv
. venv/bin/activate
```

---

TITLE: Expected Pytest Output with Coverage - Text
DESCRIPTION: Displays the typical console output when unit tests are run successfully using `pytest` with the coverage plugin. It shows the test execution progress (e.g., '..'), the test results summary, and a detailed coverage report showing the percentage of code covered per file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_6

LANGUAGE: text
CODE:

```
platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
plugins: cov-6.0.0, flask-1.3.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 2 items

githubnavigator/tests.py ..                                     [100%]

---------- coverage: platform darwin, python 3.10.0-final-0 ----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
githubnavigator/__init__.py          0      0   100%
githubnavigator/application.py      13      0   100%
githubnavigator/containers.py        8      0   100%
githubnavigator/services.py         14      0   100%
githubnavigator/tests.py            34      0   100%
githubnavigator/views.py            10      0   100%
----------------------------------------------------
TOTAL                               79      0   100%
```

---

TITLE: Creating a Dockerfile for the Monitoring Daemon - Bash
DESCRIPTION: Defines a Dockerfile to build the monitoring daemon container using the official Python 3.13 image. It sets the working directory, copies source code, installs dependencies listed in requirements.txt, and configures the container to launch the monitoring daemon as a module. Dependencies: Docker must be installed; the requirements.txt file and the monitoringdaemon package must exist. The resulting container is ready to run the monitoring service.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_2

LANGUAGE: bash
CODE:

```
FROM python:3.13-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

RUN apt-get install openssl \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -rf ~/.cache

CMD ["python", "-m", "monitoringdaemon"]
```

---

TITLE: Listing Application Directory Structure in Bash
DESCRIPTION: Shows the file and directory layout of the Sanic example application using a bash code block. This structure defines the organization of the app into modules such as containers.py, handlers.py, services.py, and tests.py, plus configuration and requirements files. Understanding this structure is essential for navigating and extending the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/sanic.rst#_snippet_4

LANGUAGE: bash
CODE:

```
./
├── giphynavigator/
│   ├── __init__.py
│   ├── __main__.py
│   ├── application.py
│   ├── containers.py
│   ├── giphy.py
│   ├── handlers.py
│   ├── services.py
│   └── tests.py
├── config.yml
└── requirements.txt
```

---

TITLE: Running the Example Script - Bash
DESCRIPTION: Executes the main example script using the Python interpreter associated with the activated virtual environment. This runs the code demonstrating the decoupled packages.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/decoupled-packages/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
python -m example
```

---

TITLE: Attribute Injection with Factory Provider in dependency_injector (Python)
DESCRIPTION: This snippet covers using the add_attributes() method with Factory providers to inject attributes into created objects. Attribute injections complement constructor arguments, allowing finer-grained dependency placement post-instantiation. Requires Python and dependency_injector; supports attribute key-value pairs for additional configuration. Dependencies can be any values or providers that resolve at creation time.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_2

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_attribute_injections.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-18

```

---

TITLE: Setting Up Basic YAML Configuration
DESCRIPTION: Defines configuration values for the CSV movie finder, including file path and delimiter settings.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_7

LANGUAGE: yaml
CODE:

```
finder:

  csv:
    path: "data/movies.csv"
    delimiter: ","

```

---

TITLE: Running the Password Hashing Example with Python
DESCRIPTION: Command to execute the password hashing example application that demonstrates Callable provider injection using dependency-injector. The example is contained in example.py.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/password-hashing/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
python example.py
```

---

TITLE: Checking Docker and Docker Compose Versions - Bash
DESCRIPTION: Checks that required versions of Docker and Docker Compose are installed by running command-line queries. These commands should be executed in a terminal before proceeding with the tutorial to ensure that containerization prerequisites are satisfied. Docker and Docker Compose must be installed and accessible via the command line for proper setup.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_0

LANGUAGE: bash
CODE:

```
docker --version
docker compose version
```

---

TITLE: Main container class for dependency injection setup (Python)
DESCRIPTION: Defines a declarative dependency injection container using the 'dependency-injector' library, which will hold all application components, such as factories and singletons, to manage dependencies centrally.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_1

LANGUAGE: Python
CODE:

```
"""Containers module."""

from dependency_injector import containers


class Container(containers.DeclarativeContainer):
    ...
```

---

TITLE: Running the Password Hashing Example (Bash)
DESCRIPTION: This command executes the Python script containing the password hashing example. Running this command will demonstrate the functionality implemented in 'example.py'.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/password-hashing.rst#_snippet_1

LANGUAGE: bash
CODE:

```
python example.py
```

---

TITLE: Activating Python Virtual Environment (Bash)
DESCRIPTION: This command sources the activation script for the 'venv' virtual environment. Activating the environment modifies the shell's PATH so that commands like `python` and `pip` refer to the executables within the virtual environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
. venv/bin/activate
```

---

TITLE: Defining an Asynchronous Service with Redis Dependency in Python
DESCRIPTION: Implements an example `Service` class in `services.py` that depends on an `aioredis.Redis` connection pool, injected during initialization. It provides asynchronous methods `process` to set a key-value pair in Redis and `get` to retrieve the value associated with a key.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-redis.rst#_snippet_2

LANGUAGE: Python
CODE:

```
"Services module."

import uuid

import aioredis


class Service:
    """Service that works with redis.

    Service has a dependency on redis connection pool. It uses it for
    setting and getting a key asynchronously.
    """

    def __init__(self, redis: aioredis.Redis) -> None:
        """Initialize service.

        Args:
            redis (aioredis.Redis): Redis connection pool.
        """
        self.redis = redis

    async def process(self) -> str:
        """Set key in redis.

        Returns:
            str: Value of the key that was set.
        """
        key = str(uuid.uuid4())
        value = str(uuid.uuid4())
        await self.redis.set(key, value, expire=60)
        return value

    async def get(self, key: str) -> str | None:
        """Get key from redis.

        Args:
            key (str): Key to get.

        Returns:
            str | None: Value of the key or None if key does not exist.
        """
        return await self.redis.get(key)

```

---

TITLE: Updating Dependencies in requirements.txt
DESCRIPTION: Lists required Python packages for the application including Dependency Injector, Flask, Bootstrap-Flask, PyGithub, and PyYAML for configuration parsing.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_17

LANGUAGE: bash
CODE:

```
dependency-injector
flask
bootstrap-flask
pygithub
pyyaml
```

---

TITLE: Running the Starlette Example Application (Bash)
DESCRIPTION: Shows two alternative commands to run the Starlette application defined in `example.py`. The first command runs the script directly using Python, which might include custom logging configuration. The second uses `uvicorn`, a common ASGI server, with the `--factory` option to dynamically load the application instance (presumably `container.app`) from the `example` module.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/starlette-lifespan/README.rst#_snippet_2

LANGUAGE: Bash
CODE:

```
python example.py
# or (logging won't be configured):
uvicorn --factory example:container.app
```

---

TITLE: Creating Application Entry Point with Dependency Injection
DESCRIPTION: Implements the main module with dependency wiring to inject the MovieLister from the container into the main function.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_8

LANGUAGE: python
CODE:

```
"""Main module."""

from dependency_injector.wiring import Provide, inject

from .listers import MovieLister
from .containers import Container


@inject
def main(lister: MovieLister = Provide[Container.lister]) -> None:
    print("Francis Lawrence movies:")
    for movie in lister.movies_directed_by("Francis Lawrence"):
        print("\t-", movie)

    print("2016 movies:")
    for movie in lister.movies_released_in(2016):
        print("\t-", movie)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    main()

```

---

TITLE: Sample pytest Output with Coverage Report
DESCRIPTION: This snippet presents example output from running the pytest command with coverage, showing testing environment details, test collection and execution status (3 tests passed), and a coverage summary of individual files and overall project coverage percentage. It helps verify test success and coverage metrics.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_6

LANGUAGE:
CODE:

```
platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
plugins: cov-6.0.0, anyio-4.4.0, asyncio-0.24.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 3 items

giphynavigator/tests.py ...                                     [100%]

---------- coverage: platform darwin, python 3.10.0-final-0 ----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
giphynavigator/__init__.py          0      0   100%
giphynavigator/__main__.py          4      4     0%
giphynavigator/application.py      10      0   100%
giphynavigator/containers.py        7      0   100%
giphynavigator/giphy.py            14      9    36%
giphynavigator/handlers.py         11      0   100%
giphynavigator/services.py          9      1    89%
giphynavigator/tests.py            39      0   100%
---------------------------------------------------
TOTAL                              94     14    85%
```

---

TITLE: Disabling Automatic Wiring in Python
DESCRIPTION: Shows how to configure wiring but disable the automatic wiring behavior, requiring manual calling of the wire() method.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_10

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=["yourapp.module1"],
        auto_wire=False,
    )


if __name__ == "__main__":
    container = Container()  # container.wire() is NOT called automatically
    container.wire()         # wire to "yourapp.module1"
    ...
```

---

TITLE: Initializing Dependency Injector Container in Python
DESCRIPTION: Creates an initial, empty dependency injection container class `Container` in `containers.py`, inheriting from `dependency_injector.containers.DeclarativeContainer`. This container will later hold application components and manage their dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_6

LANGUAGE: Python
CODE:

```
"""Containers module."""

from dependency_injector import containers


class Container(containers.DeclarativeContainer):
    ...
```

---

TITLE: Example Daemon Log Output (Bash)
DESCRIPTION: This snippet shows sample log output from the running monitoring daemon container. It demonstrates the dispatcher starting up and the HttpMonitors performing checks against configured URLs, including response codes, content lengths, and request times.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_22

LANGUAGE: bash
CODE:

```
Starting asyncio-daemon-tutorial_monitor_1 ... done
Attaching to asyncio-daemon-tutorial_monitor_1
monitor_1  | [2020-08-08 18:09:08,540] [INFO] [Dispatcher]: Starting up
monitor_1  | [2020-08-08 18:09:08,618] [INFO] [HttpMonitor]: Check
monitor_1  |     GET http://example.com
monitor_1  |     response code: 200
monitor_1  |     content length: 648
monitor_1  |     request took: 0.077 seconds
monitor_1  | [2020-08-08 18:09:08,722] [INFO] [HttpMonitor]: Check
monitor_1  |     GET https://httpbin.org/get
monitor_1  |     response code: 200
monitor_1  |     content length: 310
monitor_1  |     request took: 0.18 seconds
monitor_1  | [2020-08-08 18:09:13,619] [INFO] [HttpMonitor]: Check
monitor_1  |     GET http://example.com
monitor_1  |     response code: 200
monitor_1  |     content length: 648
monitor_1  |     request took: 0.066 seconds
monitor_1  | [2020-08-08 18:09:13,681] [INFO] [HttpMonitor]: Check
monitor_1  |     GET https://httpbin.org/get
monitor_1  |     response code: 200
monitor_1  |     content length: 310
monitor_1  |     request took: 0.126 seconds
```

---

TITLE: Creating Abstract Factory Providers in dependency_injector (Python)
DESCRIPTION: This snippet illustrates using AbstractFactory providers for cases when the concrete implementation of a base class is not determined at container definition. An AbstractFactory restricts provided objects to a specified type and requires explicit override before use. It is based on Factory and has a usage pattern requiring dependency_injector. Dependencies include a base type, with the override pattern for dynamic binding.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_6

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/abstract_factory.py
   :language: python
   :lines: 3-
   :emphasize-lines: 34

```

---

TITLE: Injecting Initialization Arguments with Factory Provider in dependency_injector (Python)
DESCRIPTION: This snippet shows how Factory providers can manage complex object graphs by injecting dependencies at construction and passing context-specific arguments. It illustrates context argument appending, keyword argument precedence, and how to deeply nest dependencies for layered assembly. Requires Python and dependency_injector; suitable for scenarios where objects need runtime-specific values or differential parameterization at instantiation.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/factory.rst#_snippet_1

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/factory_init_injections.py
   :language: python
   :lines: 3-

```

---

TITLE: Integrating with Flask using Dependency Injector in Python
DESCRIPTION: Example showing how to integrate Python Dependency Injector with the Flask web framework by wiring container providers to Flask view functions.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_14

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from flask import Flask, request


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )


app = Flask(__name__)
container = Container()
container.config.api_key.from_env("API_KEY", required=True)
container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
container.wire(modules=[__name__])


@app.route("/")
@inject
def index(api_client: ApiClient = Provide[Container.api_client]):
    query = request.args.get("query", "")
    return api_client.search(query=query)


if __name__ == "__main__":
    app.run()
```

---

TITLE: Installing Project Requirements for Django + Dependency Injector
DESCRIPTION: Command to install all the required Python packages listed in the requirements.txt file, including Django and Dependency Injector.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/django/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Specifying Dependency: flake8 (Python)
DESCRIPTION: Adds 'flake8', a command-line utility for enforcing style guide compliance. It wraps PyFlakes, pycodestyle, and McCabe.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_6

LANGUAGE: Python requirements
CODE:

```
flake8
```

---

TITLE: Configuring Application Monitors (YAML)
DESCRIPTION: This YAML snippet provides example configuration for the monitoring daemon. It defines logging format and level, and configuration sections for two specific monitors (`example` and `httpbin`). Each monitor's configuration includes the HTTP method, URL, timeout, and check interval.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_20

LANGUAGE: yaml
CODE:

```
log:
  level: "INFO"
  format: "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"

monitors:

  example:
    method: "GET"
    url: "http://example.com"
    timeout: 5
    check_every: 5

  httpbin:
    method: "GET"
    url: "https://httpbin.org/get"
    timeout: 5
    check_every: 5
```

---

TITLE: Resetting Singletons in Sub-Containers with Python Dependency Injector
DESCRIPTION: This snippet illustrates resetting singletons not only in the main container but also in nested sub-containers such as providers.Container and providers.DependenciesContainer using the .reset_singletons() method. It shows the hierarchical effect of the reset operation, ensuring all singleton instances within nested containers are cleared. Requires Dependency Injector and container structure with sub-containers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/reset_singletons.rst#_snippet_1

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class Subcontainer(containers.DeclarativeContainer):
    sub_service = providers.Singleton(object)

class Container(containers.DeclarativeContainer):
    subcontainer = providers.Container(Subcontainer)

container = Container()
container.subcontainer().sub_service()
container.reset_singletons()  # Resets all singletons including those in subcontainers
```

---

TITLE: Overriding Dependency Injector Providers Declaratively with Decorator in Python
DESCRIPTION: Shows how to use the @containers.override decorator to declaratively override providers in a Dependency Injector container. The decorator takes a target container as an argument, enabling providers in the decorated container to override those with matching names in the target. This approach is ideal for modular applications or extensions, as it allows dynamic behavior changes by importing modules without modifying application code. Requires dependency_injector and Python decorators knowledge. Providers are replaced by name and must match across containers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/overriding.rst#_snippet_1

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers

class Service:
    ...

class ExtensionService(Service):
    ...

class MainContainer(containers.DeclarativeContainer):
    service = providers.Singleton(Service)

@containers.override(MainContainer)
class ExtensionContainer(containers.DeclarativeContainer):
    service = providers.Singleton(ExtensionService)

```

---

TITLE: Creating and Activating Virtual Environment for Django Project
DESCRIPTION: Commands to create a virtual environment named 'venv' and activate it for the Django application. This isolates the project dependencies from the system Python installation.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/django/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
virtualenv venv
. venv/bin/activate
```

---

TITLE: Setting Github Personal Access Token (Bash)
DESCRIPTION: This command sets the `GITHUB_TOKEN` environment variable to your personal access token. This is necessary for authenticated requests to the Github API, significantly increasing the hourly rate limit compared to unauthenticated requests.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_7

LANGUAGE: bash
CODE:

```
export GITHUB_TOKEN=<your token>
```

---

TITLE: Specifying Dependency: tox (Python)
DESCRIPTION: Adds 'tox', a generic virtual environment management and test automation tool. It's often used for checking packages in different Python environments.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_4

LANGUAGE: Python requirements
CODE:

```
tox
```

---

TITLE: Error Handling in Strict Mode (Python)
DESCRIPTION: Illustrates how the `from_*` methods behave in strict mode, raising exceptions (`FileNotFoundError`, `ValueError`) if configuration files do not exist or required data (like environment variables or dictionary keys) is undefined.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_20

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True)


if __name__ == "__main__":
    container = Container()

    try:
        container.config.from_yaml("does-not_exist.yml")  # raise exception
    except FileNotFoundError:
        ...

    try:
        container.config.from_ini("does-not_exist.ini")  # raise exception
    except FileNotFoundError:
        ...

    try:
        container.config.from_pydantic(EmptySettings())  # raise exception
    except ValueError:
        ...

    try:
        container.config.from_env("UNDEFINED_ENV_VAR")  # raise exception
    except ValueError:
        ...

    try:
        container.config.from_dict({})  # raise exception
    except ValueError:
        ...
```

---

TITLE: Expected Sanic Application Startup Log Output
DESCRIPTION: This snippet shows a sample log output from starting the Sanic application, indicating the server is running and listening on http://0.0.0.0:8000, and the worker process has started successfully. It is an info-level log useful for confirming proper launch of the server.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_3

LANGUAGE:
CODE:

```
[2020-09-23 18:16:31 -0400] [48258] [INFO] Goin' Fast @ http://0.0.0.0:8000
[2020-09-23 18:16:31 -0400] [48258] [INFO] Starting worker [48258]
```

---

TITLE: Defining Project Dependencies in requirements.txt
DESCRIPTION: Specifies the initial Python package dependencies (`dependency-injector` and `flask`) required for the project in the `requirements.txt` file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_2

LANGUAGE: Bash
CODE:

```
dependency-injector
flask
```

---

TITLE: Testing FastAPI Endpoints Using Provider Overriding - Python
DESCRIPTION: Illustrates how to write tests for the FastAPI application using `pytest`. It specifically demonstrates `dependency_injector`'s provider overriding feature, showing how to use a context manager (`with container.provider.override(...)`) to replace production dependencies (like the `GiphyClient`) with mock objects during testing, ensuring isolated and predictable test execution.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi.rst#_snippet_4

LANGUAGE: python
CODE:

```
# Code included from ../../examples/miniapps/fastapi/giphynavigator/tests.py
# Emphasized lines 29, 57, 72 likely highlight points of provider overriding or test setup.
```

---

TITLE: Using Dependency Injector Framework in Python
DESCRIPTION: Demonstrates how to use the Dependency Injector framework to manage dependencies. It creates a container with configuration and providers for ApiClient and Service, and uses the @inject decorator to automatically inject dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/introduction/di_in_python.rst#_snippet_2

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient,
        api_key=config.api_key,
        timeout=config.timeout,
    )

    service = providers.Factory(
        Service,
        api_client=api_client,
    )


@inject
def main(service: Service = Provide[Container.service]) -> None:
    ...


if __name__ == "__main__":
    container = Container()
    container.config.api_key.from_env("API_KEY", required=True)
    container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
    container.wire(modules=[__name__])

    main()  # <-- dependency is injected automatically

    with container.api_client.override(mock.Mock()):
        main()  # <-- overridden dependency is injected automatically
```

---

TITLE: Using .reset_singletons() with a Context Manager in Python Dependency Injector
DESCRIPTION: This snippet presents usage of the .reset_singletons() method within a Python context manager. It ensures singleton instances are reset both on entering and exiting the context, providing a scoped and controlled reset of singletons during a block of code execution. This pattern helps isolate singleton state changes to specific code segments. Requires Dependency Injector and container with singleton providers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/reset_singletons.rst#_snippet_2

LANGUAGE: python
CODE:

```
from dependency_injector import containers, providers
from contextlib import contextmanager

class Container(containers.DeclarativeContainer):
    service = providers.Singleton(object)

container = Container()

@contextmanager
def reset_singletons_context(container):
    container.reset_singletons()
    try:
        yield
    finally:
        container.reset_singletons()

with reset_singletons_context(container):
    container.service()  # Singletons reset on enter and exit
```

---

TITLE: Setting up Virtual Environment - Bash
DESCRIPTION: Creates a standard Python virtual environment named 'venv' in the current directory and activates it. This isolates project dependencies from the system Python installation.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/decoupled-packages/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
python3 -m venv venv
. venv/bin/activate
```

---

TITLE: Strict Mode Error Handling for Undefined Environment Variables (INI/Python)
DESCRIPTION: Demonstrates that in strict mode, environment variable interpolation raises a `ValueError` if it encounters an undefined variable without a default value within a configuration file (e.g., INI).
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_21

LANGUAGE: ini
CODE:

```
section:
  option: ${UNDEFINED}
```

LANGUAGE: python
CODE:

```
    try:
        container.config.from_yaml("undefined_env.yml")  # raise exception
    except ValueError:
        ...
```

---

TITLE: Defining Python Dependencies for Runtime and Testing
DESCRIPTION: Specifies the necessary Python libraries for the project, typically used in a `requirements.txt` file. Runtime dependencies include `dependency-injector`, `fastapi`, `uvicorn`, and `redis` (version 4.2 or higher). Testing dependencies, marked by a comment, include `pytest`, `pytest-asyncio`, `pytest-cov`, and `httpx`. These packages can be installed using pip.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-redis/requirements.txt#_snippet_0

LANGUAGE: plaintext
CODE:

```
dependency-injector
fastapi
uvicorn
redis>=4.2

# For testing:
pytest
pytest-asyncio
pytest-cov
httpx
```

---

TITLE: Blueprint View with Dependency Injection in Python
DESCRIPTION: Implements a Flask blueprint that has dependencies on a search service and configuration options, injected via Wiring to facilitate separation of concerns and testability. This module defines HTTP route handlers using injected dependencies to process requests.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/flask-blueprints.rst#_snippet_1

LANGUAGE: python
CODE:

```
# Content of githubnavigator/blueprints/example.py
# Defines Flask blueprint with dependency injection for search service and configs
from flask import Blueprint, render_template, request
from dependency_injector.wiring import inject, Provide

example_bp = Blueprint('example', __name__)

@inject
@example_bp.route('/', methods=['GET'])
def index(search_service=Provide['github_service'], config=Provide['config']):
    query = request.args.get('q', '')
    results = search_service.search_repositories(query) if query else []
    return render_template('index.html', results=results, config=config)

```

---

TITLE: Setting up Virtual Environment with Bash
DESCRIPTION: This snippet demonstrates how to create and activate a Python virtual environment for isolating project dependencies using bash commands. It requires having virtualenv installed. The commands create a new virtual environment named "venv" and activate it for use in the current shell session. This prepares the environment for consistent dependency installation and package management.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
virtualenv venv
. venv/bin/activate
```

---

TITLE: Specifying Dependency: boto3 (Python)
DESCRIPTION: Includes 'boto3', the Amazon Web Services (AWS) SDK for Python. It allows Python developers to write software that makes use of AWS services like S3, EC2, etc.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_18

LANGUAGE: Python requirements
CODE:

```
boto3
```

---

TITLE: Extending Monitoring to `https://httpbin.org`
DESCRIPTION: Adds configuration and container factory provider for a monitor targeting `https://httpbin.org`. The section updates the container setup to include a new monitor for HTTPS endpoint verification, leveraging the same `HttpMonitor` class and custom options. The configuration supports easy extension for additional URLs.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_18

LANGUAGE: YAML
CODE:

```
monitors:

  # Existing monitor settings

  # New monitor for https://httpbin.org
  httpbin:
    method: "GET"
    url: "https://httpbin.org"
    timeout: 5
    check_every: 5
```

---

TITLE: Running the Example Application with Environment Variable - Python
DESCRIPTION: Sets the environment variable 'GIPHY_API_KEY' and launches the 'giphynavigator.application' module as the main application. Dependencies: Python environment with required packages installed, Giphy API key (obtainable from Giphy documentation). Output: The REST API server listens for HTTP requests at http://0.0.0.0:8080/.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/aiohttp/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
export GIPHY_API_KEY=wBJ2wZG7SRqfrU9nPgPiWvORmloDyuL0
python -m giphynavigator.application
```

---

TITLE: Expected Flask Startup Output - Text
DESCRIPTION: This snippet shows the typical console output when the Flask development server successfully starts. It confirms the application file being served, the environment mode, debug status, and the local address where the application is running (http://127.0.0.1:5000/).
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_3

LANGUAGE: text
CODE:

```
* Serving Flask app "githubnavigator.application" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with fsevents reloader
* Debugger is active!
* Debugger PIN: 473-587-859
```

---

TITLE: Resource Provider with Wiring and Closing in Flask Application
DESCRIPTION: Integrates resource provider with wiring to implement per-function execution scope in a Flask application. The Closing marker ensures that the resource is shutdown after each function execution.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_9

LANGUAGE: python
CODE:

```
# This is a partial code snippet highlighted in the documentation
# The full implementation would include Flask setup and more components
@app.route("/")
@inject
def index(service: Closing[Service] = Provide[Container.service]):
    return "Hello, World!"
```

---

TITLE: Movie entity class representing a movie object (Python)
DESCRIPTION: Defines the Movie class with attributes for title, year, and director, including a custom **repr** method for readable string representations. This class models the core movie data used throughout the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_3

LANGUAGE: Python
CODE:

```
"""Movie entities module."""


class Movie:

    def __init__(self, title: str, year: int, director: str):
        self.title = str(title)
        self.year = int(year)
        self.director = str(director)

    def __repr__(self):
        return "{0}(title={1}, year={2}, director={3})".format(
            self.__class__.__name__,
            repr(self.title),
            repr(self.year),
            repr(self.director),
        )
```

---

TITLE: Specifying Dependency: pip (Python)
DESCRIPTION: Adds 'pip', the standard package installer for Python. While usually available by default, explicitly listing it ensures a specific version or presence.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_10

LANGUAGE: Python requirements
CODE:

```
pip
```

---

TITLE: Creating Python Virtual Environment (Bash)
DESCRIPTION: This command uses `virtualenv` to create a new, isolated Python environment named 'venv' in the current directory. This practice helps manage project-specific dependencies without conflicts with the system Python installation.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
virtualenv venv
```

---

TITLE: Loading Configuration from INI File Using Dependency Injector in Python
DESCRIPTION: Illustrates how to load configuration data from an INI file using the Configuration provider's from_ini method. Supports environment variable interpolation within the INI file for dynamic values. Alternatively, INI file paths can be passed when declaring the Configuration provider in a container to load configuration automatically.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_0

LANGUAGE: python
CODE:

```
class Container(containers.DeclarativeContainer):

    config = providers.Configuration(ini_files=["./config.ini"])


if __name__ == "__main__":
    container = Container()  # Config is loaded from ./config.ini
```

---

TITLE: Resource Subclass Initializer in Python
DESCRIPTION: Creates a custom resource initializer by subclassing resources.Resource. This approach provides explicit init and shutdown methods for more complex resource management.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_7

LANGUAGE: python
CODE:

```
from dependency_injector import resources


class MyResource(resources.Resource):

    def init(self, argument1=..., argument2=...) -> SomeResource:
        return SomeResource()

    def shutdown(self, resource: SomeResource) -> None:
        # shutdown
        ...


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        MyResource,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Basic Module Import and Function Call in Python
DESCRIPTION: Demonstrates a simple relative import of a module and calling a function from it.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/wiring.rst#_snippet_7

LANGUAGE: python
CODE:

```
from . import module

module.fn()
```

---

TITLE: Handling Undefined Environment Variables in Configuration (Python)
DESCRIPTION: Demonstrates the default behavior of the Configuration provider where undefined environment variables without defaults are replaced with empty strings during interpolation. Also shows how to enforce variable existence by setting `envs_required=True` when loading configuration from a YAML file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_13

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_env_interpolation_os_default.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12
```

LANGUAGE: python
CODE:

```
container.config.from_yaml("config.yml", envs_required=True)
```

---

TITLE: Container Definition in Python for Dependency Injection
DESCRIPTION: Defines a declarative container in Python using Dependency Injector, outlining dependencies for the Flask application components such as services and configuration. This container manages dependency wiring, facilitating component injections across the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/flask-blueprints.rst#_snippet_0

LANGUAGE: python
CODE:

```
# Content of githubnavigator/containers.py
# Defines dependency injection container for the Flask app components
import dependency_injector.containers as containers
import dependency_injector.providers as providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    github_service = providers.Singleton(
        GithubService,  # Presumed service class for GitHub interactions
        token=config.github_token
    )
    app_settings = providers.Configuration()
    # Additional dependencies can be wired here

```

---

TITLE: Using ThreadSafeSingleton for Thread-Safe Singleton in Python
DESCRIPTION: This snippet introduces `ThreadSafeSingleton` as a thread-safe variant of the singleton provider, suitable for multi-threaded environments, avoiding race conditions by ensuring only one instance is created per container. The code demonstrates its declaration and typical usage.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/singleton.rst#_snippet_3

LANGUAGE: python
CODE:

```
dependency_injector.providers.ThreadSafeSingleton

thread_safe_singleton = dependency_injector.providers.ThreadSafeSingleton(SomeClass)

# Inject and use in multi-threaded environment
container = dependency_injector.containers.Container()
container.thread_safe_service = thread_safe_singleton
```

---

TITLE: Defining Application Structure for FastAPI-Redis Example in Bash
DESCRIPTION: Displays the directory and file structure for the example FastAPI application using Redis and Dependency Injector. This layout organizes the project into distinct modules for the main application, container configuration, Redis utilities, services, and tests.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-redis.rst#_snippet_0

LANGUAGE: Bash
CODE:

```
./
├── fastapiredis/
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── redis.py
│   ├── services.py
│   └── tests.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

TITLE: Resetting the Singleton Instance in Python
DESCRIPTION: This code snippet explains how to reset a memorized singleton object by invoking its `reset()` method. Resetting clears the reference, allowing a fresh instance upon next access. The reset operation is also demonstrated within a context manager to automatically reset on entering and exiting the scope.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/singleton.rst#_snippet_1

LANGUAGE: python
CODE:

```
with container.service.reset():
    # The singleton instance is reset here
    pass
```

---

TITLE: Overriding Providers Using override_providers() Method in Python
DESCRIPTION: This snippet showcases how to override providers on an existing container instance using the override_providers() method, which accepts keyword arguments mapping provider names to alternative implementations. This dynamic override allows the container to return mock or substituted objects at runtime.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/declarative.rst#_snippet_4

LANGUAGE: python
CODE:

```
container = Container()

container.override_providers(foo=mock.Mock(Foo), bar=mock.Mock(Bar))

assert isinstance(container.foo(), mock.Mock)
assert isinstance(container.bar(), mock.Mock)
```

---

TITLE: Implementing Flask View with Dependency Injection - Python
DESCRIPTION: This Python snippet defines a Flask view function `index` that demonstrates dependency injection using the `dependency_injector.wiring.inject` decorator and `dependency_injector.providers.Provide` provider. It injects a `SearchService` instance and configuration values (`default_query`, `default_limit`) from the application's Dependency Injector container. The view retrieves 'query' and 'limit' parameters from the request arguments, falling back to injected defaults, uses the search service to find repositories, and renders an HTML template ('index.html') with the results.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_22

LANGUAGE: python
CODE:

```
from .containers import Container


@inject
def index(
        search_service: SearchService = Provide[Container.search_service],
        default_query: str = Provide[Container.config.default.query],
        default_limit: int = Provide[Container.config.default.limit.as_int()],
):
    query = request.args.get("query", default_query)
    limit = request.args.get("limit", default_limit, int)

    repositories = search_service.search_repositories(query, limit)

    return render_template(
        "index.html",
        query=query,
        limit=limit,
        repositories=repositories,
    )
```

---

TITLE: Example REST API JSON Response - Giphy Search Endpoint
DESCRIPTION: Shows a sample JSON response from the REST API after performing a search for GIFs related to 'Dependency Injector'. The response includes query parameters, result limits, and a list of GIF objects containing their URLs. Inputs: HTTP request to the API; Outputs: structured JSON representing search results.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/aiohttp/README.rst#_snippet_3

LANGUAGE: json
CODE:

```
{
    "query": "Dependency Injector",
    "limit": 10,
    "gifs": [
        {
            "url": "https://giphy.com/gifs/boxes-dependent-swbf2-6Eo7KzABxgJMY"
        },
        {
            "url": "https://giphy.com/gifs/depends-J56qCcOhk6hKE"
        },
        {
            "url": "https://giphy.com/gifs/web-series-ccstudios-bro-dependent-1lhU8KAVwmVVu"
        },
        {
            "url": "https://giphy.com/gifs/TheBoysTV-friends-friend-weneedeachother-XxR9qcIwcf5Jq404Sx"
        },
        {
            "url": "https://giphy.com/gifs/netflix-a-series-of-unfortunate-events-asoue-9rgeQXbwoK53pcxn7f"
        },
        {
            "url": "https://giphy.com/gifs/black-and-white-sad-skins-Hs4YzLs2zJuLu"
        },
        {
            "url": "https://giphy.com/gifs/always-there-for-you-i-am-here-PlayjhCco9jHBYrd9w"
        },
        {
            "url": "https://giphy.com/gifs/stream-famous-dollar-YT2dvOByEwXCdoYiA1"
        },
        {
            "url": "https://giphy.com/gifs/i-love-you-there-for-am-1BhGzgpZXYWwWMAGB1"
        },
        {
            "url": "https://giphy.com/gifs/life-like-twerk-9hlnWxjHqmH28"
        }
    ]
}
```

---

TITLE: Loading Configuration from a Literal Value Using Dependency Injector in Python
DESCRIPTION: Example demonstrating usage of from_value method to load a single configuration value directly into the Configuration provider. Useful for injecting constants or simple values not sourced from external files or environment variables.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_10

LANGUAGE: python
CODE:

```
# Example usage (content omitted for brevity)
container.config.some_option.from_value(value)
```

---

TITLE: Installing Dependency Injector via pip
DESCRIPTION: This snippet demonstrates installing the Dependency Injector package from PyPI using pip, including handling of pre-compiled wheels for various operating systems and Python versions. It notes the compilation requirements if wheels are unavailable.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/introduction/installation.rst#_snippet_0

LANGUAGE: bash
CODE:

```
pip install dependency-injector
```

---

TITLE: Configuring Application with Container Wiring in Django App
DESCRIPTION: In 'web/apps.py', the container is wired to the application's views module, enabling automatic injection of dependencies into view functions or classes. This configuration ensures that dependencies are properly injected according to the wiring rules, facilitating modular dependency management.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/django.rst#_snippet_3

LANGUAGE: Python
CODE:

```
.. literalinclude:: ../../examples/miniapps/django/web/apps.py
   :language: python
   :emphasize-lines: 13
```

---

TITLE: Running Pytest for Coverage Reporting
DESCRIPTION: Shows the bash command to run pytest over the movies/tests.py file and generate a coverage report for the movies package. Requires pytest and coverage to be installed and the test file located at 'movies/tests.py'. Inputs are test cases; output is coverage summary printed to terminal.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/cli.rst#_snippet_17

LANGUAGE: bash
CODE:

```
pytest movies/tests.py --cov=movies
```

---

TITLE: Run Unit Tests with Coverage using Docker Compose
DESCRIPTION: This command executes the unit tests located in `webapp/tests.py` using `pytest` within a temporary `webapp` container. It also generates a code coverage report for the `webapp` directory using the `--cov` flag.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/README.rst#_snippet_3

LANGUAGE: bash
CODE:

```
docker compose run --rm webapp py.test webapp/tests.py --cov=webapp
```

---

TITLE: Requiring Specific Configuration Options with `.required()` (Python)
DESCRIPTION: Demonstrates using the `.required()` modifier during injection to ensure a specific configuration option exists, raising an error if it's undefined. This can be used independently of the global strict mode setting.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_23

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_required.py
   :language: python
   :lines: 11-20
   :emphasize-lines: 8-9
```

---

TITLE: Implementing Giphy Search Service in Python
DESCRIPTION: This Python class defines the SearchService responsible for executing Giphy searches. It depends on a GiphyClient instance, injected via its constructor, to perform the actual API call and formats the results.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_9

LANGUAGE: python
CODE:

```
"""Services module."""

from .giphy import GiphyClient


class SearchService:

    def __init__(self, giphy_client: GiphyClient):
        self._giphy_client = giphy_client

    async def search(self, query, limit):
        """Search for gifs and return formatted data."""
        if not query:
            return []

        result = await self._giphy_client.search(query, limit)

        return [{"url": gif["url"]} for gif in result["data"]]
```

---

TITLE: Showing Test and Coverage Report Output - Bash
DESCRIPTION: This Bash snippet displays the expected output after running the `pytest` command with coverage. It shows the test collection progress, the results of the tests (two passed), and the coverage report summary, indicating 100% coverage for all tested modules.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_29

LANGUAGE: bash
CODE:

```
platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
plugins: cov-3.0.0, flask-1.2.0
collected 2 items

githubnavigator/tests.py ..                                     [100%]

---------- coverage: platform darwin, python 3.10.0-final-0 ----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
githubnavigator/__init__.py          0      0   100%
githubnavigator/application.py      13      0   100%
githubnavigator/containers.py        8      0   100%
githubnavigator/services.py         14      0   100%
githubnavigator/tests.py            34      0   100%
githubnavigator/views.py            10      0   100%
----------------------------------------------------
TOTAL                               79      0   100%
```

---

TITLE: Implementing the Application Entry Point in Python
DESCRIPTION: Reference to the Python script `example/__main__.py`. This file acts as the main entry point, initializes and wires the dependency injection container, retrieves a service instance (`UserService`), and executes its core logic.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-single-container.rst#_snippet_2

LANGUAGE: python
CODE:

```
# Source: examples/miniapps/application-single-container/example/__main__.py
# Application entry point.
# Initializes container, wires modules, gets service, runs logic.
```

---

TITLE: Displaying Application Directory Structure Using Bash
DESCRIPTION: Shows the overall directory layout of the FastAPI+SQLAlchemy example project, outlining the key modules and configuration files involved in the setup and deployment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_8

LANGUAGE: bash
CODE:

```
./
├── webapp/
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── database.py
│   ├── endpoints.py
│   ├── models.py
│   ├── repositories.py
│   ├── services.py
│   └── tests.py
├── config.yml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

TITLE: Running Unit Tests with Pytest using Bash
DESCRIPTION: Command to execute the project's unit tests located in `giphynavigator/tests.py` using the `pytest` framework. The `--cov=giphynavigator` flag is included to generate a code coverage report for the specified package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_5

LANGUAGE: bash
CODE:

```
py.test giphynavigator/tests.py --cov=giphynavigator
```

---

TITLE: JSON File Example with Environment Variable Interpolation
DESCRIPTION: Sample JSON configuration illustrating environment variable substitution with placeholders like "${ENV_VAR}" and optional default values "${ENV_VAR:default}" used within JSON string values to enable dynamic runtime substitution.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_6

LANGUAGE: json
CODE:

```
{
    "section": {
        "option1": "${ENV_VAR}",
        "option2": "${ENV_VAR}/path",
        "option3": "${ENV_VAR:default}"
    }
}
```

---

TITLE: Asynchronous `_run_monitor` Method for Monitor Checks
DESCRIPTION: Defines an asynchronous static method `_run_monitor` that executes periodic monitor checks. It calculates the interval until the next check, runs the monitor's check method, handles exceptions, and waits asynchronously. Dependencies include `asyncio` and `time`. It is intended for scheduling monitor tasks within an asyncio event loop.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_9

LANGUAGE: Python
CODE:

```
@staticmethod
async def _run_monitor(monitor: Monitor) -> None:
    def _until_next(last: float) -> float:
        time_took = time.time() - last
        return monitor.check_every - time_took

    while True:
        time_start = time.time()

        try:
            await monitor.check()
        except asyncio.CancelledError:
            break
        except Exception:
            monitor.logger.exception("Error executing monitor check")

        await asyncio.sleep(_until_next(last=time_start))
```

---

TITLE: Expected Flask Development Server Output (Text)
DESCRIPTION: This snippet shows the typical console output when the Flask development server starts successfully. It confirms that the application is running, specifies the environment and debug mode, and provides the local address to access the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_6

LANGUAGE: text
CODE:

```
* Serving Flask app "githubnavigator.application" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with fsevents reloader
* Debugger is active!
* Debugger PIN: 473-587-859
```

---

TITLE: Setup Virtual Environment - Bash
DESCRIPTION: Creates a Python virtual environment named `venv` in the current directory and then activates it for the current shell session. This isolates project dependencies, preventing conflicts with system-wide packages.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
virtualenv venv
. venv/bin/activate
```

---

TITLE: Using Custom Type Conversion for Configuration Values (Python)
DESCRIPTION: Demonstrates using the `.as_(callback)` method to apply a custom conversion function to a configuration value before injection. The configuration value is passed as the first argument to the callback function.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_18

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_type_custom.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18
```

---

TITLE: Generator Initializer without Return Value in Python
DESCRIPTION: Shows how to use a generator initializer without returning a resource object. This pattern is useful when the resource provider only needs to perform initialization and shutdown actions.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_6

LANGUAGE: python
CODE:

```
def init_resource(argument1=..., argument2=...):
    # initialization
    ...

    yield

    # shutdown
    ...


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        init_resource,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Install Project Dependencies - Bash
DESCRIPTION: Installs all required Python packages listed in the `requirements.txt` file. This command should be executed within the activated virtual environment to ensure dependencies are installed locally.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Visualizing Example Project Structure
DESCRIPTION: Displays the directory layout of the example application using a bash command representation, illustrating the separation of concerns into different Python modules like `adapters.py`, `containers.py`, and `usecases.py`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/use-cases.rst#_snippet_0

LANGUAGE: bash
CODE:

```

./
└── example/
    ├── __init__.py
    ├── __main__.py
    ├── adapters.py
    ├── containers.py
    └── usecases.py

```

---

TITLE: Using Asynchronous Resource Providers in Python
DESCRIPTION: Demonstrates how to use asynchronous resource providers in an async context. Methods like **call**(), init(), and shutdown() must be awaited when working with async resources.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_13

LANGUAGE: python
CODE:

```
import asyncio


class Container(containers.DeclarativeContainer):

    connection = providers.Resource(init_async_connection)


async def main():
    container = Container()
    connection = await container.connection()
    connection = await container.connection.init()
    connection = await container.connection.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
```

---

TITLE: Creating Configuration Aliases (Python)
DESCRIPTION: Illustrates how to use the Configuration provider as a context manager (`with container.config.set(...)`) to create temporary aliases for configuration options within a specific code block.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_24

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_alias.py
   :language: python
   :lines: 3-
   :emphasize-lines: 14,22
```

---

TITLE: Dependency Injector Container for Logger and Dispatcher
DESCRIPTION: Defines a `Container` class using `dependency_injector` to configure application resources including logging setup and the dispatcher factory. It utilizes configuration from a YAML file and sets up logging to stdout at specified levels and formats. The dispatcher is instantiated through a factory with monitor placeholders, preparing the application for task orchestration.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_10

LANGUAGE: Python
CODE:

```
"""Containers module."""

import logging
import sys

from dependency_injector import containers, providers

from . import dispatcher


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    dispatcher = providers.Factory(
        dispatcher.Dispatcher,
        monitors=providers.List(
            # TODO: add monitors
        ),
    )
```

---

TITLE: Implementing Service Classes with Dependency Injection in Python
DESCRIPTION: Defines service classes that receive their dependencies through constructor injection. Shows how to implement domain logic services with dependencies on database and AWS S3 components.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-multiple-containers.rst#_snippet_3

LANGUAGE: python
CODE:

```
../../examples/miniapps/application-multiple-containers/example/services.py
```

---

TITLE: Setting Flask Environment to Development (Bash)
DESCRIPTION: This command sets the `FLASK_ENV` environment variable to `development`. This enables Flask's development features, such as the debugger and reloader, which are useful during the development phase.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_4

LANGUAGE: bash
CODE:

```
export FLASK_ENV=development
```

---

TITLE: Asynchronous Generator Initializer in Python
DESCRIPTION: Creates a resource provider with an asynchronous generator initializer for handling both async initialization and cleanup. This pattern is ideal for managing connection lifecycles.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_11

LANGUAGE: python
CODE:

```
async def init_async_resource(argument1=..., argument2=...):
    connection = await connect()
    yield connection
    await connection.close()


class Container(containers.DeclarativeContainer):

    resource = providers.Resource(
        init_async_resource,
        argument1=...,
        argument2=...,
    )
```

---

TITLE: Enabling Strict Mode for Configuration (Python)
DESCRIPTION: Shows how to initialize the Configuration provider in strict mode (`strict=True`). In strict mode, accessing any undefined configuration option raises an error.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_19

LANGUAGE: python
CODE:

```
.. literalinclude:: ../../examples/providers/configuration/configuration_strict.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12
```

---

TITLE: Installing Application Requirements Using Pip - Python
DESCRIPTION: Installs all required Python dependencies for the project as specified in 'requirements.txt' using pip. Prerequisite: activate the virtual environment prior to running. Inputs: none (reads from requirements.txt). Output: all packages are installed locally in the virtual environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/aiohttp/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Individual Resource Initialization and Shutdown in Python
DESCRIPTION: Demonstrates how to initialize and shutdown individual resources using the init() and shutdown() methods. This allows for more granular control over resource lifecycles.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/resource.rst#_snippet_2

LANGUAGE: python
CODE:

```
container = Container()
container.thread_pool.init()
container.thread_pool.shutdown()
```

---

TITLE: Calling Aggregated Providers by Key in Python
DESCRIPTION: Shows how to call an aggregated provider by providing its key as a first argument with additional parameters. This allows accessing specific providers from the aggregate.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/aggregate.rst#_snippet_1

LANGUAGE: python
CODE:

```
yaml_reader = container.config_readers("yaml", "./config.yml", foo=...)
```

---

TITLE: Filtering Traversed Providers by Type (Python)
DESCRIPTION: Illustrates how to use the `types` argument with the `.traverse()` method to iterate only over providers of specific types. This example filters for `providers.Resource` instances within the container and prints them. Assumes `container` is an initialized `dependency_injector.containers.Container` instance and `providers` refers to `dependency_injector.providers`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/containers/traversal.rst#_snippet_0

LANGUAGE: python
CODE:

```
container = Container()

for provider in container.traverse(types=[providers.Resource]):
    print(provider)

 # <dependency_injector.providers.Resource(<function init_database at 0x10bd2cb80>) at 0x10d346b40>
 # <dependency_injector.providers.Resource(<function init_cache at 0x10be373a0>) at 0x10d346bc0>
```

---

TITLE: Defining `HttpClient` for Asynchronous HTTP Requests
DESCRIPTION: Creates an `HttpClient` class utilizing `aiohttp` to send asynchronous HTTP requests with specified method, URL, and timeout. The `request()` method manages the client session and returns the server response, enabling monitors to perform web resource checks with non-blocking I/O. Dependencies include `aiohttp`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_13

LANGUAGE: Python
CODE:

```
"""Http client module."""

from aiohttp import ClientSession, ClientTimeout, ClientResponse


class HttpClient:

    async def request(self, method: str, url: str, timeout: int) -> ClientResponse:
        async with ClientSession(timeout=ClientTimeout(timeout)) as session:
            async with session.request(method, url) as response:
                return response
```

---

TITLE: Installing Project Dependencies (Bash)
DESCRIPTION: This command uses `pip`, the Python package installer, to read the list of required libraries from the `requirements.txt` file and install them into the currently active virtual environment. These packages are necessary for the application to function.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Retrieving Aggregated Provider by Attribute Name in Python
DESCRIPTION: Demonstrates how to retrieve an aggregated provider by using its key as an attribute name, offering a more concise syntax for accessing specific providers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/aggregate.rst#_snippet_2

LANGUAGE: python
CODE:

```
yaml_reader = container.config_readers.yaml("./config.yml", foo=...)
```

---

TITLE: Specifying Dependency: numpy (Python)
DESCRIPTION: Includes 'numpy', the fundamental package for scientific computing with Python, providing support for large, multi-dimensional arrays and matrices.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_16

LANGUAGE: Python requirements
CODE:

```
numpy
```

---

TITLE: Creating Tests File in Bash
DESCRIPTION: This snippet shows the project structure and highlights the creation of a new file, 'tests.py', where the application's unit and integration tests will be written.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_18

LANGUAGE: bash
CODE:

```
./
├── giphynavigator/
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── giphy.py
│   ├── handlers.py
│   ├── services.py
│   └── tests.py
├── venv/
├── config.yml
└── requirements.txt
```

---

TITLE: Specifying Dependency: pytest-asyncio (Python)
DESCRIPTION: Includes 'pytest-asyncio', a pytest plugin that provides fixtures and markers to make it easier to test asyncio applications.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_3

LANGUAGE: Python requirements
CODE:

```
pytest-asyncio
```

---

TITLE: Setting Flask Application Entry Point (Bash)
DESCRIPTION: This command sets the `FLASK_APP` environment variable to `githubnavigator.application`. Flask uses this variable to locate the main application instance when executing subcommands like `flask run`.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_3

LANGUAGE: bash
CODE:

```
export FLASK_APP=githubnavigator.application
```

---

TITLE: Run Unit Tests with Coverage - Bash
DESCRIPTION: Executes the unit tests located in `githubnavigator/tests.py` using the `pytest` framework. The `--cov=githubnavigator` flag also enables code coverage analysis, measuring how much of the code in the `githubnavigator` package is exercised by the tests.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask/README.rst#_snippet_5

LANGUAGE: bash
CODE:

```
py.test githubnavigator/tests.py --cov=githubnavigator
```

---

TITLE: Installing Required Dependencies for Python Application
DESCRIPTION: Command to install all the project dependencies specified in the requirements.txt file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-single-container/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Specifying Dependency: pydocstyle (Python)
DESCRIPTION: Adds 'pydocstyle', a static analysis tool for checking compliance of Python docstrings against style conventions.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_8

LANGUAGE: Python requirements
CODE:

```
pydocstyle
```

---

TITLE: Running Pytest Tests and Coverage - Bash
DESCRIPTION: This Bash command executes the `pytest` tests located in `githubnavigator/tests.py`. The `--cov=githubnavigator` flag enables code coverage reporting using `pytest-cov`, targeting the `githubnavigator` package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_28

LANGUAGE: bash
CODE:

```
py.test githubnavigator/tests.py --cov=githubnavigator
```

---

TITLE: Creating SQLAlchemy User Model in Python
DESCRIPTION: Declares an SQLAlchemy ORM model for user entities including attributes like ID and other relevant fields. This model defines the database table schema and serves as the base for data operations performed by the repository.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/fastapi-sqlalchemy.rst#_snippet_5

LANGUAGE: python
CODE:

```
Contents of webapp/models.py with user model definition
```

---

TITLE: Creating Index Page Template Extending Base Layout
DESCRIPTION: Defines the index page (`index.html`) which extends `base.html`. It sets the page title, creates a Bootstrap container, adds a heading, and includes a form with input fields for search query and limit. It uses Jinja2 templating for dynamic content like pre-filling the search query (`{{ query }}`), setting the selected limit (`{{ limit }}`), displaying the result count (`{{ repositories|length }}`), and iterating through `repositories` (though the loop body is incomplete) to display search results in a table.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_13

LANGUAGE: HTML
CODE:

```
{% extends "base.html" %}

{% block title %}Github Navigator{% endblock %}

{% block content %}
<div class="container">
    <h1 class="mb-4">Github Navigator</h1>

    <form>
        <div class="form-group form-row">
            <div class="col-10">
                <label for="search_query" class="col-form-label">
                    Search for:
                </label>
                <input class="form-control" type="text" id="search_query"
                       placeholder="Type something to search on the GitHub"
                       name="query"
                       value="{{ query if query }}">
            </div>
            <div class="col">
                <label for="search_limit" class="col-form-label">
                    Limit:
                </label>
                <select class="form-control" id="search_limit" name="limit">
                    {% for value in [5, 10, 20] %}
                    <option {% if value == limit %}selected{% endif %}>
                        {{ value }}
                    </option>
                    {% endfor %}
                </select>
            </div>
        </div>
    </form>

    <p><small>Results found: {{ repositories|length }}</small></p>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>#</th>
                <th>Repository</th>
                <th class="text-nowrap">Repository owner</th>
                <th class="text-nowrap">Last commit</th>
            </tr>
        </thead>
        <tbody>
        {% for repository in repositories %} {{n}}
            <tr>
              <th>{{ loop.index }}</th>
              <td><a href="{{ repository.url }}">
                  {{ repository.name }}</a>
              </td>
              <td><a href="{{ repository.owner.url }}">
                  <img src="{{ repository.owner.avatar_url }}"
                       alt="avatar" height="24" width="24"/></a>
                  <a href="{{ repository.owner.url }}">
                      {{ repository.owner.login }}</a>
              </td>
```

---

TITLE: Executing Dependency Injector Example via CLI
DESCRIPTION: These commands illustrate how to run the provided example script (`example`) as a Python module from the command line. They pass environment arguments (`prod` or `test`) and an email address to the script, demonstrating different execution contexts or configurations handled by the dependency injection setup.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/use-cases/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
python -m example prod example@example.com
```

LANGUAGE: bash
CODE:

```
python -m example test example@example.com
```

---

TITLE: Starting the Application with Docker Compose
DESCRIPTION: Provides terminal commands and expected logs to start the application using `docker compose up`. The logs indicate startup, shutdown, and the dispatcher activity, confirming that the application skeleton operates correctly with the dispatcher starting and exiting gracefully due to no active monitoring tasks.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_12

LANGUAGE: Bash
CODE:

```
docker compose up
```

---

TITLE: Running Flask Development Server (Bash)
DESCRIPTION: This command starts the built-in Flask development server. It hosts the web application, making it accessible locally, typically at `http://127.0.0.1:5000/` by default.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_5

LANGUAGE: bash
CODE:

```
flask run
```

---

TITLE: Implementation of Adapters (adapters.py)
DESCRIPTION: This referenced Python module (`example/adapters.py`) contains concrete implementations of interfaces or abstract classes defined elsewhere (likely used by use cases). It provides different adapter sets, possibly for 'test' and 'prod' modes, handling external interactions like database access or sending emails. These adapters are intended to be injected via the DI container. The actual code is external.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/use-cases.rst#_snippet_4

---

TITLE: Setting GitHub Personal Access Token as Environment Variable
DESCRIPTION: Command to set a GitHub personal access token as an environment variable to increase the API rate limit from 60 to 5000 requests per hour.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/django/README.rst#_snippet_4

LANGUAGE: bash
CODE:

```
export GITHUB_TOKEN=<your token>
```

---

TITLE: Creating Flask View Function for GitHub Repository Search
DESCRIPTION: Defines the index view function to handle search requests, retrieve query parameters, and render the index template with search results. This view will be the main entry point for the web application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_14

LANGUAGE: python
CODE:

```
"""Views module."""

from flask import request, render_template


def index():
    query = request.args.get("query", "Dependency Injector")
    limit = request.args.get("limit", 10, int)

    repositories = []

    return render_template(
        "index.html",
        query=query,
        limit=limit,
        repositories=repositories,
    )
```

---

TITLE: Defining Application Services in Python
DESCRIPTION: Reference to the Python module `example/services.py`. This file defines the application's services (`UserService`, `AuthService`), which receive dependencies like database connections and other services via their constructors (dependency injection).
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-single-container.rst#_snippet_3

LANGUAGE: python
CODE:

```
# Source: examples/miniapps/application-single-container/example/services.py
# Contains service layer classes (e.g., UserService, AuthService).
# Demonstrates dependency injection in constructors.
```

---

TITLE: Implementation of Business Use Cases (usecases.py)
DESCRIPTION: This referenced Python file (`example/usecases.py`) encapsulates the core business logic of the application. It defines classes or functions representing specific operations (like user signup), which depend on abstract interfaces (like database or email service adapters) provided through dependency injection at runtime. The actual code is external.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/use-cases.rst#_snippet_5

---

TITLE: Integrating Bootstrap-Flask into Application Factory in Python
DESCRIPTION: Modifies the `create_app` function in `application.py` to integrate the `Bootstrap-Flask` extension. It imports `Bootstrap` from `flask_bootstrap`, initializes it, and then calls `bootstrap.init_app(app)` to register the extension with the Flask application, enabling Bootstrap features.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_11

LANGUAGE: Python
CODE:

```
"""Application module."""

from flask import Flask
from flask_bootstrap import Bootstrap

from .containers import Container
from . import views


def create_app() -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container
    app.add_url_rule("/", "index", views.index)

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
```

---

TITLE: Making a Test API Request using HTTPie in Bash
DESCRIPTION: This Bash command uses the `httpie` tool to send a GET request to the running aiohttp application's root endpoint ('/'). It includes query parameters for search query and limit.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_14

LANGUAGE: bash
CODE:

```
http http://0.0.0.0:8080/ query=="wow,it works" limit==5
```

---

TITLE: Running Tests with Docker Compose and Pytest (Bash)
DESCRIPTION: This Bash command executes the test suite for the monitoring daemon within the Docker environment using `docker compose run`. It runs the `pytest` command on the `monitoringdaemon/tests.py` file and includes the `--cov` flag to generate a test coverage report for the `monitoringdaemon` package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_25

LANGUAGE: bash
CODE:

```
docker compose run --rm monitor py.test monitoringdaemon/tests.py --cov=monitoringdaemon
```

---

TITLE: INI File Example with Environment Variable Interpolation
DESCRIPTION: Sample INI configuration implementing environment variable interpolation with placeholders like ${ENV_VAR}, ${ENV_VAR}/path, and ${ENV_VAR:default} formats to enable substitution from environment variables or fallback to defaults at runtime.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/configuration.rst#_snippet_1

LANGUAGE: ini
CODE:

```
[section]
option1 = ${ENV_VAR}
option2 = ${ENV_VAR}/path
option3 = ${ENV_VAR:default}
```

---

TITLE: Run Application with Docker Compose
DESCRIPTION: This command starts the application services defined in the `docker-compose.yml` file in the foreground, attaching to the container logs. It typically launches the web server and any dependent services like databases.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
docker compose up
```

---

TITLE: Configuring Application Settings using INI
DESCRIPTION: Reference to the INI file `config.ini`. This file provides configuration values for the application, such as database connection details and AWS settings, read by the dependency injection container.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-single-container.rst#_snippet_4

LANGUAGE: ini
CODE:

```
# Source: examples/miniapps/application-single-container/config.ini
# Contains application configuration in INI format.
# [database]
# host = ...
# [aws]
# access_key_id = ...
```

---

TITLE: Visualizing Provider Dependency Tree - Bash Syntax
DESCRIPTION: This diagram, formatted as a bash code block, visualizes the dependency graph among various providers within the dependency_injector framework. While presented in bash-marked syntax, it represents an abstract tree rather than an executable shell script. No external dependencies are required; the primary purpose is to illustrate that calling one provider can cascade into the instantiation of dependencies via other providers. Inputs and outputs are logical relationships, not code execution. The snippet is intended strictly for conceptual demonstration and does not perform any real operations.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/providers/index.rst#_snippet_0

LANGUAGE: bash
CODE:

```
provider1()
│
├──> provider2()
│
├──> provider3()
│    │
│    └──> provider4()
│
└──> provider5()
     │
     └──> provider6()
```

---

TITLE: Running the FastAPI Application using Bash
DESCRIPTION: Commands to start the FastAPI web application. It first sets the required `GIPHY_API_KEY` environment variable and then uses `uvicorn` to serve the application defined in `giphynavigator.application:app`, enabling auto-reload for development.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
export GIPHY_API_KEY=wBJ2wZG7SRqfrU9nPgPiWvORmloDyuL0
uvicorn giphynavigator.application:app --reload
```

---

TITLE: Running the Flask Development Server in Bash
DESCRIPTION: Sets environment variables `FLASK_APP` (specifying the application module `githubnavigator.application`) and `FLASK_ENV` (enabling development mode with debugging and auto-reloading), then starts the Flask development server using the `flask run` command.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_8

LANGUAGE: Bash
CODE:

```
export FLASK_APP=githubnavigator.application
export FLASK_ENV=development
flask run
```

---

TITLE: Starting Django Development Server
DESCRIPTION: Command to run the Django development server, which makes the GitHub navigator application accessible at http://127.0.0.1:8000/.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/django/README.rst#_snippet_3

LANGUAGE: bash
CODE:

```
python manage.py runserver
```

---

TITLE: Configuring Application with YAML
DESCRIPTION: Provides a YAML configuration file for the application that defines database connection parameters and AWS credentials. The configuration will be loaded and injected into the containers.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-multiple-containers.rst#_snippet_4

LANGUAGE: yaml
CODE:

```
../../examples/miniapps/application-multiple-containers/config.yml
```

---

TITLE: Running Unit Tests with Coverage Using py.test - Python
DESCRIPTION: Executes the test suite for the application using pytest, targeting the 'giphynavigator/tests.py' file and measuring code coverage for the 'giphynavigator' package. Dependencies: pytest and pytest-cov must be installed, and the virtual environment should be active. Output: detailed test results and code coverage statistics.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/aiohttp/README.rst#_snippet_4

LANGUAGE: bash
CODE:

```
py.test giphynavigator/tests.py --cov=giphynavigator
```

---

TITLE: Configuring Docker Compose for Daemon - YAML
DESCRIPTION: Defines a docker-compose.yml configuration to build and run the monitoring daemon in a container. It builds the image from the local Dockerfile and mounts the project directory to the /code path within the container for hot reload or development convenience. Docker Compose must be installed, and the Dockerfile and source files should be present.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_3

LANGUAGE: yaml
CODE:

```
services:

  monitor:
    build: ./
    image: monitoring-daemon
    volumes:
      - "./:/code"
```

---

TITLE: Running the Example Application via Command Line
DESCRIPTION: Shows how to execute the application script (`run.py`) using the Python interpreter. Command-line arguments specify the operational mode ('test' or 'prod') and an example email, demonstrating how to pass runtime configuration.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples-other/use-cases.rst#_snippet_3

LANGUAGE: bash
CODE:

```
python run.py test example@example.com
```

LANGUAGE: bash
CODE:

```
python run.py prod example@example.com
```

---

TITLE: Expected Pytest Test Run Output (Text)
DESCRIPTION: This snippet displays the expected console output when running the unit tests with coverage. It indicates test collection, test execution results ('.'), and a summary table of the code coverage report.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/flask-blueprints/README.rst#_snippet_9

LANGUAGE: text
CODE:

```
platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
plugins: cov-6.0.0, flask-1.3.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 2 items

githubnavigator/tests.py ..                                     [100%]

---------- coverage: platform darwin, python 3.10.0-final-0 ----------
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
githubnavigator/__init__.py                  0      0   100%
githubnavigator/application.py              13      0   100%
githubnavigator/blueprints/__init__.py       0      0   100%
githubnavigator/blueprints/example.py       12      0   100%
githubnavigator/containers.py                8      0   100%
githubnavigator/services.py                 14      0   100%
githubnavigator/tests.py                    34      0   100%
------------------------------------------------------------
TOTAL                                       81      0   100%
```

---

TITLE: Example Application Startup Log Output
DESCRIPTION: Shows the expected console output when running `docker compose up`. This includes SQLAlchemy engine logs (database connection tests, table creation) and Uvicorn server startup messages indicating the application is running and accessible.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi-sqlalchemy/README.rst#_snippet_2

LANGUAGE: text
CODE:

```
Starting fastapi-sqlalchemy_webapp_1 ... done
Attaching to fastapi-sqlalchemy_webapp_1
webapp_1  | 2022-02-04 22:07:19,804 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1
webapp_1  | 2022-02-04 22:07:19,804 INFO sqlalchemy.engine.base.Engine ()
webapp_1  | 2022-02-04 22:07:19,804 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1
webapp_1  | 2022-02-04 22:07:19,804 INFO sqlalchemy.engine.base.Engine ()
webapp_1  | 2022-02-04 22:07:19,805 INFO sqlalchemy.engine.base.Engine PRAGMA main.table_info("users")
webapp_1  | 2022-02-04 22:07:19,805 INFO sqlalchemy.engine.base.Engine ()
webapp_1  | 2022-02-04 22:07:19,808 INFO sqlalchemy.engine.base.Engine PRAGMA temp.table_info("users")
webapp_1  | 2022-02-04 22:07:19,808 INFO sqlalchemy.engine.base.Engine ()
webapp_1  | 2022-02-04 22:07:19,809 INFO sqlalchemy.engine.base.Engine
webapp_1  | CREATE TABLE users (
webapp_1  | 	id INTEGER NOT NULL,
webapp_1  | 	email VARCHAR,
webapp_1  | 	hashed_password VARCHAR,
webapp_1  | 	is_active BOOLEAN,
webapp_1  | 	PRIMARY KEY (id),
webapp_1  | 	UNIQUE (email),
webapp_1  | 	CHECK (is_active IN (0, 1))
webapp_1  | )
webapp_1  |
webapp_1  |
webapp_1  | 2022-02-04 22:07:19,810 INFO sqlalchemy.engine.base.Engine ()
webapp_1  | 2022-02-04 22:07:19,821 INFO sqlalchemy.engine.base.Engine COMMIT
webapp_1  | INFO:     Started server process [8]
webapp_1  | INFO:     Waiting for application startup.
webapp_1  | INFO:     Application startup complete.
webapp_1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

TITLE: Running Django Migrations
DESCRIPTION: Command to apply database migrations for the Django project, ensuring the database schema is properly set up before running the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/django/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
python manage.py migrate
```

---

TITLE: Expected Output from the Python Dependency Injector Example
DESCRIPTION: The expected console output showing debug logs from the application's services: UserService finding the user, AuthService authenticating the user, and PhotoService uploading the photo.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-single-container/README.rst#_snippet_3

LANGUAGE: bash
CODE:

```
[2020-10-06 15:32:33,195] [DEBUG] [example.services.UserService]: User user@example.com has been found in database
[2020-10-06 15:32:33,195] [DEBUG] [example.services.AuthService]: User user@example.com has been successfully authenticated
[2020-10-06 15:32:33,195] [DEBUG] [example.services.PhotoService]: Photo photo.jpg has been successfully uploaded by user user@example.com
```

---

TITLE: Running Unit Tests with Pytest via Docker Compose (Bash)
DESCRIPTION: Executes the unit tests located in 'monitoringdaemon/tests.py' using pytest within a temporary Docker container for the 'monitor' service. The '--rm' flag ensures the container is removed after the tests run, and '--cov' generates a test coverage report for the 'monitoringdaemon' package. Requires Docker and Docker Compose installed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/asyncio-daemon/README.rst#_snippet_2

LANGUAGE: bash
CODE:

```
docker compose run --rm monitor py.test monitoringdaemon/tests.py --cov=monitoringdaemon
```

---

TITLE: Running the Example Application (Bash)
DESCRIPTION: This command executes the main application module ('application') using the Python interpreter. It's the standard way to run a Python package or module directly from the command line, assuming 'application.py' or an '**main**.py' within an 'application' directory exists in the Python path.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/commands-and-handlers/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
python -m application
```

---

TITLE: Sample Coverage Report Output for Python Package
DESCRIPTION: This snippet displays the coverage report output generated after running pytest with coverage. It details the number of statements, missed statements, and overall coverage percentage for each module, helping identify untested code areas.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/aiohttp.rst#_snippet_22

LANGUAGE: bash
CODE:

```
   platform darwin -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
   plugins: asyncio-0.16.0, anyio-3.3.4, aiohttp-0.3.0, cov-3.0.0
   collected 3 items

   giphynavigator/tests.py ...                                     [100%]

   ---------- coverage: platform darwin, python 3.10.0-final-0 ----------
   Name                            Stmts   Miss  Cover
   ---------------------------------------------------
   giphynavigator/__init__.py          0      0   100%
   giphynavigator/application.py      13      2    85%
   giphynavigator/containers.py        7      0   100%
   giphynavigator/giphy.py            14      9    36%
   giphynavigator/handlers.py         10      0   100%
   giphynavigator/services.py          9      1    89%
   giphynavigator/tests.py            37      0   100%
   ---------------------------------------------------
   TOTAL                              90     12    87%
```

---

TITLE: Creating Virtual Environment using Bash
DESCRIPTION: Commands to create a new Python virtual environment named 'venv' using the `virtualenv` tool and activate it within the current bash session. This step isolates project dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
virtualenv venv
. venv/bin/activate
```

---

TITLE: Installing Python Dependencies with pip in Bash
DESCRIPTION: Installs the Python packages listed in the `requirements.txt` file using the `pip` package installer within the activated virtual environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_3

LANGUAGE: Bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Installing Python Dependencies - Bash
DESCRIPTION: Installs all project dependencies listed in the 'requirements.txt' file using pip. This command should be run within the activated virtual environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/decoupled-packages/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Specifying Dependency: pydantic (Python)
DESCRIPTION: Pins 'pydantic' to version 1.10.17. Pydantic is a data validation and settings management library using Python type annotations, often used with FastAPI.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_15

LANGUAGE: Python requirements
CODE:

```
pydantic==1.10.17
```

---

TITLE: Specifying Dependency: coverage (Python)
DESCRIPTION: Includes 'coverage', a tool for measuring code coverage of Python programs. It monitors your program, notes which parts of the code have been executed, and reports on the results.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_5

LANGUAGE: Python requirements
CODE:

```
coverage
```

---

TITLE: Specifying Dependency: pytest (Python)
DESCRIPTION: Adds 'pytest', a widely used testing framework for Python. It simplifies writing small tests and scales to support complex functional testing.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_2

LANGUAGE: Python requirements
CODE:

```
pytest
```

---

TITLE: Starting Daemon with Docker Compose (Bash)
DESCRIPTION: This Bash command initiates the monitoring daemon using Docker Compose. It assumes a `docker-compose.yml` file exists that defines the service named `monitor`. Running this command starts the container(s) specified in the Docker Compose file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_21

LANGUAGE: bash
CODE:

```
docker compose up
```

---

TITLE: Specifying Dependency: sphinx_autobuild (Python)
DESCRIPTION: Includes 'sphinx_autobuild', a tool that builds Sphinx documentation automatically on changes, often with a live-reloading web server.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_9

LANGUAGE: Python requirements
CODE:

```
sphinx_autobuild
```

---

TITLE: Specifying Dependency: mypy (Python)
DESCRIPTION: Includes 'mypy', an optional static type checker for Python. It helps find errors in code without running it by checking type hints.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_11

LANGUAGE: Python requirements
CODE:

```
mypy
```

---

TITLE: Specifying Dependency: typing_extensions (Python)
DESCRIPTION: Includes 'typing_extensions', a package that backports new features from Python's 'typing' module to older Python versions, enabling the use of modern type hints.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_20

LANGUAGE: Python requirements
CODE:

```
typing_extensions
```

---

TITLE: Specifying Dependency: setuptools (Python)
DESCRIPTION: Includes 'setuptools', a library fundamental for packaging Python projects. It provides tools for building, distributing, and installing Python packages.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_1

LANGUAGE: Python requirements
CODE:

```
setuptools
```

---

TITLE: Installing Updated Python Dependencies in Bash
DESCRIPTION: Re-runs the `pip install -r requirements.txt` command to install the newly added `bootstrap-flask` package and any updated versions of existing dependencies specified in the `requirements.txt` file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_10

LANGUAGE: Bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Sample JSON Response of Giphy GIF Search API
DESCRIPTION: This JSON snippet presents the expected output from calling the Sanic-based GIF search REST API. It shows a search query for "Dependency Injector" limited to 10 GIFs, each represented by an object containing a URL to the corresponding GIF on Giphy. This demonstrates the structure of API data returned by the application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_4

LANGUAGE: json
CODE:

```
{
    "query": "Dependency Injector",
    "limit": 10,
    "gifs": [
        {
            "url": "https://giphy.com/gifs/boxes-dependent-swbf2-6Eo7KzABxgJMY"
        },
        {
            "url": "https://giphy.com/gifs/depends-J56qCcOhk6hKE"
        },
        {
            "url": "https://giphy.com/gifs/web-series-ccstudios-bro-dependent-1lhU8KAVwmVVu"
        },
        {
            "url": "https://giphy.com/gifs/TheBoysTV-friends-friend-weneedeachother-XxR9qcIwcf5Jq404Sx"
        },
        {
            "url": "https://giphy.com/gifs/netflix-a-series-of-unfortunate-events-asoue-9rgeQXbwoK53pcxn7f"
        },
        {
            "url": "https://giphy.com/gifs/black-and-white-sad-skins-Hs4YzLs2zJuLu"
        },
        {
            "url": "https://giphy.com/gifs/always-there-for-you-i-am-here-PlayjhCco9jHBYrd9w"
        },
        {
            "url": "https://giphy.com/gifs/stream-famous-dollar-YT2dvOByEwXCdoYiA1"
        },
        {
            "url": "https://giphy.com/gifs/i-love-you-there-for-am-1BhGzgpZXYWwWMAGB1"
        },
        {
            "url": "https://giphy.com/gifs/life-like-twerk-9hlnWxjHqmH28"
        }
    ]
}
```

---

TITLE: Verifying Dependency Installation in Bash
DESCRIPTION: Executes short Python commands via the shell to import `dependency_injector` and `flask` and print their versions, confirming successful installation and availability within the environment.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_4

LANGUAGE: Bash
CODE:

```
python -c "import dependency_injector; print(dependency_injector.__version__)"
python -c "import flask; print(flask.__version__)"
```

---

TITLE: Displaying Application File Structure using Bash
DESCRIPTION: This Bash snippet shows the directory and file structure of the example Python application. It outlines the layout of the `example` package, configuration files (`config.ini`, `logging.ini`), and the requirements file.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/examples/application-single-container.rst#_snippet_0

LANGUAGE: bash
CODE:

```
./
├── example/
│   ├── __init__.py
│   ├── __main__.py
│   ├── containers.py
│   └── services.py
├── config.ini
├── logging.ini
└── requirements.txt
```

---

TITLE: Showing Project Directory Structure - Bash
DESCRIPTION: This Bash snippet illustrates the expected directory structure of the project, showing the location of source files, templates, configuration, requirements, and specifically highlights the new `tests.py` file within the `githubnavigator` package.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_26

LANGUAGE: bash
CODE:

```
./
├── githubnavigator/
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   ├── __init__.py
│   ├── application.py
│   ├── containers.py
│   ├── services.py
│   ├── tests.py
│   └── views.py
├── venv/
├── config.yml
└── requirements.txt
```

---

TITLE: Updating Dependencies with Bootstrap-Flask in requirements.txt
DESCRIPTION: Updates the `requirements.txt` file to include the `bootstrap-flask` package. This is necessary to add Bootstrap 4 styling and components to the Flask application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_9

LANGUAGE: Bash
CODE:

```
dependency-injector
flask
bootstrap-flask
```

---

TITLE: Specifying Dependency: httpx (Python)
DESCRIPTION: Includes 'httpx', a fully featured HTTP client for Python that provides sync and async APIs, and support for HTTP/2.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_13

LANGUAGE: Python requirements
CODE:

```
httpx
```

---

TITLE: Listing Project Files (Bash)
DESCRIPTION: This Bash snippet displays the directory structure of the project, specifically highlighting the location of the `tests.py` file within the `monitoringdaemon` package. It provides context for where the test code snippet should be placed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_23

LANGUAGE: bash
CODE:

```
./
├── monitoringdaemon/
│   ├── __init__.py
│   ├── __main__.py
│   ├── containers.py
│   ├── dispatcher.py
│   ├── http.py
│   ├── monitors.py
│   └── tests.py
├── config.yml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

TITLE: Installing Python Dependencies with Bash
DESCRIPTION: This snippet provides the bash command to install all required Python dependencies listed in the requirements.txt file using pip. It assumes an active virtual environment for isolated package installation relevant to the Sanic + Dependency Injector Giphy API project.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/sanic/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
pip install -r requirements.txt
```

---

TITLE: Building Docker Image with Docker Compose (Bash)
DESCRIPTION: Builds the Docker image required for the example application using the configuration specified in the docker-compose.yml file. Requires Docker and Docker Compose installed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/asyncio-daemon/README.rst#_snippet_0

LANGUAGE: bash
CODE:

```
docker compose build
```

---

TITLE: Specifying Python Project Requirements - Bash
DESCRIPTION: Appends required dependencies for the monitoring daemon application to the requirements.txt file using standard Python package names. These packages provide dependency injection, async HTTP client functionality, YAML config parsing, and testing utilities. No arguments are required, and output is written to a file; versions are not pinned.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/asyncio-daemon.rst#_snippet_1

LANGUAGE: bash
CODE:

```
dependency-injector
aiohttp
pyyaml
pytest
pytest-asyncio
pytest-cov
```

---

TITLE: Setting Up Python Virtual Environment in Bash
DESCRIPTION: Creates a Python 3 virtual environment named `venv` within the project directory and activates it using the source command. This isolates project dependencies.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_1

LANGUAGE: Bash
CODE:

```
python3 -m venv venv
. venv/bin/activate
```

---

TITLE: Running Docker Environment with Docker Compose (Bash)
DESCRIPTION: Starts and runs the application environment defined in the docker-compose.yml file. This command launches the necessary containers, including the asyncio daemon. Requires Docker and Docker Compose installed.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/asyncio-daemon/README.rst#_snippet_1

LANGUAGE: bash
CODE:

```
docker compose up
```

---

TITLE: Specifying Dependency: cython (Python)
DESCRIPTION: Pins the 'cython' package to version 3.0.11. Cython is a programming language that makes writing C extensions for Python as easy as writing Python itself, often used for performance-critical sections.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_0

LANGUAGE: Python requirements
CODE:

```
cython==3.0.11
```

---

TITLE: Specifying Dependency: mypy_boto3_s3 (Python)
DESCRIPTION: Adds 'mypy_boto3_s3', a type stub package for the AWS S3 service part of boto3. This provides type hints for static analysis tools like mypy when using S3.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_19

LANGUAGE: Python requirements
CODE:

```
mypy_boto3_s3
```

---

TITLE: Example API JSON Response
DESCRIPTION: Sample JSON data returned by the Giphy navigator API endpoint. The response includes the original search query ('Dependency Injector'), the number of results requested (limit: 10), and an array of 'gifs', each containing a URL pointing to a GIF on Giphy.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_4

LANGUAGE: json
CODE:

```
{
    "query": "Dependency Injector",
    "limit": 10,
    "gifs": [
        {
            "url": "https://giphy.com/gifs/boxes-dependent-swbf2-6Eo7KzABxgJMY"
        },
        {
            "url": "https://giphy.com/gifs/depends-J56qCcOhk6hKE"
        },
        {
            "url": "https://giphy.com/gifs/web-series-ccstudios-bro-dependent-1lhU8KAVwmVVu"
        },
        {
            "url": "https://giphy.com/gifs/TheBoysTV-friends-friend-weneedeachother-XxR9qcIwcf5Jq404Sx"
        },
        {
            "url": "https://giphy.com/gifs/netflix-a-series-of-unfortunate-events-asoue-9rgeQXbwoK53pcxn7f"
        },
        {
            "url": "https://giphy.com/gifs/black-and-white-sad-skins-Hs4YzLs2zJuLu"
        },
        {
            "url": "https://giphy.com/gifs/always-there-for-you-i-am-here-PlayjhCco9jHBYrd9w"
        },
        {
            "url": "https://giphy.com/gifs/stream-famous-dollar-YT2dvOByEwXCdoYiA1"
        },
        {
            "url": "https://giphy.com/gifs/i-love-you-there-for-am-1BhGzgpZXYWwWMAGB1"
        },
        {
            "url": "https://giphy.com/gifs/life-like-twerk-9hlnWxjHqmH28"
        }
    ]
}
```

---

TITLE: Example Uvicorn Server Output
DESCRIPTION: Illustrative console output displayed when the FastAPI application is successfully started using Uvicorn. It confirms the server is running on the specified address and port (http://127.0.0.1:8000) and indicates that the application startup is complete.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/fastapi/README.rst#_snippet_3

LANGUAGE: text
CODE:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [4795] using watchgod
INFO:     Started server process [4797]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

TITLE: Expected Output of the Example Application
DESCRIPTION: The expected log output from running the example application, showing debug messages from the UserService, AuthService, and PhotoService components.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/application-multiple-containers/README.rst#_snippet_3

LANGUAGE: bash
CODE:

```
[2020-10-06 15:36:55,961] [DEBUG] [example.services.UserService]: User user@example.com has been found in database
[2020-10-06 15:36:55,961] [DEBUG] [example.services.AuthService]: User user@example.com has been successfully authenticated
[2020-10-06 15:36:55,961] [DEBUG] [example.services.PhotoService]: Photo photo.jpg has been successfully uploaded by user user@example.com
```

---

TITLE: Example Script Output - Bash
DESCRIPTION: Shows the expected output from running the example script. This illustrates the results of the data retrieval and aggregation logic implemented in the decoupled components.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/examples/miniapps/decoupled-packages/README.rst#_snippet_3

LANGUAGE: bash
CODE:

```
Retrieve user id=1, photos count=5
Retrieve user id=2, photos count=10
Aggregate analytics from user and photo bundles
```

---

TITLE: Defining a Pull Sign Unicode Character in reStructuredText Documentation
DESCRIPTION: This snippet defines a custom reStructuredText substitution named 'pull' that represents a leftwards arrow emoji (⬅️) using Unicode code points U+2B05 (leftwards black arrow) and U+FE0F (variation selector for emoji presentation).
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/README.rst#_snippet_1

LANGUAGE: reStructuredText
CODE:

```
.. |pull| unicode:: U+2B05 U+FE0F .. pull sign
```

---

TITLE: Creating Project Directory in Bash
DESCRIPTION: Creates the main project directory `ghnav-flask-tutorial` and changes the current working directory into it, preparing the workspace for the Flask application.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/docs/tutorials/flask.rst#_snippet_0

LANGUAGE: Bash
CODE:

```
mkdir ghnav-flask-tutorial
cd ghnav-flask-tutorial
```

---

TITLE: Including External Requirements File (Python)
DESCRIPTION: Instructs the package installer (like pip) to install all packages listed in the 'requirements-ext.txt' file. This is used to separate different sets of dependencies, such as core dependencies from development or optional ones.
SOURCE: https://github.com/ets-labs/python-dependency-injector/blob/master/requirements-dev.txt#_snippet_21

LANGUAGE: Python requirements
CODE:

```
-r requirements-ext.txt
```
