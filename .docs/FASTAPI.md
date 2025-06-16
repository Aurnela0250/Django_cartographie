TITLE: Defining Multiple Pydantic Models for User Data in Python
DESCRIPTION: This snippet defines distinct Pydantic models (`UserIn`, `UserInDB`, `UserOut`) for handling user data at different stages: input (with plaintext password), database storage (with hashed password), and output (without password). It also includes a `create_user` function demonstrating the data flow and transformation between these models, using `**user_in.dict()` for unpacking.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Optional
from pydantic import BaseModel

# Simulate a password hasher and user saver
def fake_password_hasher(password: str):
    return "hashed" + password

def fake_save_user(user_in_db: "UserInDB"):
    # Simulate saving to a database
    print(f"Saving user: {user_in_db.username} to DB")
    return user_in_db

# Input model: User provides password
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None

# Database model: Stores hashed password
class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: Optional[str] = None

# Output model: Does not expose password
class UserOut(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# Example usage
def create_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    saved_user = fake_save_user(user_in_db)
    user_out = UserOut(**saved_user.dict())
    return user_out

# Test the function
user_input = UserIn(username="john", password="secret", email="john.doe@example.com")
created_user = create_user(user_input)
print(f"Created user (output): {created_user.username}, {created_user.email}")
```

---

TITLE: Including Routers in Main App (Python)
DESCRIPTION: Uses app.include_router() to integrate path operations from APIRouter instances (users.router, items.router) defined in imported modules into the main FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_18

LANGUAGE: Python
CODE:

```
app.include_router(users.router)
app.include_router(items.router)
```

---

TITLE: Installing FastAPI with Standard Dependencies
DESCRIPTION: This command installs the FastAPI framework along with its recommended standard dependencies. These dependencies include essential libraries like Uvicorn for serving the application and Pydantic for data validation and serialization, which are crucial for developing FastAPI applications.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_0

LANGUAGE: console
CODE:

```
pip install "fastapi[standard]"
```

---

TITLE: Basic FastAPI Application Example (main.py)
DESCRIPTION: A minimal FastAPI application demonstrating two GET endpoints: a root endpoint returning 'Hello: World' and an item endpoint that accepts an integer `item_id` and an optional string query parameter `q`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/deployment/docker.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Declaring Dependencies in FastAPI Path Operations
DESCRIPTION: These FastAPI path operation functions (`/items/` and `/users/`) demonstrate how to declare a dependency using `Depends`. By assigning `Depends(common_parameters)` to a parameter, FastAPI automatically calls the `common_parameters` dependency function and injects its return value into the path operation, promoting code reuse.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/index.md#_snippet_2

LANGUAGE: Python
CODE:

```
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

---

TITLE: Running FastAPI Application with Uvicorn
DESCRIPTION: This command starts the FastAPI application using Uvicorn, a fast ASGI server. The `--reload` flag enables automatic server reloading upon code changes, which is highly beneficial during development. The application typically becomes accessible at `http://127.0.0.1:8000`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/index.md#_snippet_0

LANGUAGE: Shell
CODE:

```
uvicorn main:app --reload
```

---

TITLE: Importing FastAPI Class (Python)
DESCRIPTION: This snippet demonstrates how to import the `FastAPI` class from the `fastapi` library, which is the foundational step for creating a new FastAPI application. It is a prerequisite for defining routes, middleware, and other application components.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/fastapi.md#_snippet_0

LANGUAGE: python
CODE:

```
from fastapi import FastAPI
```

---

TITLE: Importing Depends for Dependency Injection - Python
DESCRIPTION: This snippet shows how to import the `Depends` function directly from the `fastapi` library. `Depends()` is a fundamental FastAPI utility used to declare dependencies, enabling dependency injection and the creation of reusable components in your application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/dependencies.md#_snippet_0

LANGUAGE: python
CODE:

```
from fastapi import Depends
```

---

TITLE: Instantiating FastAPI Application
DESCRIPTION: This line creates an instance of the `FastAPI` class, typically named `app`. This `app` object is the main entry point for defining all your API's routes and operations, and it's the object referenced by ASGI servers like Uvicorn to run your application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_4

LANGUAGE: Python
CODE:

```
app = FastAPI()
```

---

TITLE: Defining a GET Path Operation in FastAPI
DESCRIPTION: This snippet illustrates how to define a GET path operation in FastAPI. It uses the @app.get() decorator to associate the read_url function with the /some/url endpoint, returning a JSON response. This demonstrates FastAPI's server-side API building, mirroring the simplicity of Requests for client-side operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/alternatives.md#_snippet_1

LANGUAGE: Python
CODE:

```
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

---

TITLE: Defining Python Types and Pydantic Models
DESCRIPTION: This snippet demonstrates how to use standard Python type hints for function parameters and define a data model using Pydantic's BaseModel. Pydantic models provide data validation and serialization, leveraging Python's type annotations. It shows a simple function with a typed argument and a `User` model with `int`, `str`, and `date` fields.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/features.md#_snippet_0

LANGUAGE: Python
CODE:

```
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

---

TITLE: Creating a Basic FastAPI Application in Python
DESCRIPTION: This snippet initializes a FastAPI application and defines a root endpoint (`/`) that returns a JSON response. It demonstrates the minimal code required to create a functional web API with FastAPI, serving a simple 'Hello World' message.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Running FastAPI Application
DESCRIPTION: This console command uses Uvicorn to serve the FastAPI application, enabling automatic reloading on code changes. It targets the app instance within the main.py file, making the API accessible locally.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/first-steps.md#_snippet_1

LANGUAGE: console
CODE:

```
uvicorn main:app --reload
```

---

TITLE: Running FastAPI Application with Uvicorn (Console)
DESCRIPTION: This command starts the FastAPI application using Uvicorn. It specifies `main:app` where `main` refers to the `main.py` file and `app` is the FastAPI instance within it. The `--reload` flag enables automatic server restart on code changes, which is useful during development.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_4

LANGUAGE: Console
CODE:

```
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

TITLE: Create Virtual Environment using venv
DESCRIPTION: This snippet demonstrates how to create a virtual environment using Python's built-in `venv` module. The command creates a new isolated environment in a `.venv` directory within your project, ensuring project-specific package isolation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/ja/docs/virtual-environments.md#_snippet_1

LANGUAGE: console
CODE:

```
$ python -m venv .venv
```

---

TITLE: Full FastAPI Lifespan Context Manager Definition
DESCRIPTION: This snippet defines the `lifespan` asynchronous context manager using `@asynccontextmanager`. It demonstrates how to establish a database connection during application startup (before `yield`) and disconnect it during application shutdown (after `yield`), ensuring resources are properly managed throughout the application's lifecycle.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/events.md#_snippet_1

LANGUAGE: Python
CODE:

```
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run before the application starts
    await db.connect()
    print("Application startup complete.")
    yield
    # Code to run after the application shuts down
    await db.disconnect()
```

---

TITLE: Defining a Pydantic Data Model for Request Body - Python
DESCRIPTION: This code defines a Pydantic model named `Item` by inheriting from `BaseModel`. It specifies the expected data structure for a request body, including required fields (`name`, `price`) and optional fields (`description`, `tax`) with default `None` values, enabling automatic data validation and serialization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_1

LANGUAGE: Python
CODE:

```
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

---

TITLE: Defining a GET Endpoint in FastAPI
DESCRIPTION: This FastAPI snippet illustrates how to define a server-side GET endpoint. The `@app.get("/some/url")` decorator maps the `read_url` function to handle GET requests for the `/some/url` path, returning a JSON object as the response. This showcases FastAPI's declarative routing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/alternatives.md#_snippet_1

LANGUAGE: Python
CODE:

```
@app.get("/some/url")
def read_url():
    return {"message": "Hello World"}
```

---

TITLE: Defining X-Token Dependency (Python 3.9+ Annotated)
DESCRIPTION: Defines a simple dependency function `get_token` in `app/dependencies.py` that reads the `X-Token` header using `Annotated`. It raises an `HTTPException` if the token is not 'fake-super-secret-token'.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/bigger-applications.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import Header, HTTPException


async def get_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    return token
```

---

TITLE: Basic FastAPI Application Testing with TestClient and Pytest
DESCRIPTION: This snippet demonstrates how to set up basic tests for a FastAPI application using `TestClient` and `pytest`. It shows importing `TestClient`, initializing it with the FastAPI app instance, and writing a test function to make a GET request and assert the response's status code and JSON content.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/testing.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

---

TITLE: Defining a Pydantic Data Model in Python
DESCRIPTION: This code defines a Pydantic `Item` model inheriting from `BaseModel`. It specifies data types for `name`, `price`, and optional `description` and `tax` fields, which FastAPI uses for automatic data validation and serialization of request bodies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_1

LANGUAGE: Python
CODE:

```
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

---

TITLE: Importing Pydantic BaseModel in Python
DESCRIPTION: This snippet demonstrates how to import the `BaseModel` class from the Pydantic library. `BaseModel` is essential for defining data structures that FastAPI uses to validate and serialize request bodies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_0

LANGUAGE: Python
CODE:

```
from pydantic import BaseModel
```

---

TITLE: Database Dependency Setup with Yield (Python)
DESCRIPTION: This snippet demonstrates the initial part of a database dependency using `yield`. The code before and including `yield` is executed before the path operation, setting up the database session. The yielded value (`db`) is then injected into the dependent function.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_0

LANGUAGE: Python
CODE:

```
def get_db():
    db = DBSession()
    try:
        yield db
```

---

TITLE: Declaring Complex Model Body Parameters in FastAPI (Python)
DESCRIPTION: This snippet shows how to declare a complex `Item` model as a parameter in FastAPI. Using a Pydantic model (implied by `Item`), FastAPI automatically handles JSON body parsing, validation, and serialization, providing comprehensive editor support.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_9

LANGUAGE: Python
CODE:

```
item: Item
```

---

TITLE: Overriding FastAPI Dependencies for Testing - Python
DESCRIPTION: This snippet illustrates how to override a FastAPI dependency (`get_settings`) for testing purposes using `app.dependency_overrides`. A mock `get_settings_override` function is defined to return a `Settings` object with a specific `admin_email`, allowing tests to run with controlled configurations without affecting the actual application settings.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_13

LANGUAGE: Python
CODE:

```
from fastapi.testclient import TestClient
from main import app, get_settings
from config import Settings

def get_settings_override():
    return Settings(admin_email="testing@example.com")

client = TestClient(app)

app.dependency_overrides[get_settings] = get_settings_override

def test_info_override():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "testing@example.com"
    }
```

---

TITLE: Validating Hashed Passwords for User Authentication in FastAPI
DESCRIPTION: This snippet demonstrates how to validate a user's provided password against a stored hashed password. It uses a `UserInDB` Pydantic model to handle user data and raises an `HTTPException` with a 401 status code if the passwords do not match, preventing unauthorized access.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/simple-oauth2.md#_snippet_2

LANGUAGE: Python
CODE:

```
# ... (inside your login function, after user lookup)
# In a real application, use a proper password hashing library like passlib
if form_data.password != user.hashed_password:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
```

---

TITLE: Basic FastAPI Application (main.py)
DESCRIPTION: This Python code defines a simple FastAPI application with two endpoints: a root endpoint that returns 'Hello: World' and an item endpoint that accepts an `item_id` and an optional query parameter `q`. It demonstrates basic routing and type hinting in FastAPI.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Configuring CORS Middleware in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to add and configure `CORSMiddleware` to a FastAPI application. It defines a list of allowed origins, enables credentials, and permits all HTTP methods and headers for cross-origin requests, ensuring the API can be accessed from specified front-end applications. This setup is crucial for web applications hosted on different domains or ports than the API.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/cors.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

---

TITLE: Declaring a Pydantic Model as a Request Body Parameter
DESCRIPTION: This snippet shows how to declare a Pydantic `Item` model as a parameter in a FastAPI path operation. FastAPI automatically recognizes this as a request body, validates the incoming data against the model, and provides it as a Python object.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

---

TITLE: Adding Custom ASGI Middleware with FastAPI - Python
DESCRIPTION: Demonstrates the recommended way to add any ASGI middleware to a FastAPI application using `app.add_middleware()`. This method ensures proper handling of server errors and custom exception handlers. It takes the middleware class as the first argument and any additional arguments for the middleware.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/middleware.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

---

TITLE: Defining Python Types and Pydantic Models in FastAPI
DESCRIPTION: This snippet demonstrates the use of standard Python type declarations for function parameters and the definition of a Pydantic BaseModel for data validation and serialization. It highlights how FastAPI leverages these types for automatic data handling and enhanced editor support.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/features.md#_snippet_0

LANGUAGE: Python
CODE:

```
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

---

TITLE: Declaring Async Path Operation Function (FastAPI, Python)
DESCRIPTION: This example shows how to define a FastAPI path operation function using `async def` when it needs to interact with an asynchronous third-party library via `await`. Using `async def` allows FastAPI to optimize performance by releasing the event loop while waiting for I/O-bound operations to complete, improving concurrency.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_1

LANGUAGE: Python
CODE:

```
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

---

TITLE: Declaring Request Body Parameter in FastAPI Path Operation - Python
DESCRIPTION: This snippet shows how to declare a request body parameter in a FastAPI path operation function. By type-hinting the parameter `item` with the `Item` Pydantic model, FastAPI automatically handles JSON parsing, validation, and provides the structured data to the function.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_4

LANGUAGE: Python
CODE:

```
@app.post("/items/")
async def create_item(item: Item):
```

---

TITLE: Defining Separate Input and Output User Models
DESCRIPTION: This snippet defines two Pydantic models: `UserIn` for input, which includes a `password` field, and `UserOut` for output, which explicitly excludes the `password` field. This separation is a best practice for security, ensuring that sensitive data like passwords are not inadvertently exposed in API responses.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

---

TITLE: Returning Input User Object in FastAPI Endpoint
DESCRIPTION: This line within a FastAPI path operation function demonstrates returning the `user` object, which was received as input and potentially contains sensitive data like a password. Despite returning the full input object, FastAPI's `response_model` (set to `UserOut` in the decorator) will automatically filter the output to only include fields defined in `UserOut`, ensuring data security.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_4

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

---

TITLE: Extracting Set Values with Pydantic's exclude_unset (Python)
DESCRIPTION: This line of code demonstrates how to use Pydantic's `model_dump(exclude_unset=True)` (or `.dict()` in Pydantic v1) to create a dictionary containing only the fields that were explicitly set in the incoming request model. This is crucial for partial updates, as it prevents default values from overwriting existing data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-updates.md#_snippet_2

LANGUAGE: Python
CODE:

```
update_data = item.model_dump(exclude_unset=True)
```

---

TITLE: Importing CORSMiddleware in FastAPI
DESCRIPTION: This snippet demonstrates how to import the CORSMiddleware class, which is used to handle Cross-Origin Resource Sharing (CORS) policies in a FastAPI application. It allows you to configure which origins, methods, and headers are permitted for cross-origin requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/middleware.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi.middleware.cors import CORSMiddleware
```

---

TITLE: Awaiting an Asynchronous Function Call in Python
DESCRIPTION: This snippet demonstrates the use of the `await` keyword in Python. When `await` is used before an asynchronous function call (like `get_burgers`), it tells the Python event loop to pause the current function's execution until the awaited operation completes, allowing other tasks to run concurrently in the meantime.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_3

LANGUAGE: Python
CODE:

```
burgers = await get_burgers(2)
```

---

TITLE: Running FastAPI with Gunicorn and Uvicorn Workers
DESCRIPTION: This command starts the Gunicorn server, which acts as a master process, and spawns multiple Uvicorn worker processes to handle incoming requests. It specifies the application entry point (`main:app`), the number of workers (`--workers 4`), the worker class (`--worker-class uvicorn.workers.UvicornWorker`), and the binding address and port (`--bind 0.0.0.0:80`).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/server-workers.md#_snippet_1

LANGUAGE: Shell
CODE:

```
$ gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

---

TITLE: Running Uvicorn in Docker for FastAPI
DESCRIPTION: This command defines the entry point for a Docker container, running the Uvicorn ASGI server. It specifies that the FastAPI application is located at 'app.main:app', listens on all network interfaces ('0.0.0.0'), and uses port '80'. This is a standard way to serve FastAPI applications within a Docker container.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_18

LANGUAGE: Dockerfile
CODE:

```
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

TITLE: Implementing Active User Dependencies for Authentication in FastAPI
DESCRIPTION: This snippet defines two FastAPI dependencies: `get_current_user` for basic authentication and `get_current_active_user` which builds upon it to ensure the authenticated user is also active. Both raise `HTTPException` for unauthenticated or inactive users, providing robust access control for protected routes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/simple-oauth2.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

# Placeholder for a function that retrieves user from a database
def get_user(username: str):
    # In a real app, this would query your database
    fake_users_db = {
        "johndoe": {"username": "johndoe", "full_name": "John Doe", "email": "john@example.com", "hashed_password": "fakehashedsecret", "disabled": False},
        "janedoe": {"username": "janedoe", "full_name": "Jane Doe", "email": "jane@example.com", "hashed_password": "fakehashedsecret", "disabled": True}
    }
    if username in fake_users_db:
        return UserInDB(**fake_users_db[username])
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

---

TITLE: Creating a Basic FastAPI Application
DESCRIPTION: This Python code defines a simple FastAPI application with two HTTP GET endpoints. The root endpoint ('/') returns a basic 'Hello: World' JSON response, while the '/items/{item_id}' endpoint demonstrates how to define path parameters (item_id) and optional query parameters (q), returning them in the response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Creating a Basic FastAPI Application with Async Endpoints
DESCRIPTION: This Python code illustrates a FastAPI application where endpoint functions are defined using `async def`. This approach is beneficial for I/O-bound operations, allowing the server to handle multiple requests concurrently without blocking, thereby improving performance and responsiveness. It includes a root endpoint and an item endpoint, both asynchronous.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Database Dependency Teardown with Yield (Python)
DESCRIPTION: This snippet shows the cleanup part of a database dependency. The code after the `yield` statement is executed after the response has been created but before it is sent, ensuring resources like database sessions are properly closed.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_2

LANGUAGE: Python
CODE:

```
    finally:
        db.close()
```

---

TITLE: Reading a Single Hero by ID in FastAPI
DESCRIPTION: This FastAPI endpoint retrieves a single `Hero` object from the database using its `hero_id`. It queries the session for the hero and raises an `HTTPException` with a 404 status if the hero is not found, ensuring proper error handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_8

LANGUAGE: Python
CODE:

```
@app.get("/heroes/{hero_id}", response_model=Hero)
def read_hero(*, session: SessionDep, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

---

TITLE: Declaring Class Dependency in Path Operation (Annotated)
DESCRIPTION: This snippet shows the preferred way to declare a class-based dependency, `CommonQueryParams`, within a FastAPI path operation function using `Annotated` and `Depends`. The type annotation `CommonQueryParams` provides strong type hints for editor support, while `Depends(CommonQueryParams)` instructs FastAPI on how to resolve the dependency.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_3

LANGUAGE: Python
CODE:

```
commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
```

---

TITLE: Returning JSON Content from FastAPI Path Operation
DESCRIPTION: This snippet shows how to return a Python dictionary from a FastAPI path operation function. FastAPI automatically converts dictionaries, lists, and other supported types into JSON responses, simplifying API development.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_11

LANGUAGE: Python
CODE:

```
return {"message": "Hello World"}
```

---

TITLE: Running FastAPI Development Server
DESCRIPTION: This command initiates the FastAPI development server, automatically reloading the application upon code changes in `main.py`. It provides a local URL for accessing the API and displays server logs, indicating successful startup and watch directories.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/index.md#_snippet_0

LANGUAGE: console
CODE:

```
$ fastapi dev main.py

  FastAPI   Starting development server 🚀

             Searching for package file structure from directories
             with __init__.py files
             Importing from /home/user/code/awesomeapp

   module   🐍 main.py

     code   Importing the FastAPI app object from the module with
             the following code:

             from main import app

      app   Using import string: main:app

   server   Server started at http://127.0.0.1:8000
   server   Documentation at http://127.0.0.1:8000/docs

      tip   Running in development mode, for production use:
             fastapi run

             Logs:

     INFO   Will watch for changes in these directories:
             ['/home/user/code/awesomeapp']
     INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C
             to quit)
     INFO   Started reloader process [383138] using WatchFiles
     INFO   Started server process [383153]
     INFO   Waiting for application startup.
     INFO   Application startup complete.
```

---

TITLE: Defining Pydantic Models (Python 3.8+)
DESCRIPTION: Shows how to define a Pydantic model using type hints for data validation and structure, suitable for Python 3.8+ environments. Pydantic leverages these definitions for automatic data handling, including `List` from the `typing` module for collections.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_29

LANGUAGE: Python
CODE:

```
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    customer_name: str
    total_amount: float
    items: List[str] = []
    delivery_date: Optional[datetime] = None
```

---

TITLE: Defining a SQLModel Hero Table
DESCRIPTION: This Python class defines the 'Hero' database model using SQLModel, mapping it to a SQL table. It includes fields for 'id' (primary key), 'name' (indexed string), 'secret_name' (string), and 'age' (optional indexed integer), combining Pydantic's data validation with SQLAlchemy's ORM capabilities.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing import Optional
from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
```

---

TITLE: Initializing Main FastAPI Application
DESCRIPTION: This snippet initializes the main FastAPI application (app) and defines a basic path operation at /main. This application serves as the primary entry point for the overall service. It requires the FastAPI class from the fastapi library.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/main")
async def read_main():
    return {"message": "Hello from main app"}
```

---

TITLE: Uvicorn Command Referencing FastAPI Instance
DESCRIPTION: This command demonstrates how Uvicorn references the `app` instance from `main.py`. The `app` variable is the instantiated `FastAPI` object, serving as the application entry point for the ASGI server to run your API.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_5

LANGUAGE: console
CODE:

```
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

TITLE: Generating a Secure Random Secret Key (Console)
DESCRIPTION: This console command uses `openssl` to generate a cryptographically secure random hexadecimal string of 32 bytes (64 characters). This string is intended to be used as a `SECRET_KEY` for signing JWT tokens, ensuring their integrity and preventing tampering.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/oauth2-jwt.md#_snippet_3

LANGUAGE: console
CODE:

```
$ openssl rand -hex 32
```

---

TITLE: Validating HTTP Basic Auth Credentials Securely with `secrets`
DESCRIPTION: This snippet demonstrates how to securely validate HTTP Basic Auth credentials in FastAPI using Python's `secrets` module. It employs `secrets.compare_digest()` to prevent timing attacks by ensuring a constant comparison time, converting credentials to bytes before comparison, and raising an `HTTPException` for incorrect credentials.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/security/http-basic-auth.md#_snippet_1

LANGUAGE: Python
CODE:

```
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic_auth = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(basic_auth)):
    correct_username = secrets.compare_digest(credentials.username.encode("utf8"), b"stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password.encode("utf8"), b"swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "password": credentials.password}
```

---

TITLE: Declaring Dependencies in FastAPI Path Operations (Python)
DESCRIPTION: These snippets illustrate how to integrate a dependency into FastAPI path operation functions using `Annotated` and `Depends`. The `common_parameters` function is automatically called, and its return value is injected into the `commons` parameter, streamlining the use of shared logic across different endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/index.md#_snippet_2

LANGUAGE: Python
CODE:

```
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

---

TITLE: Defining Data Models with Pydantic
DESCRIPTION: Introduces Pydantic, a library for data validation and settings management using Python type hints. It shows how to define a data model by inheriting from `BaseModel` and declaring typed attributes. Pydantic automatically validates data against these types, providing robust data handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_16

LANGUAGE: Python
CODE:

```
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

LANGUAGE: Python
CODE:

```
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

LANGUAGE: Python
CODE:

```
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

---

TITLE: Calling an Asynchronous Library Function in Python
DESCRIPTION: This snippet demonstrates how to call a function from a third-party library that supports asynchronous operations. The `await` keyword is used to pause the execution of the current coroutine until the `some_library()` function completes its I/O-bound task, allowing other tasks to run concurrently.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_0

LANGUAGE: Python
CODE:

```
results = await some_library()
```

---

TITLE: Defining X-Token Dependency (Python 3.9+ Annotated)
DESCRIPTION: Defines a dependency function `get_token` that reads the `X-Token` header from the request using `Annotated` for type hints. It raises an `HTTPException` if the header value is not 'fake-super-secret-token'.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_4

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import Header, HTTPException


async def get_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
```

---

TITLE: Declaring Path Parameter Metadata with Annotated
DESCRIPTION: This snippet shows how to declare metadata for a path parameter using `Path` and `Annotated`. The `title` parameter provides a descriptive name for the `item_id` path parameter, which is an integer. Path parameters are always required.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params-numeric-validations.md#_snippet_1

LANGUAGE: Python
CODE:

```
    item_id: Annotated[int, Path(title="The ID of the item to get")],
```

---

TITLE: Filtering Response Data with response_model_exclude (List) - FastAPI Python
DESCRIPTION: This snippet illustrates using the `response_model_exclude` parameter with a `list` (which FastAPI converts to a `set`) to omit specific attributes from the API response. Here, 'tax' and 'description' are excluded. FastAPI gracefully handles lists/tuples for these parameters, converting them to sets internally for correct functionality.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/response-model.md#_snippet_6

LANGUAGE: Python
CODE:

```
@app.get("/items/{item_id}", response_model=Item, response_model_exclude=["tax", "description"])
async def read_item_exclude(item_id: str):
    return {
        "name": "Bar",
        "description": "Another description",
        "price": 20.0,
        "tax": 1.0,
    }
```

---

TITLE: Defining a Basic FastAPI Application with Models
DESCRIPTION: This Python snippet demonstrates how to set up a simple FastAPI application. It defines a Pydantic `Item` model for data validation and a POST endpoint that accepts and returns data, showcasing the basic structure for API development and the use of `ResponseMessage`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/generate-clients.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

class ResponseMessage(BaseModel):
    message: str

class Item(BaseModel):
    name: str

app = FastAPI()

@app.post("/items/", response_model=ResponseMessage)
def create_item(item: Item):
    return {"message": "Hello World"}
```

---

TITLE: Creating a Basic FastAPI Application
DESCRIPTION: This snippet defines a basic FastAPI application with two GET endpoints: a root endpoint and an item endpoint that accepts a path parameter and an optional query parameter. It demonstrates the fundamental structure of a FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Create Basic FastAPI Application with GET Endpoints
DESCRIPTION: This code demonstrates how to set up a basic FastAPI application, defining two GET endpoints: a root path and an item path with a path parameter and an optional query parameter. It includes both synchronous (`def`) and asynchronous (`async def`) implementations for route handlers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Using `Annotated` for Metadata (Python 3.9+)
DESCRIPTION: Demonstrates the use of `Annotated` from the standard `typing` module in Python 3.9+ to add additional metadata to type hints. The first parameter to `Annotated` is the actual type, while subsequent parameters provide metadata for tools like FastAPI or Pydantic's `Field`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_30

LANGUAGE: Python
CODE:

```
from typing import Annotated
from pydantic import BaseModel, Field

class ModelWithAnnotated(BaseModel):
    item_name: Annotated[str, Field(min_length=3, max_length=50)]
```

---

TITLE: Annotated Dockerfile for FastAPI
DESCRIPTION: This Dockerfile provides a step-by-step guide to building a FastAPI Docker image, with inline comments explaining each command. It covers selecting a base image, setting the working directory, copying dependencies, installing Python packages, and copying the application code.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_4

LANGUAGE: Dockerfile
CODE:

```
# (1)
FROM python:3.9

# (2)
WORKDIR /code

# (3)
COPY ./requirements.txt /code/requirements.txt

# (4)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)
COPY ./app /code/app
```

---

TITLE: Declaring Query Parameters with Defaults - FastAPI Python
DESCRIPTION: This snippet demonstrates how to declare query parameters in FastAPI with default integer values. Parameters like `skip` and `limit` are automatically parsed from the URL query string and converted to their specified Python types, providing data validation and automatic documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

---

TITLE: Running FastAPI Application with Uvicorn - Console
DESCRIPTION: Provides the command-line instruction to run the FastAPI application using Uvicorn. It specifies the application entry point ('app.main:app') and uses the '--reload' flag for development purposes, enabling automatic code reloading on changes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_11

LANGUAGE: Console
CODE:

```
$ uvicorn app.main:app --reload
<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

TITLE: Installing Uvicorn for Serving FastAPI Applications
DESCRIPTION: This command installs Uvicorn, an ASGI server, with its standard dependencies. Uvicorn is a lightweight and fast server that is commonly used to run FastAPI applications in production environments.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_1

LANGUAGE: console
CODE:

```
pip install "uvicorn[standard]"
```

---

TITLE: Configuring FastAPI Application Metadata
DESCRIPTION: This snippet demonstrates how to provide detailed metadata for your FastAPI application by passing arguments like title, description, version, terms of service, contact information, and license details directly to the FastAPI constructor. This metadata is then used to populate the automatically generated OpenAPI documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/metadata.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI(
    title="My Super Project",
    description="This is a very long description for my super project.",
    version="2.5.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpool",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@app.get("/items/")
async def read_items():
    return {"message": "Hello World"}
```

---

TITLE: Securely Validating HTTP Basic Credentials with `secrets.compare_digest()` in FastAPI
DESCRIPTION: This snippet shows how to securely validate HTTP Basic credentials using Python's `secrets.compare_digest()` function. It converts the provided username and password to bytes before comparison to prevent timing attacks. If the credentials do not match the expected values, an `HTTPException` with a 401 Unauthorized status and a `WWW-Authenticate` header is raised.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/security/http-basic-auth.md#_snippet_1

LANGUAGE: Python
CODE:

```
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username.encode("utf-8"), b"stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password.encode("utf-8"), b"swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "password": credentials.password}
```

---

TITLE: Initializing FastAPI App with Global Dependencies - Python
DESCRIPTION: Illustrates the main application file (`app/main.py`) where the `FastAPI` instance is created. It demonstrates how to declare global dependencies that will be applied to all path operations in the application, including those from included routers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/bigger-applications.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends

from .dependencies import get_query_token

from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
```

---

TITLE: Defining Pydantic Models (Python 3.10+)
DESCRIPTION: Demonstrates defining a Pydantic model using standard type hints, including `Optional` and `list[str]`, for data validation and structure. This example is tailored for Python 3.10+ syntax, showcasing how Pydantic validates and converts input data into structured objects.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_27

LANGUAGE: Python
CODE:

```
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: list[str] = []
```

---

TITLE: Updating FastAPI Application with Pydantic Model and PUT Endpoint (Python)
DESCRIPTION: This Python code updates the `main.py` file to introduce a Pydantic `Item` model for data validation and a new `PUT` endpoint. The `Item` model defines the structure for incoming request bodies, ensuring type safety and enabling automatic documentation. The `update_item` function handles `PUT` requests to `/items/{item_id}`, accepting an `item_id` and an `Item` object as the request body.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_6

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

---

TITLE: Creating a Basic FastAPI Application
DESCRIPTION: This Python code defines a simple FastAPI application with two endpoints. The root endpoint (`/`) returns a 'Hello: World' message, and the `/items/{item_id}` endpoint demonstrates path parameters and optional query parameters. This serves as the core application logic to be containerized.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Testing Asynchronous FastAPI Endpoints with Pytest and AsyncClient
DESCRIPTION: This snippet demonstrates how to write an asynchronous test for a FastAPI application using `pytest` and `httpx.AsyncClient`. The `@pytest.mark.anyio` decorator enables the test function to run asynchronously, allowing the use of `await` with `AsyncClient` to make requests to the FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/async-tests.md#_snippet_1

LANGUAGE: Python
CODE:

```
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

---

TITLE: Upgrade FastAPI App with Pydantic Model and PUT Request
DESCRIPTION: This snippet demonstrates how to extend a FastAPI application to handle request bodies using Pydantic models. It defines an `Item` BaseModel and adds a `PUT` endpoint to update an item, showcasing how FastAPI automatically validates and parses incoming JSON data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

---

TITLE: Defining Pydantic Models (Python 3.9+)
DESCRIPTION: Illustrates defining a Pydantic model for data validation and structure, compatible with Python 3.9+ syntax. It shows how Pydantic uses type hints to validate and convert data, providing a robust way to define expected data shapes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_28

LANGUAGE: Python
CODE:

```
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    name: str
    price: float
    is_available: bool = True
    categories: list[str] = []
```

---

TITLE: Defining Items Router with APIRouter (Python)
DESCRIPTION: Creates an `APIRouter` instance for item-related path operations. It is configured with a path prefix `/items`, a tag `items`, a default 404 response, and the `get_token` dependency applied to all its path operations. It includes example path operations for `/` and `/{item_id}`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_7

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": "baz"}
```

---

TITLE: Defining Asynchronous Path Operation Function - FastAPI Python
DESCRIPTION: This snippet highlights the `async def` syntax used to define an asynchronous path operation function in FastAPI. Asynchronous functions are crucial for handling I/O-bound operations efficiently without blocking the event loop.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_16

LANGUAGE: Python
CODE:

```
async def
```

---

TITLE: Creating a Hero Entry in FastAPI with SQLModel
DESCRIPTION: This FastAPI endpoint handles the creation of a new `Hero` entry. It accepts a `Hero` object from the request body, adds it to the database session, commits the transaction, refreshes the object to include database-generated fields (like `id`), and returns the created hero.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_6

LANGUAGE: Python
CODE:

```
@app.post("/heroes/", response_model=Hero)
def create_hero(*, session: SessionDep, hero: Hero):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

---

TITLE: Defining Hero Table Model Inheriting from HeroBase
DESCRIPTION: This snippet defines the `Hero` table model, which inherits from `HeroBase` and includes additional fields specific to the database table, such as `id` and `secret_name`. By setting `table=True`, it designates `Hero` as a SQLModel table, leveraging inheritance for field reusability.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_11

LANGUAGE: Python
CODE:

```
class HeroBase(SQLModel):
    name: str
    age: int | None = None

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    secret_name: str
```

---

TITLE: Declaring Annotated Dependency Parameter in FastAPI
DESCRIPTION: This snippet illustrates the declaration of a dependency parameter using Python's `Annotated` type hint combined with FastAPI's `Depends` function. It demonstrates how to specify a dependency, `common_parameters`, and its expected type, `dict`, directly within a function signature for type checking and dependency injection.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/index.md#_snippet_3

LANGUAGE: Python
CODE:

```
commons: Annotated[dict, Depends(common_parameters)]
```

---

TITLE: Enforcing HTTPS/WSS Redirection with HTTPSRedirectMiddleware - Python
DESCRIPTION: Illustrates how to add `HTTPSRedirectMiddleware` to a FastAPI application. This middleware automatically redirects all incoming HTTP or WS requests to their secure HTTPS or WSS counterparts, ensuring secure communication.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/middleware.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Creating a SQLModel Session Dependency in FastAPI
DESCRIPTION: This snippet defines a FastAPI dependency that provides a new SQLModel `Session` for each request using `yield`, ensuring proper session management. It also creates an `Annotated` type alias, `SessionDep`, to simplify its use in route functions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_4

LANGUAGE: Python
CODE:

```
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
```

---

TITLE: Implementing Custom ID Validation with AfterValidator in Python
DESCRIPTION: This snippet demonstrates how to create a custom validator function (`validate_item_id`) using Pydantic's `AfterValidator` and `Annotated` in FastAPI. It ensures that an item ID string starts with either 'isbn-' or 'imdb-', raising a `ValueError` if the condition is not met, and shows how to apply this validator to a path parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_24

LANGUAGE: python
CODE:

```
from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()

def validate_item_id(value: str):
    if not value.startswith(("isbn-", "imdb-")):
        raise ValueError("Item ID must start with 'isbn-' or 'imdb-'")
    return value

ItemId = Annotated[str, AfterValidator(validate_item_id)]

@app.get("/items/{item_id}")
async def read_item(item_id: ItemId):
    return {"item_id": item_id, "message": "Item ID is valid"}
```

---

TITLE: Defining Pydantic v2 BaseSettings Class
DESCRIPTION: This Python snippet defines a `Settings` class inheriting from `BaseSettings` (from `pydantic_settings`). It declares application configuration attributes with type annotations and default values, enabling Pydantic to automatically load and validate settings from environment variables.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_2

LANGUAGE: Python
CODE:

```
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
```

---

TITLE: Asynchronous `async with` Statement Example
DESCRIPTION: This snippet demonstrates the use of an `async with` statement with an asynchronous context manager, such as the `lifespan` function. This pattern is used to manage asynchronous resources, ensuring that setup (`await do_stuff()`) and teardown operations are handled correctly within an `async` context.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/events.md#_snippet_4

LANGUAGE: Python
CODE:

```
async with lifespan(app):
    await do_stuff()
```

---

TITLE: Injecting a Class-Based Dependency into a Path Operation
DESCRIPTION: This snippet demonstrates how to integrate the `CommonQueryParams` class as a dependency into a FastAPI path operation. By type-hinting `commons` as `CommonQueryParams` and assigning `Depends(CommonQueryParams)`, FastAPI instantiates the class and provides its instance to the `read_items` function. This allows the path operation to access the parsed query parameters via the `commons` object.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_7

LANGUAGE: Python
CODE:

```
@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return commons
```

---

TITLE: Implementing Custom Exception Handler in FastAPI
DESCRIPTION: This example shows how to register a custom exception handler using `@app.exception_handler()` for a specific custom exception, `UnicornException`. The handler intercepts the exception, allowing the application to return a custom `JSONResponse` with a specific status code and content, overriding default FastAPI behavior.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

app = FastAPI()

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

---

TITLE: Defining Asynchronous GET Path Operation in FastAPI
DESCRIPTION: This snippet defines an asynchronous path operation function for the root URL (`/`) using the `GET` HTTP method. FastAPI calls this `async` function when a `GET` request is received at the specified path, making it suitable for I/O-bound operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_9

LANGUAGE: Python
CODE:

```
@app.get("/")
async def root():
```

---

TITLE: Implementing OAuth2 Scopes in FastAPI: Global View
DESCRIPTION: This comprehensive snippet demonstrates the full integration of OAuth2 scopes in a FastAPI application. It includes defining the OAuth2 security scheme with specific scopes, handling user authentication, creating JWT tokens that embed user scopes, and protecting API endpoints based on required permissions. It serves as a complete example of a secure API with scope-based authorization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/security/oauth2-scopes.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# ... (User, Token, authenticate_user, create_access_token, get_current_user models and functions)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items."
    }
)

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Security(oauth2_scheme, scopes=["me"])]):
    return current_user


@app.get("/items/", response_model=list[Item])
async def read_items(current_user: Annotated[User, Security(oauth2_scheme, scopes=["items"])]):
    return [
        {"item_id": "Foo", "owner": "Alice"},
        {"item_id": "Bar", "owner": "Bob"}
    ]

# ... (Item model definition)
```

---

TITLE: Defining a Common Dependency Function (Python)
DESCRIPTION: This snippet defines an asynchronous function `common_parameters` that serves as a dependency. It accepts optional query parameters `q` (string), `skip` (integer, default 0), and `limit` (integer, default 100), then returns them as a dictionary. This function encapsulates reusable logic for handling common request parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/index.md#_snippet_0

LANGUAGE: Python
CODE:

```
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
```

---

TITLE: Using OAuth2PasswordBearer as a Dependency in FastAPI
DESCRIPTION: Integrates the `oauth2_scheme` as a dependency in a FastAPI path operation. This automatically handles the extraction and validation of the Bearer token from the `Authorization` header, providing the token string to the function parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/first-steps.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

---

TITLE: Defining Pydantic `BaseSettings` for Application Configuration
DESCRIPTION: This Python snippet defines a `Settings` class inheriting from Pydantic's `BaseSettings`. It declares configuration fields with type hints and default values, allowing Pydantic to automatically load values from environment variables (e.g., `APP_NAME`, `ADMIN_EMAIL`) and perform validation, including field-specific constraints like `gt` and `le`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_5

LANGUAGE: python
CODE:

```
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = Field(50, gt=0, le=100)
```

---

TITLE: Defining a Pydantic Model with Optional Fields in Python
DESCRIPTION: This snippet defines a Pydantic `Item` model. The `description` and `tax` fields are explicitly marked as optional using `Union[str, None]` and `Union[float, None]` respectively, and are assigned a default value of `None`. This model structure is fundamental to how FastAPI and Pydantic v2 generate distinct OpenAPI schemas for input and output contexts.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/separate-openapi-schemas.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
```

---

TITLE: Testing FastAPI Application with Separate Test File
DESCRIPTION: This snippet demonstrates how to structure tests in a separate `test_main.py` file, importing the FastAPI application instance from `app.main`. It utilizes `TestClient` to make a GET request to the root endpoint and asserts the expected status code and JSON response, suitable for larger project structures.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/testing.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

---

TITLE: Defining Path Operations with Specific Order in FastAPI
DESCRIPTION: This snippet demonstrates the importance of path operation order in FastAPI. The more specific path `/users/me` must be declared before the more general `/users/{user_id}` to ensure the correct handler is invoked, preventing the general path from incorrectly matching the specific one.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

---

TITLE: Injecting Settings into FastAPI Path Operations - Python
DESCRIPTION: This code demonstrates how to inject the `Settings` object into a FastAPI path operation using `Depends(get_settings)`. The `info` endpoint retrieves and returns the `app_name` and `admin_email` from the application settings, ensuring consistent configuration access across the API.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_12

LANGUAGE: Python
CODE:

```
from fastapi import Depends, FastAPI
from .config import get_settings, Settings

app = FastAPI()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email
    }
```

---

TITLE: Building a FastAPI Docker Image
DESCRIPTION: This Dockerfile defines the steps to build a Docker image for a FastAPI application. It starts from a Python 3.9 base image, sets the working directory, copies `requirements.txt`, installs dependencies, copies the application code, and sets the default command to run the FastAPI application using `fastapi run`. It also includes a commented-out line for running behind a proxy.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_0

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

---

TITLE: Multi-stage Dockerfile for Poetry-based FastAPI Applications
DESCRIPTION: This multi-stage Dockerfile is designed for FastAPI projects that use Poetry for dependency management. The first stage (`requirements-stage`) installs Poetry and exports dependencies to a `requirements.txt` file. The second stage then uses this `requirements.txt` to install dependencies efficiently, resulting in a smaller final image. This approach optimizes image size and build time.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_17

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
```

---

TITLE: Returning Unauthorized HTTP Exception for Basic Auth
DESCRIPTION: This snippet shows how to raise an `HTTPException` with a 401 Unauthorized status code when authentication fails. It includes the `WWW-Authenticate` header with the value "Basic" to instruct the client (e.g., a web browser) to prompt the user for credentials.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/security/http-basic-auth.md#_snippet_5

LANGUAGE: Python
CODE:

```
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Basic"},
)
```

---

TITLE: Reusing Default Exception Handlers in FastAPI
DESCRIPTION: This example shows how to extend FastAPI's default exception handling behavior by importing and reusing the built-in `http_exception_handler` and `request_validation_exception_handler`. Custom logic, such as logging, can be added before delegating to the default handlers, allowing for both custom actions and standard error responses.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_11

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"OMG! The client sent invalid data!: {exc.errors()}")
    return await request_validation_exception_handler(request, exc)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    print(f"OMG! An HTTP error!: {exc.detail}")
    return await http_exception_handler(request, exc)
```

---

TITLE: Testing Authenticated FastAPI Endpoints with TestClient
DESCRIPTION: This snippet provides comprehensive tests for a FastAPI application with authenticated GET and POST endpoints. It demonstrates how to send headers and JSON bodies with `TestClient` requests, asserting various status codes and response contents for cases with valid, invalid, and missing authentication tokens.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/testing.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi.testclient import TestClient
from app.app_b.main import app

client = TestClient(app)

def test_read_items():
    response = client.get("/items/", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == [{"item_id": "Foo"}, {"item_id": "Bar"}]

def test_read_items_bad_token():
    response = client.get("/items/", headers={"X-Token": "bad-token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}

def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "fake-super-secret-token"},
        json={"name": "Baz", "description": "The Baz", "price": 50.2},
    )
    assert response.status_code == 200
    assert response.json() == {"name": "Baz", "description": "The Baz", "price": 50.2}

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "bad-token"},
        json={"name": "Baz", "description": "The Baz", "price": 50.2},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}

def test_create_item_no_token():
    response = client.post(
        "/items/",
        json={"name": "Baz", "description": "The Baz", "price": 50.2},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}
```

---

TITLE: Combining Path Parameters with Request Body in FastAPI
DESCRIPTION: This example shows how to define a path operation that accepts both a path parameter (`item_id`) and a request body (`item` of type `Item`). FastAPI intelligently distinguishes between them based on their type annotations, automatically extracting data from the URL path and the request body respectively.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_6

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
```

---

TITLE: Defining a GET Path Operation
DESCRIPTION: This snippet demonstrates how to define a GET path operation using the `@app.get()` decorator in FastAPI. The decorator associates the following asynchronous Python function with the specified URL path (`/`) and the HTTP GET method, making it responsible for handling incoming GET requests to that route.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_7

LANGUAGE: Python
CODE:

```
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

TITLE: Building a Docker Image for FastAPI
DESCRIPTION: This Dockerfile defines the steps to create a Docker image for a FastAPI application. It starts from a Python base image, sets the working directory, copies `requirements.txt`, installs Python dependencies, and then copies the application code.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/deployment/docker.md#_snippet_0

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
```

---

TITLE: Configuring CORS Middleware in FastAPI
DESCRIPTION: This snippet demonstrates how to configure Cross-Origin Resource Sharing (CORS) in a FastAPI application using `CORSMiddleware`. It sets up a list of allowed origins, enables credentials, and allows all HTTP methods and headers for cross-origin requests. This middleware intercepts incoming requests to handle CORS preflight and simple requests, ensuring proper communication between different origins.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/cors.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost",
    "https://example.org",
    "https://www.example.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

TITLE: Basic FastAPI Application Testing with TestClient
DESCRIPTION: This snippet demonstrates how to test a basic FastAPI application using `TestClient`. It initializes the client with the FastAPI app, sends a GET request to the root path, and asserts the status code and JSON response. Tests are standard `def` functions, not `async def`, allowing direct use with `pytest`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

---

TITLE: Reducing Duplication with Pydantic Model Inheritance in Python
DESCRIPTION: This snippet demonstrates how to reduce code duplication by using Pydantic model inheritance. A `UserBase` model defines common attributes, and `UserIn`, `UserInDB`, and `UserOut` models inherit from it, adding only their specific fields (e.g., `password`, `hashed_password`) or simply inheriting all fields, ensuring consistency and maintainability.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_7

LANGUAGE: Python
CODE:

```
from typing import Optional
from pydantic import BaseModel

# Base model with common fields
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# Input model: inherits from UserBase, adds password
class UserIn(UserBase):
    password: str

# Database model: inherits from UserBase, adds hashed_password
class UserInDB(UserBase):
    hashed_password: str

# Output model: inherits from UserBase (no password or hashed_password)
class UserOut(UserBase):
    pass
```

---

TITLE: Defining a Basic HTTP Middleware in FastAPI
DESCRIPTION: This snippet illustrates the fundamental structure for creating an HTTP middleware in FastAPI. It uses the `@app.middleware("http")` decorator to register an asynchronous function that receives the `request` object and a `call_next` function. The `call_next` function processes the request and returns the `response`, which can then be further modified before being returned by the middleware.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/middleware.md#_snippet_0

LANGUAGE: Python
CODE:

```
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response
```

---

TITLE: Importing HTTPSRedirectMiddleware in FastAPI
DESCRIPTION: This snippet illustrates how to import the HTTPSRedirectMiddleware class, which automatically redirects all incoming HTTP requests to their HTTPS equivalents. This is crucial for enforcing secure communication and protecting sensitive data in a FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/middleware.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

---

TITLE: Raising HTTPException for Not Found Items in FastAPI
DESCRIPTION: This example shows how to raise an `HTTPException` with a `404 Not Found` status code when a requested item ID does not exist. The `detail` parameter provides a custom error message to the client, which FastAPI automatically converts to a JSON response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_1

LANGUAGE: Python
CODE:

```
items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}
```

---

TITLE: Users APIRouter Module - Python
DESCRIPTION: Defines a simple APIRouter for user-related routes. This module is intended to be imported and included in the main application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/pt/docs/tutorial/bigger-applications.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]
```

---

TITLE: Calling Awaitable Third-Party Library (Python)
DESCRIPTION: This snippet demonstrates the syntax for calling a function from a third-party library that supports asynchronous operations and requires the `await` keyword. It highlights how to pause execution until the asynchronous operation completes, allowing the program to perform other tasks in the interim.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_0

LANGUAGE: Python
CODE:

```
results = await some_library()
```

---

TITLE: Declaring Custom Model Type Hint in FastAPI
DESCRIPTION: This snippet illustrates how to declare a type hint for a custom `Item` model. FastAPI automatically validates and serializes data based on the structure defined in the `Item` class, leveraging Pydantic.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_8

LANGUAGE: Python
CODE:

```
item: Item
```

---

TITLE: Using Pydantic `Settings` in a FastAPI Application
DESCRIPTION: This snippet demonstrates how to import and use the `settings` object (an instance of `BaseSettings`) within a FastAPI application. It exposes configuration values like `app_name`, `admin_email`, and `items_per_user` via an API endpoint, showcasing how Pydantic centralizes and provides type-safe access to application settings.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_6

LANGUAGE: python
CODE:

```
from fastapi import FastAPI

from .config import settings

app = FastAPI()

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

---

TITLE: Defining Query Parameter with Annotated and Default Value - FastAPI Python
DESCRIPTION: This is the recommended way to define a query parameter `q` using `Annotated` in FastAPI. The actual default value for the parameter is set directly on the function parameter (`="rick"`), while `Query()` is used within `Annotated` to provide FastAPI-specific metadata without conflicting defaults.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/de/docs/tutorial/query-params-str-validations.md#_snippet_7

LANGUAGE: Python
CODE:

```
q: Annotated[str, Query()] = "rick"
```

---

TITLE: Returning HTTP 401 Unauthorized for Invalid Credentials
DESCRIPTION: This snippet shows how to respond with an HTTP 401 Unauthorized status code when credentials are incorrect. It uses FastAPI's `HTTPException` to set the status, provide a detail message, and include the `WWW-Authenticate: Basic` header, prompting the client (browser) to re-request credentials.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/security/http-basic-auth.md#_snippet_3

LANGUAGE: Python
CODE:

```
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Basic"},
)
```

---

TITLE: Retrieving User Data and Handling Invalid Credentials in FastAPI
DESCRIPTION: This code snippet shows how to retrieve user data from a simulated database using the provided username. If the user is not found, it raises an `HTTPException` with a 401 status code and a detail message indicating incorrect credentials, ensuring proper error handling for authentication failures.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/simple-oauth2.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import HTTPException, status
# ... (inside your login function)
user = get_user(form_data.username)
if not user:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
```

---

TITLE: Running Uvicorn with Multiple Workers via CLI
DESCRIPTION: This command demonstrates how to start a Uvicorn server with four worker processes, binding it to all network interfaces on port 8080. The output shows the parent process managing the individual worker processes, each handling application startup, indicating increased concurrency for handling requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/server-workers.md#_snippet_3

LANGUAGE: bash
CODE:

```
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

---

TITLE: Pydantic `BaseSettings` for Dependency Injection
DESCRIPTION: This `Settings` class is designed to be used with dependency injection frameworks (like FastAPI's dependency system). By not instantiating `Settings()` directly within the configuration file, it allows the framework to manage its lifecycle and provide it as a dependency where needed, promoting testability and modularity.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_10

LANGUAGE: python
CODE:

```
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = Field(50, gt=0, le=100)
```

---

TITLE: Performing Partial Update with PATCH in FastAPI (Python)
DESCRIPTION: This complete FastAPI `PATCH` endpoint demonstrates the process for applying partial updates to an item. It retrieves the stored item, creates a Pydantic model from it, extracts only the set values from the incoming request using `exclude_unset`, updates the stored model copy, converts it to a JSON-compatible format with `jsonable_encoder`, and saves the changes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-updates.md#_snippet_4

LANGUAGE: Python
CODE:

```
@app.patch("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
```

---

TITLE: FastAPI Application with Authenticated GET and POST Endpoints
DESCRIPTION: This snippet defines a FastAPI application with two endpoints, `/items/` (GET and POST), both requiring an `X-Token` header for authentication. It demonstrates how to use `Header` for dependency injection and raise `HTTPException` for invalid or missing tokens, ensuring secure access to resources.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/testing.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
async def read_items(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]

@app.post("/items/")
async def create_item(item: dict, x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return item
```

---

TITLE: Adding Middleware to FastAPI Application using add_middleware in Python
DESCRIPTION: This snippet illustrates the recommended way to add middleware in FastAPI (and Starlette) using the `app.add_middleware()` method. It takes the middleware class as the first argument, followed by any keyword arguments for the middleware's constructor. This method correctly integrates the middleware into the FastAPI application's processing chain, handling data and custom exceptions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/middleware.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

---

TITLE: Dependency with Yield and Error Handling (Python)
DESCRIPTION: This example illustrates how to use `try`, `except`, and `finally` blocks within a `yield` dependency. This allows catching exceptions that occur during the dependency's usage (e.g., in a path operation) and ensures cleanup code in `finally` is always executed, regardless of errors.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_3

LANGUAGE: Python
CODE:

```
def get_db():
    db = DBSession()
    try:
        yield db
    except Exception as e:
        print(f"Error during DB session: {e}")
    finally:
        db.close()
```

---

TITLE: Defining Pydantic v1 BaseSettings Class
DESCRIPTION: This Python snippet defines a `Settings` class inheriting from `BaseSettings` (from `pydantic` for v1). It specifies application configuration attributes with types and optional defaults, allowing Pydantic to automatically handle environment variable loading and validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_3

LANGUAGE: Python
CODE:

```
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
```

---

TITLE: Importing FastAPI Class
DESCRIPTION: This line imports the `FastAPI` class from the `fastapi` library. The `FastAPI` class is the core component that provides all the functionality for building your API, inheriting capabilities from Starlette.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
```

---

TITLE: Importing Depends for FastAPI Dependencies
DESCRIPTION: This line imports `FastAPI`, `Depends`, and `Query` from the `fastapi` module. `Depends` is a crucial utility in FastAPI for declaring dependencies, allowing functions to receive injected values from other dependency functions or directly from request parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/index.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends, Query
```

---

TITLE: Importing Depends for Dependency Injection (Python)
DESCRIPTION: This snippet shows the essential import statement for `Depends` from the `fastapi` module. `Depends` is a crucial utility in FastAPI's dependency injection system, enabling the declaration and automatic injection of dependencies into path operation functions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/index.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends, Query
```

---

TITLE: Accessing Pydantic Model Attributes
DESCRIPTION: This snippet demonstrates how to access the attributes of a Pydantic model instance (`item`) received as a request body. Once validated by FastAPI, the model's fields can be directly accessed using dot notation, similar to any Python object.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

---

TITLE: Creating an Asynchronous FastAPI Application
DESCRIPTION: This snippet shows an alternative implementation of the basic FastAPI application using `async def` for the route functions. This is suitable for applications that perform asynchronous operations, allowing for better concurrency.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_4

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

---

TITLE: Defining Synchronous GET Path Operation in FastAPI
DESCRIPTION: This snippet demonstrates defining a synchronous path operation function for the root URL (`/`) with the `GET` HTTP method. Unlike `async` functions, this `def` function is suitable for CPU-bound operations or when asynchronous capabilities are not required.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_10

LANGUAGE: Python
CODE:

```
@app.get("/")
def root():
```

---

TITLE: Defining Python Types and Pydantic Models
DESCRIPTION: This snippet demonstrates the use of standard Python type hints for function parameters and the definition of a data model using Pydantic's BaseModel. It showcases how to declare a string type for a function argument and define a 'User' model with integer, string, and date fields, leveraging Python's built-in 'datetime.date' and Pydantic for structured data validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/features.md#_snippet_0

LANGUAGE: Python
CODE:

```
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

---

TITLE: Including APIRouter Instances in Main App - FastAPI Python
DESCRIPTION: Demonstrates how to include the imported `APIRouter` instances (`users.router`, `items.router`) into the main `FastAPI` application instance using `app.include_router()`. This integrates the routes defined in the submodules into the main application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/bigger-applications.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends

from .dependencies import get_query_token

from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
```

---

TITLE: Installing Uvicorn (Standard)
DESCRIPTION: This command installs Uvicorn with its standard dependencies, including `uvloop` for a high-performance `asyncio` event loop, which significantly improves performance for asynchronous operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/manually.md#_snippet_0

LANGUAGE: Shell
CODE:

```
$ pip install "uvicorn[standard]"
```

---

TITLE: Setting Response Model to UserOut in FastAPI Post Endpoint
DESCRIPTION: This snippet shows the `response_model` parameter of the `@app.post()` decorator explicitly set to `UserOut`. This configuration instructs FastAPI to use the `UserOut` Pydantic model for data validation, serialization, and OpenAPI documentation of the response, effectively filtering out any fields (like passwords) not present in `UserOut` from the final API response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class UserOut(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
```

---

TITLE: Declaring a Path Parameter with an Enum Type in FastAPI
DESCRIPTION: This snippet shows how to declare a path parameter `model_name` with a type annotation of `ModelName` (the Enum class). FastAPI automatically uses the Enum's predefined values for validation and documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_8

LANGUAGE: Python
CODE:

```
@app.get("/models/{model_name}")
```

---

TITLE: Using Dependencies in WebSocket Endpoints
DESCRIPTION: This example shows how to integrate FastAPI's dependency injection system (`Depends`, `Path`, `Query`, `Cookie`) with WebSocket endpoints. Dependencies can be used to validate path parameters, query parameters, or inject other services before establishing the WebSocket connection.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/websockets.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, WebSocket, WebSocketException, status, Depends, Path, Query, Cookie

app = FastAPI()

async def get_cookie_or_token(
    websocket: WebSocket,
    session: str | None = Cookie(default=None),
    token: str | None = Query(default=None),
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int = Path(),
    q: int | None = Query(default=None),
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}, client_id: {client_id}, q: {q}, cookie_or_token: {cookie_or_token}")
    except WebSocketException as e:
        print(f"WebSocket disconnected: {e.code}")
```

---

TITLE: Pydantic Model with Optional Fields and Default Values
DESCRIPTION: This Pydantic `Item` model demonstrates fields with default values: `description` is optional and defaults to `None`, `tax` defaults to `10.5`, and `tags` defaults to an empty list. These defaults are used when values are not explicitly provided, influencing how data is serialized and potentially omitted from responses using `response_model_exclude_unset`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_6

LANGUAGE: Python
CODE:

```
from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

app = FastAPI()

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]
```

---

TITLE: Defining Simple APIRouter (Python)
DESCRIPTION: Initializes a basic APIRouter instance within a submodule file (app/internal/admin.py) to group related path operations, which can then be included in a main application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_19

LANGUAGE: Python
CODE:

```
router = APIRouter()
```

---

TITLE: Declaring Basic Path Parameters in FastAPI
DESCRIPTION: This snippet demonstrates how to declare a simple path parameter `item_id` in a FastAPI GET route. The value from the URL path is automatically passed as an argument to the asynchronous function, allowing the API to respond with the received ID.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

---

TITLE: FastAPI Asynchronous Path Operation
DESCRIPTION: Demonstrates a FastAPI path operation defined as an `async def` function. This allows the endpoint to `await` asynchronous operations, such as fetching burgers, without blocking the server and enabling concurrent handling of multiple requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_7

LANGUAGE: Python
CODE:

```
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

---

TITLE: Defining User Path Operations with APIRouter
DESCRIPTION: Shows how to define path operations for a specific domain (users) in a separate file (`app/routers/users.py`) using `APIRouter`, including importing the router and defining GET endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me/", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

---

TITLE: FastAPI Application Dependencies (requirements.txt)
DESCRIPTION: This snippet shows a typical `requirements.txt` file, listing the Python packages required for a FastAPI application, including `fastapi`, `pydantic`, and `uvicorn`, along with their version constraints. This file is used by `pip` to install project dependencies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_1

LANGUAGE: Text
CODE:

```
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
```

---

TITLE: Installing FastAPI with Standard Dependencies (Python)
DESCRIPTION: This command installs FastAPI along with its 'standard' group of optional dependencies. These include libraries for email validation, HTTP client functionality for testing, template rendering, form parsing, and a high-performance ASGI server like Uvicorn.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_13

LANGUAGE: Python
CODE:

```
pip install "fastapi[standard]"
```

---

TITLE: Installing FastAPI with Standard Dependencies
DESCRIPTION: This command installs FastAPI along with a set of commonly used standard optional dependencies, such as Uvicorn for the server and Pydantic for data validation. It is recommended to execute this command within an activated Python virtual environment to manage project dependencies effectively.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/index.md#_snippet_1

LANGUAGE: console
CODE:

```
$ pip install "fastapi[standard]"

---> 100%
```

---

TITLE: Including Routers in Main App - Python
DESCRIPTION: Demonstrates how to include the 'APIRouter' instances from the imported router modules ('users.router', 'items.router') into the main 'FastAPI' application using the 'app.include_router()' method. This integrates the routes defined in the separate router files into the main application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_7

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from app.dependencies import get_token_header

from app.routers import items, users
from app.internal import admin

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

TITLE: Running FastAPI App (Console)
DESCRIPTION: Provides the command-line command fastapi dev app/main.py to start the FastAPI development server (Uvicorn) with auto-reloading for the specified application file.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_22

LANGUAGE: Console
CODE:

```
fastapi dev app/main.py
```

---

TITLE: Declare Integer Path Parameter in FastAPI
DESCRIPTION: Demonstrates declaring an integer path parameter `item_id` using standard Python type hints. This enables automatic validation, editor support, and documentation within FastAPI.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_6

LANGUAGE: Python
CODE:

```
item_id: int
```

---

TITLE: Running FastAPI Application in Development Mode
DESCRIPTION: This console command starts the FastAPI development server. The `fastapi dev` command automatically reloads the application on code changes, making it convenient for development. The server typically runs on `http://127.0.0.1:8000`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md#_snippet_4

LANGUAGE: console
CODE:

```
$ fastapi dev main.py
```

---

TITLE: FastAPI Automatic Interactive API Documentation
DESCRIPTION: This section highlights FastAPI's built-in support for generating interactive API documentation using Swagger UI and ReDoc. It explains how to access these documentation interfaces at `/docs` and `/redoc` respectively, providing a visual representation of the API endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_4

LANGUAGE: APIDOC
CODE:

```
FastAPI automatically generates interactive API documentation based on your code. Access Swagger UI at `/docs` and ReDoc at `/redoc`. These interfaces provide a visual representation of all defined endpoints, their parameters, and expected responses, facilitating API exploration and testing.
```

---

TITLE: Including Admin Router with Custom Config - Python
DESCRIPTION: Demonstrates including the 'admin.router' into the main 'FastAPI' application using 'app.include_router()'. This example shows how to apply custom configurations like a URL 'prefix' ('/admin'), 'tags' ('admin'), 'dependencies' (e.g., 'get_token_header'), and specific 'responses' directly during the inclusion process.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_9

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from app.dependencies import get_token_header

from app.routers import items, users
from app.internal import admin

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

TITLE: Streaming File-Like Objects with StreamingResponse in FastAPI
DESCRIPTION: This example demonstrates using `StreamingResponse` to stream content from a file-like object. It uses a regular `def` function for the path operation since `open()` is not an async operation, and returns a `StreamingResponse` with an iterator that yields file chunks.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/custom-response.md#_snippet_9

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/file-stream")
def stream_file():
    def iterfile():
        with open("large_file.txt", mode="rb") as file_like:
            yield from file_like
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
```

---

TITLE: Running FastAPI Application with Uvicorn
DESCRIPTION: This console command initiates the FastAPI application using fastapi dev, which internally uses Uvicorn. It starts a development server, making the application accessible at http://127.0.0.1:8000. This command is essential for testing and running FastAPI applications locally.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md#_snippet_3

LANGUAGE: Console
CODE:

```
fastapi dev main.py
```

---

TITLE: Reading Multiple Heroes with Pagination in FastAPI
DESCRIPTION: This FastAPI endpoint retrieves a list of `Hero` objects from the database. It supports pagination through optional `offset` and `limit` query parameters, allowing clients to fetch a subset of heroes. It uses `session.exec(select(Hero).offset(offset).limit(limit))` to query the database.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_7

LANGUAGE: Python
CODE:

```
@app.get("/heroes/", response_model=List[Hero])
def read_heroes(
    *,
    session: SessionDep,
    offset: int = 0,
    limit: Optional[int] = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
```

---

TITLE: Defining Application Settings Class
DESCRIPTION: This snippet shows how to define a Pydantic `BaseSettings` class (or `Settings` in Pydantic v2) to hold application configurations. Unlike a global instance, this class is designed to be instantiated within a dependency, making it easier to manage and override settings, especially during testing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/settings.md#_snippet_0

LANGUAGE: Python
CODE:

```
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
```

---

TITLE: Pinning FastAPI Version Range (Minor Updates)
DESCRIPTION: This snippet illustrates how to specify a flexible version range for FastAPI (e.g., `0.45.0` or newer, but strictly less than `0.46.0`). This allows for automatic updates to bug fixes and non-breaking changes within the `0.45.x` series while preventing updates to `0.46.0` or higher, which might introduce breaking changes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/versions.md#_snippet_1

LANGUAGE: txt
CODE:

```
fastapi>=0.45.0,<0.46.0
```

---

TITLE: Accessing Pydantic Model Attributes in FastAPI Endpoint - Python
DESCRIPTION: This complete FastAPI endpoint demonstrates how to access and utilize the attributes of a received Pydantic `Item` model within a path operation function. It shows how to convert the model to a dictionary, perform conditional logic based on optional fields, and return a modified response, leveraging the type safety and structure provided by Pydantic.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

---

TITLE: Pinning FastAPI to a Minor Version Range (Example 2) in requirements.txt
DESCRIPTION: This snippet provides another example of pinning FastAPI to a minor version range (e.g., 0.45.x) in `requirements.txt`. This strategy is recommended to receive patch updates (bug fixes) without automatically upgrading to new minor versions which might contain breaking changes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/versions.md#_snippet_2

LANGUAGE: txt
CODE:

```
fastapi>=0.45.0,<0.46.0
```

---

TITLE: Reading .env Settings with Pydantic
DESCRIPTION: This snippet shows how to configure a Pydantic `Settings` class to automatically load environment variables from a `.env` file. The configuration method differs slightly between Pydantic v1 (using an inner `Config` class) and Pydantic v2 (using the `model_config` attribute).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/settings.md#_snippet_5

LANGUAGE: Python
CODE:

```
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str

    model_config = SettingsConfigDict(env_file=".env") # Pydantic v2
```

LANGUAGE: Python
CODE:

```
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str

    class Config: # Pydantic v1
        env_file = ".env"
```

---

TITLE: Starting FastAPI with Multiple Workers using `fastapi` command
DESCRIPTION: This command initiates the FastAPI application located in `main.py` using the `fastapi` CLI, configuring it to run with 4 worker processes. It leverages the built-in `fastapi` runner to manage the application's concurrency, providing a simplified startup experience.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/server-workers.md#_snippet_0

LANGUAGE: Shell
CODE:

```
fastapi run --workers 4 main.py
```

---

TITLE: Combining Body, Path, and Query Parameters in FastAPI
DESCRIPTION: This snippet demonstrates a FastAPI path operation that simultaneously handles a request body (`item`), a path parameter (`item_id`), and an optional query parameter (`q`). FastAPI automatically parses and validates each parameter from its respective source (body, URL path, or query string).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body.md#_snippet_7

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    results = {"item_id": item_id, **item.dict()}
    if q:
        results.update({"q": q})
    return results
```

---

TITLE: Defining Async Path Operation with Await - FastAPI Python
DESCRIPTION: This FastAPI path operation function `read_burgers` is defined as `async def`, allowing it to correctly `await` the `get_burgers` asynchronous function. This demonstrates the proper pattern for integrating asynchronous operations within FastAPI route handlers, ensuring that I/O-bound tasks do not block the event loop. The `@app.get('/burgers')` decorator registers this function as an HTTP GET endpoint.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_7

LANGUAGE: Python
CODE:

```
@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

---

TITLE: Defining FastAPI Lifespan Async Context Manager
DESCRIPTION: This snippet defines the `lifespan` function as an `asynccontextmanager`, which is used by FastAPI to manage application startup and shutdown events. The code before `yield` executes on startup, and the code after `yield` executes on shutdown, making it suitable for initializing and cleaning up shared resources.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/events.md#_snippet_1

LANGUAGE: Python
CODE:

```
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["regression_model"] = RegressionModel()
    yield
    # Clean up the ML models
    ml_models.clear()
```

---

TITLE: Creating a Settings Dependency Function
DESCRIPTION: This Python code defines a FastAPI dependency function, `get_settings`, which instantiates and returns the `Settings` object. The `@lru_cache()` decorator is used to ensure that the settings object is created only once per application lifecycle, optimizing performance.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/settings.md#_snippet_1

LANGUAGE: Python
CODE:

```
from functools import lru_cache

from .config import Settings

@lru_cache()
def get_settings():
    return Settings()
```

---

TITLE: Starting FastAPI with Multiple Workers using `uvicorn` command
DESCRIPTION: This command directly starts the FastAPI application `main:app` using Uvicorn, binding it to `0.0.0.0:8080` and configuring it to run with 4 worker processes. It offers granular control over Uvicorn's server parameters, suitable for more specific deployment scenarios.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/server-workers.md#_snippet_1

LANGUAGE: Shell
CODE:

```
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

---

TITLE: Defining FastAPI Header Dependencies - Python
DESCRIPTION: These asynchronous functions define dependencies that extract specific headers (`X-Key`, `X-Token`) from the incoming request. They serve as prerequisites for path operations, ensuring that required headers are present and can be validated. These functions can also declare other sub-dependencies if needed.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md#_snippet_1

LANGUAGE: Python
CODE:

```
async def verify_key(x_key: Annotated[str | None, Header()] = None):
async def verify_token(x_token: Annotated[str | None, Header()] = None):
```

---

TITLE: Handling Dependency Errors with HTTPException - Python
DESCRIPTION: This code demonstrates how dependencies can raise `HTTPException` to signal errors or unmet requirements. If a required header is missing or invalid, an appropriate HTTP status code and detail message are returned to the client, preventing the path operation from executing. This ensures robust error handling within the dependency chain.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md#_snippet_2

LANGUAGE: Python
CODE:

```
if x_key is None:
    raise HTTPException(status_code=400, detail="X-Key header required")
if x_token is None:
    raise HTTPException(status_code=400, detail="X-Token header required")
```

---

TITLE: Declaring Pydantic Model Attributes with Field in Python
DESCRIPTION: This snippet illustrates how to use `Field` within a Pydantic `BaseModel` to define attributes with default values, validation, and metadata. It shows how `Field` parameters like `default`, `title`, `max_length`, `gt` (greater than), and `description` are applied to model fields.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-fields.md#_snippet_1

LANGUAGE: Python
CODE:

```
description: Union[str, None] = Field(
    default=None, title="Description of the item", max_length=300
)
price: float = Field(gt=0, description="The price must be greater than zero")
```

---

TITLE: Include APIRouter in another APIRouter (Python)
DESCRIPTION: This snippet shows how to include one APIRouter instance (`other_router`) into another (`router`). This allows nesting router structures. Ensure this inclusion is done before the parent router (`router`) is included in the main FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_23

LANGUAGE: Python
CODE:

```
router.include_router(other_router)
```

---

TITLE: Adding Max Length Validation to Optional Query Parameter
DESCRIPTION: This snippet demonstrates adding a `max_length` validation to an optional query parameter `q`. The `Query` dependency is used to specify that the string value for `q` must not exceed 50 characters, while still allowing it to be `None`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_4

LANGUAGE: Python
CODE:

```
q: Union[str, None] = Query(default=None, max_length=50)
```

---

TITLE: Building a FastAPI Docker Image
DESCRIPTION: This Dockerfile defines the steps to build a Docker image for a FastAPI application. It starts from a Python base image, sets the working directory, copies `requirements.txt`, installs dependencies, copies the application code, and defines the command to run the Uvicorn server.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_0

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
```

---

TITLE: Installing Python Dependencies with pip
DESCRIPTION: This command demonstrates how to install Python package dependencies listed in a `requirements.txt` file using `pip`. The `-r` flag specifies the file containing the list of packages, ensuring all necessary libraries for the FastAPI application are installed.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_2

LANGUAGE: console
CODE:

```
$ pip install -r requirements.txt
---> 100%
Successfully installed fastapi pydantic
```

---

TITLE: Example .env File Configuration (Bash)
DESCRIPTION: This snippet shows an example of a .env file, which is used to store environment variables. These variables can then be loaded by applications, typically for configuration purposes. It defines ADMIN_EMAIL and APP_NAME.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_8

LANGUAGE: Bash
CODE:

```
ADMIN_EMAIL="deadpool@example.com"
APP_NAME="ChimichangApp"
```

---

TITLE: Defining List Query Parameter in FastAPI
DESCRIPTION: This snippet demonstrates how to define a query parameter `q` in FastAPI that can accept multiple values, which are then collected into a Python `list`. It explicitly uses `Query` to ensure correct interpretation, allowing URLs like `?q=foo&q=bar` to be parsed into `['foo', 'bar']`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_16

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: list[str] | None = Query(default=None)):
    results = {"q": q}
    return results
```

---

TITLE: Using a Nested Pydantic Submodel as an Attribute
DESCRIPTION: This snippet shows how to use a previously defined Pydantic model (e.g., `Image`) as the type for an attribute within another model. This allows for deeply nested JSON structures, with FastAPI providing automatic validation and documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md#_snippet_7

LANGUAGE: Python
CODE:

```
image: Image
```

---

TITLE: Defining Startup and Shutdown Logic in FastAPI Lifespan (Core)
DESCRIPTION: This snippet illustrates the core logic within an async context manager for FastAPI's lifespan events. Code before `yield` runs on application startup (e.g., loading an ML model), and code after `yield` runs on shutdown (e.g., clearing resources). This ensures resources are managed once for the entire application lifecycle.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/events.md#_snippet_0

LANGUAGE: Python
CODE:

```
ml_models["regression_model"] = RegressionModel()
yield
# Clean up the ML models
ml_models.clear()
```

---

TITLE: Declaring Pydantic v2 Model Examples for JSON Schema
DESCRIPTION: This snippet demonstrates how to add example data to a Pydantic v2 model's JSON Schema using the `model_config` attribute. The `json_schema_extra` dictionary, specifically its `examples` key, allows embedding sample data that will appear in the generated OpenAPI documentation, providing clear examples for API consumers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Annotated[str | None, Field(examples=["A very long description"])] = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
```

---

TITLE: Adding a Background Task to a FastAPI Path Operation
DESCRIPTION: This snippet shows how to add a previously defined task function (`write_notification`) to the `background_tasks` object within a FastAPI path operation. The `.add_task()` method accepts the task function, followed by its positional and keyword arguments.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/background-tasks.md#_snippet_2

LANGUAGE: Python
CODE:

```
    background_tasks.add_task(write_notification, email, message="some notification")
```

---

TITLE: Declaring OAuth2 Security Scheme with Scopes in FastAPI
DESCRIPTION: This snippet shows how to define an OAuth2 security scheme using `OAuth2PasswordBearer` and explicitly declare available scopes. The `scopes` parameter is a dictionary where keys are scope names (e.g., 'me', 'items') and values are their descriptions. These declared scopes will be visible in the OpenAPI documentation (e.g., Swagger UI) for users to select during authorization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/security/oauth2-scopes.md#_snippet_1

LANGUAGE: Python
CODE:

```
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items."
    }
)
```

---

TITLE: Building a Docker Image for FastAPI
DESCRIPTION: This Dockerfile defines the steps to build a Docker image for the FastAPI application. It starts from a Python 3.9 base image, sets the working directory, copies the `requirements.txt` file, installs dependencies, and then copies the application code. This multi-stage approach optimizes image size and build time.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_4

LANGUAGE: dockerfile
CODE:

```
# (1)!
FROM python:3.9

# (2)!
WORKDIR /code

# (3)!
COPY ./requirements.txt /code/requirements.txt

# (4)!
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (5)!
COPY ./app /code/app
```

---

TITLE: Creating a Hero with HeroCreate and Returning HeroPublic in FastAPI
DESCRIPTION: This FastAPI endpoint handles the creation of new heroes. It accepts a `HeroCreate` model for input validation and uses `response_model=HeroPublic` to ensure the returned data is validated and serialized according to the public model, even though the internal `Hero` table model is returned.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_15

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter
from sqlmodel import Session, select
from typing import List

# Assuming Hero, HeroCreate, HeroPublic are defined
# class Hero(HeroBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)

router = APIRouter()

@router.post("/heroes/", response_model=HeroPublic)
def create_hero(*, session: Session, hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

---

TITLE: Reading a Single Hero with HeroPublic in FastAPI
DESCRIPTION: This FastAPI endpoint retrieves a single hero by its ID. It uses `response_model=HeroPublic` to ensure the returned hero object is validated and serialized according to the public data model, raising an HTTP 404 error if the hero is not found.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_17

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

# Assuming Hero, HeroPublic are defined
router = APIRouter()

@router.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(*, session: Session, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

---

TITLE: Deleting a Hero by ID in FastAPI
DESCRIPTION: This FastAPI endpoint handles the deletion of a `Hero` entry by its ID. It retrieves the hero, raises a 404 error if not found, deletes it from the session, commits the change, and returns a success message or the deleted hero's ID.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_9

LANGUAGE: Python
CODE:

```
@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: SessionDep, hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
```

---

TITLE: Implementing Process Time Header in FastAPI Middleware
DESCRIPTION: This snippet demonstrates a complete FastAPI HTTP middleware that measures the request processing time and adds it as a custom `X-Process-Time` header to the response. It utilizes `time.perf_counter()` for precise timing, capturing the time before and after the `call_next` function, and then modifies the `response` headers before returning it.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/middleware.md#_snippet_1

LANGUAGE: Python
CODE:

```
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

TITLE: Configuring APIRouter for Items
DESCRIPTION: Demonstrates configuring an `APIRouter` instance in `app/routers/items.py` for item-related path operations. It sets a common `prefix` (`/items`), `tags` (`items`), a required `dependencies` list (using the `get_token` dependency), and default `responses` for all included routes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/bigger-applications.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "description": "The Foo description"}

```

---

TITLE: Using UserIn Model for Both Request and Response
DESCRIPTION: This snippet demonstrates using the `UserIn` Pydantic model for both the request body and the `response_model` in a FastAPI POST endpoint. While convenient, this approach can inadvertently return sensitive data like plaintext passwords in the API response, posing a security risk if not handled carefully.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user
```

---

TITLE: FastAPI OAuth2 Password Flow Initial Setup
DESCRIPTION: This complete example demonstrates the foundational setup for implementing OAuth2 password flow in FastAPI. It defines the OAuth2PasswordBearer scheme with a tokenUrl and protects a path operation, automatically generating OpenAPI documentation for authentication. Requires python-multipart for form data parsing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/first-steps.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

---

TITLE: Running FastAPI Application with Uvicorn (Python)
DESCRIPTION: This snippet demonstrates how to run a FastAPI application using Uvicorn directly from a Python script. It initializes a FastAPI app and starts the Uvicorn server, making the application accessible on the specified host and port, typically within an `if __name__ == "__main__":` block.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/debugging.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

TITLE: Overriding a Specific Dependency in FastAPI
DESCRIPTION: This snippet demonstrates how to replace a specific dependency with a mock or test-specific implementation using `app.dependency_overrides`. It maps the original dependency function (e.g., `get_numeric_auth_service`) to its test override (e.g., `mock_numeric_auth_service`), allowing isolated testing without external service calls.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/testing-dependencies.md#_snippet_0

LANGUAGE: Python
CODE:

```
app.dependency_overrides[get_numeric_auth_service] = mock_numeric_auth_service
```

---

TITLE: Running FastAPI Development Server
DESCRIPTION: This command starts the FastAPI development server using `fastapi dev`, pointing to `tutorial001.py`. It shows the server running on `http://127.0.0.1:8000` and confirms that the documentation on port `8008` will not conflict.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/contributing.md#_snippet_6

LANGUAGE: console
CODE:

```
$ fastapi dev tutorial001.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

TITLE: Running FastAPI Development Server
DESCRIPTION: This command starts the FastAPI development server using `fastapi dev`. It automatically reloads the application on code changes and provides URLs for the application and its interactive documentation. The server runs on `http://127.0.0.1:8000` by default.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_1

LANGUAGE: console
CODE:

```
$ fastapi dev main.py
```

---

TITLE: Installing Python Dependencies in Dockerfile
DESCRIPTION: This `RUN` instruction installs the Python dependencies listed in `/code/requirements.txt` using pip. The `--no-cache-dir` flag prevents pip from storing downloaded packages in a cache, and `--upgrade` ensures packages are upgraded if already installed. This step benefits from Docker's build cache if `requirements.txt` hasn't changed.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_8

LANGUAGE: Dockerfile
CODE:

```
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

---

TITLE: Defining Path Operations using FastAPI APIRouter
DESCRIPTION: This example demonstrates how to define multiple path operations (GET requests in this case) using the APIRouter instance. Each operation is associated with a specific path and can include tags for documentation purposes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

---

TITLE: Mixed Required, Default, and Optional Query Parameters - FastAPI Python
DESCRIPTION: This example illustrates the flexibility of FastAPI in handling a mix of query parameter types: `needy` is required, `skip` has a default value, and `limit` is optional. This allows for robust API design accommodating various input requirements.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

---

TITLE: Defining OAuth2PasswordBearer Scheme
DESCRIPTION: This line initializes OAuth2PasswordBearer, specifying the relative tokenUrl where clients should send credentials to obtain an access token. This configuration is crucial for FastAPI to generate the correct OpenAPI security scheme documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/first-steps.md#_snippet_2

LANGUAGE: Python
CODE:

```
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

---

TITLE: Running FastAPI Application with Uvicorn
DESCRIPTION: This command starts the FastAPI application using Uvicorn, enabling hot-reloading for development. It specifies `main` as the module and `app` as the FastAPI instance to run.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/websockets.md#_snippet_4

LANGUAGE: console
CODE:

```
$ uvicorn main:app --reload
```

---

TITLE: Including User and Item APIRouters - Python
DESCRIPTION: Includes the APIRouter instances from the imported 'users' and 'items' modules into the main FastAPI application using `app.include_router()`, making their routes part of the main app.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/pt/docs/tutorial/bigger-applications.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

from .routers import items, users

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
```

---

TITLE: Updating Pydantic Model with update Parameter (Python)
DESCRIPTION: This snippet shows how to create an updated copy of an existing Pydantic model using `model_copy(update=...)` (or `.copy()` in Pydantic v1). The `update_data` dictionary, typically generated using `exclude_unset`, is merged into the `stored_item_model`, applying only the specified partial changes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-updates.md#_snippet_3

LANGUAGE: Python
CODE:

```
updated_item = stored_item_model.model_copy(update=update_data)
```

---

TITLE: FastAPI Application Python Dependencies (requirements.txt)
DESCRIPTION: An example `requirements.txt` file specifying the required Python packages and their version constraints for a FastAPI application, including `fastapi`, `pydantic`, and `uvicorn`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/deployment/docker.md#_snippet_1

LANGUAGE: text
CODE:

```
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
```

---

TITLE: Declaring Union Response Model in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to define a FastAPI endpoint that can return a response conforming to one of several Pydantic models using `typing.Union`. The `response_model` argument is set to `Union[PlaneItem, CarItem]`, allowing the API to return either a `PlaneItem` or a `CarItem` object. It's crucial to list the more specific type first in the `Union`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_8

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class PlaneItem(BaseModel):
    size: float
    wings: int

class CarItem(BaseModel):
    brand: str
    model: str

app = FastAPI()

@app.get("/items/", response_model=Union[PlaneItem, CarItem])
async def read_items():
    # Example return for PlaneItem
    return {"size": 10.0, "wings": 2}
```

---

TITLE: Defining Settings in a Separate Python Module
DESCRIPTION: This Python snippet illustrates defining the `Settings` class in a dedicated `config.py` file. This modular approach centralizes configuration definitions, improving code organization and reusability across different parts of a larger application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_6

LANGUAGE: Python
CODE:

```
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
```

---

TITLE: Defining HeroCreate Data Model in Python
DESCRIPTION: This snippet defines the `HeroCreate` Pydantic model, used for validating data received when creating a new hero. It includes the `secret_name` field, which is accepted during creation but not exposed in public responses.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_13

LANGUAGE: Python
CODE:

```
from typing import Optional
from sqlmodel import Field, SQLModel

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

class HeroCreate(HeroBase):
    secret_name: str
```

---

TITLE: Accessing Pydantic Settings in FastAPI Endpoint
DESCRIPTION: This Python code demonstrates how to access the instantiated `settings` object within a FastAPI endpoint. The endpoint retrieves and returns configured values like `app_name`, `admin_email`, and `items_per_user`, showcasing runtime configuration usage.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_4

LANGUAGE: Python
CODE:

```
@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }
```

---

TITLE: Defining Path Operation with Extra Data Types in FastAPI
DESCRIPTION: This snippet defines a FastAPI path operation `/items/{item_id}` that accepts various extra data types as parameters, including UUID, datetime, date, time, and timedelta. These types are automatically validated and converted by FastAPI, leveraging Pydantic's capabilities, and are returned as part of a dictionary.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-data-types.md#_snippet_0

LANGUAGE: Python
CODE:

```
from datetime import datetime, date, time, timedelta
from uuid import UUID

from fastapi import FastAPI, Body

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime | None = Body(default=None),
    end_date: date | None = Body(default=None),
    repeat_at: time | None = Body(default=None),
    process_after: timedelta | None = Body(default=None),
):
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
    }
```

---

TITLE: Defining a Class-Based Dependency
DESCRIPTION: This snippet defines the `CommonQueryParams` class, designed to encapsulate common query parameters for FastAPI dependencies. Its `__init__` method accepts `q`, `skip`, and `limit` as arguments, which FastAPI automatically populates from the request. This class acts as a callable, allowing its instance to be injected into path operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_4

LANGUAGE: Python
CODE:

```
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
```

---

TITLE: Running Uvicorn with Inline Environment Variables for Pydantic Settings
DESCRIPTION: This command demonstrates how to launch a FastAPI application using Uvicorn while simultaneously setting environment variables (`ADMIN_EMAIL`, `APP_NAME`) inline. Pydantic's `BaseSettings` will automatically detect and load these variables, configuring the application at runtime without modifying code.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_7

LANGUAGE: console
CODE:

```
$ ADMIN_EMAIL="deadpool@example.com" APP_NAME="ChimichangApp" uvicorn main:app
<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

TITLE: Declaring Class Type Hints
DESCRIPTION: Demonstrates how to use custom classes as type hints for function parameters. This allows for strong type checking and improved code readability when working with object-oriented structures. The example defines a `Person` class and a function that expects a `Person` instance.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_15

LANGUAGE: Python
CODE:

```
class Person:
    def __init__(self, name: str):
        self.name = name

def introduce_person(person: Person):
    print(f"This person's name is {person.name}.")
```

---

TITLE: Managing Database Connections with FastAPI `yield` Dependencies
DESCRIPTION: This snippet demonstrates how to manage a database connection using a FastAPI dependency with `yield`. The code before `yield` establishes the connection, which is then provided to path operations. The code in the `finally` block after `yield` ensures the connection is properly closed, even if errors occur during the request processing, making it suitable for resource management.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_0

LANGUAGE: Python
CODE:

```
def get_database():
    # Assume connect_to_db() returns a database connection object
    db = connect_to_db()
    try:
        yield db
    finally:
        # This code runs after the response has been delivered
        db.close()
```

---

TITLE: Declare Complex Model Parameter in FastAPI
DESCRIPTION: Shows how to declare a complex request body or parameter `item` using a custom `Item` model. This leverages Pydantic for automatic data validation, serialization, and interactive API documentation in FastAPI.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_7

LANGUAGE: Python
CODE:

```
item: Item
```

---

TITLE: Basic Dockerfile for FastAPI with Uvicorn/Gunicorn
DESCRIPTION: This Dockerfile provides a basic setup for a FastAPI application using the `tiangolo/uvicorn-gunicorn-fastapi` base image. It copies `requirements.txt`, installs dependencies, and then copies the application code into the `/app` directory. This is suitable for standard FastAPI projects.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_15

LANGUAGE: Dockerfile
CODE:

```
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
```

---

TITLE: Chaining and Nesting FastAPI `yield` Dependencies
DESCRIPTION: This example illustrates how to create a chain of nested dependencies where each dependency uses `yield`. FastAPI ensures that the setup code for each dependency runs in the correct order (e.g., A then B then C), and their respective cleanup code (after `yield`) is executed in reverse order (e.g., C then B then A), allowing for complex resource management flows across multiple layers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import Depends

def dependency_a():
    print("Running dependency_a setup")
    yield "a_value"
    print("Running dependency_a cleanup")

def dependency_b(dep_a: str = Depends(dependency_a)):
    print(f"Running dependency_b setup with {dep_a}")
    yield f"b_value_from_{dep_a}"
    print(f"Running dependency_b cleanup for {dep_a}")

def dependency_c(dep_b: str = Depends(dependency_b)):
    print(f"Running dependency_c setup with {dep_b}")
    yield f"c_value_from_{dep_b}"
    print(f"Running dependency_c cleanup for {dep_b}")
```

---

TITLE: Defining a Dependency Function in FastAPI
DESCRIPTION: This Python function serves as a dependency, accepting parameters like `q`, `skip`, and `limit`. It processes these inputs and returns a dictionary containing their values, which can then be injected into FastAPI path operations. It demonstrates how a dependency function can take arguments similar to path operation functions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/index.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Optional

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
```

---

TITLE: Defining an Optional Query Parameter in FastAPI
DESCRIPTION: This snippet demonstrates how to define an optional query parameter `q` in a FastAPI path operation. By setting its type hint to `str | None` and its default value to `None`, FastAPI automatically recognizes it as optional, allowing requests to be made without providing this parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(q: str | None = None):
    if q:
        return {"q": q}
    return {"message": "No q parameter"}
```

---

TITLE: Pinning Exact FastAPI Version
DESCRIPTION: This snippet shows how to pin an exact version of FastAPI (e.g., `0.45.0`) in a `requirements.txt` file. This practice ensures that your application consistently uses a specific, tested version, preventing unexpected behavior from newer, potentially breaking, releases.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/versions.md#_snippet_0

LANGUAGE: txt
CODE:

```
fastapi==0.45.0
```

---

TITLE: Defining Python Dependencies in requirements.txt
DESCRIPTION: This snippet defines the required Python packages and their version constraints for a FastAPI application. It specifies `fastapi[standard]` and `pydantic`, ensuring compatibility and stability by setting precise version ranges. This file is typically used by `pip` to install project dependencies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_1

LANGUAGE: Text
CODE:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

---

TITLE: Declaring Typed Path Parameters in FastAPI
DESCRIPTION: This example shows how to add a type annotation (`int`) to a path parameter in FastAPI. This enables automatic data conversion from the URL string to a Python integer, providing type safety and better editor support.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

---

TITLE: Including and Excluding Fields in FastAPI Response Model
DESCRIPTION: This snippet demonstrates `response_model_include` and `response_model_exclude` parameters. `response_model_include` specifies a set of fields to include, omitting all others. `response_model_exclude` specifies a set of fields to exclude, including all others. These parameters offer fine-grained control over the response payload, though using separate Pydantic models for input/output is generally recommended for clearer OpenAPI documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_8

LANGUAGE: Python
CODE:

```
from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

app = FastAPI()

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}

@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item_name(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public(item_id: str):
    return items[item_id]
```

---

TITLE: Updating a Hero with HeroUpdate in FastAPI
DESCRIPTION: This FastAPI endpoint handles partial updates of a hero using an HTTP PATCH operation. It accepts a `HeroUpdate` model, extracts only the fields that were explicitly set by the client using `exclude_unset=True`, and applies these changes to the existing hero record in the database.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_18

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

# Assuming Hero, HeroUpdate, HeroPublic are defined
router = APIRouter()

@router.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(*, session: Session, hero_id: int, hero: HeroUpdate):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

---

TITLE: Mounting Sub-Application to Main FastAPI App
DESCRIPTION: This snippet demonstrates how to integrate an independent FastAPI sub-application (subapi) into the main application (app) using app.mount(). The sub-application is mounted at the /subapi path, making its routes accessible under this prefix. This operation requires both the main app and the subapi instances to be defined and imported from fastapi.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()
subapi = FastAPI()

app.mount("/subapi", subapi)
```

---

TITLE: Defining an Asynchronous Function with `async def` in Python
DESCRIPTION: This code illustrates how to define an asynchronous function using the `async def` syntax. Functions declared with `async def` are 'awaitable' and can contain `await` expressions, making them suitable for I/O-bound operations where the function can yield control while waiting for external resources.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_4

LANGUAGE: Python
CODE:

```
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

---

TITLE: Defining Independent FastAPI Sub-Application
DESCRIPTION: This snippet creates an independent FastAPI application instance (subapi) that is designed to be mounted within a larger application. It includes a basic path operation at /sub specific to this sub-application. This instance functions as a standalone FastAPI app before integration.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/sub-applications.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

subapi = FastAPI()

@subapi.get("/sub")
async def read_sub():
    return {"message": "Hello from sub app"}
```

---

TITLE: Declaring Response Model in FastAPI Post Endpoint
DESCRIPTION: This snippet demonstrates how to declare a `response_model` for a FastAPI POST endpoint. The `response_model` parameter in the `@app.post()` decorator ensures that the output data is transformed, validated, and documented according to the `Item` Pydantic model, even if the function returns the input item directly.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

---

TITLE: Combining Multiple Body and Query Parameters in FastAPI
DESCRIPTION: Demonstrates how to define a FastAPI path operation that accepts multiple body parameters (Pydantic models and singular values using `Body()`) along with an optional query parameter. FastAPI automatically distinguishes between body and query parameters based on their declaration.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-multiple-params.md#_snippet_7

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(gt=0),
    q: Union[str, None] = None,
):
    results = {"item_id": item_id, "item": item.dict(), "user": user.dict(), "importance": importance}
    if q:
        results.update({"q": q})
    return results
```

---

TITLE: Defining a Custom Dependency Function in FastAPI
DESCRIPTION: This snippet shows how to create a reusable dependency function that reads a custom header (X-Token). It uses fastapi.Header to extract the header value and raises an HTTPException if the token is invalid, enforcing authentication or validation logic.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import Header, HTTPException

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
```

---

TITLE: Creating Database Tables on FastAPI Startup
DESCRIPTION: This snippet demonstrates how to automatically create all defined database tables when the FastAPI application starts. It uses the `on_event('startup')` decorator to execute `SQLModel.metadata.create_all(engine)`, ensuring the database schema is ready before handling requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_5

LANGUAGE: Python
CODE:

```
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

---

TITLE: Initializing OAuth2 Password Bearer in FastAPI
DESCRIPTION: This snippet initializes a FastAPI application and configures OAuth2 security using `OAuth2PasswordBearer`. It defines a dependency that expects a token from the client, enabling the automatic generation of an 'Authorize' button in the interactive API documentation (Swagger UI) and enforcing authentication for protected endpoints. The `tokenUrl` parameter specifies the endpoint where the client should send username and password to obtain a token.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/first-steps.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

---

TITLE: Upgrading FastAPI with Pydantic Model and PUT Request
DESCRIPTION: This snippet extends the FastAPI application by introducing a Pydantic `BaseModel` to define the structure of a request body. It adds a `PUT` endpoint that accepts an `item_id` path parameter and an `Item` object as a request body, demonstrating how to handle structured input.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_7

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

---

TITLE: Building a Docker Image with Multiple Uvicorn Workers
DESCRIPTION: This Dockerfile builds an image for a FastAPI application, configuring Uvicorn to run with multiple worker processes. It copies application dependencies and source code, then uses the `CMD` instruction to start the FastAPI application via `fastapi run` with the `--workers` option set to 4. This setup is suitable for single-server deployments or Docker Compose where cluster-level replication is not managed externally.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_17

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# (1)!
CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

---

TITLE: Initialize FastAPI App with Global Dependencies
DESCRIPTION: Demonstrates importing the FastAPI class and creating an application instance. It shows how to declare global dependencies that will be applied to all path operations in the application, including those defined in included APIRouters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_13

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends

# Assume get_query_token is a dependency function
async def get_query_token(token: str):
    ...

app = FastAPI(dependencies=[Depends(get_query_token)])
```

---

TITLE: Applying Global Dependencies to FastAPI Application - Python
DESCRIPTION: This snippet demonstrates how to add a global dependency to a FastAPI application by passing a list of `Depends` objects to the `FastAPI` constructor. These dependencies will be automatically applied to all path operations defined within the application, ensuring consistent behavior like authentication or common parameter handling across the entire API.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/global-dependencies.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends

# Define a common dependency function
async def get_query_token(token: str):
    if token != "jessica":
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return token

# Initialize FastAPI application with a global dependency
app = FastAPI(dependencies=[Depends(get_query_token)])

@app.get("/items/")
async def read_items():
    return {"message": "This endpoint requires the global dependency"}

@app.get("/users/")
async def read_users():
    return {"message": "So does this one!"}
```

---

TITLE: Dockerfile for Single-File FastAPI Application (Dockerfile)
DESCRIPTION: This Dockerfile is configured for a FastAPI application structured as a single `main.py` file. It sets the base image to `python:3.9`, defines the working directory, copies `requirements.txt` and installs dependencies, and finally copies the `main.py` file into the `/code/` directory. The highlighted lines indicate the specific changes for a single-file setup.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_15

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)!
COPY ./main.py /code/
```

---

TITLE: Declaring a Simple Required Query Parameter in FastAPI
DESCRIPTION: This snippet demonstrates the basic syntax for declaring a required query parameter in FastAPI. By simply type-hinting the parameter without assigning a default value, it becomes mandatory for clients to provide this parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_14

LANGUAGE: Python
CODE:

```
q: str
```

---

TITLE: Integrating BackgroundTasks with FastAPI Dependencies
DESCRIPTION: This snippet illustrates how `BackgroundTasks` can be used within FastAPI's dependency injection system. It shows a dependency function (`get_query_background_tasks`) that adds a task based on a query parameter, and how this dependency is injected into a path operation, which then adds another background task.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/background-tasks.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, BackgroundTasks, Depends

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message + "\n")

def get_query_background_tasks(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"query: {q}")
    return background_tasks

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks = Depends(get_query_background_tasks),
):
    background_tasks.add_task(write_log, f"message for {email}")
    return {"message": "Notification sent in the background"}
```

---

TITLE: Testing WebSocket Connections with FastAPI TestClient (Python)
DESCRIPTION: This snippet demonstrates how to establish and test a WebSocket connection using FastAPI's `TestClient`. It utilizes a `with` statement to manage the WebSocket session, allowing for sending and receiving data, and asserting expected responses. This method ensures proper connection handling and cleanup.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/testing-websockets.md#_snippet_0

LANGUAGE: Python
CODE:

```
with client.websocket_connect("/ws") as websocket:
    data = websocket.receive_json()
    assert data == {"msg": "Hello WebSocket"}
```

---

TITLE: Creating a Virtual Environment with venv (Shell)
DESCRIPTION: This command initializes a new Python virtual environment using the built-in `venv` module. It creates a `.venv` directory within the current project, which will contain an isolated Python interpreter and its own set of installed packages. This should be done once per project to ensure dependency isolation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_1

LANGUAGE: Shell
CODE:

```
$ python -m venv .venv
```

---

TITLE: Updating Item with PUT in FastAPI (Python)
DESCRIPTION: This snippet defines a FastAPI `PUT` endpoint to fully replace an existing item. It uses `jsonable_encoder` to convert the incoming Pydantic model data into a JSON-compatible format suitable for storage, ensuring types like `datetime` are properly serialized. The entire existing item is replaced with the new data provided in the request body.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-updates.md#_snippet_0

LANGUAGE: Python
CODE:

```
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded
```

---

TITLE: Installing FastAPI Standard Dependencies
DESCRIPTION: This command installs FastAPI with its standard set of dependencies. This approach is often preferred for production deployments to minimize the installed footprint by including only essential packages.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/index.md#_snippet_2

LANGUAGE: Shell
CODE:

```
pip install "fastapi[standard]"
```

---

TITLE: Resetting All Dependency Overrides in FastAPI
DESCRIPTION: This snippet shows how to clear all active dependency overrides in a FastAPI application. By setting `app.dependency_overrides` to an empty dictionary, all previously configured overrides are removed, restoring the application's default dependency behavior.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/testing-dependencies.md#_snippet_1

LANGUAGE: Python
CODE:

```
app.dependency_overrides = {}
```

---

TITLE: Declaring FastAPI Class Dependency (Annotated, Shortcut)
DESCRIPTION: This snippet illustrates FastAPI's shortcut for declaring class-based dependencies with `Annotated`. When the parameter's type hint is the dependency class, `Depends()` can be called without arguments, making the declaration more concise and eliminating repetition.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_10

LANGUAGE: Python
CODE:

```
commons: Annotated[CommonQueryParams, Depends()]
```

---

TITLE: Copying Requirements File for Docker Cache (Dockerfile)
DESCRIPTION: This Dockerfile instruction copies the `requirements.txt` file into the `/code/requirements.txt` path within the Docker image. This is a crucial step for Docker's build cache optimization, ensuring that the dependency installation step can leverage the cache if `requirements.txt` hasn't changed, saving significant build time.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_9

LANGUAGE: Dockerfile
CODE:

```
COPY ./requirements.txt /code/requirements.txt
```

---

TITLE: Copying Application Code to Docker Image (Dockerfile)
DESCRIPTION: This Dockerfile instruction copies the entire `./app` directory from the build context into the `/code/app` directory within the Docker image. This step is placed near the end of the Dockerfile because application code changes frequently, and placing it later minimizes cache invalidation for preceding layers (like dependency installation).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_11

LANGUAGE: Dockerfile
CODE:

```
COPY ./app /code/app
```

---

TITLE: Defining User Input Model with Plaintext Password
DESCRIPTION: This Pydantic model, `UserIn`, defines the structure for user input, including a `password` field as a plain string. While suitable for input, using this same model as a `response_model` (as shown in the subsequent snippet) would expose the password in the API response, which is a security vulnerability.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    password: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

app = FastAPI()

@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):
    return user
```

---

TITLE: Main Application File Structure - Python
DESCRIPTION: Shows the basic structure of the main application file ('app/main.py') for a larger FastAPI project. It includes importing the 'FastAPI' class and importing the router modules ('items', 'users') from the 'app.routers' package to avoid name collisions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_6

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from app.dependencies import get_token_header

from app.routers import items, users
from app.internal import admin

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

TITLE: Importing BaseModel for Request Body Definition - Python
DESCRIPTION: This snippet demonstrates how to import `BaseModel` from the Pydantic library, which is the foundational class for defining data models used in FastAPI request bodies. It's a prerequisite for creating structured data schemas.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body.md#_snippet_0

LANGUAGE: Python
CODE:

```
from pydantic import BaseModel
```

---

TITLE: Defining X-Token Dependency (Python 3.8+ Annotated)
DESCRIPTION: Defines a dependency function `get_token` that reads the `X-Token` header from the request using `Annotated` for type hints. It raises an `HTTPException` if the header value is not 'fake-super-secret-token'. This version uses `Header` without parentheses.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import Header, HTTPException


async def get_token(x_token: Annotated[str, Header]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
```

---

TITLE: Importing HTTPException in FastAPI
DESCRIPTION: This snippet demonstrates how to import the `HTTPException` class from the `fastapi` module. `HTTPException` is essential for raising HTTP-specific errors within FastAPI applications, allowing for custom status codes and detail messages.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, HTTPException
```

---

TITLE: Declaring List Body Parameters in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to declare a function parameter in FastAPI to expect a JSON body that is a list of Pydantic models. It shows both `List[Image]` for older Python versions and `list[Image]` for Python 3.9 and above, providing strong type hints for editor support and validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md#_snippet_13

LANGUAGE: Python
CODE:

```
images: List[Image]
```

LANGUAGE: Python
CODE:

```
images: list[Image]
```

---

TITLE: Items APIRouter Module - Python
DESCRIPTION: Defines a simple APIRouter for item-related routes. This module is intended to be imported and included in the main application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/pt/docs/tutorial/bigger-applications.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter

router = APIRouter()

@router.get("/items/")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}]
```

---

TITLE: Initializing SQL Database Tables
DESCRIPTION: This Python function, 'create_db_and_tables', uses 'SQLModel.metadata.create_all(engine)' to generate all defined database tables. It iterates through all SQLModel table classes (like 'Hero') and creates their corresponding tables in the database connected via the provided engine, ensuring the database schema matches the application's models.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_3

LANGUAGE: python
CODE:

```
from sqlmodel import SQLModel

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

---

TITLE: Running FastAPI in Development Mode with CLI
DESCRIPTION: This snippet demonstrates how to start a FastAPI application in development mode using the `fastapi dev` command. It shows the console output, including server startup details, documentation links, and the auto-reload feature. This mode is suitable for development due to auto-reloading and listening on localhost.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/fastapi-cli.md#_snippet_0

LANGUAGE: Shell
CODE:

```
$ fastapi dev main.py

  FastAPI   Starting development server 🚀

             Searching for package file structure from directories with
             __init__.py files
             Importing from /home/user/code/awesomeapp

    module   🐍 main.py

      code   Importing the FastAPI app object from the module with the
             following code:

             from main import app

       app   Using import string: main:app

    server   Server started at http://127.0.0.1:8000
    server   Documentation at http://127.0.0.1:8000/docs

       tip   Running in development mode, for production use:
             fastapi run

             Logs:

      INFO   Will watch for changes in these directories:
             ['/home/user/code/awesomeapp']
      INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to
             quit)
      INFO   Started reloader process [383138] using WatchFiles
      INFO   Started server process [383153]
      INFO   Waiting for application startup.
      INFO   Application startup complete.
```

---

TITLE: Incorrectly Calling an Asynchronous Function
DESCRIPTION: Highlights an incorrect attempt to call an `async def` function (`get_burgers`) without using the `await` keyword. Asynchronous functions must be awaited to ensure proper execution within an `async` context.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_6

LANGUAGE: Python
CODE:

```
# This won't work, because get_burgers was defined with: async def
burgers = get_burgers(2)
```

---

TITLE: Handling Multiple Status Codes with JSONResponse in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to return different HTTP status codes (e.g., 200 OK, 201 Created) from a single FastAPI path operation. It achieves this by directly returning a `JSONResponse` object, allowing explicit control over the `status_code` and response content. This is useful for 'upsert' operations where an item might be updated if it exists or created if it does not.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/additional-status-codes.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# In a real application, this would typically be a database or persistent storage
items_db = {}

@app.put("/items/{item_id}")
async def update_item(item_id: str, item_data: dict):
    """
    Updates an existing item or creates a new one if it doesn't exist.
    Returns 200 OK if updated, 201 Created if new.
    """
    if item_id not in items_db:
        items_db[item_id] = item_data
        return JSONResponse(
            status_code=201,
            content={
                "message": "Item created",
                "item_id": item_id,
                "item": item_data
            }
        )
    else:
        items_db[item_id].update(item_data)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Item updated",
                "item_id": item_id,
                "item": items_db[item_id]
            }
        )

```

---

TITLE: Declaring Union Types in Python
DESCRIPTION: Demonstrates how to declare a variable that can accept multiple data types. For Python 3.6+, `typing.Union` is used. For Python 3.10+, the `|` operator provides a more concise syntax for union types. This ensures type checking allows for different valid inputs.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_11

LANGUAGE: Python
CODE:

```
from typing import Union

def process_item(item: Union[int, str]):
    if isinstance(item, int):
        return f"Integer: {item}"
    else:
        return f"String: {item.upper()}"
```

LANGUAGE: Python
CODE:

```
def process_item_py310(item: int | str):
    if isinstance(item, int):
        return f"Integer: {item}"
    else:
        return f"String: {item.upper()}"
```

---

TITLE: Setting FastAPI Application Command (Exec Form)
DESCRIPTION: Configures the Docker container to run the FastAPI application using `fastapi run` on port 80. This uses the recommended exec form for the `CMD` instruction, ensuring graceful shutdown and proper lifespan event handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_5

LANGUAGE: Dockerfile
CODE:

```
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

---

TITLE: Setting a Dependency Override in FastAPI for Testing
DESCRIPTION: This snippet demonstrates how to set a dependency override in a FastAPI application. It assigns a new override function to an original dependency within the `app.dependency_overrides` dictionary, ensuring the override is used instead of the original during tests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/testing-dependencies.md#_snippet_0

LANGUAGE: Python
CODE:

```
app.dependency_overrides[original_dependency_function] = override_dependency_function
```

---

TITLE: Importing Query and Annotated for FastAPI Validation
DESCRIPTION: This snippet shows the necessary imports for adding advanced validation to FastAPI parameters. It imports `Annotated` from `typing` for type hint metadata and `Query` from `fastapi` to define query parameter-specific validations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Annotated
from fastapi import FastAPI, Query
```

---

TITLE: Declaring Single Body Example in FastAPI
DESCRIPTION: This snippet shows how to provide a single example for a request body in a FastAPI path operation using the `Body()` function's `examples` parameter. The example, defined as a list containing a dictionary, is embedded directly into the generated JSON Schema for the request body, making it visible in the API documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Annotated[str | None, Field(examples=["A very long description"])] = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

---

TITLE: Creating a Virtual Environment with uv (Shell)
DESCRIPTION: This command uses the `uv` tool to create a new Python virtual environment. By default, `uv` creates the environment in a `.venv` directory, providing an alternative to the standard `venv` module for environment management. This is a quick way to set up an isolated environment if `uv` is already installed.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_2

LANGUAGE: Shell
CODE:

```
$ uv venv
```

---

TITLE: Defining GET Path Operation Decorator - FastAPI Python
DESCRIPTION: This snippet illustrates the `@app.get()` decorator used in FastAPI to define a path operation for handling HTTP GET requests. It maps the root path '/' to a Python function, indicating that the decorated function will be executed when a GET request is made to this URL.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_8

LANGUAGE: Python
CODE:

```
@app.get("/\")
```

---

TITLE: Declaring Query Parameters with Pydantic Model in FastAPI
DESCRIPTION: This snippet demonstrates how to define a group of related query parameters using a Pydantic `BaseModel`. Each field in the model corresponds to a query parameter, allowing for type validation, default values, and additional metadata. The model is then injected into a FastAPI path operation using `Query()`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-param-models.md#_snippet_0

LANGUAGE: python
CODE:

```
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class CommonQueryParams(BaseModel):
    q: Optional[str] = None
    skip: int = 0
    limit: int = 100

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Query()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = [{"item_id": "Foo"}, {"item_id": "Bar"}]
    response.update({"items": items[commons.skip : commons.skip + commons.limit]})
    return response
```

---

TITLE: Defining Global Authentication Dependencies (Python)
DESCRIPTION: These asynchronous functions define two global dependencies, `verify_key` and `verify_token`, which validate specific HTTP header values (`X-Key` and `X-Token`). If the headers are missing or invalid, an `HTTPException` is raised, effectively blocking unauthorized requests. Although these functions return values, those values are not passed to the path operation functions when used as global dependencies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md#_snippet_1

LANGUAGE: Python
CODE:

```
async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
```

---

TITLE: Accessing Request Body in Validation Error Handler in FastAPI
DESCRIPTION: This snippet illustrates how to access the invalid request body within a `RequestValidationError` handler. The handler is modified to return a JSON response that includes both the validation error details and the original invalid request body, which is useful for debugging or providing detailed feedback to the user.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_9

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    title: str
    size: int

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body}
    )
```

---

TITLE: Creating a SQLModel Database Engine
DESCRIPTION: This Python code creates a SQLModel engine, which is responsible for managing connections to the SQLite database file 'database.db'. The 'check_same_thread=False' argument is crucial for SQLite when used with FastAPI, allowing multiple threads (e.g., from different requests or dependencies) to safely access the same database connection.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_2

LANGUAGE: python
CODE:

```
from sqlmodel import create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})
```

---

TITLE: Handling Invalid Request Body with Try-Except in FastAPI
DESCRIPTION: This snippet demonstrates how to use a `try-except` block to gracefully handle potential errors when parsing a request body, specifically JSON. If `request.json()` fails (e.g., due to malformed JSON), the `except` block catches the exception, allowing the application to return a custom `JSONResponse` with a 400 Bad Request status, preventing a server error.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/how-to/custom-request-and-route.md#_snippet_2

LANGUAGE: Python
CODE:

```
try:
    body = await request.json()
except Exception:
    response = JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Invalid JSON"},
    )
    return response
```

---

TITLE: Configuring HTTPS Redirect Middleware in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to add the `HTTPSRedirectMiddleware` to a FastAPI application. This middleware automatically redirects all incoming `http` or `ws` requests to their secure `https` or `wss` counterparts, ensuring secure communication. It requires no additional parameters and is typically used to enforce secure connections across the application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/middleware.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
```

---

TITLE: Handling Optional Body Parameters in FastAPI
DESCRIPTION: Demonstrates how to define an optional request body parameter (a Pydantic model `Item`) in a FastAPI path operation by setting its default value to `None`. This allows the API endpoint to receive a request body, but it is not mandatory for the request to be valid. It also shows mixing path and query parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-multiple-params.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Union[Item, None] = None,
    name: Union[str, None] = None,
    description: Union[str, None] = None,
    price: Union[float, None] = None,
    tax: float = Query(None, deprecated=True),
):
    results = {"item_id": item_id}
    if item:
        results.update(item.dict())
    if name:
        results.update({"name": name})
    if description:
        results.update({"description": description})
    if price:
        results.update({"price": price})
    if tax:
        results.update({"tax": tax})
    return results
```

---

TITLE: Recommended Default Value with Annotated and Query in FastAPI
DESCRIPTION: This snippet illustrates the recommended method for setting a default value for a query parameter using `Annotated` and `Query` in FastAPI. The default value is assigned directly to the function parameter, ensuring clarity and consistency with standard Python practices.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_12

LANGUAGE: Python
CODE:

```
q: Annotated[str, Query()] = "rick"
```

---

TITLE: Mounting Static Files with FastAPI
DESCRIPTION: This snippet demonstrates how to mount a directory of static files in a FastAPI application. It imports `StaticFiles` from `fastapi.staticfiles` and uses `app.mount()` to serve files from the 'static' directory under the '/static' URL path. The `name` parameter provides an internal reference.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/static-files.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
```

---

TITLE: Adding Generic ASGI Middleware with FastAPI's add_middleware - Python
DESCRIPTION: Illustrates the recommended way to integrate any ASGI middleware into a FastAPI application using `app.add_middleware()`. This method simplifies middleware setup and ensures proper interaction with FastAPI's internal error handling and exception management.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/middleware.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

---

TITLE: Protecting Endpoint with OAuth2 Dependency
DESCRIPTION: This snippet shows how to secure a path operation by injecting oauth2_scheme as a dependency. FastAPI automatically validates the Authorization header, extracts the bearer token, and passes it to the token parameter, or returns a 401 Unauthorized error if invalid.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/first-steps.md#_snippet_3

LANGUAGE: Python
CODE:

```
@app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
```

---

TITLE: Declaring Optional Types with Union Operator (`|`)
DESCRIPTION: Shows how to declare optional types using the `|` operator, available in Python 3.10 and later, as a more concise alternative to `typing.Optional`. This syntax explicitly states that a parameter can be either the specified type or `None`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_13

LANGUAGE: Python
CODE:

```
from typing import Optional

def greet_optional(name: Optional[str] = None):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, World!")
```

LANGUAGE: Python
CODE:

```
from typing import Optional

def greet_optional_b(name: Optional[str]):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, there!")
```

LANGUAGE: Python
CODE:

```
def greet_optional_py310(name: str | None = None):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, there!")
```

---

TITLE: Integrating BackgroundTasks with Dependency Injection
DESCRIPTION: This example illustrates how `BackgroundTasks` can be integrated with FastAPI's Dependency Injection system. A dependency function (`get_background_tasks_from_dependency`) can receive and add tasks to the `BackgroundTasks` object, which is then passed to the path operation function. This allows multiple parts of the application, including dependencies, to contribute background tasks that are executed after the response is sent.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/background-tasks.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, BackgroundTasks, Depends

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as log:
        log.write(message + "\n")

# Dependency that adds a background task
def get_background_tasks_from_dependency(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "Task added by a dependency.")
    return background_tasks

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks = Depends(get_background_tasks_from_dependency),
    message: str = "some notification"
):
    # This task is added by the path operation function
    background_tasks.add_task(write_log, f"Notification for {email}: {message}")
    return {"message": "Notification sent in the background"}
```

---

TITLE: Adding Description Metadata to Query Parameter (FastAPI)
DESCRIPTION: This snippet shows how to include a detailed `description` for a query parameter using `Query`. This descriptive text is incorporated into the OpenAPI documentation, providing comprehensive information about the parameter's purpose and usage to API consumers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_20

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: str | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
    )
):
    results = {"q": q}
    return results
```

---

TITLE: Installing Python Packages from requirements.txt using pip
DESCRIPTION: Installs all packages listed in the `requirements.txt` file using `pip`. This is the recommended method for managing project dependencies, ensuring consistent environments across different machines and deployments.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_13

LANGUAGE: console
CODE:

```
$ pip install -r requirements.txt
---> 100%
```

---

TITLE: Defining Application Settings with Pydantic - Python
DESCRIPTION: This snippet defines the `Settings` class using Pydantic's `BaseSettings` to manage application configuration. It includes `app_name` and `admin_email` fields. The `get_settings` function, decorated with `@lru_cache`, ensures that the `Settings` object is instantiated only once, optimizing performance for subsequent calls.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_11

LANGUAGE: Python
CODE:

```
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str

@lru_cache
def get_settings():
    return Settings()
```

---

TITLE: Importing Request Parameter Functions in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to import the essential request parameter functions (Body, Cookie, File, Form, Header, Path, Query) directly from the `fastapi` library. These functions are crucial for defining how data is extracted from different parts of an HTTP request within FastAPI path operations or dependencies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/parameters.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import Body, Cookie, File, Form, Header, Path, Query
```

---

TITLE: API Documentation: OAuth2PasswordRequestForm Class
DESCRIPTION: Details the `OAuth2PasswordRequestForm` class dependency used in FastAPI for handling OAuth2 password flow form data, including its expected fields and behavior.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/security/simple-oauth2.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
OAuth2PasswordRequestForm:
  Description: A class dependency for declaring form request bodies in OAuth2 password flow.
  Fields:
    username: string (required)
    password: string (required)
    scope: string (optional, space-separated list of scopes)
    grant_type: string (optional, typically "password")
    client_id: string (optional)
    client_secret: string (optional)
  Notes:
    - The 'scope' field is singular but represents multiple space-separated scopes.
    - 'OAuth2PasswordRequestForm' does not enforce 'grant_type' to be 'password'. Use 'OAuth2PasswordRequestFormStrict' for strict enforcement.
    - This is a standard class dependency, not a special FastAPI class, but provided for convenience due to common use case.
```

---

TITLE: Performing Asynchronous HTTP Requests in Pytest with AsyncClient
DESCRIPTION: This snippet shows how to use `httpx.AsyncClient` within an asynchronous `pytest` function to make requests to a FastAPI application. It demonstrates instantiating `AsyncClient` with the FastAPI `app` object and using `await` to send a GET request and receive the response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/async-tests.md#_snippet_3

LANGUAGE: Python
CODE:

```
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

---

TITLE: Installing FastAPI with Standard Extras using uv
DESCRIPTION: Installs the `fastapi` package and its 'standard' extra dependencies using `uv`'s `pip install` command. `uv` is an alternative installer that can be faster than `pip` and is used similarly for direct package installations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_12

LANGUAGE: console
CODE:

```
$ uv pip install "fastapi[standard]"
---> 100%
```

---

TITLE: Securing Host Headers with TrustedHostMiddleware - Python
DESCRIPTION: Demonstrates how to integrate `TrustedHostMiddleware` to protect against HTTP Host Header attacks by validating the `Host` header of incoming requests against a predefined list of allowed domain names. Requests with invalid host headers will result in a `400 Bad Request` response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/middleware.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
```

---

TITLE: Defining Webhooks in FastAPI
DESCRIPTION: This snippet demonstrates how to define webhooks in a FastAPI application using the `app.webhooks` attribute. It includes a Pydantic model (`WebhookData`) for the webhook payload and two webhook definitions (`new-subscription` and `cancellation`) that receive this payload via a POST request. These definitions will be automatically included in the OpenAPI schema for documentation, making it easier for users to implement their webhook receivers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/openapi-webhooks.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel

class WebhookData(BaseModel):
    message: str
    event_type: Literal["new-subscription", "cancellation"]

app = FastAPI()

@app.webhooks.post("new-subscription")
def new_subscription_webhook(data: WebhookData):
    """
    Receive a new subscription event.
    """
    print(f"New subscription: {data.message} ({data.event_type})")
    return {"status": "ok"}

@app.webhooks.post("cancellation")
def cancellation_webhook(data: WebhookData):
    """
    Receive a cancellation event.
    """
    print(f"Cancellation: {data.message} ({data.event_type})")
    return {"status": "ok"}
```

---

TITLE: Upgrading pip for Python Projects
DESCRIPTION: Upgrades the `pip` package installer to its latest version within the active Python virtual environment. This is a crucial first step to prevent common installation errors and should typically be performed once after creating a virtual environment.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_8

LANGUAGE: console
CODE:

```
$ python -m pip install --upgrade pip

---> 100%
```

---

TITLE: Disabling Dependency Caching with Annotated in FastAPI (Python)
DESCRIPTION: This Python 3.8+ snippet demonstrates how to force a dependency to be called on every request, even if it's a common sub-dependency, by setting `use_cache=False` with `Annotated`. This ensures a 'fresh' value is always retrieved instead of a cached one.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/sub-dependencies.md#_snippet_3

LANGUAGE: Python
CODE:

```
async def needy_dependency(fresh_value: Annotated[str, Depends(get_value, use_cache=False)]):
    return {"fresh_value": fresh_value}
```

---

TITLE: Awaiting Asynchronous Operations in Python
DESCRIPTION: Demonstrates the use of the `await` keyword to pause execution until an asynchronous operation, such as `get_burgers(2)`, completes. This allows Python to perform other tasks concurrently while waiting for the result.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_3

LANGUAGE: Python
CODE:

```
burgers = await get_burgers(2)
```

---

TITLE: Declaring a Dictionary Type Hint (Python 3.9+)
DESCRIPTION: This snippet demonstrates how to declare a variable as a dictionary using the native `dict` type with square bracket notation, available in Python 3.9+. It requires two type parameters: the first for the keys and the second for the values.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_14

LANGUAGE: Python
CODE:

```
prices: dict[str, float] = {"apple": 1.0, "banana": 2.0}
```

---

TITLE: Setting Uvicorn Command in Dockerfile
DESCRIPTION: This `CMD` instruction defines the default command to execute when the Docker container starts. It runs the Uvicorn server, serving the FastAPI application `app.main:app` on all network interfaces (`0.0.0.0`) and port 80. The command will be executed from the `/code` working directory.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_5

LANGUAGE: Dockerfile
CODE:

```
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

TITLE: Declaring an Async FastAPI Path Operation Function
DESCRIPTION: This FastAPI path operation function is declared with `async def` because it performs an I/O-bound operation by awaiting `some_library()`. Using `async def` allows FastAPI to run other tasks concurrently while this function is waiting for the library call to complete, improving overall application responsiveness.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_1

LANGUAGE: Python
CODE:

```
@app.get('/')
async def read_results():
    results = await some_library()
    return results
```

---

TITLE: Defining POST Path Operation Decorator - FastAPI Python
DESCRIPTION: This snippet shows the `@app.post()` decorator, used in FastAPI to define a path operation that handles HTTP POST requests. It's typically used for creating new resources or submitting data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_9

LANGUAGE: Python
CODE:

```
@app.post()
```

---

TITLE: Declaring Integer Path/Query Parameters in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to declare an integer type for a parameter in FastAPI using standard Python type hints. This single declaration enables automatic validation, conversion, and documentation for `item_id`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_8

LANGUAGE: Python
CODE:

```
item_id: int
```

---

TITLE: Combining Path and Query Parameters - FastAPI Python
DESCRIPTION: This example demonstrates how FastAPI seamlessly handles both path and query parameters within a single endpoint function. FastAPI intelligently distinguishes between `item_id` (path parameter) and `q`, `skip`, `limit` (query parameters) based on their declaration.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "user_id": user_id}
    if q:
        item.update({"q": q})
    if short:
        item.update({"description": "This is a short description."})
    return item
```

---

TITLE: Defining a Nested Dependency with Cookie Parameter
DESCRIPTION: This example showcases a more complex dependency, `query_or_cookie_extractor`, which itself depends on `query_extractor`. It also demonstrates how to extract a value from a cookie (`last_query`) and use it as a fallback if the primary query parameter is not provided.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/sub-dependencies.md#_snippet_1

LANGUAGE: Python
CODE:

```
async def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q
```

---

TITLE: Running FastAPI with Uvicorn
DESCRIPTION: This command starts the FastAPI application `app` located in `main.py` using Uvicorn. It configures the server to listen on all available network interfaces (`0.0.0.0`) on port `80`. The `--reload` option, though not shown in the snippet, is mentioned as a development-only feature.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/manually.md#_snippet_2

LANGUAGE: Shell
CODE:

```
$ uvicorn main:app --host 0.0.0.0 --port 80
```

---

TITLE: Dockerfile for Single-File FastAPI Application
DESCRIPTION: This Dockerfile is tailored for a FastAPI application where the main file (`main.py`) is directly in the project root, not nested within an `app` directory. It sets up the Python environment, installs dependencies, and then copies the `main.py` file to the `/code` directory in the image. The `hl_lines` annotation highlights the `COPY` instruction for the main file.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_13

LANGUAGE: Dockerfile
CODE:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# (1)
COPY ./main.py /code/
```

---

TITLE: Running Docker Container
DESCRIPTION: This command runs a new Docker container based on the `myimage`. The `-d` flag runs the container in detached mode (in the background). `--name mycontainer` assigns a specific name to the container. The `-p 80:80` flag maps port 80 of the host to port 80 of the container, making the application accessible.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_11

LANGUAGE: Bash
CODE:

```
docker run -d --name mycontainer -p 80:80 myimage
```

---

TITLE: Defining an Asynchronous FastAPI Application
DESCRIPTION: This snippet defines a simple FastAPI application with an asynchronous root endpoint. It uses `async def` for the path operation function, indicating that it performs asynchronous operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/async-tests.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

TITLE: Declaring Optional String Type with `| None` (Python 3.10+)
DESCRIPTION: This example shows the modern Python 3.10+ syntax for type hints where a value can be `None`. Using `str | None` is a concise alternative to `Optional[str]` and `Union[str, None]`. The `name` parameter defaults to `None`, allowing the function to be called without it.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_19

LANGUAGE: Python
CODE:

```
def say_hi(name: str | None = None):
    if name:
        print(f"Hello {name}")
    else:
        print("Hello World")
```

---

TITLE: Declaring List of Strings (Python 3.9+)
DESCRIPTION: This snippet demonstrates the modern Python 3.9+ syntax for type-hinting a variable as a list containing string elements. It uses the built-in `list` type directly with square brackets for generic type parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body-nested-models.md#_snippet_0

LANGUAGE: Python
CODE:

```
my_list: list[str]
```

---

TITLE: Implement Nested Pydantic Models in FastAPI
DESCRIPTION: Shows how to define and use nested Pydantic models to represent complex, hierarchical JSON structures in FastAPI request bodies, enabling deep validation and automatic documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/body-nested-models.md#_snippet_3

LANGUAGE: Python
CODE:

```
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str
```

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: Image
```

LANGUAGE: JSON
CODE:

```
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

---

TITLE: Including Router with Custom Parameters (Python)
DESCRIPTION: Includes an existing APIRouter (admin.router) using app.include_router(), applying custom settings like prefix, tags, dependencies, and responses during inclusion without altering the original router definition.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_20

LANGUAGE: Python
CODE:

```
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
```

---

TITLE: Copying Requirements File to Docker Image
DESCRIPTION: This `COPY` instruction adds the `requirements.txt` file from the build context to the `/code/requirements.txt` path inside the Docker image. This step is placed early in the Dockerfile to leverage Docker's build cache, as the `requirements.txt` file changes less frequently than the application code.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_7

LANGUAGE: Dockerfile
CODE:

```
COPY ./requirements.txt /code/requirements.txt
```

---

TITLE: Defining Asynchronous Functions with async def
DESCRIPTION: Illustrates how to define an asynchronous function using `async def`. This declaration signals to Python that the function can be 'paused' at `await` expressions, allowing the event loop to switch to other tasks.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_4

LANGUAGE: Python
CODE:

```
async def get_burgers(number: int):
    # Do some asynchronous stuff to create the burgers
    return burgers
```

---

TITLE: Declaring Single File Parameter with UploadFile
DESCRIPTION: This snippet demonstrates using `UploadFile` for file parameters. `UploadFile` is preferred for larger files as it spools content to disk, preventing excessive memory usage. It provides attributes like `filename` and `content_type`, and file-like asynchronous methods for reading and writing. The endpoint returns the filename and content type of the uploaded file.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/request-files.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename, "content_type": file.content_type}
```

---

TITLE: Rendering HTML Templates with FastAPI and Jinja2
DESCRIPTION: This Python snippet demonstrates how to configure and use Jinja2 templates in a FastAPI application. It initializes `Jinja2Templates` by specifying the directory where templates are located and defines a path operation that renders an HTML template, passing the `Request` object and dynamic context data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/templates.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        name="item.html",
        context={
            "request": request,
            "id": id
        }
    )
```

---

TITLE: Defining Optional Query Parameter with Query() - FastAPI Python
DESCRIPTION: This code shows how to declare an optional query parameter `q` by setting its default value to `Query(default=None)`. This makes the parameter non-required, similar to setting `q = None`, but explicitly declares it as a FastAPI query parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/de/docs/tutorial/query-params-str-validations.md#_snippet_1

LANGUAGE: Python
CODE:

```
q: Union[str, None] = Query(default=None)
```

---

TITLE: Initializing FastAPI Application
DESCRIPTION: This snippet initializes a FastAPI application instance, setting basic metadata such as title, version, summary, and description. These details are used to populate the 'info' object in the generated OpenAPI schema.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/extending-openapi.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI(
    title="My Super Project",
    version="2.5.0",
    summary="This is a very fancy project, with auto docs",
    description="This is a very fancy project, with auto docs and everything",
)
```

---

TITLE: Applying Numeric Validations (`gt`, `lt`) to Float Path Parameters
DESCRIPTION: This snippet demonstrates applying 'greater than' (`gt`) and 'less than' (`lt`) numeric validations to a `float` path parameter. This allows specifying a range where the value must be strictly between two numbers, for example, between 0 and 1 (exclusive).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/path-params-numeric-validations.md#_snippet_6

LANGUAGE: Python
CODE:

```
@app.get("/items/{item_id}")
async def read_items(
    item_id: float = Path(..., title="The ID of the item to get", gt=0, lt=1)
):
    return {"item_id": item_id}
```

---

TITLE: Declaring Additional Response with Pydantic Model (Python)
DESCRIPTION: This snippet demonstrates how to declare an additional response for a FastAPI path operation using the `responses` parameter. It specifies a `404` HTTP status code with a Pydantic `Message` model, which FastAPI uses to generate the OpenAPI schema for this error response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/additional-responses.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Response
from pydantic import BaseModel

class Message(BaseModel):
    message: str

class Item(BaseModel):
    id: str
    value: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"}
    }
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "The Foo Wrestlers"}
    return Response(status_code=404)
```

---

TITLE: Relative Import of APIRouters in Main App
DESCRIPTION: Shows how to import APIRouter instances from submodules within the same package using a relative import (single dot). This is typically done in the main application file to bring in routers defined in other files.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_14

LANGUAGE: Python
CODE:

```
from .routers import items, users
```

---

TITLE: Creating a Nested Dependency with Cookie Fallback in FastAPI (Python)
DESCRIPTION: This FastAPI dependency, `query_or_cookie_extractor`, demonstrates nesting by depending on `query_extractor` to get an initial query value. If no query is provided, it attempts to retrieve a `last_query` from a cookie, showcasing how dependencies can also be 'dependants' themselves.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/sub-dependencies.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Optional
from fastapi import Depends, Cookie

async def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)):
    if not q:
        return last_query
    return q
```

---

TITLE: Defining File and Form Parameters in FastAPI Path Operations
DESCRIPTION: This code defines parameters within a FastAPI path operation to accept both file uploads and form data. `file` receives raw bytes, `fileb` receives an `UploadFile` object for more metadata, and `token` captures a string from a form field. All are declared as required parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-forms-and-files.md#_snippet_2

LANGUAGE: Python
CODE:

```
file: bytes = File(...),
fileb: UploadFile = File(...),
token: str = Form(...),
```

---

TITLE: Reading UploadFile Contents Asynchronously
DESCRIPTION: This Python snippet demonstrates how to asynchronously read the contents of an `UploadFile` object within an `async` path operation function. The `await` keyword is necessary because `read()` is an `async` method provided by `UploadFile`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-files.md#_snippet_1

LANGUAGE: python
CODE:

```
contents = await myfile.read()
```

---

TITLE: Running FastAPI Development Server
DESCRIPTION: This command demonstrates how to start the FastAPI development server using `fastapi dev main.py`. It automatically detects the FastAPI application and runs it with Uvicorn, enabling auto-reload for local development.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_5

LANGUAGE: console
CODE:

```
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

TITLE: Using a Pydantic Model as Response Model in FastAPI
DESCRIPTION: This FastAPI path operation illustrates using the `Item` Pydantic model as an output (response model) via the `response_model` parameter. When a model with default values is used for output, fields like `description` are marked as required in the OpenAPI schema because they will always have a value (even if `null`), ensuring clients can consistently expect the field to be present in the response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/separate-openapi-schemas.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return {"name": "Foo", "price": 42}
```

---

TITLE: Running FastAPI Application with Uvicorn (Console)
DESCRIPTION: This command starts the Uvicorn server, pointing it to the FastAPI application instance (`app`) within the `main.py` file. It configures the server to listen on all available network interfaces (`0.0.0.0`) on port `80`, making the application accessible.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/manually.md#_snippet_3

LANGUAGE: console
CODE:

```
uvicorn main:app --host 0.0.0.0 --port 80
```

---

TITLE: Implementing HTTP Basic Authentication in FastAPI
DESCRIPTION: This snippet demonstrates how to set up HTTP Basic Authentication in a FastAPI application. It imports `HTTPBasic` and `HTTPBasicCredentials`, initializes `HTTPBasic` as a security dependency, and then uses `Depends(security)` in a path operation function to automatically receive `HTTPBasicCredentials` containing the username and password provided by the client.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/security/http-basic-auth.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
```

---

TITLE: Install python-jose for JWT Operations
DESCRIPTION: Installs the `python-jose` library, specifically with the `cryptography` extra. This library is essential for creating, encoding, decoding, and verifying JSON Web Tokens (JWT) in Python applications, providing cryptographic functionalities for secure token handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/oauth2-jwt.md#_snippet_1

LANGUAGE: console
CODE:

```
$ pip install "python-jose[cryptography]"
```

---

TITLE: Using Settings Dependency in a Path Operation
DESCRIPTION: This example demonstrates how to inject the `Settings` object into a FastAPI path operation function using `Depends(get_settings)`. Once injected, the application settings like `app_name` and `admin_email` can be accessed and used within the endpoint logic.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/settings.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import Depends, FastAPI

from .config import Settings
from .main import get_settings # Assuming get_settings is in main.py for context

app = FastAPI()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
    }
```

---

TITLE: Importing TestClient for FastAPI Testing - Python
DESCRIPTION: This snippet demonstrates how to import the `TestClient` class from the `fastapi.testclient` module. This class is essential for testing FastAPI applications by allowing direct interaction with the application's code without requiring an active HTTP server connection.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/testclient.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi.testclient import TestClient
```

---

TITLE: Install passlib for Password Hashing
DESCRIPTION: Installs the `passlib` library along with the `bcrypt` hashing algorithm. `passlib` is a comprehensive password hashing framework for Python, and `bcrypt` is a strong, adaptive hashing algorithm recommended for securely storing user passwords.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/oauth2-jwt.md#_snippet_2

LANGUAGE: console
CODE:

```
$ pip install "passlib[bcrypt]"
```

---

TITLE: Using Shorthand Dependency in Path Operation
DESCRIPTION: This snippet showcases the shorthand `Depends()` syntax within a FastAPI path operation. By using `Depends()` without arguments, FastAPI infers the dependency class (`CommonQueryParams`) from the parameter's type hint, leading to more concise and readable dependency declarations within path operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_15

LANGUAGE: Python
CODE:

```
@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```

---

TITLE: Using TestClient with a Context Manager in Python
DESCRIPTION: This snippet demonstrates how to use FastAPI's `TestClient` within a `with` statement. This pattern ensures that the test client's resources are properly managed and closed after the test, preventing resource leaks. It shows a basic GET request and assertions on the response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/testing-websockets.md#_snippet_0

LANGUAGE: Python
CODE:

```
with TestClient(app) as client:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
```

---

TITLE: Installing Uvicorn and Gunicorn
DESCRIPTION: This command installs both Uvicorn (with its standard dependencies for better performance) and Gunicorn. Gunicorn acts as the process manager, while Uvicorn serves the ASGI application, enabling a robust and concurrent setup for FastAPI.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/server-workers.md#_snippet_0

LANGUAGE: Shell
CODE:

```
$ pip install "uvicorn[standard]" gunicorn
```

---

TITLE: Importing APIRouter Class in Python
DESCRIPTION: This snippet demonstrates how to import the `APIRouter` class directly from the `fastapi` library. The `APIRouter` class is essential for organizing routes and handlers in larger FastAPI applications, allowing for modular API design.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/apirouter.md#_snippet_0

LANGUAGE: python
CODE:

```
from fastapi import APIRouter
```

---

TITLE: Defining Optional Query Parameter (Python 3.10+) - FastAPI Python
DESCRIPTION: This snippet demonstrates defining an optional query parameter `q` using the Python 3.10+ union syntax (`str | None`) and `Query(default=None)`. It achieves the same optionality as `Union[str, None]` while explicitly marking it as a FastAPI query parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/de/docs/tutorial/query-params-str-validations.md#_snippet_3

LANGUAGE: Python
CODE:

```
q: str | None = Query(default=None)
```

---

TITLE: Defining a Class-Based Dependency with **init**
DESCRIPTION: This snippet defines `CommonQueryParams`, a Python class designed to serve as a FastAPI dependency. Its `__init__` method declares parameters (`q`, `skip`, `limit`) that FastAPI will automatically resolve from incoming request query parameters. This class-based approach provides superior type hinting and editor support compared to returning a raw dictionary.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_2

LANGUAGE: Python
CODE:

```
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit
```

---

TITLE: Registering Lifespan Context Manager with FastAPI
DESCRIPTION: This snippet shows how to register the custom `lifespan` asynchronous context manager with a FastAPI application. By passing `lifespan=lifespan` to the `FastAPI` constructor, the application will automatically execute the `lifespan` function's startup and shutdown logic.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/events.md#_snippet_5

LANGUAGE: Python
CODE:

```
app = FastAPI(lifespan=lifespan)
```

---

TITLE: Defining a File Parameter with UploadFile in FastAPI
DESCRIPTION: This snippet illustrates how to define a file parameter using `UploadFile`. This is the recommended method for larger files as it leverages spooled temporary files, preventing excessive memory consumption and providing access to file metadata and asynchronous file operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/request-files.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename, "content_type": file.content_type}
```

---

TITLE: Declaring BackgroundTasks in FastAPI Path Operations
DESCRIPTION: This snippet demonstrates how to import `FastAPI` and `BackgroundTasks` and declare a `BackgroundTasks` parameter in a path operation function. FastAPI automatically handles the creation and injection of this dependency, allowing you to add background tasks that run after the response is sent.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/background-tasks.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_notification(email: str, message=""):
    with open("log.txt", "a") as log:
        log.write(f"notification for {email}: {message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
```

---

TITLE: Installing HTTPX for TestClient
DESCRIPTION: This command installs the 'httpx' library, which is a required dependency for using Starlette's TestClient to test FastAPI applications. It should be executed within an activated virtual environment to manage project dependencies effectively.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md#_snippet_0

LANGUAGE: console
CODE:

```
$ pip install httpx
```

---

TITLE: Defining Asynchronous Test Functions with pytest-anyio and HTTPX AsyncClient
DESCRIPTION: This snippet illustrates how to define an asynchronous test function using `pytest.mark.anyio` to enable `async def` tests. It demonstrates the setup of `httpx.AsyncClient` with a FastAPI application and sending an asynchronous request using `await client.get('/')`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/async-tests.md#_snippet_0

LANGUAGE: python
CODE:

```
import pytest
from httpx import AsyncClient
# from app.main import app # Assuming 'app' is your FastAPI application instance

@pytest.mark.anyio
async def test_example_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        # Further assertions would go here
```

---

TITLE: Implementing Trusted Host Middleware in FastAPI (Python)
DESCRIPTION: This snippet shows how to integrate `TrustedHostMiddleware` into a FastAPI application to protect against HTTP Host header attacks. It validates the `Host` header of incoming requests against a list of `allowed_hosts`. If the host is not allowed, a `400` response is returned. The `allowed_hosts` parameter accepts a list of domain names, including wildcards for subdomains.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/middleware.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.org"])
```

---

TITLE: Adding Min and Max Length Validations with Annotated - FastAPI Python
DESCRIPTION: This snippet demonstrates how to apply both `min_length` and `max_length` string validations to an optional query parameter `q` using `Annotated`. This approach ensures that the input string adheres to both minimum and maximum length constraints, providing robust data validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/de/docs/tutorial/query-params-str-validations.md#_snippet_9

LANGUAGE: Python
CODE:

```
q: Annotated[str | None, Query(min_length=3, max_length=50)] = None
```

---

TITLE: Overriding Settings for Testing
DESCRIPTION: This snippet illustrates how to easily override the `get_settings` dependency during testing. By assigning a custom function to `app.dependency_overrides[get_settings]`, you can provide specific settings (e.g., a test `admin_email`) for isolated and predictable test scenarios. Remember to clear overrides after tests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/settings.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi.testclient import TestClient
from main import app, get_settings, Settings

def test_info_with_override():
    def override_get_settings():
        return Settings(admin_email="test@example.com")

    app.dependency_overrides[get_settings] = override_get_settings
    client = TestClient(app)
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "test@example.com",
    }
    app.dependency_overrides.clear() # Clean up
```

---

TITLE: Running FastAPI with Uvicorn for Debugging
DESCRIPTION: This Python snippet illustrates a basic FastAPI application configured to run directly using Uvicorn when the script is executed. Placing `uvicorn.run()` within the `if __name__ == "__main__":` block allows for easy debugging by enabling the server to start only when the file is run as the main program, not when imported.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/debugging.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

TITLE: Adding Max Length Validation with Annotated and Query
DESCRIPTION: This snippet demonstrates how to apply a maximum length validation to an optional query parameter `q` using `Annotated` and `Query`. By including `Query(max_length=50)` within `Annotated`, FastAPI enforces that the provided string for `q` does not exceed 50 characters, while still keeping the parameter optional.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_6

LANGUAGE: Python
CODE:

```
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    if q:
        return {"q": q}
    return {"message": "No q parameter"}
```

---

TITLE: Defining FastAPI Models and Path Operations
DESCRIPTION: This Python snippet demonstrates a basic FastAPI application defining Pydantic models for request and response payloads (`Item` and `ResponseMessage`) and implementing path operations. These models are crucial as they provide the schema information used by OpenAPI for client generation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/generate-clients.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ResponseMessage(BaseModel):
    message: str

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"name": "Foo", "price": 42.0, "is_offer": True}

@app.put("/items/{item_id}", response_model=ResponseMessage)
async def update_item(item_id: int, item: Item):
    return {"message": f"Item {item.name} updated successfully for ID {item_id}"}
```

---

TITLE: Enforcing HTTPS Redirection with `HTTPSRedirectMiddleware` - FastAPI
DESCRIPTION: This snippet demonstrates how to use `HTTPSRedirectMiddleware` to automatically redirect all incoming HTTP or WS requests to their secure HTTPS or WSS counterparts. This middleware ensures that all communication with the application occurs over a secure channel, enhancing security by preventing unencrypted data transmission. It requires no additional parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/middleware.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Running FastAPI with Root Path via CLI
DESCRIPTION: This console command demonstrates how to start a FastAPI application using the `fastapi run` command, specifying a `root_path` (`/api/v1`) as a command-line argument. This configuration informs the application about the path prefix added by an upstream proxy, allowing it to generate correct URLs for its endpoints and documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md#_snippet_2

LANGUAGE: Console
CODE:

```
$ fastapi run main.py --root-path /api/v1
```

---

TITLE: Add Custom Tags, Responses, and Dependencies to Path Operation
DESCRIPTION: Shows how to add extra tags, responses, and dependencies specifically to a single path operation within an APIRouter, in addition to any defined at the router level. This allows for fine-grained control over documentation and behavior for individual endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_12

LANGUAGE: Python
CODE:

```
@router.get("/custom-item/{item_id}",
                tags=["custom"],
                responses={403: {"description": "Operation forbidden"}},
                dependencies=[Depends(get_current_user)])
async def read_custom_item(item_id: str):
     # ... implementation ...
     pass
```

---

TITLE: Validating Host Headers with `TrustedHostMiddleware` - FastAPI
DESCRIPTION: This snippet shows how to implement `TrustedHostMiddleware` to protect against HTTP Host header attacks by validating the `Host` header of incoming requests. It requires the `allowed_hosts` parameter, which is a list of permitted domain names, supporting wildcards for subdomains. Requests with invalid host headers will receive a `400` response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/middleware.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Using `Annotated` for Metadata (Python 3.8+)
DESCRIPTION: Illustrates how to use `Annotated` from `typing_extensions` in Python 3.8+ to attach metadata to type hints. This allows tools like FastAPI to interpret additional information beyond the basic type, enhancing API behavior definition through metadata like Pydantic's `Field`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_31

LANGUAGE: Python
CODE:

```
from typing_extensions import Annotated
from pydantic import BaseModel, Field

class AnotherModel(BaseModel):
    description: Annotated[str, Field(min_length=10)]
```

---

TITLE: Configuring Uvicorn Server Startup
DESCRIPTION: This Python line configures and starts the Uvicorn server for a FastAPI application. It specifies the application object (`app`), the host address (`0.0.0.0` for network accessibility), and the port (`8000`), making the API accessible for development and testing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/debugging.md#_snippet_3

LANGUAGE: Python
CODE:

```
uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

TITLE: Handling Multiple Body Parameters in FastAPI
DESCRIPTION: Illustrates how FastAPI automatically handles multiple Pydantic models (`Item` and `User`) as body parameters. When multiple models are declared, FastAPI expects a JSON body where each model's data is nested under a key corresponding to its parameter name (e.g., `item` and `user`).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-multiple-params.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item.dict(), "user": user.dict()}
    return results
```

---

TITLE: Starting Uvicorn with Root Path (Console)
DESCRIPTION: This command starts the Uvicorn server for a FastAPI application (`main:app`) and sets the `--root-path` to `/api/v1`. This informs the application that it is being served under this sub-path, which is crucial when running behind a reverse proxy like Traefik.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/behind-a-proxy.md#_snippet_9

LANGUAGE: console
CODE:

```
uvicorn main:app --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

TITLE: Importing Path and Annotated in FastAPI
DESCRIPTION: This snippet demonstrates how to import `Path` from `fastapi` and `Annotated` from `typing`. `Path` is used for declaring path parameters, while `Annotated` is recommended for type hints with metadata in FastAPI versions 0.95.0 and above.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params-numeric-validations.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import FastAPI, Path
```

---

TITLE: Declaring Required Query Parameter with Validation
DESCRIPTION: This snippet declares a required query parameter `q` of type `str`. It uses `Query(min_length=3)` to enforce that the provided string must have a minimum length of 3 characters. Since no default is provided, the parameter is mandatory.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_9

LANGUAGE: Python
CODE:

```
q: str = Query(min_length=3)
```

---

TITLE: Adding a Background Task to a Path Operation
DESCRIPTION: This line demonstrates how to add a background task using the `add_task()` method of the `BackgroundTasks` object. It takes the task function (`write_notification`), positional arguments (`email`), and keyword arguments (`message="some notification"`) for the task function. The task will execute after the HTTP response is sent.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/background-tasks.md#_snippet_2

LANGUAGE: Python
CODE:

```
    background_tasks.add_task(write_notification, email, message="some notification")
```

---

TITLE: Declaring List of Pydantic Models (Python 3.9+)
DESCRIPTION: This snippet demonstrates the Python 3.9+ syntax for type-hinting a variable as a list containing `Image` Pydantic models. It uses the built-in `list` type directly with type parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body-nested-models.md#_snippet_3

LANGUAGE: Python
CODE:

```
images: list[Image]
```

---

TITLE: Importing FastAPI Security Modules - Python
DESCRIPTION: This snippet imports various security classes and utilities from the `fastapi.security` module. These classes are used to define different authentication and authorization schemes, such as API Key, HTTP Basic/Bearer, OAuth2, and OpenID Connect, which integrate with FastAPI's dependency injection system and OpenAPI documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/security/index.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi.security import (
    APIKeyCookie,
    APIKeyHeader,
    APIKeyQuery,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPDigest,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2PasswordRequestFormStrict,
    OpenIdConnect,
    SecurityScopes,
)
```

---

TITLE: Simplified Parameter Ordering with Annotated (No _ needed)
DESCRIPTION: This snippet demonstrates that when using `Annotated` for path and query parameters, the `_`trick for parameter ordering is unnecessary.`Annotated`allows flexible parameter declaration order as`Path`and`Query` are not used as default values.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params-numeric-validations.md#_snippet_5

LANGUAGE: Python
CODE:

```
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str, Query(min_length=3)]
```

---

TITLE: Setting Custom Headers with Response Parameter in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to set custom HTTP headers in a FastAPI response by injecting the `Response` object as a dependency into the path operation function. Headers are added to the `response.headers` dictionary, allowing for direct manipulation of the outgoing HTTP response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/response-headers.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/items/")
def read_items(response: Response):
    response.headers["X-Cat-Dog"] = "Hello from the other side"
    return {"item_id": "Foo"}
```

---

TITLE: Importing Dependencies with Relative Path - FastAPI Python
DESCRIPTION: Demonstrates importing dependencies from a parent directory using relative import (`..`) within a FastAPI router module (`app/routers/items.py`). This is crucial for structuring larger applications across multiple files and directories.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/bigger-applications.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_items():
    return [{"item_id": "Foo", "owner": "Alice"}, {"item_id": "Bar", "owner": "Bob"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}


@router.get("/open/", tags=["custom"], responses={403: {"description": "Operation forbidden"}})
async def read_open_item():
    return {"item_id": "open"}
```

---

TITLE: Declaring Optional Types with `typing.Optional`
DESCRIPTION: Illustrates how to define a parameter that can be of a specific type (e.g., `str`) or `None`. This is achieved using `Optional` from the `typing` module, which is equivalent to `Union[Type, None]`. This pattern is common for nullable parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_12

LANGUAGE: Python
CODE:

```
from typing import Optional

def greet_optional(name: Optional[str] = None):
    if name:
        print(f"Hello, {name}!")
    else:
        print("Hello, World!")
```

---

TITLE: Declaring Optional String Type with `Optional` (Python 3.6+)
DESCRIPTION: This snippet demonstrates how to declare a parameter that can be either a `str` or `None` using `Optional[str]` from the `typing` module. The parameter `name` has a default value of `None`, making it truly optional in function calls. It prints a greeting based on whether a name is provided.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_18

LANGUAGE: Python
CODE:

```
from typing import Optional

def say_hi(name: Optional[str] = None):
    if name:
        print(f"Hello {name}")
    else:
        print("Hello World")
```

---

TITLE: Declaring Required Query Parameters - FastAPI Python
DESCRIPTION: This snippet shows how to define a required query parameter in FastAPI by omitting its default value. If the `needy` parameter is not provided in the URL, FastAPI will automatically return a validation error, ensuring necessary data is always present.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    return {"item_id": item_id, "needy": needy}
```

---

TITLE: Forbidding Extra Query Parameters with Pydantic Config in FastAPI
DESCRIPTION: This snippet shows how to restrict query parameters to only those explicitly defined in a Pydantic model. By setting `Config.extra = "forbid"` within the model, FastAPI will return an error if the client sends any query parameters not declared in the `CommonQueryParams` model.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-param-models.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class CommonQueryParams(BaseModel):
    q: Optional[str] = None
    skip: int = 0
    limit: int = 100

    class Config:
        extra = "forbid"

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Query()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = [{"item_id": "Foo"}, {"item_id": "Bar"}]
    response.update({"items": items[commons.skip : commons.skip + commons.limit]})
    return response
```

---

TITLE: Declaring Simple Python Type Hints
DESCRIPTION: This snippet illustrates the use of various basic Python type hints, including `int`, `float`, `bool`, and `bytes`, within a function's parameter declarations. It demonstrates how to explicitly declare common built-in types for improved code clarity and static analysis.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_8

LANGUAGE: Python
CODE:

```
def process_data(count: int, price: float, is_active: bool, raw_data: bytes):
    # Example usage of parameters
    print(f"Count: {count}, Price: {price}, Active: {is_active}, Raw Data Length: {len(raw_data)}")
    if is_active and count > 0:
        return price * count
    return 0.0

# Example calls
process_data(10, 25.5, True, b"some_bytes")
```

---

TITLE: Using jsonable_encoder with Pydantic Models and Datetime in FastAPI
DESCRIPTION: This snippet demonstrates how to use FastAPI's `jsonable_encoder()` to convert a Pydantic model instance, which includes a `datetime` object, into a JSON-compatible Python dictionary. This conversion ensures that complex data types are properly serialized for storage or transmission, making `datetime` objects into ISO 8601 strings and Pydantic models into standard dictionaries.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/encoder.md#_snippet_0

LANGUAGE: Python
CODE:

```
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None

app = FastAPI()

fake_db = {}

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return {"message": f"Item {id} updated successfully"}
```

---

TITLE: Instantiating Pydantic Settings Object (Python)
DESCRIPTION: This snippet demonstrates the direct instantiation of a Settings object. Each call to Settings() creates a new instance, which, if configured to read from a .env file, would re-read the file, potentially leading to performance overhead.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_9

LANGUAGE: Python
CODE:

```
Settings()
```

---

TITLE: Dockerfile for FastAPI with Bigger Applications Structure
DESCRIPTION: This Dockerfile is adapted for FastAPI applications following a 'bigger applications' structure, where the main application code resides in a nested `app` directory (e.g., `/app/app`). The key difference is the `COPY` command, which correctly places the application files within the container's `/app/app` directory.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_16

LANGUAGE: Dockerfile
CODE:

```
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
```

---

TITLE: Declaring a Synchronous FastAPI Path Operation Function
DESCRIPTION: This FastAPI path operation function is declared with a standard `def` because it calls a synchronous `some_library()` function that does not support `await`. FastAPI will run this function in a separate thread pool to prevent blocking the main event loop, ensuring the application remains responsive even during I/O-bound synchronous operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/async.md#_snippet_2

LANGUAGE: Python
CODE:

```
@app.get('/')
def results():
    results = some_library()
    return results
```

---

TITLE: Chained Sub-Dependencies with Yield (Python)
DESCRIPTION: This snippet demonstrates a chain of sub-dependencies (`dependency_a` -> `dependency_b` -> `dependency_c`), where each uses `yield`. FastAPI ensures the setup and teardown phases of these dependencies are executed in the correct order, respecting their dependencies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import Depends, FastAPI

async def dependency_a():
    print("Dependency A setup")
    yield "A_value"
    print("Dependency A teardown")

async def dependency_b(dep_a: str = Depends(dependency_a)):
    print(f"Dependency B setup with {dep_a}")
    yield "B_value"
    print("Dependency B teardown")

async def dependency_c(dep_b: str = Depends(dependency_b)):
    print(f"Dependency C setup with {dep_b}")
    yield "C_value"
    print("Dependency C teardown")
```

---

TITLE: Defining X-Token Dependency (Python 3.8+ Optional)
DESCRIPTION: Defines a simple dependency function `get_token` in `app/dependencies.py` that reads the `X-Token` header using `Optional`. It raises an `HTTPException` if the token is not 'fake-super-secret-token'.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/bigger-applications.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Optional

from fastapi import Header, HTTPException


async def get_token(x_token: Optional[str] = Header(None)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    return token
```

---

TITLE: Path Parameter Numeric Validation: Greater Than and Less Than or Equal
DESCRIPTION: This snippet demonstrates applying multiple numeric validations to a path parameter. `gt=0` ensures `item_id` is strictly greater than 0, and `le=1000` ensures it is less than or equal to 1000, defining a valid range for the integer parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params-numeric-validations.md#_snippet_7

LANGUAGE: Python
CODE:

```
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
```

---

TITLE: Defining a Dictionary-Returning Dependency Function
DESCRIPTION: This snippet defines a Python function `common_parameters` that serves as a dependency. It takes optional query parameters `q`, `skip`, and `limit`, and returns them as a dictionary. FastAPI uses this function to inject common parameters into path operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_0

LANGUAGE: Python
CODE:

```
def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
```

---

TITLE: Declaring Multiple Request Body Parameters in FastAPI
DESCRIPTION: This snippet shows how to define multiple Pydantic models as request body parameters in a FastAPI path operation. FastAPI automatically recognizes these as distinct body parameters and expects a JSON object where each parameter's name is a key, containing its respective model's data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body-multiple-params.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
```

---

TITLE: Configuring Multiple OpenAPI Servers with Root Path in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to configure a FastAPI application with multiple OpenAPI servers, including a `root_path`. FastAPI automatically prepends a server entry for the `root_path` to the provided list, allowing the same docs UI to interact with different environments (e.g., staging, production) while respecting the API's base path behind a proxy.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md#_snippet_12

LANGUAGE: Python
CODE:

```
app = FastAPI(
    root_path="/api/v1",
    openapi_servers=[
        {"url": "https://stag.example.com", "description": "Staging environment"},
        {"url": "https://prod.example.com", "description": "Production environment"}
    ]
)
```

---

TITLE: Defining a Simple Query Extractor Dependency in FastAPI (Python)
DESCRIPTION: This snippet defines a basic FastAPI dependency function, `query_extractor`, which extracts an optional query parameter `q` of type string. It serves as a simple example to demonstrate the concept of a 'dependable' function that returns a value to its callers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/sub-dependencies.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Optional

async def query_extractor(q: Optional[str] = None):
    return q
```

---

TITLE: Defining Multiple Media Types for FastAPI Response (Python)
DESCRIPTION: This snippet demonstrates how to declare an additional media type, such as `image/png`, for a FastAPI path operation's main response using the `responses` parameter. It also shows how to return a file directly using `FileResponse` when the image media type is requested, alongside the default JSON response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/additional-responses.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get(
    "/portal",
    responses={
        200: {
            "content": {
                "image/png": {"schema": {"type": "string", "format": "binary"}},
                "application/json": {"schema": {"type": "object", "properties": {"message": {"type": "string"}}}}
            },
            "description": "Return a JSON object or a PNG image."
        }
    }
)
async def get_portal(accept: str | None = None):
    if accept and "image/png" in accept:
        return FileResponse("portal.png", media_type="image/png")
    return {"message": "Hello Portal"}
```

---

TITLE: Running FastAPI with Proxy Headers (Dockerfile)
DESCRIPTION: Configures the FastAPI application to trust headers from a TLS Termination Proxy (e.g., Nginx, Traefik) by adding the `--proxy-headers` option to the `fastapi run` command. This ensures Uvicorn correctly interprets HTTPS and other proxy-related information.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_8

LANGUAGE: Dockerfile
CODE:

```
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

---

TITLE: Handling GZip Compression with GZipMiddleware - Python
DESCRIPTION: Illustrates how to add `GZipMiddleware` to a FastAPI application to automatically compress responses for clients that include `"gzip"` in their `Accept-Encoding` header. It supports configuration parameters like `minimum_size` to control when compression is applied and `compresslevel` for compression intensity.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/middleware.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

TITLE: Adding GZip Compression Middleware in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to add `GZipMiddleware` to a FastAPI application. This middleware automatically compresses responses for clients that support GZip encoding (indicated by the `Accept-Encoding` header). It can be configured with `minimum_size` to only compress responses larger than a specified byte count, improving performance for small responses.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/middleware.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=500)
```

---

TITLE: Importing and Initializing APIRouter in FastAPI
DESCRIPTION: This snippet shows how to import the APIRouter class from the fastapi library and create an instance of it. This router instance will be used to define path operations for a specific part of the application, like user-related routes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter

router = APIRouter()
```

---

TITLE: Defining FastAPI Lifespan Context Manager (Yield Block)
DESCRIPTION: This snippet shows the core `yield` block within an `asynccontextmanager` decorated function. Code before `yield` runs on application startup, and code after `yield` runs on application shutdown. This is used for managing resources like database connections.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/events.md#_snippet_0

LANGUAGE: Python
CODE:

```
    await db.connect()
    print("Application startup complete.")
    yield
    await db.disconnect()
```

---

TITLE: Declaring Synchronous Path Operation Function (FastAPI, Python)
DESCRIPTION: This snippet illustrates how to define a FastAPI path operation function using a standard `def` when interacting with a synchronous (blocking) third-party library, such as most traditional database clients. FastAPI automatically runs these `def` functions in a separate thread pool, preventing them from blocking the main asynchronous event loop and maintaining responsiveness.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/async.md#_snippet_2

LANGUAGE: Python
CODE:

```
@app.get('/')
def results():
    results = some_library()
    return results
```

---

TITLE: Declaring Optional Query Parameter with Validation and Explicit Default
DESCRIPTION: This snippet declares an optional query parameter `q` of type `Union[str, None]`. It uses `Query(default=None)` to explicitly set the default to `None` and adds a `min_length=3` validation, ensuring that if provided, the string must be at least 3 characters long.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_7

LANGUAGE: Python
CODE:

```
q: Union[str, None] = Query(default=None, min_length=3)
```

---

TITLE: Applying 'Greater Than' (`gt`) and 'Less Than or Equal To' (`le`) Validations
DESCRIPTION: This example shows how to combine 'greater than' (`gt`) and 'less than or equal to' (`le`) numeric validations for a path parameter. The `item_id` must be an integer strictly greater than 0 and less than or equal to 1000.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/path-params-numeric-validations.md#_snippet_5

LANGUAGE: Python
CODE:

```
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000)
):
    return {"item_id": item_id}
```

---

TITLE: Declare List Fields with Type Parameters in FastAPI
DESCRIPTION: Explains how to specify the type of elements within a list field using type parameters (e.g., `list[str]` for Python 3.9+ or `List[str]` for older versions), ensuring type-safe list validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/body-nested-models.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import List
```

LANGUAGE: Python
CODE:

```
my_list: list[str]
```

LANGUAGE: Python
CODE:

```
from typing import List

my_list: List[str]
```

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str]
```

---

TITLE: Customizing Docs and Disabling ReDoc in FastAPI (Python)
DESCRIPTION: This example illustrates how to configure the URLs for FastAPI's built-in documentation UIs. It shows how to set a custom path for Swagger UI using `docs_url` and how to completely disable ReDoc by setting `redoc_url=None` during `FastAPI` app initialization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/metadata.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI(docs_url="/documentation", redoc_url=None)
```

---

TITLE: Defining X-Token Dependency (Python 3.8+)
DESCRIPTION: Defines a dependency function `get_token` that reads the `X-Token` header from the request using a default value with `Header()`. It raises an `HTTPException` if the header value is not 'fake-super-secret-token'. This version does not use `Annotated`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_6

LANGUAGE: Python
CODE:

```
from fastapi import Header, HTTPException


async def get_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
```

---

TITLE: Handling Multiple File Uploads
DESCRIPTION: This snippet shows how to handle multiple file uploads by declaring the parameter type as a `List` of `bytes` or `UploadFile`. FastAPI automatically processes each uploaded file in the list. The endpoints return the sizes of `bytes` files or the filenames of `UploadFile` instances.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/request-files.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import List

from fastapi import FastAPI, File

app = FastAPI()

@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}
```

LANGUAGE: Python
CODE:

```
from typing import List

from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

---

TITLE: Running a Python Program within a Virtual Environment
DESCRIPTION: Executes a Python script named `main.py` using the Python interpreter from the active virtual environment. This ensures that the program runs with the specific packages installed in that environment, demonstrating basic program execution.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_16

LANGUAGE: console
CODE:

```
$ python main.py

Hello World
```

---

TITLE: Setup for FastAPI Lifespan Context Manager
DESCRIPTION: This code provides the necessary imports and defines a `Database` class with `connect` and `disconnect` asynchronous methods. A global `db` instance is created, which will be managed by the `lifespan` context manager to simulate resource initialization and cleanup.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/events.md#_snippet_2

LANGUAGE: Python
CODE:

```
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI

# This is a placeholder for a real database connection pool or similar resource
# In a real app, this would be initialized with actual connection details
# and potentially a connection pool.
class Database:
    def __init__(self):
        self.connection = None

    async def connect(self):
        print("Connecting to database...")
        self.connection = "Database connection object" # Simulate connection
        print("Database connected.")

    async def disconnect(self):
        print("Disconnecting from database...")
        self.connection = None
        print("Database disconnected.")

db = Database() # Global instance
```

---

TITLE: Defining BackgroundTasks Parameter in FastAPI
DESCRIPTION: This snippet demonstrates how to import `BackgroundTasks` from `fastapi` and declare it as a parameter in a path operation function. FastAPI automatically injects an instance of `BackgroundTasks` for managing background operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/background-tasks.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_notification(email: str, message=""): # This function is defined later
    with open("log.txt", mode="a") as log:
        log.write(f"notification for {email}: {message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
```

---

TITLE: Example File Structure
DESCRIPTION: Illustrates a typical directory and file layout for a larger FastAPI application using Python packages and modules.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_0

LANGUAGE: Text/Diagram
CODE:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```

---

TITLE: Declaring Additional Response Model in FastAPI
DESCRIPTION: This snippet demonstrates how to define an additional response for a FastAPI path operation using the `responses` parameter. It specifies a 404 status code with a `Message` Pydantic model, which FastAPI uses to generate the OpenAPI schema for this error response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/additional-responses.md#_snippet_0

LANGUAGE: Python
CODE:

```
responses={
    404: {"description": "Additional Response", "model": Message},
}
```

---

TITLE: Handling WebSocket Messages (Receive and Send)
DESCRIPTION: This code block illustrates the core logic within a FastAPI WebSocket endpoint for accepting a connection, continuously receiving text messages, and sending a response back to the client. It utilizes `await websocket.receive_text()` to get data and `await websocket.send_text()` to send data asynchronously.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

---

TITLE: Class Constructor (`__init__`) for Dependencies
DESCRIPTION: This snippet highlights the `__init__` method within a class-based dependency. FastAPI calls this constructor to create an instance of the class, automatically injecting path, query, or other parameters defined in its signature. This mechanism allows the class to encapsulate and process request data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_5

LANGUAGE: Python
CODE:

```
def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
```

---

TITLE: Setting Max Length for Optional Query Parameter - Python
DESCRIPTION: This snippet demonstrates how to use `Query` to add a `max_length` validation to an optional string query parameter `q`. The parameter `q` will be optional (defaulting to `None`), but if provided, its length must not exceed 50 characters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/query-params-str-validations.md#_snippet_2

LANGUAGE: Python
CODE:

```
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
```

---

TITLE: Using a Class Instance as a Dependency in FastAPI
DESCRIPTION: This snippet illustrates how to integrate the instantiated class (`checker`) as a dependency in a FastAPI path operation function. FastAPI will call the `__call__` method of the `checker` instance and inject its return value into the `fixed_content_included` parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/advanced-dependencies.md#_snippet_4

LANGUAGE: Python
CODE:

```
@app.get("/items/")
async def read_items(fixed_content_included: bool = Depends(checker)):
    return {"fixed_content_included": fixed_content_included}
```

---

TITLE: Example of Installing FastAPI with Standard Extras
DESCRIPTION: This command provides an example of installing the FastAPI library along with its 'standard' extra dependencies using pip. It illustrates the typical output of a successful package installation, where packages are downloaded from PyPI and extracted into the Python environment, by default the global one.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_20

LANGUAGE: Console
CODE:

```
// Don't run this now, it's just an example 🤓
$ pip install "fastapi[standard]"
---> 100%
```

---

TITLE: Streaming Response with Async Generator in FastAPI
DESCRIPTION: This snippet shows how to use `StreamingResponse` to stream data using an asynchronous generator. It's suitable for large responses or real-time data, allowing the server to send parts of the response as they become available, rather than waiting for the entire response to be generated.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/custom-response.md#_snippet_8

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

async def generate_large_data():
    for i in range(10):
        yield f"Line {i}\n"
        await asyncio.sleep(0.1)

@app.get("/stream")
async def stream_data():
    return StreamingResponse(generate_large_data(), media_type="text/plain")
```

---

TITLE: Original Optional String Type Hint (Python 3.10+)
DESCRIPTION: This code snippet illustrates the standard Python 3.10+ type hint for an optional string parameter, where `str | None` indicates that the variable `q` can be either a string or `None`. The default value of `None` makes the parameter optional.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_2

LANGUAGE: Python
CODE:

```
q: str | None = None
```

---

TITLE: Using ORJSONResponse for Performance in FastAPI
DESCRIPTION: This snippet demonstrates how to configure a FastAPI path operation to use `ORJSONResponse` for improved performance, especially with large JSON responses. By setting `response_class=ORJSONResponse` in the decorator, FastAPI uses `orjson` for serialization, which is faster than the default JSON encoder. This is suitable when the returned content is guaranteed to be JSON-serializable.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/custom-response.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()

@app.get("/items/", response_class=ORJSONResponse)
async def read_items():
    return {"message": "Hello World"}
```

---

TITLE: Adding Max Length Validation to Optional Query Parameter - FastAPI Python
DESCRIPTION: This snippet extends the `Query()` declaration to include `max_length=50`, adding a string validation rule. FastAPI will automatically validate the input, provide clear error messages for invalid data, and document this constraint in the OpenAPI schema.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/de/docs/tutorial/query-params-str-validations.md#_snippet_5

LANGUAGE: Python
CODE:

```
q: Union[str, None] = Query(default=None, max_length=50)
```

---

TITLE: Testing FastAPI Application with Relative Import
DESCRIPTION: This snippet illustrates how to test a FastAPI application when the test file (`test_main.py`) resides in the same Python package as the application file (`main.py`). It uses a relative import to access the `app` object and then tests the root endpoint using `TestClient`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

---

TITLE: Marking Pytest Functions for Asynchronous Execution with AnyIO
DESCRIPTION: This snippet highlights the `@pytest.mark.anyio` decorator, which is crucial for enabling asynchronous execution within a `pytest` test function. It allows the test to use `await` and interact with asynchronous code, such as `httpx.AsyncClient`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/async-tests.md#_snippet_2

LANGUAGE: Python
CODE:

```
@pytest.mark.anyio
```

---

TITLE: Initializing FastAPI Application with Lifespan
DESCRIPTION: This snippet shows how to integrate the defined `lifespan` async context manager into a FastAPI application by passing it to the `lifespan` parameter during `FastAPI` instance creation. This tells FastAPI to use the specified startup and shutdown logic for the application's lifecycle.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/events.md#_snippet_5

LANGUAGE: Python
CODE:

```
app = FastAPI(lifespan=lifespan)
```

---

TITLE: Adding Basic Type Hints to Function Parameters (Python)
DESCRIPTION: This snippet demonstrates adding basic type hints (`str`) to the `first_name` and `last_name` parameters of a function. This allows editors and tools to provide better autocompletion and error checking, improving developer experience without changing runtime behavior.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_1

LANGUAGE: Python
CODE:

```
def get_full_name(first_name: str, last_name: str):
    return f"{first_name.title()} {last_name.title()}"
```

---

TITLE: Protecting Against Host Header Attacks with TrustedHostMiddleware - Python
DESCRIPTION: Shows how to integrate `TrustedHostMiddleware` to validate the `Host` header of incoming requests, preventing HTTP Host Header attacks. It requires a list of `allowed_hosts`, which can include wildcard domains, and returns a `400` response for invalid hosts.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/middleware.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Declaring List of Models Response in FastAPI (Python)
DESCRIPTION: This snippet shows how to define a FastAPI endpoint that returns a list of Pydantic models. By setting `response_model=List[Item]`, the API expects to return a JSON array where each element conforms to the `Item` Pydantic model. This uses `typing.List` for type hinting.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_10

LANGUAGE: Python
CODE:

```
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/items/", response_model=List[Item])
async def read_items():
    return [{"name": "Foo", "price": 42.0}, {"name": "Bar", "price": 24.0}]
```

---

TITLE: Generate a Random Hexadecimal Secret Key
DESCRIPTION: Uses the `openssl` command-line tool to generate a 32-byte (64-character hexadecimal) random string. This generated string is suitable for use as a `SECRET_KEY` for signing JWTs, ensuring cryptographic strength and uniqueness for security purposes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/oauth2-jwt.md#_snippet_3

LANGUAGE: console
CODE:

```
$ openssl rand -hex 32
```

---

TITLE: Using a Nested Dependency in a FastAPI Path Operation
DESCRIPTION: This snippet illustrates how to integrate the previously defined nested dependency, `query_or_cookie_extractor`, into a FastAPI path operation. FastAPI automatically resolves the dependency chain, ensuring `query_extractor` is executed before `query_or_cookie_extractor`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/sub-dependencies.md#_snippet_2

LANGUAGE: Python
CODE:

```
@app.get("/items/")
async def read_query(query_or_cookie: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_cookie}
```

---

TITLE: Including Admin APIRouter with Custom Config - Python
DESCRIPTION: Includes the 'admin.router' with custom parameters like a '/admin' prefix, 'admin' tag, 'get_token_header' dependency, and a specific response, demonstrating how to configure included routers without modifying their source files. Also adds a direct root route.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/pt/docs/tutorial/bigger-applications.md#_snippet_6

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from .dependencies import get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
```

---

TITLE: Installing python-multipart for File Uploads
DESCRIPTION: This command installs the `python-multipart` library, which is a required dependency for FastAPI to handle file uploads, as files are sent as 'form data'. It's recommended to install it within a virtual environment.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-files.md#_snippet_0

LANGUAGE: console
CODE:

```
$ pip install python-multipart
```

---

TITLE: Setting HTTP Status Code in FastAPI Path Operation (Python)
DESCRIPTION: This snippet demonstrates how to explicitly set the HTTP status code for a FastAPI path operation using the `status_code` parameter in the decorator. It shows setting a '201 Created' status, commonly used after successfully creating a new resource.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/response-status-code.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"message": f"Item {name} created successfully"}
```

---

TITLE: Setting Custom HTTP Status Code for FastAPI Endpoint (Python)
DESCRIPTION: This example shows how to define a FastAPI application and set a custom HTTP status code for a GET endpoint using `status.HTTP_418_IM_A_TEAPOT`. The `status_code` parameter in the `@app.get()` decorator allows specifying the desired response status for the endpoint's successful execution.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/status.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

---

TITLE: Streaming File-like Objects with FastAPI StreamingResponse (Python)
DESCRIPTION: This snippet demonstrates how to use StreamingResponse in FastAPI to efficiently stream content from a file-like object without loading it entirely into memory. It defines a generator function 'iterfile' that yields chunks from the file, ensuring the file is properly closed after the response is sent. This is useful for large files or cloud storage interactions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/custom-response.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, StreamingResponse
from pathlib import Path

app = FastAPI()

# A dummy file for demonstration
dummy_file_path = Path("dummy.txt")
if not dummy_file_path.exists():
    with open(dummy_file_path, "w") as f:
        f.write("This is a dummy file content.\n")
        f.write("It has multiple lines.\n")
        f.write("And will be streamed.\n")

def iterfile():
    with open(dummy_file_path, mode="rb") as file_like:
        yield from file_like

@app.get("/stream-file/")
def stream_file():
    return StreamingResponse(iterfile(), media_type="text/plain")
```

---

TITLE: Type Hinting for Lists (Python 3.6+)
DESCRIPTION: This snippet shows how to declare a type hint for a list containing elements of a specific type using `typing.List`. It requires importing `List` from the `typing` module and specifying the element type (e.g., `str`) within square brackets.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import List

def process_items(items: List[str]):
    for item in items:
        print(item.upper())
```

---

TITLE: Including Scopes in JWT Token Creation in FastAPI
DESCRIPTION: This snippet demonstrates how to include the requested OAuth2 scopes directly into the JWT access token's payload. The `form_data.scopes` property, obtained from the `OAuth2PasswordRequestForm`, contains the list of scopes requested by the client. By embedding these scopes, the token can later be used to verify permissions against protected endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/security/oauth2-scopes.md#_snippet_2

LANGUAGE: Python
CODE:

```
access_token = create_access_token(
    data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
)
```

---

TITLE: Defining an Endpoint with File and Form Parameters - Python
DESCRIPTION: This example demonstrates how to define a FastAPI endpoint that accepts both a file upload (`UploadFile`) and a form field (`Form`). The `UploadFile` type is suitable for handling larger files, while `Form` is used for standard string or numerical form fields. This setup requires the client to send data using the `multipart/form-data` content type.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/request-forms-and-files.md#_snippet_1

LANGUAGE: Python
CODE:

```
@app.post("/files_and_form/")
async def create_file_and_form(
    file: UploadFile,
    token: str = Form(...)
):
    return {
        "filename": file.filename,
        "token": token
    }
```

---

TITLE: Installing Uvicorn with Standard Dependencies (Console)
DESCRIPTION: This command installs the Uvicorn ASGI server along with its recommended standard dependencies, including `uvloop` for high-performance asynchronous operations. It's a prerequisite for manually running a FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/manually.md#_snippet_2

LANGUAGE: console
CODE:

```
pip install "uvicorn[standard]"
```

---

TITLE: Declaring a Class-Based Dependency with Type Hint
DESCRIPTION: This snippet shows the full declaration of a class-based dependency within a path operation. It uses a type hint (`CommonQueryParams`) for `commons` and assigns `Depends(CommonQueryParams)` to indicate that FastAPI should inject an instance of `CommonQueryParams`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_8

LANGUAGE: Python
CODE:

```
commons: CommonQueryParams = Depends(CommonQueryParams)
```

---

TITLE: Defining Deeply Nested Pydantic Models
DESCRIPTION: This snippet demonstrates the creation of arbitrarily deeply nested Pydantic models. It defines `Image`, `Item` (which can contain a list of `Image`s), and `Offer` (which contains a list of `Item`s), showcasing complex data structures with FastAPI.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md#_snippet_12

LANGUAGE: Python
CODE:

```
from typing import Optional
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: set[str] = set()
    images: Optional[list[Image]] = None

class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: list[Item]
```

---

TITLE: Declaring Required Query Parameter with Validation and Ellipsis Default
DESCRIPTION: This snippet declares a required query parameter `q` that can be a string or `None`. By using `default=...` (ellipsis), it explicitly marks the parameter as required, even though its type hint includes `None`. It also applies a `min_length=3` validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_10

LANGUAGE: Python
CODE:

```
q: Union[str, None] = Query(default=..., min_length=3)
```

---

TITLE: Setting Min and Max Length for Optional Query Parameter - Python
DESCRIPTION: This snippet extends the string validation by adding a `min_length` constraint of 3 characters, in addition to the existing `max_length` of 50. If the optional parameter `q` is provided, its length must be between 3 and 50 characters, inclusive.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/query-params-str-validations.md#_snippet_3

LANGUAGE: Python
CODE:

```
async def read_items(
    q: Union[str, None] = Query(default=None, min_length=3, max_length=50)
):
```

---

TITLE: Defining a File Parameter with Bytes in FastAPI
DESCRIPTION: This example shows how to define a file parameter using `File()` with a `bytes` type hint. This approach reads the entire file content into memory, making it suitable for handling small files efficiently.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/request-files.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/file/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}
```

---

TITLE: Creating a Background Task Function in Python
DESCRIPTION: This snippet defines a standard Python function, `write_notification`, intended to be run as a background task. It simulates sending an email by writing a notification message to a log file. Background task functions can be `async def` or `def`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/background-tasks.md#_snippet_1

LANGUAGE: Python
CODE:

```
def write_notification(email: str, message=""):
    with open("log.txt", mode="a") as log:
        log.write(f"notification for {email}: {message}\n")
```

---

TITLE: Importing Pydantic Field in Python
DESCRIPTION: This snippet demonstrates how to import the `Field` class from the `pydantic` library. `Field` is used to define additional validation and metadata for model attributes within Pydantic models, similar to `Query`, `Path`, and `Body` in FastAPI.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-fields.md#_snippet_0

LANGUAGE: Python
CODE:

```
from pydantic import BaseModel, Field
```

---

TITLE: Returning Custom XML Response with FastAPI Response Class
DESCRIPTION: This snippet shows how to return a custom response, in this case XML, using the base `Response` class. It allows specifying the `content`, `status_code`, `headers`, and `media_type` directly, giving full control over the HTTP response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/custom-response.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/legacy-items/")
async def get_legacy_data():
    data = """
    <root>
        <item>Item 1</item>
    </root>
    """
    return Response(content=data, media_type="application/xml")
```

---

TITLE: Defining HeroBase for Shared Model Fields
DESCRIPTION: This snippet defines `HeroBase`, a SQLModel class that serves as a base for other hero-related models. It includes common fields like `name` and `age`, promoting code reuse and consistency across different hero representations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_10

LANGUAGE: Python
CODE:

```
class HeroBase(SQLModel):
    name: str
    age: int | None = None
```

---

TITLE: Using `fastapi.status` Constants for HTTP Status Codes
DESCRIPTION: This snippet illustrates how to use named constants from `fastapi.status` (e.g., `status.HTTP_201_CREATED`) to set HTTP status codes. This approach improves code readability, maintainability, and leverages editor autocompletion, making it less error-prone than using raw numeric codes directly.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/response-status-code.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"message": f"Item {name} created successfully"}
```

---

TITLE: Disabling Dependency Caching without Annotated in FastAPI (Python)
DESCRIPTION: This snippet shows how to disable dependency caching in FastAPI for Python 3.8+ by setting `use_cache=False` directly in the `Depends` function. This ensures the `get_value` dependency is executed for every request, providing a non-cached result.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/sub-dependencies.md#_snippet_4

LANGUAGE: Python
CODE:

```
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
```

---

TITLE: Understanding Required vs. Optional Parameters with Type Hints
DESCRIPTION: Explores the nuance between `Optional[Type]` and `Union[Type, None]` when a parameter does not have a default value. Even if typed as `Optional`, the parameter remains required unless a default value (like `None`) is explicitly provided. This snippet demonstrates the behavior in Python 3.6+ and Python 3.10+.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_14

LANGUAGE: Python
CODE:

```
from typing import Optional

def say_hi(name: Optional[str]):
    if name:
        print(f"Hi, {name}")
    else:
        print("Hi, there!")
```

LANGUAGE: Python
CODE:

```
def say_hi_py310(name: str | None):
    if name:
        print(f"Hi, {name}")
    else:
        print("Hi, there!")
```

---

TITLE: Using fastapi.status for Semantic HTTP Status Codes (Python)
DESCRIPTION: This snippet illustrates how to use the `fastapi.status` module to reference HTTP status codes by their semantic names (e.g., `status.HTTP_201_CREATED`) instead of raw integer values. This approach enhances code readability and leverages editor autocomplete for convenience.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/response-status-code.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"message": f"Item {name} created successfully"}
```

---

TITLE: Receiving and Sending WebSocket Messages
DESCRIPTION: This code demonstrates how to receive text messages from a WebSocket connection using `await websocket.receive_text()` and send text messages back using `await websocket.send_text()`. This forms the core of bidirectional communication within the WebSocket endpoint.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/websockets.md#_snippet_3

LANGUAGE: Python
CODE:

```
while True:
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")
```

---

TITLE: Declaring an Optional Query Parameter with Annotated and Query in FastAPI
DESCRIPTION: This snippet shows how to declare an optional query parameter in FastAPI using `Annotated` and `Query`, while also applying a `min_length` validation. The parameter is made optional by explicitly setting its default value to `None`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_15

LANGUAGE: Python
CODE:

```
q: Annotated[str | None, Query(min_length=3)] = None
```

---

TITLE: Reading Multiple Heroes with HeroPublic in FastAPI
DESCRIPTION: This FastAPI endpoint retrieves a list of all heroes from the database. It uses `response_model=List[HeroPublic]` to ensure that each hero object in the returned list is validated and serialized according to the `HeroPublic` data model.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_16

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter
from sqlmodel import Session, select
from typing import List

# Assuming Hero, HeroPublic are defined
router = APIRouter()

@router.get("/heroes/", response_model=List[HeroPublic])
def read_heroes(*, session: Session):
    heroes = session.exec(select(Hero)).all()
    return heroes
```

---

TITLE: Creating an Enum Class for Predefined Path Parameters in FastAPI
DESCRIPTION: This snippet defines a `ModelName` Enum class that inherits from `str` and `Enum`. It provides predefined string values ('alexnet', 'resnet', 'lenet') for path parameters, allowing FastAPI to validate inputs and generate accurate API documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_7

LANGUAGE: Python
CODE:

```
from enum import Enum

from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```

---

TITLE: Adding Dependencies to FastAPI Path Operation Decorator - Python
DESCRIPTION: This snippet demonstrates how to attach a list of dependencies directly to a FastAPI path operation decorator. These dependencies will be executed before the path operation function, but their return values will not be passed as parameters to the function. This is useful for enforcing prerequisites like authentication or validation without cluttering function signatures.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md#_snippet_0

LANGUAGE: Python
CODE:

```
@app.get("/items/", dependencies=[Depends(verify_key), Depends(verify_token)])
```

---

TITLE: Example Request Body for Multiple Parameters
DESCRIPTION: This JSON object demonstrates the expected structure of the request body when multiple Pydantic models (`item` and `user`) are declared as body parameters. Each model's data is nested under a key corresponding to its parameter name.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body-multiple-params.md#_snippet_3

LANGUAGE: JSON
CODE:

```
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

---

TITLE: Setting Root Path in FastAPI Application Constructor
DESCRIPTION: This Python snippet demonstrates how to configure the `root_path` directly within the `FastAPI` application constructor. This method is an alternative to command-line arguments for informing the application about the path prefix added by a proxy, ensuring correct URL generation and routing.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/behind-a-proxy.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/app")
async def read_main():
    return {"message": "Hello World"}
```

---

TITLE: Declaring a Union Type Hint (Python 3.10+)
DESCRIPTION: This snippet demonstrates the new syntax for declaring a union type in Python 3.10 and above, using the vertical bar (`|`) to separate possible types. This allows a variable to accept values of multiple specified types.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/python-types.md#_snippet_16

LANGUAGE: Python
CODE:

```
item: int | str = 1
```

---

TITLE: Using Union Type Hint with Pipe Operator in Python 3.10+
DESCRIPTION: This snippet shows the Python 3.10+ syntax for defining a `Union` type hint using the pipe (`|`) operator. It indicates that `some_variable` can be either a `PlaneItem` or a `CarItem`, providing a more concise alternative to `typing.Union`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/extra-models.md#_snippet_6

LANGUAGE: Python
CODE:

```
some_variable: PlaneItem | CarItem
```

---

TITLE: FastAPI Lifespan Imports and Shared Model Definition
DESCRIPTION: This snippet shows the necessary imports for defining an async context manager and the declaration of a shared dictionary (`ml_models`) to hold machine learning models. It also includes a placeholder `RegressionModel` class to simulate a real model, demonstrating how shared resources are structured for lifespan management.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/events.md#_snippet_2

LANGUAGE: Python
CODE:

```
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI

# This is a fake model, just to simulate a real one
class RegressionModel:
    def predict(self, x: float):
        return x * 2

ml_models: Dict[str, RegressionModel] = {}
```

---

TITLE: Nested Dataclasses and Pydantic Dataclasses (Python)
DESCRIPTION: This snippet showcases advanced usage of `dataclasses` in FastAPI, including nested structures and the use of `pydantic.dataclasses` as a direct replacement for standard `dataclasses` for enhanced features or specific scenarios. It demonstrates defining complex data models with lists of other dataclasses, using them for both request bodies and response models, and how FastAPI handles serialization of such structures. The code also highlights combining `def` and `async def` route operations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/pt/docs/advanced/dataclasses.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from dataclasses import field
from pydantic.dataclasses import dataclass

app = FastAPI()

@dataclass
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)

@dataclass
class Author:
    name: str
    items: list[Item] = field(default_factory=list)

@app.post("/authors/", response_model=Author)
async def create_author(author: Author):
    return author

@app.post("/items-list/")
async def create_items(items: list[Item]):
    return {"items": items}

@app.get("/authors-list/", response_model=list[Author])
def get_authors_list():
    return [
        {"name": "Author 1", "items": [{"name": "Book 1", "price": 10.0}]},
        {"name": "Author 2", "items": [{"name": "Book 2", "price": 20.0}]}
    ]
```

---

TITLE: Defining HeroUpdate Data Model in Python
DESCRIPTION: This snippet defines the `HeroUpdate` Pydantic model, designed for updating existing hero records. All fields are re-declared as optional with a default value of `None`, allowing clients to send only the fields they wish to modify.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/sql-databases.md#_snippet_14

LANGUAGE: Python
CODE:

```
from typing import Optional
from sqlmodel import Field, SQLModel

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
```

---

TITLE: Type Hinting for Lists (Python 3.9+)
DESCRIPTION: This snippet demonstrates the simplified syntax for type hinting lists in Python 3.9 and later. It allows using the built-in `list` type directly with square brackets to specify the contained element type, eliminating the need to import `List` from `typing`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/python-types.md#_snippet_6

LANGUAGE: Python
CODE:

```
def process_items(items: list[str]):
    for item in items:
        print(item.upper())
```

---

TITLE: Defining a Nested Pydantic Submodel (Image)
DESCRIPTION: This snippet defines a simple Pydantic `Image` model with `url` and `name` attributes. This model can then be used as a type for attributes in other Pydantic models, enabling nested data structures.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md#_snippet_6

LANGUAGE: Python
CODE:

```
class Image(BaseModel):
    url: str
    name: str
```

---

TITLE: Applying Custom APIRoute Class to FastAPI Router
DESCRIPTION: This Python snippet demonstrates how to apply a custom `APIRoute` class, such as `TimedRoute`, to an entire `APIRouter`. By setting the `route_class` parameter during `APIRouter` initialization, all path operations defined within this router will automatically use the specified custom route class, inheriting its modified behavior (e.g., adding response timing headers).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/custom-request-and-route.md#_snippet_4

LANGUAGE: Python
CODE:

```
router = APIRouter(route_class=TimedRoute)
```

---

TITLE: Defining OpenAPI Tags Metadata in FastAPI
DESCRIPTION: This snippet shows how to define a list of dictionaries, `tags_metadata`, to provide additional information for your API tags. Each dictionary can include a `name`, `description` (which supports Markdown), and `externalDocs` for linking to external documentation. This metadata is then passed to the `openapi_tags` argument of the FastAPI application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/metadata.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with **users**.",
        "externalDocs": {
            "description": "Users external docs",
            "url": "https://example.com/docs/users/",
        },
    },
    {
        "name": "items",
        "description": "Manage **items**. So many good items.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)
```

---

TITLE: Running Uvicorn Server Conditionally (Python)
DESCRIPTION: This line of Python code starts the Uvicorn server for the FastAPI application. It is typically placed inside an `if __name__ == "__main__":` block to ensure it only runs when the script is executed directly, not when imported as a module.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/debugging.md#_snippet_3

LANGUAGE: Python
CODE:

```
uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

TITLE: Declaring Cookies with Pydantic Model in FastAPI
DESCRIPTION: This snippet demonstrates how to define a group of related cookie parameters using a Pydantic `BaseModel`. The model is then used as a dependency with `Annotated` and `Cookie()` in a FastAPI path operation, allowing FastAPI to automatically extract and validate cookie values into the Pydantic model instance.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/cookie-param-models.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Annotated
from fastapi import FastAPI, Cookie
from pydantic import BaseModel

app = FastAPI()

class MyCookies(BaseModel):
    hello: str
    foo: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[MyCookies, Cookie()]):
    return {"cookies": cookies.model_dump()}
```

---

TITLE: Defining Form Parameters in FastAPI (Python)
DESCRIPTION: This code illustrates how to define parameters within a FastAPI path operation function using the `Form` dependency. By assigning `Form()` as the default value, FastAPI expects these parameters to be sent as form fields (e.g., `username` and `password` for an OAuth2 password flow), allowing for automatic parsing and validation similar to `Body` or `Query` parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-forms.md#_snippet_2

LANGUAGE: Python
CODE:

```
async def login(username: str = Form(), password: str = Form()):
```

---

TITLE: Setting root_path in FastAPI Application
DESCRIPTION: Illustrates how to explicitly set the `root_path` parameter when initializing the `FastAPI` application instance. This is an alternative to passing it via command-line arguments and is useful when the `root_path` is known at application startup.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/behind-a-proxy.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Importing Custom Response Classes in FastAPI
DESCRIPTION: This snippet demonstrates how to import various custom response classes directly from `fastapi.responses`. These classes allow developers to return specific content types like files, HTML, JSON, plain text, redirects, or streamed data directly from FastAPI path operations, offering fine-grained control over the HTTP response.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/responses.md#_snippet_0

LANGUAGE: python
CODE:

```
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    ORJSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
    UJSONResponse,
)
```

---

TITLE: Query Parameter Numeric Validation: Floats (Greater Than and Less Than)
DESCRIPTION: This snippet illustrates numeric validations for a `float` query parameter. `gt=0` requires the `price` to be strictly greater than 0, and `lt=1000` requires it to be strictly less than 1000, allowing for precise floating-point range constraints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params-numeric-validations.md#_snippet_8

LANGUAGE: Python
CODE:

```
    price: Annotated[
        float,
        Query(
            gt=0,
            lt=1000,
            title="Price of the item",
            description="Price of the item, must be greater than 0 and less than 1000",
            deprecated=True,
        ),
    ],
```

---

TITLE: Path Parameter Numeric Validation: Greater Than or Equal
DESCRIPTION: This snippet shows how to add a numeric validation to a path parameter using `Path`. The `ge=1` argument ensures that the `item_id` integer must be greater than or equal to 1, enforcing a minimum value for the parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params-numeric-validations.md#_snippet_6

LANGUAGE: Python
CODE:

```
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)],
```

---

TITLE: Setting Numeric HTTP Status Code in FastAPI
DESCRIPTION: This snippet demonstrates how to declare a specific HTTP status code (e.g., 201 Created) for a FastAPI path operation by directly passing the numeric code to the `status_code` parameter in the decorator. This ensures the API returns the desired status for successful resource creation, which is then reflected in the OpenAPI documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/response-status-code.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"message": f"Item {name} created successfully"}
```

---

TITLE: Yielded Value Injection (Python)
DESCRIPTION: This snippet highlights the `yield` statement itself. The value yielded by the dependency function is the actual object that FastAPI injects into the path operation function or other dependencies that depend on it.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_1

LANGUAGE: Python
CODE:

```
        yield db
```

---

TITLE: Creating a Custom GzipRequest Class in FastAPI
DESCRIPTION: This Python class, `GzipRequest`, extends FastAPI's `Request` to automatically decompress gzip-encoded request bodies. It overrides the `body()` method to check for the 'Content-Encoding: gzip' header and uses `gzip.decompress` if present, otherwise it processes the body normally. This allows a single route to handle both compressed and uncompressed requests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/custom-request-and-route.md#_snippet_0

LANGUAGE: Python
CODE:

```
import gzip
from starlette.requests import Request
from starlette.types import Message

class GzipRequest(Request):
    async def body(self) -> bytes:
        if "gzip" in self.headers.get("Content-Encoding", ""):
            return gzip.decompress(await super().body())
        return await super().body()
```

---

TITLE: Defining a List of Nested Pydantic Submodels
DESCRIPTION: This snippet shows how to define an attribute as a list containing instances of another Pydantic model (e.g., `list[Image]`). This allows FastAPI to expect, validate, and document a JSON array of complex objects.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md#_snippet_10

LANGUAGE: Python
CODE:

```
images: list[Image]
```

---

TITLE: Validate Special Types with Pydantic in FastAPI
DESCRIPTION: Demonstrates using Pydantic's specialized types, such as `HttpUrl`, to enforce specific data formats and provide enhanced validation and automatic OpenAPI documentation for fields like URLs.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/body-nested-models.md#_snippet_4

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: Union[Image, None] = None
```

---

TITLE: Uvicorn Command with Proxy Headers in Dockerfile
DESCRIPTION: This `CMD` instruction configures Uvicorn to run the FastAPI application, enabling `--proxy-headers`. This option is crucial when the application is deployed behind a proxy like Nginx or Traefik, allowing Uvicorn to correctly interpret X-Forwarded-For and other proxy-related headers.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_6

LANGUAGE: Dockerfile
CODE:

```
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

---

TITLE: Query Parameter List with Default Values (FastAPI)
DESCRIPTION: This snippet shows how to define a query parameter `q` in FastAPI that expects a list of values and provides a default list (`['foo', 'bar']`) if no values are supplied in the URL. This ensures the parameter always has a list value, even when omitted from the request.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_17

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: list[str] = Query(default=["foo", "bar"])):
    results = {"q": q}
    return results
```

---

TITLE: Defining a FastAPI WebSocket Endpoint
DESCRIPTION: This snippet demonstrates how to define a basic WebSocket endpoint in a FastAPI application. It uses the `@app.websocket()` decorator to register the `/ws` path and injects a `WebSocket` object, which is essential for handling bidirectional communication.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/websockets.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Further logic for handling messages goes here
    pass
```

---

TITLE: Handling Username and Password with OAuth2PasswordRequestForm in FastAPI
DESCRIPTION: This snippet demonstrates how to use `OAuth2PasswordRequestForm` with FastAPI's `Depends` to handle incoming `username` and `password` credentials for OAuth2 token requests. It automatically parses form data, including optional `scope` and `grant_type` fields, simplifying the process of receiving authentication data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/simple-oauth2.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authentication logic will go here
    pass
```

---

TITLE: Importing APIRouter Modules (Avoiding Collisions) - Python
DESCRIPTION: Imports the 'items' and 'users' router modules directly from the 'routers' package to prevent potential name collisions if their 'router' variables were imported individually.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/pt/docs/tutorial/bigger-applications.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

from .routers import items, users
```

---

TITLE: Running Pytest Tests for FastAPI Application
DESCRIPTION: This command executes the `pytest` test runner, which automatically discovers and runs all tests within the project directory. The output provides a summary of the test session, including collected items and the final test results, indicating successful completion of all tests.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/testing.md#_snippet_6

LANGUAGE: Bash
CODE:

```
pytest
```

---

TITLE: Generating Bearer Access Token Response in FastAPI
DESCRIPTION: This snippet illustrates how to construct the response for a successful token request. It returns a JSON object containing `access_token` (here, a placeholder using the username) and `token_type` set to 'bearer', adhering to OAuth2 specifications for token issuance.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/security/simple-oauth2.md#_snippet_3

LANGUAGE: Python
CODE:

```
# ... (inside your login function, after successful validation)
return {"access_token": user.username, "token_type": "bearer"}
```

---

TITLE: Defining Optional Query Parameter with Default None (Python 3.10+)
DESCRIPTION: This snippet defines an optional query parameter `q` using the Python 3.10+ `str | None` syntax. Assigning `None` as the default value makes the parameter optional, and FastAPI handles the default behavior.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_3

LANGUAGE: Python
CODE:

```
q: str | None = None
```

---

TITLE: Handling Optional File Uploads in FastAPI
DESCRIPTION: This snippet demonstrates how to define optional file parameters using `Union[bytes, None]` or `Union[UploadFile, None]` in FastAPI path operations. It checks if a file was provided and returns a message or its size/details accordingly, allowing clients to send requests without a file.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-files.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Union

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_file(file: Union[bytes, None] = None):
    if not file:
        return {"message": "No file sent"}
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No upload file sent"}
    return {"filename": file.filename, "content_type": file.content_type}
```

---

TITLE: Implementing a TimedRoute Custom APIRoute Class in FastAPI
DESCRIPTION: This Python class, `TimedRoute`, extends `fastapi.routing.APIRoute` to measure and report the response time of path operations. It overrides `get_route_handler()` to wrap the original handler, recording the start and end times, calculating the duration, and adding an 'X-Response-Time' header to the response before returning it. This provides a simple way to monitor API performance.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/custom-request-and-route.md#_snippet_5

LANGUAGE: Python
CODE:

```
import time
from fastapi.routing import APIRoute
from starlette.responses import Response

class TimedRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request) -> Response:
            start_time = time.time()
            response = await original_route_handler(request)
            process_time = time.time() - start_time
            response.headers["X-Response-Time"] = str(process_time)
            return response
        return custom_route_handler
```

---

TITLE: Shorthand Dependency Declaration
DESCRIPTION: This snippet introduces a shorthand for declaring class-based dependencies. When the type hint for the parameter is the same as the class to be instantiated, you can simply use `Depends()` without passing the class name again, making the code more concise.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_14

LANGUAGE: Python
CODE:

```
commons: CommonQueryParams = Depends()
```

---

TITLE: Execution Flow of FastAPI Dependencies with Yield
DESCRIPTION: This Mermaid sequence diagram illustrates the detailed execution flow of FastAPI dependencies that utilize `yield`. It shows the interaction between the client, dependency, path operation, exception handler, and background tasks, highlighting points where exceptions can be raised and handled, and when responses are sent.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_7

LANGUAGE: Mermaid
CODE:

```
sequenceDiagram

participant client as Client
participant handler as Exception handler
participant dep as Dep with yield
participant operation as Path Operation
participant tasks as Background tasks

    Note over client,operation: Can raise exceptions, including HTTPException
    client ->> dep: Start request
    Note over dep: Run code up to yield
    opt raise Exception
        dep -->> handler: Raise Exception
        handler -->> client: HTTP error response
    end
    dep ->> operation: Run dependency, e.g. DB session
    opt raise
        operation -->> dep: Raise Exception (e.g. HTTPException)
        opt handle
            dep -->> dep: Can catch exception, raise a new HTTPException, raise other exception
        end
        handler -->> client: HTTP error response
    end

    operation ->> client: Return response to client
    Note over client,operation: Response is already sent, can't change it anymore
    opt Tasks
        operation -->> tasks: Send background tasks
    end
    opt Raise other exception
        tasks -->> tasks: Handle exceptions in the background task code
    end
```

---

TITLE: Defining a List of Strings in FastAPI with Pydantic
DESCRIPTION: This snippet shows how to define a Pydantic model attribute as a list specifically containing string elements. By declaring `tags: list[str]`, FastAPI will validate and document the field as an array of strings.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-nested-models.md#_snippet_4

LANGUAGE: Python
CODE:

```
tags: list[str]
```

---

TITLE: Returning JSON Response with Item Name and ID in FastAPI (Python)
DESCRIPTION: This code snippet illustrates a typical return statement in a FastAPI endpoint, constructing a dictionary that will be automatically converted to a JSON response. It demonstrates accessing attributes (`item.name`) from a declared model and including path/query parameters (`item_id`). This line is part of a larger function that would define an API endpoint.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/index.md#_snippet_10

LANGUAGE: Python
CODE:

```
    return {"item_name": item.name, "item_id": item_id}
```

---

TITLE: Incorrect Default Value Assignment with Annotated and Query - FastAPI Python
DESCRIPTION: This snippet demonstrates an incorrect way to define a parameter using `Annotated` with `Query`. It's problematic because both `Query(default="rick")` and the function parameter default `="morty"` provide conflicting default values, leading to ambiguity and potential errors.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/de/docs/tutorial/query-params-str-validations.md#_snippet_6

LANGUAGE: Python
CODE:

```
q: Annotated[str, Query(default="rick")] = "morty"
```

---

TITLE: Organizing FastAPI Endpoints with Tags
DESCRIPTION: This Python snippet illustrates the use of `tags` in FastAPI path operations to group related endpoints. Tags help in organizing the generated OpenAPI documentation, leading to better structured and more manageable client services, such as `ItemsService` and `UsersService`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/generate-clients.md#_snippet_4

LANGUAGE: Python
CODE:

```
@app.post("/items/", response_model=ResponseMessage, tags=["items"])
@app.get("/items/", response_model=Item, tags=["items"])
@app.post("/users/", response_model=ResponseMessage, tags=["users"])
```

---

TITLE: Using a Nested Dependency in a FastAPI Path Operation (Python)
DESCRIPTION: This snippet illustrates how to integrate the `query_or_cookie_extractor` dependency into a FastAPI path operation function. FastAPI automatically resolves the nested `query_extractor` dependency first, passing its result to `query_or_cookie_extractor` before executing the path operation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/sub-dependencies.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q": query_or_default}
```

---

TITLE: Declaring Form Fields with FastAPI and Pydantic
DESCRIPTION: This snippet demonstrates how to define form fields in FastAPI using the `Form` dependency. Although a Pydantic `User` model is defined, the endpoint directly uses `Form()` for `username` and `password` parameters, allowing FastAPI to extract them from the request's form data.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-form-models.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password": password}
```

---

TITLE: Including Router within Another Router - Python
DESCRIPTION: Shows how to include one 'APIRouter' instance ('other_router') into another 'APIRouter' instance ('router') using the 'router.include_router()' method. This allows for nesting routers and organizing routes hierarchically before including the parent router in the main application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_12

LANGUAGE: Python
CODE:

```
router.include_router(other_router)
```

---

TITLE: Returning File Path with FastAPI FileResponse Class (Python)
DESCRIPTION: This snippet shows an alternative way to use FileResponse by specifying it as the response_class in the path operation decorator. This allows the path operation function to directly return the file path string, simplifying the return statement while still leveraging FileResponse for streaming and header management.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/custom-response.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

some_file_path = Path("large-video-file.mp4")
# Create a dummy file for demonstration if it doesn't exist
if not some_file_path.exists():
    with open(some_file_path, "wb") as f:
        f.write(b"This is a dummy video file content.") # Placeholder content

@app.get("/video", response_class=FileResponse)
async def get_video():
    return some_file_path
```

---

TITLE: FastAPI Return Dictionary Example
DESCRIPTION: Illustrates a typical return statement in a FastAPI endpoint, returning a dictionary that is automatically converted to JSON. It references attributes from a declared `item` object and an `item_id` path parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/README.md#_snippet_8

LANGUAGE: Python
CODE:

```
    return {"item_name": item.name, "item_id": item_id}
```

---

TITLE: Declaring Optional Query Parameters - FastAPI Python
DESCRIPTION: This example shows how to define an optional query parameter `q` by setting its default value to `None`. If the parameter is not provided in the URL, its value will be `None` within the function, allowing for flexible API endpoints.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

---

TITLE: Declaring an Optional Query Parameter with None Default
DESCRIPTION: This snippet declares an optional query parameter `q` that can be either a string or `None`. By setting its default value to `None`, FastAPI treats it as an optional parameter.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_6

LANGUAGE: Python
CODE:

```
q: Union[str, None] = None
```

---

TITLE: Example Callback Implementation using HTTPX
DESCRIPTION: This code demonstrates a simple implementation of an API callback. It sends a POST request to a predefined `callback_url` with a JSON payload indicating an invoice payment. This is an example of the actual HTTP request your API would make.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/openapi-callbacks.md#_snippet_1

LANGUAGE: Python
CODE:

```
callback_url = "https://example.com/api/v1/invoices/events/"
httpx.post(callback_url, json={"description": "Invoice paid", "paid": True})
```

---

TITLE: Declaring Additional Media Types for Responses (Python)
DESCRIPTION: This snippet shows how to define multiple media types for a single HTTP status code within the `responses` parameter. It configures the `200` response to potentially return either `application/json` or `image/png`, demonstrating how to serve different content types from a single path operation, including returning a `FileResponse`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/additional-responses.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    responses={
        200: {
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Item"}
                },
                "image/png": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
            "description": "Return the JSON item or an image."
        }
    }
)
async def read_item(item_id: str, img: bool = False):
    if img:
        return FileResponse("image.png", media_type="image/png")
    return {"id": "foo", "value": "The Foo Wrestlers"}
```

---

TITLE: Handling Optional File Uploads
DESCRIPTION: This snippet illustrates how to make file uploads optional using `Optional` from `typing` and setting the default value to `None`. It shows examples for both `bytes` and `UploadFile` types. If no file is provided, a specific message is returned; otherwise, file details are processed.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/request-files.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing import Optional

from fastapi import FastAPI, File

app = FastAPI()

@app.post("/files/")
async def create_file(file: Optional[bytes] = File(None)):
    if not file:
        return {"message": "No file sent"}
    return {"file_size": len(file)}
```

LANGUAGE: Python
CODE:

```
from typing import Optional

from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: Optional[UploadFile] = None):
    if not file:
        return {"message": "No upload file sent"}
    return {"filename": file.filename, "content_type": file.content_type}
```

---

TITLE: Defining Nested Response Models with Pydantic Dataclasses in FastAPI
DESCRIPTION: This snippet demonstrates how to use `pydantic.dataclasses` to define complex, nested response models in FastAPI. It shows the creation of `Item` and `Author` dataclasses, where `Author` contains a list of `Item` objects. The `response_model` parameter in the path operation decorator is used to specify the `Author` dataclass, enabling automatic data validation, serialization, and OpenAPI documentation generation for the nested structure. The example also highlights that the path operation can return a plain dictionary, which FastAPI will automatically convert to the specified `response_model` type.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/dataclasses.md#_snippet_0

LANGUAGE: Python
CODE:

```
from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

@dataclass
class Item:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Optional[str] = None
    tax: Optional[float] = None

@dataclass
class Author:
    name: str
    items: List[Item]

from fastapi import FastAPI

app = FastAPI()

@app.get("/authors/{author_id}", response_model=Author)
def get_author(author_id: str):
    return {
        "name": "John Doe",
        "items": [
            {"name": "Item A", "price": 10.0, "tags": ["tag1", "tag2"]},
            {"name": "Item B", "price": 20.0, "description": "A description"},
        ],
    }
```

---

TITLE: Setting Cookies via Injected Response Object in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to set an HTTP cookie by declaring a `Response` object as a parameter in a FastAPI path operation function. The `response.set_cookie()` method is used to add a cookie to the response, which FastAPI then automatically includes in the final HTTP response sent to the client. This method is suitable when you want to return a standard Python dictionary or Pydantic model, and FastAPI handles the serialization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/response-cookies.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/items/")
async def read_items(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-value")
    return {"message": "Come to the dark side, we have cookies"}
```

---

TITLE: Accessing Request Object for Client Host in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to declare and use the `Request` object directly in a FastAPI path operation function. It allows access to raw request details, such as the client's host IP address, which are not automatically extracted or validated by FastAPI's standard parameter handling. While useful for specific needs, direct `Request` object access bypasses FastAPI's automatic data validation, conversion, and OpenAPI documentation for the accessed fields.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/using-request-directly.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items/{item_id}")
async def read_root(item_id: str, request: Request):
    client_host = request.client.host
    return {"client_host": client_host, "item_id": item_id}
```

---

TITLE: Importing StaticFiles Class in FastAPI (Python)
DESCRIPTION: This snippet demonstrates how to import the `StaticFiles` class from `fastapi.staticfiles`. This class is essential for configuring FastAPI applications to serve static assets such as CSS, JavaScript, and images from a specified directory.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/reference/staticfiles.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi.staticfiles import StaticFiles
```

---

TITLE: Defining Optional Query Parameter with Default None (Union)
DESCRIPTION: This snippet defines an optional query parameter `q` of type `Union[str, None]`. By assigning `None` as the default value, FastAPI automatically infers that the parameter is optional and defaults to `None` if not provided.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/query-params-str-validations.md#_snippet_1

LANGUAGE: Python
CODE:

```
q: Union[str, None] = None
```

---

TITLE: Importing Routers as Modules (Python)
DESCRIPTION: Imports APIRouter instances by importing their containing modules (items, users) to prevent name collisions when multiple modules export variables with the same name (router).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/bigger-applications.md#_snippet_16

LANGUAGE: Python
CODE:

```
from .routers import items, users
```

---

TITLE: Caching Function Results with functools.lru_cache in Python
DESCRIPTION: This snippet illustrates the application of the `@lru_cache` decorator from Python's `functools` module. It caches the return values of the `say_hi` function based on its input arguments, ensuring that the function's logic is executed only once for each distinct combination of `name` and `salutation`, thereby optimizing performance by avoiding redundant computations.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/settings.md#_snippet_11

LANGUAGE: Python
CODE:

```
@lru_cache
def say_hi(name: str, salutation: str = "Ms."):
    return f"Hello {salutation} {name}"
```

---

TITLE: Unpacking Dictionary with Additional Keyword Arguments in Python
DESCRIPTION: This snippet shows how to create a Pydantic model instance by unpacking a dictionary (`user_in.dict()`) and simultaneously adding or overriding specific keyword arguments (`hashed_password`). This is useful for injecting new data or modifying existing fields when transforming data between models, such as adding a hashed password during user creation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_6

LANGUAGE: Python
CODE:

```
UserInDB(**user_in.dict(), hashed_password=hashed_password)
```

---

TITLE: Defining a Background Task Function
DESCRIPTION: This Python function `write_notification` serves as a background task. It takes an `email` and an optional `message` and appends a notification string to a `log.txt` file. Background task functions can be regular `def` or `async def` functions, as FastAPI handles their execution appropriately.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/background-tasks.md#_snippet_1

LANGUAGE: Python
CODE:

```
def write_notification(email: str, message=""):
    with open("log.txt", "a") as log:
        log.write(f"notification for {email}: {message}\n")
```

---

TITLE: Add .gitignore to Exclude Virtual Environment from Git
DESCRIPTION: Add a `.gitignore` file inside the `.venv` directory to prevent Git from tracking virtual environment files. This is crucial for maintaining clean repositories and avoiding unnecessary commits of generated files.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/ja/docs/virtual-environments.md#_snippet_9

LANGUAGE: console
CODE:

```
$ echo "*" > .venv/.gitignore
```

---

TITLE: Defining a Simple FastAPI Application
DESCRIPTION: This code defines a basic FastAPI application with a single GET endpoint at the root path. This structure is typical for the main application file (`main.py`) when separating application logic from test files in a larger project.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/testing.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}
```

---

TITLE: Overriding Request Validation Exception Handler in FastAPI
DESCRIPTION: This snippet demonstrates how to override the default `RequestValidationError` handler in FastAPI. It defines a custom exception handler that converts validation errors into a plain text response, providing a simpler error message to the client instead of the default JSON format.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_7

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
```

---

TITLE: Creating a Custom GzipRoute Class for FastAPI
DESCRIPTION: This Python class, `GzipRoute`, extends `fastapi.routing.APIRoute` to integrate the custom `GzipRequest`. It overrides `get_route_handler()` to ensure that incoming requests are wrapped in a `GzipRequest` instance before being passed to the path operation. This enables automatic gzip decompression for all path operations using this route class.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/custom-request-and-route.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi.routing import APIRoute
from starlette.responses import Response

class GzipRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)
        return custom_route_handler
```

---

TITLE: Returning Data from FastAPI Endpoint
DESCRIPTION: This code snippet demonstrates a typical return statement for a FastAPI endpoint. It shows how to construct a dictionary response by accessing properties like `item.name` from a typed object and including other parameters like `item_id`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/index.md#_snippet_9

LANGUAGE: Python
CODE:

```
    return {"item_name": item.name, "item_id": item_id}
```

---

TITLE: Handling GZip Responses with GZipMiddleware - Python
DESCRIPTION: Demonstrates how to use `GZipMiddleware` to automatically compress responses with GZip if the client's `Accept-Encoding` header includes "gzip". It supports `minimum_size` to avoid compressing small responses and `compresslevel` for compression quality.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/advanced/middleware.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
```

---

TITLE: Initializing a Pydantic Model Instance (UserIn) in Python
DESCRIPTION: This snippet demonstrates how to create an instance of the `UserIn` Pydantic model, providing values for its `username`, `password`, and `email` fields. This is a typical way to instantiate a data model before processing or validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/extra-models.md#_snippet_0

LANGUAGE: Python
CODE:

```
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

---

TITLE: Deprecating Query Parameters in FastAPI
DESCRIPTION: This snippet illustrates how to mark a query parameter as `deprecated` using `Query(deprecated=True)`. This flag is reflected in the OpenAPI documentation, signaling to API consumers that the parameter is obsolete and its use is discouraged, while still supporting existing clients.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_22

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: str | None = Query(
        default=None,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        deprecated=True,
    )
):
    results = {"q": q}
    return results
```

---

TITLE: Python 3.10 Union Type Annotation Syntax
DESCRIPTION: This snippet illustrates the simplified syntax for `Union` type annotations introduced in Python 3.10, using the vertical bar (`|`) operator. This syntax is valid for type annotations but not for passing as an argument value like `response_model` in FastAPI, where `typing.Union` must still be used.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/extra-models.md#_snippet_9

LANGUAGE: Python
CODE:

```
some_variable: PlaneItem | CarItem
```

---

TITLE: Recommended CMD Exec Form for FastAPI
DESCRIPTION: Illustrates the correct 'exec' form for the `CMD` instruction in a Dockerfile, which is crucial for FastAPI applications to ensure proper shutdown and trigger lifespan events. This form passes arguments as a JSON array.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_6

LANGUAGE: Dockerfile
CODE:

```
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

---

TITLE: Using Jinja2Templates in FastAPI
DESCRIPTION: This Python snippet demonstrates how to integrate `Jinja2Templates` into a FastAPI application. It involves initializing `Jinja2Templates` with a directory, defining a path operation that accepts a `Request` object, and returning a `TemplateResponse` with the template name, request object, and a context dictionary containing data for the template.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/ko/docs/advanced/templates.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        name="item.html",
        request=request,
        context={"id": id}
    )
```

---

TITLE: Using Jinja2Templates in FastAPI
DESCRIPTION: This snippet demonstrates how to integrate Jinja2 templates into a FastAPI application. It shows how to initialize `Jinja2Templates`, declare a `Request` object in a path operation, and render an HTML template using `TemplateResponse`, passing the `request` object and other data to the template context.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/templates.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
```

---

TITLE: Returning a Response Object Directly with Headers in FastAPI (Python)
DESCRIPTION: This snippet illustrates how to return a `Response` object directly from a FastAPI path operation, allowing full control over the response content, status code, and headers. Custom headers are passed as a dictionary to the `headers` parameter of the `Response` constructor.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/response-headers.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/items/")
def read_items():
    content = {"message": "Hello World"}
    headers = {"X-Cat-Dog": "Hello from the other side"}
    return Response(content=str(content), headers=headers)
```

---

TITLE: Running Uvicorn with Proxy Headers in Docker
DESCRIPTION: This command extends the basic Uvicorn execution by adding the '--proxy-headers' flag. This is crucial when the application is deployed behind a reverse proxy (like Nginx or Traefik) or a load balancer, as it instructs Uvicorn to trust X-Forwarded-For/Proto/Host headers, correctly identifying the client's original IP and protocol.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_19

LANGUAGE: Dockerfile
CODE:

```
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
```

---

TITLE: Initializing FastAPI APIRouter for Callbacks
DESCRIPTION: This snippet initializes an `APIRouter` instance specifically for defining and documenting OpenAPI callbacks. This router will contain the path operations that describe the external API expected by your service for callback notifications.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/openapi-callbacks.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import APIRouter, FastAPI, status

invoices_callback_router = APIRouter()
```

---

TITLE: Installing openapi-ts for Frontend Client Generation
DESCRIPTION: This command installs the `@hey-api/openapi-ts` package as a development dependency in a frontend project. This tool is used to generate TypeScript client code from an OpenAPI specification, enabling type-safe API interactions.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/generate-clients.md#_snippet_1

LANGUAGE: Shell
CODE:

```
npm install @hey-api/openapi-ts --save-dev
```

---

TITLE: Installing OpenAPI TypeScript Generator
DESCRIPTION: This shell command installs the `@hey-api/openapi-ts` package as a development dependency. This tool is essential for generating TypeScript API clients from an OpenAPI specification, enabling type-safe interactions with your FastAPI backend.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/generate-clients.md#_snippet_1

LANGUAGE: Shell
CODE:

```
npm install @hey-api/openapi-ts --save-dev
```

---

TITLE: Returning a Generic Response Object in FastAPI
DESCRIPTION: This snippet shows how to return a generic `Response` object directly from a FastAPI endpoint. This provides maximum control over the response content, status code, headers, and media type. However, using the base `Response` class directly means FastAPI will not automatically generate OpenAPI documentation for the response body or perform any serialization.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/custom-response.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/legacy-items/")
async def read_legacy_items():
    data = """<?xml version="1.0"?>
    <shampoo>
        <Liquid>
            <Aqua>Water</Aqua>
            <SodiumLaurethSulfate/>
            <CocamidopropylBetaine/>
        </Liquid>
        <Bar>
            <SodiumPalmate/>
            <SodiumCocoate/>
            <SodiumPalmKernelate/>
        </Bar>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")
```

---

TITLE: Defining a Custom GzipRequest Class in FastAPI
DESCRIPTION: This class extends FastAPI's `Request` to automatically decompress gzipped request bodies. It overrides the `body()` method to check for the 'Content-Encoding: gzip' header and decompresses the body if present, caching the result for subsequent access. This allows route handlers to receive uncompressed data transparently.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/how-to/custom-request-and-route.md#_snippet_0

LANGUAGE: Python
CODE:

```
class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.get("Content-Encoding", ""):
                body = gzip.decompress(body)
            self._body = body
        return self._body
```

---

TITLE: Handling Multiple File Uploads in FastAPI
DESCRIPTION: This snippet shows how to accept multiple file uploads associated with the same form field by declaring a parameter as `List[bytes]` or `List[UploadFile]`. FastAPI automatically handles parsing these files from the `multipart/form-data` request, returning a list of the respective file types.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-files.md#_snippet_5

LANGUAGE: Python
CODE:

```
from typing import List

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files/")
async def create_files(files: List[bytes]):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile]):
    return {"filenames": [file.filename for file in files]}
```

---

TITLE: Handling Multiple File Uploads in FastAPI
DESCRIPTION: This example shows how to handle multiple file uploads by declaring the parameter type as a `List[bytes]` or `List[UploadFile]`. FastAPI automatically parses multiple files sent under the same form field, providing them as a list.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/request-files.md#_snippet_7

LANGUAGE: Python
CODE:

```
from typing import List
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/multiple_bytes_files/")
async def create_multiple_bytes_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(f) for f in files]}

@app.post("/multiple_upload_files/")
async def create_multiple_upload_files(files: List[UploadFile]):
    return {"filenames": [f.filename for f in files]}
```

---

TITLE: Excluding Unset Fields from FastAPI Response Model
DESCRIPTION: This snippet demonstrates using `response_model_exclude_unset=True` in a FastAPI path operation decorator. When set, FastAPI will only include fields in the JSON response that were explicitly set (i.e., not using their default values) in the Pydantic model, reducing response payload size for optional or default-valued fields.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/response-model.md#_snippet_7

LANGUAGE: Python
CODE:

```
from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []

app = FastAPI()

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []}
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
```

---

TITLE: Other FastAPI HTTP Operation Decorators
DESCRIPTION: This snippet lists various HTTP method decorators available in FastAPI, beyond just `GET`. These decorators (`@app.post()`, `@app.put()`, `@app.delete()`, etc.) are used to define functions that handle specific HTTP operations for a given path, allowing for comprehensive API design based on standard HTTP verbs.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/first-steps.md#_snippet_8

LANGUAGE: Python
CODE:

```
@app.post()
@app.put()
@app.delete()
@app.options()
@app.head()
@app.patch()
@app.trace()
```

---

TITLE: Pinning FastAPI to an Exact Version in requirements.txt
DESCRIPTION: This snippet demonstrates how to pin FastAPI to a specific exact version (e.g., 0.112.0) in a `requirements.txt` file. This ensures that your application always uses the tested and compatible version, preventing unexpected breaking changes from newer releases.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/versions.md#_snippet_0

LANGUAGE: txt
CODE:

```
fastapi[standard]==0.112.0
```

---

TITLE: Adding Examples to Pydantic Fields
DESCRIPTION: This snippet demonstrates how to declare examples directly on individual fields within a Pydantic model using the `Field()` function's `examples` argument. This method allows for specifying sample values for specific attributes, enhancing the clarity of the generated JSON Schema and OpenAPI documentation for each field.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/schema-extra-example.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Annotated[str | None, Field(examples=["A very long description"])] = None
    price: float = Field(examples=[35.4])
    tax: float | None = None
```

---

TITLE: Optimizing Settings Instantiation with lru_cache - Python
DESCRIPTION: This snippet shows how to use the `@lru_cache` decorator from `functools` to ensure that the `get_settings` function, which instantiates the `Settings` object, is executed only once. This prevents redundant file reads or expensive object creations on subsequent calls, significantly improving performance in a web application context.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/settings.md#_snippet_16

LANGUAGE: Python
CODE:

```
from functools import lru_cache
from fastapi import Depends, FastAPI
from .config import Settings

@lru_cache
def get_settings():
    return Settings()

app = FastAPI()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email
    }
```

---

TITLE: Ordering Parameters with Query and Path in FastAPI
DESCRIPTION: This snippet illustrates how to correctly order parameters when mixing a required query parameter without `Query` and a path parameter with `Path`. Python requires parameters without default values to come before those with default values.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/path-params-numeric-validations.md#_snippet_2

LANGUAGE: Python
CODE:

```
@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

---

TITLE: Returning Enum Members from FastAPI Path Operations
DESCRIPTION: This snippet illustrates how to return Enum members directly from a FastAPI path operation. FastAPI automatically converts these Enum members to their corresponding string values in the JSON response sent to the client.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/path-params.md#_snippet_11

LANGUAGE: Python
CODE:

```
            return {"model_name": model_name, "message": "Deep Learning FTW!"}
        if model_name.value == "lenet":
            return {"model_name": model_name, "message": "LeNet Famous!"}
        return {"model_name": model_name, "message": "Have some residuals"}
```

---

TITLE: Using a Pydantic Model as Request Body in FastAPI
DESCRIPTION: This FastAPI path operation demonstrates how the `Item` Pydantic model is used as an input (request body). When a model with default values is used for input, fields like `description` are considered optional in the generated OpenAPI schema, indicating that clients are not required to provide them in the request.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/how-to/separate-openapi-schemas.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

---

TITLE: Installing Python Packages from requirements.txt using uv
DESCRIPTION: Installs all packages specified in the `requirements.txt` file using `uv`'s `pip install` command. This provides a faster alternative to `pip` for installing project dependencies from a requirements file.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_14

LANGUAGE: console
CODE:

```
$ uv pip install -r requirements.txt
---> 100%
```

---

TITLE: Incorrect CMD Shell Form for FastAPI (Avoid)
DESCRIPTION: Demonstrates the 'shell' form of the `CMD` instruction, which should be avoided for FastAPI applications. This form can prevent graceful shutdowns and proper handling of lifespan events due to how Docker processes the command.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_7

LANGUAGE: Dockerfile
CODE:

```
CMD fastapi run app/main.py --port 80
```

---

TITLE: Reading UploadFile Contents Synchronously
DESCRIPTION: This Python snippet shows how to synchronously read the contents of an `UploadFile` object when inside a normal `def` path operation function. It directly accesses the underlying `SpooledTemporaryFile` object via `myfile.file` to perform the read operation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/request-files.md#_snippet_2

LANGUAGE: python
CODE:

```
contents = myfile.file.read()
```

---

TITLE: Documenting and Overriding HTML Response in FastAPI
DESCRIPTION: This example demonstrates how to both override the response by returning an `HTMLResponse` object and ensure proper OpenAPI documentation. By setting `response_class=HTMLResponse` in the decorator, FastAPI documents the media type as `text/html`, even though the function directly returns a `Response` object.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/custom-response.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

app = FastAPI()

def generate_html_response():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/items/", response_class=HTMLResponse)
async def read_items():
    return generate_html_response()
```

---

TITLE: Executing Python Program with Environment Variables in Bash
DESCRIPTION: This console snippet demonstrates running a Python script (`main.py`) in a Bash terminal. It shows the output when `MY_NAME` is not set (using the default value) and then when `MY_NAME` is set using `export`, illustrating how the Python script dynamically reads the environment variable.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/environment-variables.md#_snippet_3

LANGUAGE: console
CODE:

```
// Here we don't set the env var yet
$ python main.py

// As we didn't set the env var, we get the default value

Hello World from Python

// But if we create an environment variable first
$ export MY_NAME="Wade Wilson"

// And then call the program again
$ python main.py

// Now it can read the environment variable

Hello Wade Wilson from Python
```

---

TITLE: Instantiating Pydantic Models in Python
DESCRIPTION: This code illustrates how to create instances of a Pydantic model, 'User', using both direct keyword arguments and dictionary unpacking. It shows flexible ways to populate model data, leveraging Python's type hints for clarity and validation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/features.md#_snippet_1

LANGUAGE: Python
CODE:

```
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30"
}

my_second_user: User = User(**second_user_data)
```

---

TITLE: Wrapping Optional Type Hint with Annotated (Python 3.10+)
DESCRIPTION: This snippet demonstrates how to wrap an optional string type hint (`str | None`) with `Annotated` in Python 3.10+. `Annotated` allows adding metadata, such as validation rules, to type hints without altering the core type, preparing it for FastAPI's advanced parameter handling.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/query-params-str-validations.md#_snippet_4

LANGUAGE: Python
CODE:

```
q: Annotated[str | None] = None
```

---

TITLE: Implementing Simple HTTP Basic Auth in FastAPI
DESCRIPTION: This snippet demonstrates the basic setup for HTTP Basic Authentication in FastAPI. It imports `HTTPBasic` and `HTTPBasicCredentials`, initializes `HTTPBasic` as a security dependency, and uses it in a path operation to receive and process user credentials.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/security/http-basic-auth.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic_auth = HTTPBasic()

@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(basic_auth)):
    return {"username": credentials.username, "password": credentials.password}
```

---

TITLE: Defining an Optional Request Body Parameter in FastAPI
DESCRIPTION: This snippet demonstrates how to declare an optional request body parameter using a Pydantic model. By setting the default value to `None`, FastAPI understands that the entire body is optional. This allows clients to send requests without a body if desired.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/body-multiple-params.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Union[Item, None] = None):
    results = {"item_id": item_id, "item": item}
    return results
```

---

TITLE: Building a Docker Image (Console)
DESCRIPTION: This console command builds a Docker image from the current directory (`.`) where the `Dockerfile` is located. The `-t myimage` flag tags the resulting image with the name `myimage`, making it easy to reference and run containers from this image later.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_12

LANGUAGE: console
CODE:

```
docker build -t myimage .
```

---

TITLE: Setting Cookies by Returning a Direct Response Object in FastAPI (Python)
DESCRIPTION: This snippet illustrates how to set an HTTP cookie by directly instantiating and returning a `Response` object (e.g., `JSONResponse`). The `response.set_cookie()` method is called on the created response object before it is returned. This approach gives full control over the response, including its content type and headers, but requires manual serialization of the response body if not using a specialized response class like `JSONResponse`.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/response-cookies.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/items-direct/")
async def read_items_direct():
    content = {"message": "Hello from the dark side!"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-value-direct")
    return response
```

---

TITLE: Adding Custom ASGI Middleware with FastAPI's `add_middleware()` - Python
DESCRIPTION: This snippet illustrates the recommended way to add custom ASGI middleware in FastAPI using `app.add_middleware()`. This method ensures proper integration with FastAPI's internal error handling and custom exception handlers. The middleware class is passed as the first argument, followed by any configuration parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/middleware.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from unicorn import UnicornMiddleware

app = FastAPI()

app.add_middleware(UnicornMiddleware, some_config="rainbow")
```

---

TITLE: Running Uvicorn with Docker CMD
DESCRIPTION: This Docker `CMD` instruction defines the default command to execute when a container starts. It runs the Uvicorn server, serving the FastAPI application instance named `app` from the `main` module (e.g., `main.py`) on all available network interfaces (`0.0.0.0`) and port `80`. This is a standard setup for containerized FastAPI applications.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/docker.md#_snippet_14

LANGUAGE: Dockerfile
CODE:

```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

---

TITLE: Importing APIRouter Submodules with Relative Path - FastAPI Python
DESCRIPTION: Shows how to import `APIRouter` instances from submodules (`app/routers/items.py`, `app/routers/users.py`) into the main application file (`app/main.py`) using relative imports (`.`). This approach helps avoid naming conflicts when multiple routers are imported.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/bigger-applications.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends

from .dependencies import get_query_token

from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(users.router)
app.include_router(items.router)
```

---

TITLE: Overriding Default Status Codes with JSONResponse in FastAPI
DESCRIPTION: This snippet demonstrates how to explicitly set HTTP status codes in a FastAPI path operation. While the `@app.post` decorator sets a default status code (e.g., 200), you can override it by returning a `JSONResponse` object with a different `status_code` (e.g., 201 for creation). This allows for fine-grained control over responses based on specific conditions, such as indicating a new resource was created versus an existing one being updated.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/additional-status-codes.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/items/", status_code=200)
async def create_item(item_id: str, new_item: bool = False):
    if new_item:
        # If a new item is truly created, return 201
        return JSONResponse(
            content={
                "message": f"Item '{item_id}' created successfully."
            },
            status_code=201
        )
    else:
        # If the item already exists or was just updated, return 200
        return {
            "message": f"Item '{item_id}' already exists or was updated."
        }
```

---

TITLE: Initializing OAuth2PasswordBearer Scheme in FastAPI
DESCRIPTION: Initializes an instance of `OAuth2PasswordBearer` to define an OAuth2 security scheme. The `tokenUrl` parameter specifies the endpoint where clients can obtain a token, which is used by OpenAPI for documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/security/first-steps.md#_snippet_3

LANGUAGE: Python
CODE:

```
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

---

TITLE: Define Generic List Fields in FastAPI Models
DESCRIPTION: Demonstrates how to declare a field as a generic list in a Pydantic model within FastAPI, allowing it to accept a list of any type.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/es/docs/tutorial/body-nested-models.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list
```

---

TITLE: Forbidding Extra Header Parameters - FastAPI Python
DESCRIPTION: This example shows how to configure a Pydantic header model to reject any extra, undeclared headers. By setting `Config.extra = "forbid"` within the `CommonHeaders` model, FastAPI will return an error response if the client sends headers not explicitly defined in the model, enhancing security and strictness.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/header-param-models.md#_snippet_1

LANGUAGE: Python
CODE:

```
from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

class CommonHeaders(BaseModel):
    x_token: Annotated[str | None, Header()] = None
    x_api_key: Annotated[str | None, Header()] = None

    class Config:
        extra = "forbid"

app = FastAPI()

@app.get("/items/")
async def read_items(common_headers: CommonHeaders):
    return common_headers
```

---

TITLE: Adding Root Route to Main App - Python
DESCRIPTION: Illustrates adding a route directly to the main 'FastAPI' application instance ('app') using a standard decorator ('@app.get("/")'). This shows that routes can be defined directly on the main app instance even after including other 'APIRouter' instances.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/bigger-applications.md#_snippet_10

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Depends
from app.dependencies import get_token_header

from app.routers import items, users
from app.internal import admin

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

TITLE: Performing HTTP Redirects with RedirectResponse in FastAPI
DESCRIPTION: This example demonstrates how to perform an HTTP redirect by returning a `RedirectResponse` object directly from a FastAPI endpoint. The `RedirectResponse` automatically sets the appropriate status code (defaulting to 307 Temporary Redirect) and the `Location` header to the provided URL, instructing the client to navigate to a different resource.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/custom-response.md#_snippet_7

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/typer")
async def redirect_typer():
    return RedirectResponse("https://typer.tiangolo.com")
```

---

TITLE: Running Pytest Tests
DESCRIPTION: This command demonstrates how to execute the pytest tests from the console. Running `pytest` will discover and run all tests marked with `@pytest.mark.anyio` or other standard pytest markers, providing a summary of the test results.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/async-tests.md#_snippet_4

LANGUAGE: console
CODE:

```
$ pytest

---> 100%
```

---

TITLE: Assigning a Class to `Depends`
DESCRIPTION: This snippet highlights the crucial part of declaring a class-based dependency: assigning the class itself (e.g., `CommonQueryParams`) to `Depends()`. FastAPI uses this to identify which callable to invoke for dependency resolution.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/dependencies/classes-as-dependencies.md#_snippet_9

LANGUAGE: Python
CODE:

```
... = Depends(CommonQueryParams)
```

---

TITLE: Compressing Responses with `GZipMiddleware` - FastAPI
DESCRIPTION: This snippet demonstrates how to use `GZipMiddleware` to automatically compress responses for clients that support GZip encoding (indicated by the `Accept-Encoding` header). It handles both standard and streaming responses. The `minimum_size` parameter can be configured to specify the smallest response size in bytes that should be gzipped, with a default of 500 bytes.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/advanced/middleware.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/")
async def read_root():
    return {"message": "Hello World, this is a long response to be gzipped." * 100}
```

---

TITLE: Returning HTMLResponse Object Directly in FastAPI
DESCRIPTION: This snippet illustrates how to return an `HTMLResponse` object directly from a FastAPI path operation. While `response_class` handles documentation, returning the response object directly gives full control over content, status code, and headers. However, this approach bypasses automatic serialization and OpenAPI documentation for the response body.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/custom-response.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
```

---

TITLE: Declaring Optional Query Parameters in Python
DESCRIPTION: These Python snippets show two ways to declare an optional query parameter `q` in a FastAPI path operation, using `typing.Union` (Python < 3.10) and the new `|` operator (Python 3.10+).
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/body-multiple-params.md#_snippet_6

LANGUAGE: Python
CODE:

```
q: Union[str, None] = None
```

LANGUAGE: Python
CODE:

```
q: str | None = None
```

---

TITLE: Sub-Dependency Teardown Using Yielded Values (Python)
DESCRIPTION: This snippet shows how the teardown logic of a dependency can still access the values yielded by its own sub-dependencies. This ensures that cleanup operations can utilize resources or information provided by upstream dependencies, maintaining proper context during teardown.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md#_snippet_5

LANGUAGE: Python
CODE:

```
from fastapi import Depends

async def dependency_a():
    print("Dependency A setup")
    yield "A_value"
    print("Dependency A teardown")

async def dependency_b(dep_a: str = Depends(dependency_a)):
    print(f"Dependency B setup with {dep_a}")
    yield "B_value"
    print(f"Dependency B teardown using {dep_a}")

async def dependency_c(dep_b: str = Depends(dependency_b)):
    print(f"Dependency C setup with {dep_b}")
    yield "C_value"
    print(f"Dependency C teardown using {dep_b}")
```

---

TITLE: Defining a FastAPI Application in main.py
DESCRIPTION: This snippet shows a basic FastAPI application defined in `main.py`. This structure allows the application instance (`app`) to be easily imported by other modules, such as separate test files, facilitating a modular approach for larger application structures.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/testing.md#_snippet_1

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}
```

---

TITLE: Clearing All Dependency Overrides in FastAPI
DESCRIPTION: This snippet shows how to clear all active dependency overrides by reassigning `app.dependency_overrides` to an empty dictionary. This is crucial for resetting the application state between tests, ensuring that overrides from previous tests do not affect subsequent ones.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/testing-dependencies.md#_snippet_1

LANGUAGE: Python
CODE:

```
app.dependency_overrides = {}
```

---

TITLE: Pinning Pydantic Version Range
DESCRIPTION: This snippet demonstrates how to pin a compatible version range for Pydantic (e.g., `1.2.0` or newer, but less than `2.0.0`) in `requirements.txt`. This is crucial because FastAPI relies heavily on Pydantic, and ensuring a compatible Pydantic version prevents potential issues arising from major Pydantic updates.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/deployment/versions.md#_snippet_3

LANGUAGE: txt
CODE:

```
pydantic>=1.2.0,<2.0.0
```

---

TITLE: Serving FastAPI Application with fastapi run in Docker
DESCRIPTION: This command specifies the entry point for a Docker container, instructing it to run a FastAPI application from `main.py` on port 80 using the `fastapi run` command. It is designed for single-file applications, allowing `fastapi run` to automatically detect and import the application.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/deployment/docker.md#_snippet_16

LANGUAGE: Shell
CODE:

```
CMD ["fastapi", "run", "main.py", "--port", "80"]
```

---

TITLE: Running Uvicorn with root_path
DESCRIPTION: Illustrates how to start a Uvicorn server and specify the `root_path` using the `--root-path` command-line argument. This informs the ASGI application about the path prefix added by a proxy, allowing it to generate correct URLs.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/behind-a-proxy.md#_snippet_2

LANGUAGE: Shell
CODE:

```
$ uvicorn main:app --root-path /api/v1

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

TITLE: Streaming Large Files with StreamingResponse in FastAPI
DESCRIPTION: This snippet illustrates how to use `StreamingResponse` in FastAPI to stream large files or generated content. The endpoint returns a `StreamingResponse` object, which takes a generator function as its content. This allows FastAPI to send data in chunks, making it suitable for large responses without loading the entire content into memory at once.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/advanced/custom-response.md#_snippet_10

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

async def generate_large_file():
    for i in range(1000):
        yield f"line {i}\n"

@app.get("/large-file")
async def get_large_file():
    return StreamingResponse(generate_large_file(), media_type="text/plain")
```

---

TITLE: Importing Path for FastAPI Applications
DESCRIPTION: This snippet demonstrates how to import the `Path` class from the `fastapi` module. `Path` is used to declare path parameters and apply validations and metadata to them, similar to `Query` for query parameters.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/zh/docs/tutorial/path-params-numeric-validations.md#_snippet_0

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Path

app = FastAPI()
```

---

TITLE: Combining Response Model, Status Code, and OpenAPI Responses in FastAPI (Python)
DESCRIPTION: This snippet illustrates how to combine `response_model`, `status_code`, and the `responses` parameter in FastAPI. It defines a `response_model` for the successful `200` response, adds a custom example for it, and also declares a `404` response with its own Pydantic model and description, enriching the OpenAPI documentation.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/additional-responses.md#_snippet_4

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    id: str
    value: str

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item found successfully",
            "content": {
                "application/json": {
                    "example": {"id": "foo", "value": "The Foo Wrestlers"}
                }
            }
        }
    }
)
async def read_item(item_id: str):
    if item_id == "foo":
        return {"id": "foo", "value": "The Foo Wrestlers"}
    return {"message": "Item not found"}
```

---

TITLE: Creating an Invoice with Callback URL in FastAPI
DESCRIPTION: This snippet defines a FastAPI path operation to create an invoice. It accepts an `Invoice` body and a `callback_url` query parameter of type `Url`. The `callbacks` argument in the decorator links this operation to a router for documenting the callback.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/openapi-callbacks.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Optional

from fastapi import APIRouter, FastAPI, status
from pydantic import Url

@app.post("/invoices/", status_code=status.HTTP_202_ACCEPTED, callbacks=invoices_callback_router.routes)
async def create_invoice(invoice: Invoice, callback_url: Url):
    """
    Create an invoice and notify the client later.
    """
    # Send the invoice to the client
    # Collect the money
    # Notify the client later
    return {"msg": "Invoice received!"}
```

---

TITLE: Example requirements.txt File Content
DESCRIPTION: Provides an example of a `requirements.txt` file, listing `fastapi` with its standard extras and `pydantic` with specific version pins. This file format is used to declare and manage a project's exact Python package dependencies.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/virtual-environments.md#_snippet_15

LANGUAGE: requirements.txt
CODE:

```
fastapi[standard]==0.113.0
pydantic==2.8.0
```

---

TITLE: Directly Returning HTMLResponse Object in FastAPI
DESCRIPTION: This snippet illustrates how to directly return an `HTMLResponse` object from a FastAPI path operation function. While this method provides full control over the response, including status code and headers, it's important to note that the response's media type (e.g., `Content-Type`) will not be automatically documented in OpenAPI unless `response_class` is also specified in the decorator. The function constructs an `HTMLResponse` instance with the desired content and status.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/advanced/custom-response.md#_snippet_2

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/items/")
async def read_items():
    content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=content, status_code=200)
```

---

TITLE: Overriding HTTP Exception Handler in FastAPI
DESCRIPTION: This code shows how to override the `HTTPException` handler in FastAPI, specifically using Starlette's `HTTPException` for broader compatibility. The custom handler returns a plain text response for HTTP errors, allowing for a simplified error presentation to the client.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/en/docs/tutorial/handling-errors.md#_snippet_8

LANGUAGE: Python
CODE:

```
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
```

---

TITLE: Defining PUT Path Operation Decorator - FastAPI Python
DESCRIPTION: This snippet demonstrates the `@app.put()` decorator, used in FastAPI to define a path operation for handling HTTP PUT requests. This method is commonly used for updating existing resources.
SOURCE: https://github.com/fastapi/fastapi/blob/master/docs/em/docs/tutorial/first-steps.md#_snippet_10

LANGUAGE: Python
CODE:

```
@app.put()
```
