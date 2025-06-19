TITLE: Define and Validate Data Models with Pydantic
DESCRIPTION: This example demonstrates how to define a data model using Pydantic's BaseModel. It showcases the use of Python type hints, default values, optional fields, and how Pydantic automatically validates and coerces external data into the defined model structure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/README.md#_snippet_0

LANGUAGE: python
CODE:

```
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: list[int] = []

external_data = {'id': '123', 'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
user = User(**external_data)
print(user)
#> User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
#> 123
```

---

TITLE: Pydantic Model Validation Successful
DESCRIPTION: This snippet demonstrates how to define a Pydantic `BaseModel` and validate external data against it, showing successful data coercion and field access. It illustrates how Pydantic handles type annotations, default values, optional fields, and complex types like dictionaries with specific value constraints, along with automatic type coercion for various input formats.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/index.md#_snippet_1

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',
    'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1',
    },
}

user = User(**external_data)

print(user.id)
# > 123
print(user.model_dump())
"""
{
    'id': 123,
    'name': 'John Doe',
    'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
    'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
}
"""
```

---

TITLE: Pydantic Model to Dictionary Conversion with `model.model_dump()`
DESCRIPTION: This section describes `model.model_dump()`, the primary method for converting a Pydantic model to a dictionary. It explains that sub-models are recursively converted and discusses parameters like `mode='json'` for JSON serializability, and options to include or exclude fields, including nested ones. It also notes exceptions for `RootModel` and the inclusion of computed fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_0

LANGUAGE: Python
CODE:

```
from typing import Any, Optional

from pydantic import BaseModel, Field, Json


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: Optional[float] = 1.1
    foo: str = Field(serialization_alias='foo_alias')
    bar: BarModel


m = FooBarModel(banana=3.14, foo='hello', bar={'whatever': 123})

# returns a dictionary:
print(m.model_dump())
#> {'banana': 3.14, 'foo': 'hello', 'bar': {'whatever': 123}}
print(m.model_dump(include={'foo', 'bar'}))
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(m.model_dump(exclude={'foo', 'bar'}))
#> {'banana': 3.14}
print(m.model_dump(by_alias=True))
#> {'banana': 3.14, 'foo_alias': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(foo='hello', bar={'whatever': 123}).model_dump(
        exclude_unset=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(banana=1.1, foo='hello', bar={'whatever': 123}).model_dump(
        exclude_defaults=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(foo='hello', bar={'whatever': 123}).model_dump(
        exclude_defaults=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}
print(
    FooBarModel(banana=None, foo='hello', bar={'whatever': 123}).model_dump(
        exclude_none=True
    )
)
#> {'foo': 'hello', 'bar': {'whatever': 123}}


class Model(BaseModel):
    x: list[Json[Any]]


print(Model(x=['{"a": 1}', '[1, 2]']).model_dump())
#> {'x': [{'a': 1}, [1, 2]]}
print(Model(x=['{"a": 1}', '[1, 2]']).model_dump(round_trip=True))
#> {'x': ['{"a":1}', '[1,2]']}
```

---

TITLE: Defining a Pydantic Model (Python)
DESCRIPTION: Defines a `User` model using Pydantic's `BaseModel`. It includes an required integer field `id` and an optional string field `name` with a default value. It also sets a configuration for string max length.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    name: str = 'Jane Doe'

    model_config = ConfigDict(str_max_length=10)  # (1)!
```

---

TITLE: Install Pydantic Core Library
DESCRIPTION: Commands to install the Pydantic core library using pip, uv, and conda package managers. Pydantic requires Python 3.9+.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/install.md#_snippet_0

LANGUAGE: bash
CODE:

```
pip install pydantic
```

LANGUAGE: bash
CODE:

```
uv add pydantic
```

LANGUAGE: bash
CODE:

```
conda install pydantic -c conda-forge
```

---

TITLE: Install Pydantic V2
DESCRIPTION: Provides the command to install the latest production release of Pydantic V2 from PyPI. This is the recommended version for new projects and migrations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_0

LANGUAGE: bash
CODE:

```
pip install -U pydantic
```

---

TITLE: Pydantic Model Validation and Serialization Example
DESCRIPTION: This Python example illustrates how Pydantic models perform validation and serialization. It uses `model_validate` to create an instance from input data and `model_dump` to serialize the model instance back into a dictionary, leveraging `pydantic-core` for high-performance operations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/architecture.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Model(BaseModel):
    foo: int


model = Model.model_validate({'foo': 1}) # (1)!
dumped = model.model_dump() # (2)!
```

---

TITLE: Defining Recursive JSON Type Alias with New Syntax (Python 3.12+)
DESCRIPTION: Defines a recursive `Json` type alias using the new `type` keyword syntax available in Python 3.12+. This syntax enables lazy evaluation, eliminating the need for forward annotation strings. The code validates the type using `pydantic.TypeAdapter` and outputs the corresponding JSON schema, showing the simplified definition compared to older Python versions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_11

LANGUAGE: Python
CODE:

```
from pydantic import TypeAdapter

type Json = dict[str, Json] | list[Json] | str | int | float | bool | None  # (1)!

ta = TypeAdapter(Json)
print(ta.json_schema())
"""
{
    '$defs': {
        'Json': {
            'anyOf': [
                {
                    'additionalProperties': {'$ref': '#/$defs/Json'},
                    'type': 'object',
                },
                {'items': {'$ref': '#/$defs/Json'}, 'type': 'array'},
                {'type': 'string'},
                {'type': 'integer'},
                {'type': 'number'},
                {'type': 'boolean'},
                {'type': 'null'}
            ]
        }
    },
    '$ref': '#/$defs/Json'
}
"""
```

---

TITLE: Defining Generic Pydantic Model (Python 3.12+ New Syntax)
DESCRIPTION: Illustrates the new PEP 695 syntax for defining generic Pydantic models in Python 3.12+, simplifying the declaration compared to older versions. Includes instantiation with different types and validation examples.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_20

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class DataModel(BaseModel):
    number: int


class Response[DataT](BaseModel):  # (1)!
    data: DataT  # (2)!


print(Response[int](data=1))
#> data=1
print(Response[str](data='value'))
#> data='value'
print(Response[str](data='value').model_dump())
#> {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
#> {'data': {'number': 1}}
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    """
    1 validation error for Response[int]
    data
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type=str]
    """
```

---

TITLE: Pydantic Model Serialization to Dict and JSON
DESCRIPTION: Demonstrates Pydantic's three serialization methods: to a Python dictionary of Python objects, to a dictionary of JSON-compatible types, and to a JSON string. It also shows how to customize output by excluding specific fields, unset values, or default values.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_2

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel


class Meeting(BaseModel):
    when: datetime
    where: bytes
    why: str = 'No idea'


m = Meeting(when='2020-01-01T12:00', where='home')
print(m.model_dump(exclude_unset=True))
#> {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}
print(m.model_dump(exclude={'where'}, mode='json'))
#> {'when': '2020-01-01T12:00:00', 'why': 'No idea'}
print(m.model_dump_json(exclude_defaults=True))
#> {"when":"2020-01-01T12:00:00","where":"home"}
```

---

TITLE: Defining and Using Nested Pydantic Models - Python
DESCRIPTION: Shows how to create complex data structures by using Pydantic models as types within other models. Demonstrates instantiation with nested data and accessing the resulting model structure. Requires `pydantic.BaseModel` and `typing.Optional`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_9

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None


class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'


class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]


m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
"""
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', banana='y'), Bar(apple='x2', banana='y')]
"""
print(m.model_dump())
"""
{
    'foo': {'count': 4, 'size': None},
    'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}],
}
"""
```

---

TITLE: Implementing Tagged Unions with Pydantic - Python
DESCRIPTION: This snippet demonstrates the implementation of a tagged (discriminated) union in Pydantic using `Literal` and `Field(discriminator='...')`. This pattern allows Pydantic to efficiently determine the correct model type within a union based on a specific field, significantly improving validation performance compared to untagged unions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_5

LANGUAGE: python
CODE:

```
from typing import Any, Literal

from pydantic import BaseModel, Field


class DivModel(BaseModel):
    el_type: Literal['div'] = 'div'
    class_name: str | None = None
    children: list[Any] | None = None


class SpanModel(BaseModel):
    el_type: Literal['span'] = 'span'
    class_name: str | None = None
    contents: str | None = None


class ButtonModel(BaseModel):
    el_type: Literal['button'] = 'button'
    class_name: str | None = None
    contents: str | None = None


class InputModel(BaseModel):
    el_type: Literal['input'] = 'input'
    class_name: str | None = None
    value: str | None = None


class Html(BaseModel):
    contents: DivModel | SpanModel | ButtonModel | InputModel = Field(
        discriminator='el_type'
    )
```

---

TITLE: Demonstrating Pydantic Model Validation Methods (Python)
DESCRIPTION: This snippet defines a Pydantic `User` model and demonstrates the usage of `model_validate`, `model_validate_json`, and `model_validate_strings` for parsing and validating different input formats (dictionaries, JSON strings, string dictionaries). It also shows how `ValidationError` is raised for invalid inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_14

LANGUAGE: python
CODE:

```
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationError


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None


m = User.model_validate({'id': 123, 'name': 'James'})
print(m)
# id=123 name='James' signup_ts=None

try:
    User.model_validate(['not', 'a', 'dict'])
except ValidationError as e:
    print(e)
    # 1 validation error for User
    #   Input should be a valid dictionary or instance of User [type=model_type, input_value=['not', 'a', 'dict'], input_type=list]
    #

m = User.model_validate_json('{"id": 123, "name": "James"}')
print(m)
# id=123 name='James' signup_ts=None

try:
    m = User.model_validate_json('{"id": 123, "name": 123}')
except ValidationError as e:
    print(e)
    # 1 validation error for User
    # name
    #   Input should be a valid string [type=string_type, input_value=123, input_type=int]
    #

try:
    m = User.model_validate_json('invalid JSON')
except ValidationError as e:
    print(e)
    # 1 validation error for User
    #   Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='invalid JSON', input_type=str]
    #

m = User.model_validate_strings({'id': '123', 'name': 'James'})
print(m)
# id=123 name='James' signup_ts=None

m = User.model_validate_strings(
    {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01T12:00:00'}
)
print(m)
# id=123 name='James' signup_ts=datetime.datetime(2024, 4, 1, 12, 0)

try:
    m = User.model_validate_strings(
        {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01'}, strict=True
    )
except ValidationError as e:
    print(e)
    # 1 validation error for User
    # signup_ts
    #   Input should be a valid datetime, invalid datetime separator, expected `T`, `t`, `_` or space [type=datetime_parsing, input_value='2024-04-01', input_type=str]
    #
```

---

TITLE: Handling Pydantic Validation Errors in Python
DESCRIPTION: Demonstrates how Pydantic raises a `ValidationError` when an invalid value is assigned to a model field and the model is subsequently validated. It shows catching the exception and printing the error details.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_17

LANGUAGE: python
CODE:

```
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior.
m.a = 'not an int'

try:
    m2 = Model.model_validate(m)
except ValidationError as e:
    print(e)
```

---

TITLE: Pydantic TypeAdapter API Reference
DESCRIPTION: Reference for the `pydantic.type_adapter.TypeAdapter` class, which provides validation, serialization, and JSON schema generation capabilities for arbitrary Python types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
pydantic.type_adapter.TypeAdapter
```

---

TITLE: Pydantic V1 to V2 Import Transformation
DESCRIPTION: Provides a general pattern for updating Pydantic V1 imports to be compatible with the `pydantic.v1` namespace in Pydantic V2. This is a key step for migrating existing V1 codebases.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_6

LANGUAGE: python
CODE:

```
from pydantic.<module> import <object>
```

LANGUAGE: python
CODE:

```
from pydantic.v1.<module> import <object>
```

---

TITLE: Pydantic V2 Field Optionality and Nullability Example
DESCRIPTION: Illustrates the new behavior of required, optional, and nullable fields in Pydantic V2, aligning more closely with `dataclasses`. It shows how `Optional[T]` fields are required by default if no default value is provided, and how different default values affect field optionality and nullability. Includes a `ValidationError` example.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_22

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel, ValidationError


class Foo(BaseModel):
    f1: str  # required, cannot be None
    f2: Optional[str]  # required, can be None - same as str | None
    f3: Optional[str] = None  # not required, can be None
    f4: str = 'Foobar'  # not required, but cannot be None


try:
    Foo(f1=None, f2=None, f4='b')
except ValidationError as e:
    print(e)
    """
    1 validation error for Foo
    f1
      Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
    """
```

---

TITLE: Pydantic Model Definition with Type Hints
DESCRIPTION: This example demonstrates how to define a Pydantic `BaseModel` using standard Python type hints for schema validation. It shows basic types like `str`, `Literal` for enumerated values, `Annotated` with `Gt` for constraints, and complex nested types like `dict` with `list` and `tuple`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_0

LANGUAGE: python
CODE:

```
from typing import Annotated, Literal

from annotated_types import Gt

from pydantic import BaseModel


class Fruit(BaseModel):
    name: str  # (1)!
    color: Literal['red', 'green']  # (2)!
    weight: Annotated[float, Gt(0)]  # (3)!
    bazam: dict[str, list[tuple[int, bool, float]]]  # (4)!


print(
    Fruit(
        name='Apple',
        color='red',
        weight=4.2,
        bazam={'foobar': [(1, True, 0.1)]},
    )
)
#> name='Apple' color='red' weight=4.2 bazam={'foobar': [(1, True, 0.1)]}
```

---

TITLE: Pydantic Field Validator: Accessing Validated Data with ValidationInfo.data
DESCRIPTION: Demonstrates how to use a Pydantic `field_validator` with `mode='after'` to compare two fields, such as `password` and `password_repeat`. It utilizes the `info.data` property of the `ValidationInfo` object to access the value of the `password` field that has already been validated.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_14

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationInfo, field_validator


class UserModel(BaseModel):
    password: str
    password_repeat: str
    username: str

    @field_validator('password_repeat', mode='after')
    @classmethod
    def check_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data['password']:
            raise ValueError('Passwords do not match')
        return value
```

---

TITLE: Pydantic Model to JSON String Conversion with `model.model_dump_json()`
DESCRIPTION: This section introduces `model.model_dump_json()`, a method that directly serializes a Pydantic model into a JSON-encoded string, producing results equivalent to `model.model_dump()`. It highlights Pydantic's ability to serialize types like `datetime` or `UUID` that `json.dumps` might not handle directly.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_1

LANGUAGE: Python
CODE:

```
from datetime import datetime

from pydantic import BaseModel


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    foo: datetime
    bar: BarModel


m = FooBarModel(foo=datetime(2032, 6, 1, 12, 13, 14), bar={'whatever': 123})
print(m.model_dump_json())
#> {"foo":"2032-06-01T12:13:14","bar":{"whatever":123}}
print(m.model_dump_json(indent=2))
"""
{
  "foo": "2032-06-01T12:13:14",
  "bar": {
    "whatever": 123
  }
}
"""
```

---

TITLE: Pydantic Before Validator: Preprocess Input to Ensure List
DESCRIPTION: The `BeforeValidator` allows preprocessing of raw input values before Pydantic's standard validation. This example demonstrates how to use it to ensure a field's value is always a list, even if a single item is provided. It highlights the flexibility but also the responsibility to handle all possible input types. The example shows both the `Annotated` pattern and the `@field_validator` decorator approach.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_3

LANGUAGE: python
CODE:

```
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ValidationError


def ensure_list(value: Any) -> Any:
    if not isinstance(value, list):
        return [value]
    else:
        return value


class Model(BaseModel):
    numbers: Annotated[list[int], BeforeValidator(ensure_list)]


print(Model(numbers=2))
try:
    Model(numbers='str')
except ValidationError as err:
    print(err)
```

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    numbers: list[int]

    @field_validator('numbers', mode='before')
    @classmethod
    def ensure_list(cls, value: Any) -> Any:
        if not isinstance(value, list):
            return [value]
        else:
            return value


print(Model(numbers=2))
try:
    Model(numbers='str')
except ValidationError as err:
    print(err)
```

---

TITLE: Validating Single User Data with Pydantic and HTTPX (Python)
DESCRIPTION: This snippet demonstrates how to fetch a single user's data from an API using httpx and validate it against a Pydantic BaseModel. It defines a User model with id, name, and email fields, then uses User.model_validate() to parse the JSON response. The httpx.raise_for_status() method ensures that HTTP errors are caught.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/requests.md#_snippet_0

LANGUAGE: Python
CODE:

```
import httpx

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


url = 'https://jsonplaceholder.typicode.com/users/1'

response = httpx.get(url)
response.raise_for_status()

user = User.model_validate(response.json())
print(repr(user))
#> User(id=1, name='Leanne Graham', email='Sincere@april.biz')
```

---

TITLE: Custom Pydantic Datetime Validator for Timezone Constraint
DESCRIPTION: This Python code defines `MyDatetimeValidator` to enforce a specific timezone on a `datetime` object using Pydantic's `Annotated` type. It utilizes `__get_pydantic_core_schema__` with a `no_info_wrap_validator_function` to apply custom validation logic before and after Pydantic's default `datetime` validation. The validator raises an error if the `datetime`'s timezone does not match the specified constraint or if a naive datetime is provided when a constraint is set.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md#_snippet_0

LANGUAGE: python
CODE:

```
import datetime as dt
from dataclasses import dataclass
from pprint import pprint
from typing import Annotated, Any, Callable, Optional

import pytz
from pydantic_core import CoreSchema, core_schema

from pydantic import (
    GetCoreSchemaHandler,
    PydanticUserError,
    TypeAdapter,
    ValidationError,
)


@dataclass(frozen=True)
class MyDatetimeValidator:
    tz_constraint: Optional[str] = None

    def tz_constraint_validator(
        self,
        value: dt.datetime,
        handler: Callable,  # (1)!
    ):
        """Validate tz_constraint and tz_info."""
        # handle naive datetimes
        if self.tz_constraint is None:
            assert (
                value.tzinfo is None
            ), 'tz_constraint is None, but provided value is tz-aware.'
            return handler(value)

        # validate tz_constraint and tz-aware tzinfo
        if self.tz_constraint not in pytz.all_timezones:
            raise PydanticUserError(
                f'Invalid tz_constraint: {self.tz_constraint}',
                code='unevaluable-type-annotation',
            )
        result = handler(value)  # (2)!
        assert self.tz_constraint == str(
            result.tzinfo
        ), f'Invalid tzinfo: {str(result.tzinfo)}, expected: {self.tz_constraint}'

        return result

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            self.tz_constraint_validator,
            handler(source_type),
        )


LA = 'America/Los_Angeles'
ta = TypeAdapter(Annotated[dt.datetime, MyDatetimeValidator(LA)])
print(
    ta.validate_python(dt.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.timezone(LA)))
)
#> 2023-01-01 00:00:00-07:53

LONDON = 'Europe/London'
try:
    ta.validate_python(
        dt.datetime(2023, 1, 1, 0, 0, tzinfo=pytz.timezone(LONDON))
    )
except ValidationError as ve:
    pprint(ve.errors(), width=100)
    """
    [{'ctx': {'error': AssertionError('Invalid tzinfo: Europe/London, expected: America/Los_Angeles')},
    'input': datetime.datetime(2023, 1, 1, 0, 0, tzinfo=<DstTzInfo 'Europe/London' LMT-1 day, 23:59:00 STD>),
    'loc': (),
    'msg': 'Assertion failed, Invalid tzinfo: Europe/London, expected: America/Los_Angeles',
    'type': 'assertion_error',
    'url': 'https://errors.pydantic.dev/2.8/v/assertion_error'}]
    """
```

---

TITLE: Annotated with Optional Fields: Correct vs. Incorrect Metadata Placement
DESCRIPTION: Compares two ways of using `Annotated` with optional fields (`| None`), showing that `Field` metadata should be applied to the union type (`Annotated[int | None, ...]`) for it to affect the field, rather than just the base type (`Annotated[int, ...] | None`). This highlights the importance of applying metadata to the correct part of the type annotation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_4

LANGUAGE: python
CODE:

```
class Model(BaseModel):
    field_bad: Annotated[int, Field(deprecated=True)] | None = None  # (1)!
    field_ok: Annotated[int | None, Field(deprecated=True)] = None  # (2)!
```

---

TITLE: Pydantic Datetime Field Handling with `datetime.datetime`
DESCRIPTION: This example illustrates how Pydantic processes `datetime.datetime` fields, accepting various formats such as ISO 8601 strings. It demonstrates the automatic parsing and conversion of a string representation into a `datetime` object, including timezone information, when assigned to a Pydantic model field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_1

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    dt: datetime = None


event = Event(dt='2032-04-23T10:20:30.400+02:30')

print(event.model_dump())
```

---

TITLE: Pydantic After Model Validator Example
DESCRIPTION: Demonstrates an 'after' model validator in Pydantic, which runs post-initialization. This example checks if `password` and `password_repeat` fields match, raising a `ValueError` if they do not. The validated instance must be returned.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_10

LANGUAGE: python
CODE:

```
from typing_extensions import Self

from pydantic import BaseModel, model_validator


class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self
```

---

TITLE: Basic RootModel Usage - Pydantic Python
DESCRIPTION: Demonstrates defining Pydantic models with a custom root type using `RootModel`, showing examples with a list of strings and a dictionary of strings. Includes validation, JSON dumping, and schema generation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_42

LANGUAGE: python
CODE:

```
from pydantic import RootModel

Pets = RootModel[list[str]]
PetsByName = RootModel[dict[str, str]]


print(Pets(['dog', 'cat']))
#> root=['dog', 'cat']
print(Pets(['dog', 'cat']).model_dump_json())
#> ["dog","cat"]
print(Pets.model_validate(['dog', 'cat']))
#> root=['dog', 'cat']
print(Pets.model_json_schema())
"""
{'items': {'type': 'string'}, 'title': 'RootModel[list[str]]', 'type': 'array'}
"""

print(PetsByName({'Otis': 'dog', 'Milo': 'cat'}))
#> root={'Otis': 'dog', 'Milo': 'cat'}
print(PetsByName({'Otis': 'dog', 'Milo': 'cat'}).model_dump_json())
#> {"Otis":"dog","Milo":"cat"}
print(PetsByName.model_validate({'Otis': 'dog', 'Milo': 'cat'}))
#> root={'Otis': 'dog', 'Milo': 'cat'}
```

---

TITLE: Optimizing TypeAdapter Instantiation (Good Example) - Python
DESCRIPTION: This snippet shows the recommended approach for using `TypeAdapter` by instantiating it once outside the function scope. This prevents redundant validator and serializer construction, improving performance by reusing the adapter across multiple function calls.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_1

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])

def my_func():
    ...
    # do something with adapter
```

---

TITLE: Generate Top-Level JSON Schema with Multiple Pydantic Models
DESCRIPTION: Shows how to generate a top-level JSON schema that includes multiple Pydantic models and their related sub-models within the `$defs` section. This uses the `models_json_schema` function to combine schemas from different models into a single schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_28

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel
from pydantic.json_schema import models_json_schema


class Foo(BaseModel):
    a: str = None


class Model(BaseModel):
    b: Foo


class Bar(BaseModel):
    c: int


_, top_level_schema = models_json_schema(
    [(Model, 'validation'), (Bar, 'validation')], title='My Schema'
)
print(json.dumps(top_level_schema, indent=2))
"""
{
  "$defs": {
    "Bar": {
      "properties": {
        "c": {
          "title": "C",
          "type": "integer"
        }
      },
      "required": [
        "c"
      ],
      "title": "Bar",
      "type": "object"
    },
    "Foo": {
      "properties": {
        "a": {
          "default": null,
          "title": "A",
          "type": "string"
        }
      },
      "title": "Foo",
      "type": "object"
    },
    "Model": {
      "properties": {
        "b": {
          "$ref": "#/$defs/Foo"
        }
      },
      "required": [
        "b"
      ],
      "title": "Model",
      "type": "object"
    }
  },
  "title": "My Schema"
}
"""
```

---

TITLE: Validating List of Users with Pydantic TypeAdapter and HTTPX (Python)
DESCRIPTION: This example illustrates how to validate a list of user objects retrieved from an API using Pydantic's TypeAdapter with httpx. It defines the same User BaseModel and then creates a TypeAdapter for list[User] to validate the entire JSON array response. This approach is useful for handling collections of models.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/requests.md#_snippet_1

LANGUAGE: Python
CODE:

```
from pprint import pprint

import httpx

from pydantic import BaseModel, EmailStr, TypeAdapter


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


url = 'https://jsonplaceholder.typicode.com/users/'  # (1)!

response = httpx.get(url)
response.raise_for_status()

users_list_adapter = TypeAdapter(list[User])

users = users_list_adapter.validate_python(response.json())
pprint([u.name for u in users])
"""
['Leanne Graham',
 'Ervin Howell',
 'Clementine Bauch',
 'Patricia Lebsack',
 'Chelsey Dietrich',
 'Mrs. Dennis Schulist',
 'Kurtis Weissnat',
 'Nicholas Runolfsdottir V',
 'Glenna Reichert',
 'Clementina DuBuque']
"""
```

---

TITLE: Serializing and Deserializing Data with Pydantic and Redis Queue (Python)
DESCRIPTION: This Python snippet demonstrates how to use Pydantic to serialize `User` model data into JSON before pushing it to a Redis queue and then deserialize and validate the data when popping it from the queue. It requires a running Redis server.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/queues.md#_snippet_0

LANGUAGE: python
CODE:

```
import redis

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_NAME = 'user_queue'


def push_to_queue(user_data: User) -> None:
    serialized_data = user_data.model_dump_json()
    r.rpush(QUEUE_NAME, user_data.model_dump_json())
    print(f'Added to queue: {serialized_data}')


user1 = User(id=1, name='John Doe', email='john@example.com')
user2 = User(id=2, name='Jane Doe', email='jane@example.com')

push_to_queue(user1)
#> Added to queue: {"id":1,"name":"John Doe","email":"john@example.com"}

push_to_queue(user2)
#> Added to queue: {"id":2,"name":"Jane Doe","email":"jane@example.com"}


def pop_from_queue() -> None:
    data = r.lpop(QUEUE_NAME)

    if data:
        user = User.model_validate_json(data)
        print(f'Validated user: {repr(user)}')
    else:
        print('Queue is empty')


pop_from_queue()
#> Validated user: User(id=1, name='John Doe', email='john@example.com')

pop_from_queue()
#> Validated user: User(id=2, name='Jane Doe', email='jane@example.com')

pop_from_queue()
#> Queue is empty
```

---

TITLE: Custom Pydantic Datetime Validator for UTC Offset Bounds
DESCRIPTION: This Python example demonstrates a custom Pydantic validator that ensures a `datetime` object's UTC offset falls within a specified `lower_bound` and `upper_bound`. The `MyDatetimeValidator` class uses `__get_pydantic_core_schema__` to wrap the default Pydantic validation, asserting that the `datetime` has a UTC offset and that it is within the defined range (in hours). It raises an error if the offset is out of bounds or if the datetime is naive.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md#_snippet_1

LANGUAGE: python
CODE:

```
import datetime as dt
from dataclasses import dataclass
from pprint import pprint
from typing import Annotated, Any, Callable

import pytz
from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler, TypeAdapter, ValidationError


@dataclass(frozen=True)
class MyDatetimeValidator:
    lower_bound: int
    upper_bound: int

    def validate_tz_bounds(self, value: dt.datetime, handler: Callable):
        """Validate and test bounds"""
        assert value.utcoffset() is not None, 'UTC offset must exist'
        assert self.lower_bound <= self.upper_bound, 'Invalid bounds'

        result = handler(value)

        hours_offset = value.utcoffset().total_seconds() / 3600
        assert (
            self.lower_bound <= hours_offset <= self.upper_bound
        ), 'Value out of bounds'

        return result

    def __get_pydantic_core_schema__(
        self,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_wrap_validator_function(
            self.validate_tz_bounds,
            handler(source_type),
        )


LA = 'America/Los_Angeles'  # UTC-7 or UTC-8
ta = TypeAdapter(Annotated[dt.datetime, MyDatetimeValidator(-10, -5)])
print(
```

---

TITLE: Handling Mutable Default Values in Pydantic Python
DESCRIPTION: Shows how Pydantic handles mutable default values (like lists or dictionaries). Unlike standard Python function arguments, Pydantic creates a deep copy of the mutable default value for each model instance if the value is not hashable, preventing unintended sharing of the default instance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_9

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Model(BaseModel):
    item_counts: list[dict[str, int]] = [{}]


m1 = Model()
m1.item_counts[0]['a'] = 1
print(m1.item_counts)

m2 = Model()
print(m2.item_counts)
```

---

TITLE: Pydantic V2: Changes to `Field` and JSON Schema Extra
DESCRIPTION: Pydantic V2's `Field` no longer supports arbitrary keyword arguments for JSON schema. Instead, `json_schema_extra` is used. The behavior of the `alias` property has changed, and several properties like `const`, `min_items`, `max_items`, `unique_items`, `allow_mutation`, `regex`, and `final` have been removed or replaced.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_13

LANGUAGE: APIDOC
CODE:

```
pydantic.Field:
  - `json_schema_extra`: Replaces arbitrary keyword arguments for adding data to JSON schema.
  - `alias` property: Returns `None` in V2 if no alias is set (V1 returned field name).
  - Removed/Changed properties:
    - `const` (removed)
    - `min_items` (use `min_length`)
    - `max_items` (use `max_length`)
    - `unique_items` (removed)
    - `allow_mutation` (use `frozen`)
    - `regex` (use `pattern`)
    - `final` (use `typing.Final` type hint)
  - Field constraints on generics:
    - No longer automatically pushed down to generic parameters.
    - Use `typing.Annotated` for inner type annotations.
      Example: `my_list: list[Annotated[str, Field(pattern=".*")]]`
```

---

TITLE: Define Alias for Validation and Serialization with Pydantic
DESCRIPTION: This snippet shows how to use `Field(alias='...')` in Pydantic to define an alias that is used for both model validation (instance creation) and serialization when `model_dump(by_alias=True)` is called. It requires `pydantic.BaseModel` and `pydantic.Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_10

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(alias='username')


user = User(username='johndoe')  # (1)!
print(user)
#> name='johndoe'
print(user.model_dump(by_alias=True))  # (2)!
#> {'username': 'johndoe'}
```

---

TITLE: Using default_factory in Pydantic Python
DESCRIPTION: Shows how to use the `default_factory` argument of `pydantic.Field` to provide a callable that generates the default value when the model is instantiated. This is useful for creating dynamic or mutable default values.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_6

LANGUAGE: python
CODE:

```
from uuid import uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

---

TITLE: Customize Pydantic Field JSON Schema with `Field` Parameters
DESCRIPTION: This example demonstrates how to use `pydantic.fields.Field` parameters like `description`, `examples`, `title`, and `json_schema_extra` to customize the generated JSON Schema for a Pydantic model. It shows how to define a `User` model with various field types and their corresponding `Field` customizations, then prints the resulting JSON Schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_10

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel, EmailStr, Field, SecretStr


class User(BaseModel):
    age: int = Field(description='Age of the user')
    email: EmailStr = Field(examples=['marcelo@mail.com'])
    name: str = Field(title='Username')
    password: SecretStr = Field(
        json_schema_extra={
            'title': 'Password',
            'description': 'Password of the user',
            'examples': ['123456'],
        }
    )


print(json.dumps(User.model_json_schema(), indent=2))
"""
{
  "properties": {
    "age": {
      "description": "Age of the user",
      "title": "Age",
      "type": "integer"
    },
    "email": {
      "examples": [
        "marcelo@mail.com"
      ],
      "format": "email",
      "title": "Email",
      "type": "string"
    },
    "name": {
      "title": "Username",
      "type": "string"
    },
    "password": {
      "description": "Password of the user",
      "examples": [
        "123456"
      ],
      "format": "password",
      "title": "Password",
      "type": "string",
      "writeOnly": true
    }
  },
  "required": [
    "age",
    "email",
    "name",
    "password"
  ],
  "title": "User",
  "type": "object"
}
"""
```

---

TITLE: Applying Numeric Constraints with Field - Python
DESCRIPTION: This example demonstrates how to apply various numeric constraints (`gt`, `ge`, `lt`, `le`, `multiple_of`, `allow_inf_nan`) to integer and float fields in a Pydantic model using `pydantic.Field`. It includes instantiation with values satisfying the constraints and printing the resulting model.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_18

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)
    love_for_pydantic: float = Field(allow_inf_nan=True)


foo = Foo(
    positive=1,
    non_negative=0,
    negative=-1,
    non_positive=0,
    even=2,
    love_for_pydantic=float('inf'),
)
print(foo)
"""
positive=1 non_negative=0 negative=-1 non_positive=0 even=2 love_for_pydantic=inf
"""
```

---

TITLE: Defining Generic Pydantic Models and Subclasses (Python)
DESCRIPTION: Defines a generic base class `BaseClass` using `pydantic.BaseModel` and `typing.Generic` with type variables `TypeX` and `TypeY`. It then defines a generic subclass `ChildClass` that inherits from `BaseClass`, fixing `TypeX` to `int` and introducing a new type variable `TypeZ`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_23

LANGUAGE: python
CODE:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

TypeX = TypeVar('TypeX')
TypeY = TypeVar('TypeY')
TypeZ = TypeVar('TypeZ')


class BaseClass(BaseModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY


class ChildClass(BaseClass[int, TypeY], Generic[TypeY, TypeZ]):
    z: TypeZ
```

---

TITLE: Handling Pydantic Validation Errors (Python)
DESCRIPTION: Demonstrates Pydantic's error handling by defining a simple `BaseModel` with fields requiring specific types. Provides invalid input data and attempts to create a model instance within a `try...except ValidationError` block. Shows how the `ValidationError` captures multiple errors and provides detailed information about each failure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_13

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    list_of_ints: list[int]
    a_float: float


data = dict(
    list_of_ints=['1', 2, 'bad'],
    a_float='not a float',
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    list_of_ints.2
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    a_float
      Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='not a float', input_type=str]
    """
```

---

TITLE: Applying Constraints to Optional Fields with Annotated - Python
DESCRIPTION: This snippet demonstrates the recommended way to apply field constraints to optional fields in Pydantic using `typing.Annotated`. It shows how `Annotated` can wrap the type and the `Field` definition to avoid potential errors that might occur when applying constraints directly to `Optional` types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_20

LANGUAGE: python
CODE:

```
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class Foo(BaseModel):
    positive: Optional[Annotated[int, Field(gt=0)]]
    # Can error in some cases, not recommended:
    non_negative: Optional[int] = Field(ge=0)
```

---

TITLE: Defining Default Values in Pydantic Python
DESCRIPTION: Demonstrates the basic ways to provide default values for model fields using direct assignment or the `default` argument of `pydantic.Field`. Both methods make the field optional during model instantiation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_5

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class User(BaseModel):
    # Both fields aren't required:
    name: str = 'John Doe'
    age: int = Field(default=20)
```

---

TITLE: Defining a Pydantic Model Field with Field()
DESCRIPTION: Shows how to use `pydantic.fields.Field` to add metadata or constraints to a model field, like making it frozen. This form assigns the `Field` call to the field annotation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Model(BaseModel):
    name: str = Field(frozen=True)
```

---

TITLE: Demonstrating Pydantic ValidationError Handling
DESCRIPTION: This Python code defines a Pydantic `Model` with various field types and custom validation. It then attempts to instantiate the model with invalid data, catches the `ValidationError`, and demonstrates printing the error object directly and accessing detailed error information using `e.errors()`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/errors.md#_snippet_2

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError, field_validator


class Location(BaseModel):
    lat: float = 0.1
    lng: float = 10.1


class Model(BaseModel):
    is_required: float
    gt_int: int = Field(gt=42)
    list_of_ints: list[int]
    a_float: float
    recursive_model: Location

    @field_validator('a_float', mode='after')
    @classmethod
    def validate_float(cls, value: float) -> float:
        if value > 2.0:
            raise ValueError('Invalid float value')
        return value


data = {
    'list_of_ints': ['1', 2, 'bad'],
    'a_float': 3.0,
    'recursive_model': {'lat': 4.2, 'lng': 'New York'},
    'gt_int': 21,
}

try:
    Model(**data)
except ValidationError as e:
    print(e)
    """
    5 validation errors for Model
    is_required
      Field required [type=missing, input_value={'list_of_ints': ['1', 2,...ew York'}, 'gt_int': 21}, input_type=dict]
    gt_int
      Input should be greater than 42 [type=greater_than, input_value=21, input_type=int]
    list_of_ints.2
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    a_float
      Value error, Invalid float value [type=value_error, input_value=3.0, input_type=float]
    recursive_model.lng
      Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='New York', input_type=str]
    """

try:
    Model(**data)
except ValidationError as e:
    print(e.errors())
    """
    [
        {
            'type': 'missing',
            'loc': ('is_required',),
            'msg': 'Field required',
            'input': {
                'list_of_ints': ['1', 2, 'bad'],
                'a_float': 3.0,
                'recursive_model': {'lat': 4.2, 'lng': 'New York'},
                'gt_int': 21,
            },

```

---

TITLE: Configure Pydantic Model with model_config Attribute
DESCRIPTION: Demonstrates how to set configuration for a Pydantic `BaseModel` using the `model_config` class attribute with `ConfigDict`. It shows an example of `str_max_length` validation and the resulting `ValidationError` when input exceeds the limit.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    model_config = ConfigDict(str_max_length=5)  # (1)!

    v: str


try:
    m = Model(v='abcdef')
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    v
      String should have at most 5 characters [type=string_too_long, input_value='abcdef', input_type=str]
    """
```

---

TITLE: Modifying Pydantic Schema with Annotated Metadata and **get_pydantic_core_schema**
DESCRIPTION: This example illustrates how to use `__get_pydantic_core_schema__` with `Annotated` metadata to add custom validation to an existing type. The `RestrictCharacters` class defines a validator that ensures a string's characters are within a specified alphabet. Unlike custom types, this implementation calls `handler(source)` to obtain the base schema before applying additional validation. It demonstrates schema generation, successful validation, and error handling for invalid inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_21

LANGUAGE: python
CODE:

```
from dataclasses import dataclass
from typing import Annotated, Any, Sequence

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler, ValidationError


@dataclass
class RestrictCharacters:
    alphabet: Sequence[str]

    def __get_pydantic_core_schema__(
        self, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        if not self.alphabet:
            raise ValueError('Alphabet may not be empty')
        schema = handler(
            source
        )  # get the CoreSchema from the type / inner constraints
        if schema['type'] != 'str':
            raise TypeError('RestrictCharacters can only be applied to strings')
        return core_schema.no_info_after_validator_function(
            self.validate,
            schema,
        )

    def validate(self, value: str) -> str:
        if any(c not in self.alphabet for c in value):
            raise ValueError(
                f'{value!r} is not restricted to {self.alphabet!r}'
            )
        return value


class MyModel(BaseModel):
    value: Annotated[str, RestrictCharacters('ABC')]


print(MyModel.model_json_schema())
"""
{
    'properties': {'value': {'title': 'Value', 'type': 'string'}},
    'required': ['value'],
    'title': 'MyModel',
    'type': 'object',
}
"""
print(MyModel(value='CBA'))
#> value='CBA'

try:
    MyModel(value='XYZ')
except ValidationError as e:
    print(e)
    """
    1 validation error for MyModel
    value
      Value error, 'XYZ' is not restricted to 'ABC' [type=value_error, input_value='XYZ', input_type=str]
    """
```

---

TITLE: Pydantic Callable Discriminator for Union of Models
DESCRIPTION: This example demonstrates using a callable `Discriminator` to differentiate between `BaseModel` types within a `Union` (e.g., `ApplePie` and `PumpkinPie`). The `get_discriminator_value` function handles both dictionary and model inputs to correctly identify the specific model during validation and serialization.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_5

LANGUAGE: python
CODE:

```
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Discriminator, Tag


class Pie(BaseModel):
    time_to_cook: int
    num_ingredients: int


class ApplePie(Pie):
    fruit: Literal['apple'] = 'apple'


class PumpkinPie(Pie):
    filling: Literal['pumpkin'] = 'pumpkin'


def get_discriminator_value(v: Any) -> str:
    if isinstance(v, dict):
        return v.get('fruit', v.get('filling'))
    return getattr(v, 'fruit', getattr(v, 'filling', None))


class ThanksgivingDinner(BaseModel):
    dessert: Annotated[
        Union[
            Annotated[ApplePie, Tag('apple')],
            Annotated[PumpkinPie, Tag('pumpkin')],
        ],
        Discriminator(get_discriminator_value),
    ]


apple_variation = ThanksgivingDinner.model_validate(
    {'dessert': {'fruit': 'apple', 'time_to_cook': 60, 'num_ingredients': 8}}
)
print(repr(apple_variation))
"""
ThanksgivingDinner(dessert=ApplePie(time_to_cook=60, num_ingredients=8, fruit='apple'))
"""

pumpkin_variation = ThanksgivingDinner.model_validate(
    {
        'dessert': {
            'filling': 'pumpkin',
            'time_to_cook': 40,
            'num_ingredients': 6,
        }
    }
)
print(repr(pumpkin_variation))
"""
ThanksgivingDinner(dessert=PumpkinPie(time_to_cook=40, num_ingredients=6, filling='pumpkin'))
"""
```

---

TITLE: Overriding Pydantic Schema for Custom Types with **get_pydantic_core_schema**
DESCRIPTION: This example demonstrates how to completely override Pydantic's schema generation for a custom type, `CompressedString`. It defines custom validation (`_validate`) and serialization (`_serialize`) logic within `__get_pydantic_core_schema__` using `core_schema.no_info_after_validator_function` and `core_schema.plain_serializer_function_ser_schema`. The example shows how `MyModel` uses `CompressedString` and prints its generated JSON schema, validated instance, and serialized output.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_20

LANGUAGE: python
CODE:

```
from dataclasses import dataclass
from typing import Any

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler


@dataclass
class CompressedString:
    dictionary: dict[int, str]
    text: list[int]

    def build(self) -> str:
        return ' '.join([self.dictionary[key] for key in self.text])

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        assert source is CompressedString
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                info_arg=False,
                return_schema=core_schema.str_schema(),
            ),
        )

    @staticmethod
    def _validate(value: str) -> 'CompressedString':
        inverse_dictionary: dict[str, int] = {}
        text: list[int] = []
        for word in value.split(' '):
            if word not in inverse_dictionary:
                inverse_dictionary[word] = len(inverse_dictionary)
            text.append(inverse_dictionary[word])
        return CompressedString(
            {v: k for k, v in inverse_dictionary.items()}, text
        )

    @staticmethod
    def _serialize(value: 'CompressedString') -> str:
        return value.build()


class MyModel(BaseModel):
    value: CompressedString


print(MyModel.model_json_schema())
"""
{
    'properties': {'value': {'title': 'Value', 'type': 'string'}},
    'required': ['value'],
    'title': 'MyModel',
    'type': 'object',
}
"""
print(MyModel(value='fox fox fox dog fox'))
"""
value = CompressedString(dictionary={0: 'fox', 1: 'dog'}, text=[0, 0, 0, 1, 0])
"""

print(MyModel(value='fox fox fox dog fox').model_dump(mode='json'))
#> {'value': 'fox fox fox dog fox'}
```

---

TITLE: Pydantic Model Duplication with model_copy
DESCRIPTION: This example demonstrates the usage of `model_copy()` to duplicate Pydantic models. It shows how to create a copy with optional updates to specific fields and how the `deep=True` argument can be used to ensure that nested models are also duplicated, rather than just having their references copied.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_23

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class BarModel(BaseModel):
    whatever: int


class FooBarModel(BaseModel):
    banana: float
    foo: str
    bar: BarModel


m = FooBarModel(banana=3.14, foo='hello', bar={'whatever': 123})

print(m.model_copy(update={'banana': 0}))
#> banana=0 foo='hello' bar=BarModel(whatever=123)
print(id(m.bar) == id(m.model_copy().bar))
#> True
# normal copy gives the same object reference for bar
print(id(m.bar) == id(m.model_copy(deep=True).bar))
#> False
# deep copy gives a new object reference for `bar`
```

---

TITLE: Pydantic Model Dump Exclusion Parameters
DESCRIPTION: This example illustrates how `exclude_unset`, `exclude_none`, and `exclude_defaults` parameters in `model_dump` can override `Field(exclude=False)`. It demonstrates that these parameters provide fine-grained control over what gets included in the dumped output based on the field's state (unset, None, or default value).
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_21

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str
    age: Optional[int] = Field(None, exclude=False)


person = Person(name='Jeremy')

print(person.model_dump())
#> {'name': 'Jeremy', 'age': None}
print(person.model_dump(exclude_none=True))
#> {'name': 'Jeremy'}
print(person.model_dump(exclude_unset=True))
#> {'name': 'Jeremy'}
print(person.model_dump(exclude_defaults=True))
#> {'name': 'Jeremy'}
```

---

TITLE: Integrating Pydantic Models with ARQ for Job Processing (Python)
DESCRIPTION: This Python snippet demonstrates how to use Pydantic BaseModel to define the structure of job data (User model) for an ARQ job queue. It shows how to serialize Pydantic models for enqueuing jobs (user.model_dump()) and deserialize/validate them when processing jobs (User.model_validate(user_data)), ensuring type safety and data integrity for background tasks. It requires Redis to be installed and running.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/queues.md#_snippet_3

LANGUAGE: python
CODE:

```
import asyncio
from typing import Any

from arq import create_pool
from arq.connections import RedisSettings

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


REDIS_SETTINGS = RedisSettings()


async def process_user(ctx: dict[str, Any], user_data: dict[str, Any]) -> None:
    user = User.model_validate(user_data)
    print(f'Processing user: {repr(user)}')


async def enqueue_jobs(redis):
    user1 = User(id=1, name='John Doe', email='john@example.com')
    user2 = User(id=2, name='Jane Doe', email='jane@example.com')

    await redis.enqueue_job('process_user', user1.model_dump())
    print(f'Enqueued user: {repr(user1)}')

    await redis.enqueue_job('process_user', user2.model_dump())
    print(f'Enqueued user: {repr(user2)}')


class WorkerSettings:
    functions = [process_user]
    redis_settings = REDIS_SETTINGS


async def main():
    redis = await create_pool(REDIS_SETTINGS)
    await enqueue_jobs(redis)


if __name__ == '__main__':
    asyncio.run(main())
```

---

TITLE: Receiving and Validating Pydantic Data from RabbitMQ (Python)
DESCRIPTION: This Python script demonstrates how to consume messages from a RabbitMQ queue, deserialize the JSON body into a Pydantic `User` model, and validate it. It uses `pika` to set up a consumer that processes incoming messages. A running RabbitMQ server is required.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/queues.md#_snippet_2

LANGUAGE: python
CODE:

```
import pika

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    QUEUE_NAME = 'user_queue'
    channel.queue_declare(queue=QUEUE_NAME)

    def process_message(
        ch: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ):
        user = User.model_validate_json(body)
        print(f'Validated user: {repr(user)}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
```

---

TITLE: Using Field Name Discriminator in Pydantic Union
DESCRIPTION: Demonstrates how to use the `discriminator` parameter with a field name ('pet_type') in a `Field` definition to distinguish between models (`Cat`, `Dog`) in a `Union`. Shows how `model_validate` uses this field to determine the correct model.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_26

LANGUAGE: python
CODE:

```
from typing import Literal, Union

from pydantic import BaseModel, Field


class Cat(BaseModel):
    pet_type: Literal['cat']
    age: int


class Dog(BaseModel):
    pet_type: Literal['dog']
    age: int


class Model(BaseModel):
    pet: Union[Cat, Dog] = Field(discriminator='pet_type')


print(Model.model_validate({'pet': {'pet_type': 'cat', 'age': 12}}))
```

---

TITLE: Pydantic V2 BaseModel API Changes and Deprecations
DESCRIPTION: This section provides a comprehensive overview of the API changes for `pydantic.BaseModel` when migrating from Pydantic V1 to V2, including method renames, deprecated functionalities, new features, and behavioral modifications.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_9

LANGUAGE: APIDOC
CODE:

```
pydantic.BaseModel Changes (V1 to V2):

Method Renames:
- __fields__ -> model_fields
- __private_attributes__ -> __pydantic_private__
- __validators__ -> __pydantic_validator__
- construct() -> model_construct()
- copy() -> model_copy()
- dict() -> model_dump()
- json_schema() -> model_json_schema()
- json() -> model_dump_json()
- parse_obj() -> model_validate()
- update_forward_refs() -> model_rebuild()

Deprecated Methods:
- parse_raw: Use model_validate_json or load data then pass to model_validate.
- parse_file: Load data then pass to model_validate.
- from_orm: Use model_validate with from_attributes=True in model config.
- .json(): Use model_dump_json().
- json_encoders (in model config): Use new serialization decorators.
- GetterDict: Removed (was an implementation detail of orm_mode).

New Functionality:
- RootModel: Replaces __root__ field for custom root models.
- Serialization Decorators:
  - @field_serializer
  - @model_serializer
  - @computed_field

Behavioral Changes:
- __eq__ method:
  - Only equal to other BaseModel instances.
  - Requires same type (or non-parametrized generic origin type), field values, extra values (if 'extra' == 'allow'), and private attribute values.
  - Not equal to dicts containing their data.
  - Non-generic models of different types are never equal.
  - Generic models with different origin types are never equal.
- Subclass Serialization: Only includes fields defined on the annotated type of the field when dumping a model (V2 behavior).
- Constructor Arguments: Arguments passed to constructor may be copied in order to perform validation and coercion.
```

---

TITLE: Defining and Instantiating Pydantic Generic Models
DESCRIPTION: Illustrates different ways to define and instantiate Pydantic models using generic type variables, both with and without bounds, and shows that the serialization output is the same regardless of how the generic type is specified.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_35

LANGUAGE: python
CODE:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

TBound = TypeVar('TBound', bound=BaseModel)
TNoBound = TypeVar('TNoBound')


class IntValue(BaseModel):
    value: int


class ItemBound(BaseModel, Generic[TBound]):
    item: TBound


class ItemNoBound(BaseModel, Generic[TNoBound]):
    item: TNoBound


item_bound_inferred = ItemBound(item=IntValue(value=3))
item_bound_explicit = ItemBound[IntValue](item=IntValue(value=3))
item_no_bound_inferred = ItemNoBound(item=IntValue(value=3))
item_no_bound_explicit = ItemNoBound[IntValue](item=IntValue(value=3))

# calling `print(x.model_dump())` on any of the above instances results in the following:
#> {'item': {'value': 3}}
```

---

TITLE: Parse Data into a List of BaseModel Instances using TypeAdapter
DESCRIPTION: This snippet illustrates how `TypeAdapter` can be used to parse raw data, such as a list of dictionaries, into a specified Pydantic type, like a `list[Item]` where `Item` is a `BaseModel`. This is useful for ad-hoc data parsing without direct `BaseModel` subclassing.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md#_snippet_2

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, TypeAdapter


class Item(BaseModel):
    id: int
    name: str


# `item_data` could come from an API call, eg., via something like:
# item_data = requests.get('https://my-api.com/items').json()
item_data = [{'id': 1, 'name': 'My Item'}]

items = TypeAdapter(list[Item]).validate_python(item_data)
print(items)
#> [Item(id=1, name='My Item')]
```

---

TITLE: Validate and Serialize TypedDict with Pydantic TypeAdapter
DESCRIPTION: This example demonstrates how to use Pydantic's `TypeAdapter` to validate and serialize a Python `TypedDict`. It shows how to validate Python objects and generate a JSON schema for the `TypedDict` structure, highlighting `validate_python`, `dump_python`, and `json_schema` methods.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_5

LANGUAGE: python
CODE:

```
from datetime import datetime

from typing_extensions import NotRequired, TypedDict

from pydantic import TypeAdapter


class Meeting(TypedDict):
    when: datetime
    where: bytes
    why: NotRequired[str]


meeting_adapter = TypeAdapter(Meeting)
m = meeting_adapter.validate_python(  # (1)!
    {'when': '2020-01-01T12:00', 'where': 'home'}
)
print(m)
#> {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}
meeting_adapter.dump_python(m, exclude={'where'})  # (2)!

print(meeting_adapter.json_schema())  # (3)!
"""
{
    'properties': {
        'when': {'format': 'date-time', 'title': 'When', 'type': 'string'},
        'where': {'format': 'binary', 'title': 'Where', 'type': 'string'},
        'why': {'title': 'Why', 'type': 'string'},
    },
    'required': ['when', 'where'],
    'title': 'Meeting',
    'type': 'object',
}
"""
```

---

TITLE: Customize Pydantic Validation Error Messages with Custom Text
DESCRIPTION: This Python code demonstrates how to create a custom error handler for Pydantic ValidationError exceptions. It uses a dictionary of custom messages to replace default error messages based on their 'type' and formats them using context variables. This allows for more user-friendly or translated error messages.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/errors.md#_snippet_4

LANGUAGE: python
CODE:

```
from pydantic_core import ErrorDetails

from pydantic import BaseModel, HttpUrl, ValidationError

CUSTOM_MESSAGES = {
    'int_parsing': 'This is not an integer! 🤦',
    'url_scheme': 'Hey, use the right URL scheme! I wanted {expected_schemes}.',
}


def convert_errors(
    e: ValidationError, custom_messages: dict[str, str]
) -> list[ErrorDetails]:
    new_errors: list[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error['type'])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = (
                custom_message.format(**ctx) if ctx else custom_message
            )
        new_errors.append(error)
    return new_errors


class Model(BaseModel):
    a: int
    b: HttpUrl


try:
    Model(a='wrong', b='ftp://example.com')
except ValidationError as e:
    errors = convert_errors(e, CUSTOM_MESSAGES)
    print(errors)
    """
    [
        {
            'type': 'int_parsing',
            'loc': ('a',),
            'msg': 'This is not an integer! 🤦',
            'input': 'wrong',
            'url': 'https://errors.pydantic.dev/2/v/int_parsing',
        },
        {
            'type': 'url_scheme',
            'loc': ('b',),
            'msg': "Hey, use the right URL scheme! I wanted 'http' or 'https'.",
            'input': 'ftp://example.com',
            'ctx': {'expected_schemes': "'http' or 'https'"},
            'url': 'https://errors.pydantic.dev/2/v/url_scheme',
        },
    ]
    """
```

---

TITLE: Generate JSON Schema from Pydantic BaseModel
DESCRIPTION: This example demonstrates how to generate a JSON schema from a Pydantic `BaseModel` using the `model_json_schema()` method. The method returns a 'jsonable' dictionary, which can then be serialized into a JSON string using `json.dumps()`. It showcases defining nested models, enums, and fields with custom configurations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_1

LANGUAGE: python
CODE:

```
import json
from enum import Enum
from typing import Annotated, Union

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class FooBar(BaseModel):
    count: int
    size: Union[float, None] = None


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    not_given = 'not_given'


class MainModel(BaseModel):
    """
    This is the description of the main model
    """

    model_config = ConfigDict(title='Main')

    foo_bar: FooBar
    gender: Annotated[Union[Gender, None], Field(alias='Gender')] = None
    snap: int = Field(
        default=42,
        title='The Snap',
        description='this is the value of snap',
        gt=30,
        lt=50,
    )


main_model_schema = MainModel.model_json_schema()  # (1)!
print(json.dumps(main_model_schema, indent=2))  # (2)!
"""
{
  "$defs": {
    "FooBar": {
      "properties": {
        "count": {
          "title": "Count",
          "type": "integer"
        },
        "size": {
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Size"
        }
      },
      "required": [
        "count"
      ],
      "title": "FooBar",
      "type": "object"
    },
    "Gender": {
      "enum": [
        "male",
        "female",
        "other",
        "not_given"
      ],
      "title": "Gender",
      "type": "string"
    }
  },
  "description": "This is the description of the main model",
  "properties": {
    "foo_bar": {
      "$ref": "#/$defs/FooBar"
    },
    "Gender": {
      "anyOf": [
        {
          "$ref": "#/$defs/Gender"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "snap": {
      "default": 42,
      "description": "this is the value of snap",
      "exclusiveMaximum": 50,
      "exclusiveMinimum": 30,
      "title": "The Snap",
      "type": "integer"
    }
  },
  "required": [
    "foo_bar"
  ],
  "title": "Main",
  "type": "object"
}
"""
```

---

TITLE: Configure Global Strict Mode for Pydantic BaseModel
DESCRIPTION: Illustrates enabling strict validation for all fields within a Pydantic `BaseModel` by setting `model_config = ConfigDict(strict=True)`. This applies strictness globally to the model, but individual fields can override it with `strict=False`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_11

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, ValidationError


class User(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    age: int
    is_active: bool


try:
    User(name='David', age='33', is_active='yes')
except ValidationError as exc:
    print(exc)
    """
    2 validation errors for User
    age
      Input should be a valid integer [type=int_type, input_value='33', input_type=str]
    is_active
      Input should be a valid boolean [type=bool_type, input_value='yes', input_type=str]
    """
```

---

TITLE: Integrating Pydantic with SQLAlchemy Models using Aliases - Python
DESCRIPTION: This snippet demonstrates how to use Pydantic models alongside SQLAlchemy models, specifically addressing conflicts with SQLAlchemy's reserved field names like 'metadata'. It shows how to define a Pydantic `BaseModel` with an alias (`metadata_`) for a field that corresponds to a SQLAlchemy `Column` named 'metadata', enabling seamless data validation and serialization. The example illustrates validating an SQLAlchemy model instance with a Pydantic model and dumping its content.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/orms.md#_snippet_0

LANGUAGE: Python
CODE:

```
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from pydantic import BaseModel, ConfigDict, Field


class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metadata: dict[str, str] = Field(alias='metadata_')


Base = declarative_base()


class MyTableModel(Base):
    __tablename__ = 'my_table'
    id = sa.Column('id', sa.Integer, primary_key=True)
    # 'metadata' is reserved by SQLAlchemy, hence the '_'
    metadata_ = sa.Column('metadata', sa.JSON)


sql_model = MyTableModel(metadata_={'key': 'val'}, id=1)
pydantic_model = MyModel.model_validate(sql_model)

print(pydantic_model.model_dump())
#> {'metadata': {'key': 'val'}}
print(pydantic_model.model_dump(by_alias=True))
#> {'metadata_': {'key': 'val'}}
```

---

TITLE: Integrate Partial JSON Parsing with Pydantic Models
DESCRIPTION: Illustrates how to combine `pydantic_core.from_json` with `BaseModel.model_validate` to parse partial JSON data directly into a Pydantic model. This allows for robust validation of incomplete inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md#_snippet_4

LANGUAGE: python
CODE:

```
from pydantic_core import from_json

from pydantic import BaseModel


class Dog(BaseModel):
    breed: str
    name: str
    friends: list


partial_dog_json = '{"breed": "lab", "name": "fluffy", "friends": ["buddy", "spot", "rufus"], "age'
dog = Dog.model_validate(from_json(partial_dog_json, allow_partial=True))
print(repr(dog))
# > Dog(breed='lab', name='fluffy', friends=['buddy', 'spot', 'rufus'])
```

---

TITLE: Dynamically Modify Pydantic JSON Schema with `json_schema_extra` Callable
DESCRIPTION: This example illustrates how to use a Python callable (function) with `json_schema_extra` to dynamically modify the generated JSON schema. The provided function receives the schema dictionary and can perform operations like removing specific keys (e.g., 'default') before the schema is finalized.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_15

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel, Field


def pop_default(s):
    s.pop('default')


class Model(BaseModel):
    a: int = Field(default=1, json_schema_extra=pop_default)


print(json.dumps(Model.model_json_schema(), indent=2))
"""
{
  "properties": {
    "a": {
      "title": "A",
      "type": "integer"
    }
  },
  "title": "Model",
  "type": "object"
}
"""
```

---

TITLE: Generate JSON Schema from Pydantic Models
DESCRIPTION: Illustrates how to generate a JSON Schema from Pydantic models, enabling self-documenting APIs and integration with JSON Schema-compatible tools. It shows the schema output for nested models.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_3

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    zipcode: str


class Meeting(BaseModel):
    when: datetime
    where: Address
    why: str = 'No idea'


print(Meeting.model_json_schema())
"""
{
    '$defs': {
        'Address': {
            'properties': {
                'street': {'title': 'Street', 'type': 'string'},
                'city': {'title': 'City', 'type': 'string'},
                'zipcode': {'title': 'Zipcode', 'type': 'string'}
            },
            'required': ['street', 'city', 'zipcode'],
            'title': 'Address',
            'type': 'object'
        }
    },
    'properties': {
        'when': {'format': 'date-time', 'title': 'When', 'type': 'string'},
        'where': {'$ref': '#/$defs/Address'},
        'why': {'default': 'No idea', 'title': 'Why', 'type': 'string'}
    },
    'required': ['when', 'where'],
    'title': 'Meeting',
    'type': 'object'
}
"""
```

---

TITLE: Pydantic Union Type Validation
DESCRIPTION: Pydantic provides extensive support for union validation, including both `typing.Union` and Python 3.10's pipe syntax (`A | B`).
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_23

LANGUAGE: APIDOC
CODE:

```
Supported Union Types:
- typing.Union
- A | B (Python 3.10+)
```

---

TITLE: Validate Nested Pydantic Model Fields with Outer Model Validator
DESCRIPTION: Demonstrates validating a field of a nested Pydantic model by placing a custom @model_validator on the outer (parent) model. The validator checks if a user's password is in a list of forbidden passwords defined in the parent model, raising a ValueError if a forbidden password is encountered.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md#_snippet_2

LANGUAGE: python
CODE:

```
from typing_extensions import Self

from pydantic import BaseModel, ValidationError, model_validator


class User(BaseModel):
    username: str
    password: str


class Organization(BaseModel):
    forbidden_passwords: list[str]
    users: list[User]

    @model_validator(mode='after')
    def validate_user_passwords(self) -> Self:
        """Check that user password is not in forbidden list. Raise a validation error if a forbidden password is encountered."""
        for user in self.users:
            current_pw = user.password
            if current_pw in self.forbidden_passwords:
                raise ValueError(
                    f'Password {current_pw} is forbidden. Please choose another password for user {user.username}.'
                )
        return self


data = {
    'forbidden_passwords': ['123'],
    'users': [
        {'username': 'Spartacat', 'password': '123'},
        {'username': 'Iceburgh', 'password': '87'},
    ],
}
try:
    org = Organization(**data)
except ValidationError as e:
    print(e)
    """
    1 validation error for Organization
      Value error, Password 123 is forbidden. Please choose another password for user Spartacat. [type=value_error, input_value={'forbidden_passwords': [...gh', 'password': '87'}]}, input_type=dict]
    """

```

---

TITLE: Defining Pydantic Model with alias and serialization_alias - Python
DESCRIPTION: This snippet shows how to use both `alias` (for validation/parsing) and `serialization_alias` (for serialization) simultaneously. It also includes an example of instantiating the model using the alias and dumping it back, showing the effect of `by_alias=True`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_17

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class MyModel(BaseModel):
    my_field: int = Field(
        alias='myValidationAlias',
        serialization_alias='my_field',
    )


m = MyModel(myValidationAlias=1)
print(m.model_dump(by_alias=True))
#> {'my_field': 1}
```

---

TITLE: Handling Pydantic Validation Errors in Python
DESCRIPTION: This Python snippet shows how to catch and print `ValidationError` exceptions raised by Pydantic when validating invalid JSON data. It defines the same `Person` model and attempts to validate a flawed JSON string, demonstrating how Pydantic aggregates multiple validation issues.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_3

LANGUAGE: python
CODE:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt, ValidationError


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


json_string = pathlib.Path('person.json').read_text()
try:
    person = Person.model_validate_json(json_string)
except ValidationError as err:
    print(err)
    """
    3 validation errors for Person
    name
    Field required [type=missing, input_value={'age': -30, 'email': 'not-an-email-address'}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.10/v/missing
    age
    Input should be greater than 0 [type=greater_than, input_value=-30, input_type=int]
        For further information visit https://errors.pydantic.dev/2.10/v/greater_than
    email
    value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='not-an-email-address', input_type=str]
    """
```

---

TITLE: Migrating Pydantic Constrained Types to Annotated Field
DESCRIPTION: Pydantic V2 removes `Constrained*` classes. This snippet demonstrates how to replace them with `Annotated[<type>, Field(...)]` for defining constrained types, such as an integer greater than or equal to zero. This new pattern provides a more flexible and explicit way to define type constraints.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_28

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConstrainedInt


class MyInt(ConstrainedInt):
    ge = 0


class Model(BaseModel):
    x: MyInt
```

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, Field

MyInt = Annotated[int, Field(ge=0)]


class Model(BaseModel):
    x: MyInt
```

---

TITLE: Define Custom Float Type with Validation and Serialization
DESCRIPTION: This snippet illustrates how to define a custom float type (`TruncatedFloat`) using `Annotated` and Pydantic's validation and serialization markers (`AfterValidator`, `PlainSerializer`, `WithJsonSchema`). It demonstrates applying validation logic (rounding), custom serialization (to scientific notation string), and defining different JSON schemas for validation and serialization modes.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_2

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import (
    AfterValidator,
    PlainSerializer,
    TypeAdapter,
    WithJsonSchema,
)

TruncatedFloat = Annotated[
    float,
    AfterValidator(lambda x: round(x, 1)),
    PlainSerializer(lambda x: f'{x:.1e}', return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]


ta = TypeAdapter(TruncatedFloat)

input = 1.02345
assert input != 1.0

assert ta.validate_python(input) == 1.0

assert ta.dump_json(input) == b'"1.0e+00"'

assert ta.json_schema(mode='validation') == {'type': 'number'}
assert ta.json_schema(mode='serialization') == {'type': 'string'}
```

---

TITLE: Allowing Extra Data in Pydantic Model - Python
DESCRIPTION: Configures a Pydantic model using `ConfigDict(extra='allow')` to accept extra data. The extra fields are included in `model_dump()` and stored in the `__pydantic_extra__` attribute. Requires `pydantic.BaseModel` and `pydantic.ConfigDict`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_8

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    x: int

    model_config = ConfigDict(extra='allow')


m = Model(x=1, y='a')  # (1)!
assert m.model_dump() == {'x': 1, 'y': 'a'}
assert m.__pydantic_extra__ == {'y': 'a'}
```

---

TITLE: Parsing Nested Attributes with Pydantic from_attributes (Python)
DESCRIPTION: Illustrates how Pydantic's `from_attributes` handles nested data structures by defining simple custom classes `PetCls` and `PersonCls` and corresponding Pydantic models `Pet` and `Person`, both configured with `from_attributes=True`. Shows creating instances of the custom classes, including nested ones, and then validating the top-level instance into the Pydantic model.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_12

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class PetCls:
    def __init__(self, *, name: str, species: str):
        self.name = name
        self.species = species


class PersonCls:
    def __init__(self, *, name: str, age: float = None, pets: list[PetCls]):
        self.name = name
        self.age = age
        self.pets = pets


class Pet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    species: str


class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: float = None
    pets: list[Pet]


bones = PetCls(name='Bones', species='dog')
orion = PetCls(name='Orion', species='cat')
anna = PersonCls(name='Anna', age=20, pets=[bones, orion])
anna_model = Person.model_validate(anna)
print(anna_model)
"""
name='Anna' age=20.0 pets=[Pet(name='Bones', species='dog'), Pet(name='Orion', species='cat')]
"""
```

---

TITLE: Validate and Serialize Data with TypeAdapter using TypedDict
DESCRIPTION: This example demonstrates how to use `TypeAdapter` to validate and serialize a list of `TypedDict` objects. It shows successful validation, error handling for invalid input, and JSON serialization of the validated data.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing_extensions import TypedDict

from pydantic import TypeAdapter, ValidationError


class User(TypedDict):
    name: str
    id: int


user_list_adapter = TypeAdapter(list[User])
user_list = user_list_adapter.validate_python([{'name': 'Fred', 'id': '3'}])
print(repr(user_list))
#> [{'name': 'Fred', 'id': 3}]

try:
    user_list_adapter.validate_python(
        [{'name': 'Fred', 'id': 'wrong', 'other': 'no'}]
    )
except ValidationError as e:
    print(e)
    """
    1 validation error for list[User]
    0.id
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='wrong', input_type=str]
    """

print(repr(user_list_adapter.dump_json(user_list)))
#> b'[{"name":"Fred","id":3}]'
```

---

TITLE: Applying String Constraints with Pydantic Field
DESCRIPTION: This snippet demonstrates how to use `min_length`, `max_length`, and `pattern` arguments within `pydantic.Field` to enforce constraints on string fields in a Pydantic `BaseModel`. It shows defining a model with these constraints and instantiating it with valid data.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_21

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Foo(BaseModel):
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r'^\d*$')  # (1)!


foo = Foo(short='foo', long='foobarbaz', regex='123')
print(foo)
```

---

TITLE: Using `validate_call` for Function Argument Validation (Python)
DESCRIPTION: This snippet demonstrates the basic application of the `@validate_call` decorator to a Python function. It shows how arguments are validated and coerced, and how `ValidationError` is raised for invalid inputs, providing robust type checking for function parameters.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validation_decorator.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import ValidationError, validate_call


@validate_call
def repeat(s: str, count: int, *, separator: bytes = b'') -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))


a = repeat('hello', 3)
print(a)
# b'hellohellohello'

b = repeat('x', '4', separator=b' ')
print(b)
# b'x x x x'

try:
    c = repeat('hello', 'wrong')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for repeat
    1
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='wrong', input_type=str]
    """
```

---

TITLE: Validate and Generate Schema for List of Integers using Pydantic TypeAdapter
DESCRIPTION: This Python snippet demonstrates the basic usage of Pydantic V2's `TypeAdapter` to validate a list of strings as integers and then generate its corresponding JSON schema. It shows how `TypeAdapter` simplifies handling non-`BaseModel` types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_24

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
assert adapter.validate_python(['1', '2', '3']) == [1, 2, 3]
print(adapter.json_schema())
#> {'items': {'type': 'integer'}, 'type': 'array'}
```

---

TITLE: Pydantic ValidationError Methods
DESCRIPTION: This section describes the methods available on a Pydantic `ValidationError` object for accessing details about validation failures.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/errors.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
ValidationError Methods:
- errors(): Returns a list of ErrorDetails errors found in the input data.
- error_count(): Returns the number of errors.
- json(): Returns a JSON representation of the list errors.
- str(e): Returns a human-readable representation of the errors.
```

---

TITLE: Validating Single JSON Data with Pydantic in Python
DESCRIPTION: This Python snippet demonstrates how to define a Pydantic `BaseModel` for a `Person` and validate a JSON string against it. It reads a JSON file, parses its content, and uses `Person.model_validate_json()` to create a `Person` object, ensuring data integrity.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_1

LANGUAGE: python
CODE:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


json_string = pathlib.Path('person.json').read_text()
person = Person.model_validate_json(json_string)
print(person)
#> name='John Doe' age=30 email='john@example.com'
```

---

TITLE: Install Pydantic with Optional Dependencies
DESCRIPTION: Commands to install Pydantic along with optional features like email validation and timezone support using pip or uv. Users can also install the dependency packages manually.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/install.md#_snippet_1

LANGUAGE: bash
CODE:

```
pip install 'pydantic[email]'
```

LANGUAGE: bash
CODE:

```
pip install 'pydantic[email,timezone]'
```

LANGUAGE: bash
CODE:

```
uv add 'pydantic[email]'
```

LANGUAGE: bash
CODE:

```
uv add 'pydantic[email,timezone]'
```

LANGUAGE: bash
CODE:

```
pip install email-validator tzdata
```

---

TITLE: Serializing Pydantic Model to Dictionary (Python)
DESCRIPTION: Shows how to use the `model_dump()` method to serialize the Pydantic model instance into a standard Python dictionary. This method recursively converts nested models and provides customization options.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_3

LANGUAGE: python
CODE:

```
assert user.model_dump() == {'id': 123, 'name': 'Jane Doe'}
```

---

TITLE: Sending Pydantic Validated Data to RabbitMQ (Python)
DESCRIPTION: This Python script shows how to serialize Pydantic `User` model data into JSON and publish it to a RabbitMQ queue using `pika`. It acts as a sender, pushing messages to the queue for a receiver to consume. A running RabbitMQ server is required.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/queues.md#_snippet_1

LANGUAGE: python
CODE:

```
import pika

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
QUEUE_NAME = 'user_queue'
channel.queue_declare(queue=QUEUE_NAME)


def push_to_queue(user_data: User) -> None:
    serialized_data = user_data.model_dump_json()
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=serialized_data,
    )
    print(f'Added to queue: {serialized_data}')


user1 = User(id=1, name='John Doe', email='john@example.com')
user2 = User(id=2, name='Jane Doe', email='jane@example.com')

push_to_queue(user1)
#> Added to queue: {"id":1,"name":"John Doe","email":"john@example.com"}

push_to_queue(user2)
#> Added to queue: {"id":2,"name":"Jane Doe","email":"jane@example.com"}

connection.close()
```

---

TITLE: Monitoring Pydantic with Logfire
DESCRIPTION: This snippet demonstrates how to integrate Pydantic with Logfire for application monitoring. It shows how to instrument Pydantic to record both successful and failed validations, providing insights into data inputs and validation errors. The example defines a `Delivery` BaseModel and shows both a successful validation and a failed one due to incorrect dimensions, with details recorded in Logfire.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/index.md#_snippet_0

LANGUAGE: Python
CODE:

```
from datetime import datetime

import logfire

from pydantic import BaseModel

logfire.configure()
logfire.instrument_pydantic()


class Delivery(BaseModel):
    timestamp: datetime
    dimensions: tuple[int, int]


# this will record details of a successful validation to logfire
m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
print(m.dimensions)
#> (10, 20)

Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10'])
```

---

TITLE: Logging Pydantic Model Data with Logfire (Python)
DESCRIPTION: This snippet demonstrates how to configure Logfire and log Pydantic model instances. It initializes Logfire with `logfire.configure()` and then uses `logfire.info()` to log a `User` model, showcasing Logfire's ability to capture and display Pydantic object details for observability.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/logfire.md#_snippet_0

LANGUAGE: python
CODE:

```
from datetime import date

import logfire

from pydantic import BaseModel

logfire.configure()  # (1)!


class User(BaseModel):
    name: str
    country_code: str
    dob: date


user = User(name='Anne', country_code='USA', dob='2000-01-01')
logfire.info('user processed: {user!r}', user=user)  # (2)!
```

---

TITLE: Python: Postponed Annotation Evaluation with Future Import
DESCRIPTION: This example demonstrates the effect of `from __future__ import annotations`, which postpones the evaluation of type hints by stringifying them. When used with Pydantic's `BaseModel`, it shows that the annotation `f: MyType` is internally stored as the string `'MyType'`, allowing `MyType` to be defined later in the module.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/resolving_annotations.md#_snippet_1

LANGUAGE: python
CODE:

```
from __future__ import annotations

from pydantic import BaseModel


class Foo(BaseModel):
    f: MyType
    # Given the future import above, this is equivalent to:
    # f: 'MyType'


type MyType = int

print(Foo.__annotations__)
#> {'f': 'MyType'}
```

---

TITLE: Pydantic Strict vs. Lax Mode Validation Example
DESCRIPTION: Demonstrates the difference in validation behavior between Pydantic's default lax mode and strict mode. It shows how a string '123' is coerced to an integer in lax mode but raises a ValidationError in strict mode.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_1

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class MyModel(BaseModel):
    x: int


print(MyModel.model_validate({'x': '123'}))  # lax mode
#> x=123

try:
    MyModel.model_validate({'x': '123'}, strict=True)  # strict mode
except ValidationError as exc:
    print(exc)
    """
    1 validation error for MyModel
    x
      Input should be a valid integer [type=int_type, input_value='123', input_type=str]
    """
```

---

TITLE: Define Generic Container with Pydantic Core Schema Python
DESCRIPTION: Defines a custom generic `Sequence` type (`MySequence`) that integrates with Pydantic validation using `__get_pydantic_core_schema__`. It shows how to handle generic arguments and delegate schema generation to Pydantic for the underlying type, demonstrating validation and instance creation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_26

LANGUAGE: python
CODE:

```
from typing import Any, Sequence, TypeVar

from pydantic_core import ValidationError, core_schema
from typing_extensions import get_args

from pydantic import BaseModel, GetCoreSchemaHandler

T = TypeVar('T')


class MySequence(Sequence[T]):
    def __init__(self, v: Sequence[T]):
        self.v = v

    def __getitem__(self, i):
        return self.v[i]

    def __len__(self):
        return len(self.v)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        instance_schema = core_schema.is_instance_schema(cls)

        args = get_args(source)
        if args:
            # replace the type and rely on Pydantic to generate the right schema
            # for `Sequence`
            sequence_t_schema = handler.generate_schema(Sequence[args[0]])
        else:
            sequence_t_schema = handler.generate_schema(Sequence)

        non_instance_schema = core_schema.no_info_after_validator_function(
            MySequence, sequence_t_schema
        )
        return core_schema.union_schema([instance_schema, non_instance_schema])


class M(BaseModel):
    model_config = dict(validate_default=True)

    s1: MySequence = [3]


m = M()
print(m)
# s1=<__main__.MySequence object at 0x0123456789ab>
print(m.s1.v)
# [3]


class M(BaseModel):
    s1: MySequence[int]


M(s1=[1])
try:
    M(s1=['a'])
except ValidationError as exc:
    print(exc)
    #
    # 2 validation errors for M
    # s1.is-instance[MySequence]
    #   Input should be an instance of MySequence [type=is_instance_of, input_value=['a'], input_type=list]
    # s1.function-after[MySequence(), json-or-python[json=list[int],python=chain[is-instance[Sequence],function-wrap[sequence_validator()]]]].0
    #   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
    #

```

---

TITLE: Validating YAML Data with Pydantic in Python
DESCRIPTION: This snippet demonstrates how to load data from a YAML file using the `PyYAML` library (`import yaml`) and validate it against a Pydantic `BaseModel`. It's commonly used for configuration files, ensuring data integrity and type correctness.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_10

LANGUAGE: yaml
CODE:

```
name: John Doe
age: 30
email: john@example.com
```

LANGUAGE: python
CODE:

```
import yaml

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


with open('person.yaml') as f:
    data = yaml.safe_load(f)

person = Person.model_validate(data)
print(person)
#> name='John Doe' age=30 email='john@example.com'
```

---

TITLE: Define Pydantic Model with `typing.Literal` for Enum-like Fields
DESCRIPTION: Demonstrates how to use `typing.Literal` in Pydantic models to restrict a field's value to a predefined set of string literals. Includes an example of successful instantiation and a `ValidationError` for an invalid input, showing how Pydantic enforces these literal constraints.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_28

LANGUAGE: python
CODE:

```
from typing import Literal

from pydantic import BaseModel, ValidationError


class Pie(BaseModel):
    flavor: Literal['apple', 'pumpkin']


Pie(flavor='apple')
Pie(flavor='pumpkin')
try:
    Pie(flavor='cherry')
except ValidationError as e:
    print(str(e))
    """
    1 validation error for Pie
    flavor
      Input should be 'apple' or 'pumpkin' [type=literal_error, input_value='cherry', input_type=str]
    """
```

---

TITLE: Pydantic Wrap Validator with Decorator Pattern
DESCRIPTION: Illustrates defining a wrap validator using the `@field_validator` decorator with `mode='wrap'`. This example also truncates strings exceeding a specified length, showcasing an alternative syntax for similar validation logic.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_6

LANGUAGE: Python
CODE:

```
from typing import Any

from typing import Annotated

from pydantic import BaseModel, Field, ValidationError, ValidatorFunctionWrapHandler, field_validator


class Model(BaseModel):
    my_string: Annotated[str, Field(max_length=5)]

    @field_validator('my_string', mode='wrap')
    @classmethod
    def truncate(cls, value: Any, handler: ValidatorFunctionWrapHandler) -> str:
        try:
            return handler(value)
        except ValidationError as err:
            if err.errors()[0]['type'] == 'string_too_long':
                return handler(value[:5])
            else:
                raise


print(Model(my_string='abcde'))
#> my_string='abcde'
print(Model(my_string='abcdef'))
#> my_string='abcde'
```

---

TITLE: Pydantic V2 Removed API Elements
DESCRIPTION: This section details the specific Pydantic classes, functions, and types that were removed in version 2. Developers migrating from Pydantic V1 to V2 should review this list to identify components that require refactoring or alternative implementations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_32

LANGUAGE: APIDOC
CODE:

```
* `pydantic.ConstrainedBytes`
* `pydantic.ConstrainedDate`
* `pydantic.ConstrainedDecimal`
* `pydantic.ConstrainedFloat`
* `pydantic.ConstrainedFrozenSet`
* `pydantic.ConstrainedInt`
* `pydantic.ConstrainedList`
* `pydantic.ConstrainedSet`
* `pydantic.ConstrainedStr`
* `pydantic.JsonWrapper`
* `pydantic.NoneBytes`
    * This was an alias to `None | bytes`.
* `pydantic.NoneStr`
    * This was an alias to `None | str`.
* `pydantic.NoneStrBytes`
    * This was an alias to `None | str | bytes`.
* `pydantic.Protocol`
* `pydantic.Required`
* `pydantic.StrBytes`
    * This was an alias to `str | bytes`.
* `pydantic.compiled`
* `pydantic.config.get_config`
* `pydantic.config.inherit_config`
* `pydantic.config.prepare_config`
* `pydantic.create_model_from_namedtuple`
* `pydantic.create_model_from_typeddict`
* `pydantic.dataclasses.create_pydantic_model_from_dataclass`
* `pydantic.dataclasses.make_dataclass_validator`
* `pydantic.dataclasses.set_validation`
* `pydantic.datetime_parse.parse_date`
* `pydantic.datetime_parse.parse_time`
* `pydantic.datetime_parse.parse_datetime`
* `pydantic.datetime_parse.parse_duration`
* `pydantic.error_wrappers.ErrorWrapper`
* `pydantic.errors.AnyStrMaxLengthError`
* `pydantic.errors.AnyStrMinLengthError`
* `pydantic.errors.ArbitraryTypeError`
* `pydantic.errors.BoolError`
* `pydantic.errors.BytesError`
* `pydantic.errors.CallableError`
* `pydantic.errors.ClassError`
* `pydantic.errors.ColorError`
* `pydantic.errors.ConfigError`
* `pydantic.errors.DataclassTypeError`
* `pydantic.errors.DateError`
* `pydantic.errors.DateNotInTheFutureError`
* `pydantic.errors.DateNotInThePastError`
* `pydantic.errors.DateTimeError`
* `pydantic.errors.DecimalError`
* `pydantic.errors.DecimalIsNotFiniteError`
* `pydantic.errors.DecimalMaxDigitsError`
* `pydantic.errors.DecimalMaxPlacesError`
* `pydantic.errors.DecimalWholeDigitsError`
* `pydantic.errors.DictError`
* `pydantic.errors.DurationError`
* `pydantic.errors.EmailError`
* `pydantic.errors.EnumError`
* `pydantic.errors.EnumMemberError`
* `pydantic.errors.ExtraError`
* `pydantic.errors.FloatError`
* `pydantic.errors.FrozenSetError`
* `pydantic.errors.FrozenSetMaxLengthError`
* `pydantic.errors.FrozenSetMinLengthError`
* `pydantic.errors.HashableError`
* `pydantic.errors.IPv4AddressError`
* `pydantic.errors.IPv4InterfaceError`
* `pydantic.errors.IPv4NetworkError`
* `pydantic.errors.IPv6AddressError`
* `pydantic.errors.IPv6InterfaceError`
* `pydantic.errors.IPv6NetworkError`
* `pydantic.errors.IPvAnyAddressError`
* `pydantic.errors.IPvAnyInterfaceError`
* `pydantic.errors.IPvAnyNetworkError`
* `pydantic.errors.IntEnumError`
* `pydantic.errors.IntegerError`
* `pydantic.errors.InvalidByteSize`
* `pydantic.errors.InvalidByteSizeUnit`
* `pydantic.errors.InvalidDiscriminator`
* `pydantic.errors.InvalidLengthForBrand`
* `pydantic.errors.JsonError`
* `pydantic.errors.JsonTypeError`
* `pydantic.errors.ListError`
* `pydantic.errors.ListMaxLengthError`
* `pydantic.errors.ListMinLengthError`
* `pydantic.errors.ListUniqueItemsError`
* `pydantic.errors.LuhnValidationError`
* `pydantic.errors.MissingDiscriminator`
* `pydantic.errors.MissingError`
* `pydantic.errors.NoneIsAllowedError`
* `pydantic.errors.NoneIsNotAllowedError`
* `pydantic.errors.NotDigitError`
* `pydantic.errors.NotNoneError`
* `pydantic.errors.NumberNotGeError`
* `pydantic.errors.NumberNotGtError`
* `pydantic.errors.NumberNotLeError`
* `pydantic.errors.NumberNotLtError`
* `pydantic.errors.NumberNotMultipleError`
* `pydantic.errors.PathError`
* `pydantic.errors.PathNotADirectoryError`
* `pydantic.errors.PathNotAFileError`
* `pydantic.errors.PathNotExistsError`
* `pydantic.errors.PatternError`
* `pydantic.errors.PyObjectError`
* `pydantic.errors.PydanticTypeError`
* `pydantic.errors.PydanticValueError`
* `pydantic.errors.SequenceError`
* `pydantic.errors.SetError`
* `pydantic.errors.SetMaxLengthError`
* `pydantic.errors.SetMinLengthError`
* `pydantic.errors.StrError`
* `pydantic.errors.StrRegexError`
* `pydantic.errors.StrictBoolError`
* `pydantic.errors.SubclassError`
* `pydantic.errors.TimeError`
* `pydantic.errors.TupleError`
* `pydantic.errors.TupleLengthError`
* `pydantic.errors.UUIDError`
* `pydantic.errors.UUIDVersionError`
* `pydantic.errors.UrlError`
* `pydantic.errors.UrlExtraError`
* `pydantic.errors.UrlHostError`
* `pydantic.errors.UrlHostTldError`
* `pydantic.errors.UrlPortError`
* `pydantic.errors.UrlSchemeError`
* `pydantic.errors.UrlSchemePermittedError`
* `pydantic.errors.UrlUserInfoError`
* `pydantic.errors.WrongConstantError`
* `pydantic.main.validate_model`
* `pydantic.networks.stricturl`
* `pydantic.parse_file_as`
* `pydantic.parse_raw_as`
* `pydantic.stricturl`
* `pydantic.tools.parse_file_as`
* `pydantic.tools.parse_raw_as`
* `pydantic.types.JsonWrapper`
* `pydantic.types.NoneBytes`
* `pydantic.types.NoneStr`
* `pydantic.types.NoneStrBytes`
* `pydantic.types.PyObject`
* `pydantic.types.StrBytes`
* `pydantic.typing.evaluate_forwardref`
```

---

TITLE: Validate and Format Product ID in Pydantic Dataclass
DESCRIPTION: Demonstrates using `@field_validator` with `mode='before'` to convert an integer `product_id` to a five-digit string with leading zeros within a Pydantic dataclass.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_9

LANGUAGE: python
CODE:

```
from pydantic import field_validator
from pydantic.dataclasses import dataclass


@dataclass
class DemoDataclass:
    product_id: str  # should be a five-digit string, may have leading zeros

    @field_validator('product_id', mode='before')
    @classmethod
    def convert_int_serial(cls, v):
        if isinstance(v, int):
            v = str(v).zfill(5)
        return v


print(DemoDataclass(product_id='01234'))
# DemoDataclass(product_id='01234')
print(DemoDataclass(product_id=2468))
# DemoDataclass(product_id='02468')
```

---

TITLE: Generate JSON Schema with computed_field in Pydantic
DESCRIPTION: Demonstrates how to define a Pydantic `BaseModel` with a `computed_field` decorated property (`volume`) and generate its JSON schema in serialization mode. The schema includes the computed field marked as read-only.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_36

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, computed_field


class Box(BaseModel):
    width: float
    height: float
    depth: float

    @computed_field
    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth


print(Box.model_json_schema(mode='serialization'))
"""
{
    'properties': {
        'width': {'title': 'Width', 'type': 'number'},
        'height': {'title': 'Height', 'type': 'number'},
        'depth': {'title': 'Depth', 'type': 'number'},
        'volume': {'readOnly': True, 'title': 'Volume', 'type': 'number'},
    },
    'required': ['width', 'height', 'depth', 'volume'],
    'title': 'Box',
    'type': 'object',
}
"""
```

---

TITLE: Instantiating a Pydantic Model (Python)
DESCRIPTION: Creates an instance of the `User` model, passing a string value for the `id` field. Pydantic will automatically coerce the string '123' to an integer during validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_1

LANGUAGE: python
CODE:

```
user = User(id='123')
```

---

TITLE: Pydantic V2 Field Definition Behavior Table
DESCRIPTION: Table detailing the behavior of field annotations in Pydantic V2 regarding required status, nullability, and default values. Covers `str`, `Optional[str]`, and `Any` types with and without default assignments.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_21

LANGUAGE: APIDOC
CODE:

```
State | Field Definition
-------------------------------------------------------|-----------------------------
Required, cannot be `None` | `f1: str`
Not required, cannot be `None`, is `'abc'` by default | `f2: str = 'abc'`
Required, can be `None` | `f3: Optional[str]`
Not required, can be `None`, is `None` by default | `f4: Optional[str] = None`
Not required, can be `None`, is `'abc'` by default | `f5: Optional[str] = 'abc'`
Required, can be any type (including `None`) | `f6: Any`
Not required, can be any type (including `None`) | `f7: Any = None`
```

---

TITLE: Pydantic AliasChoices with AliasPath for Flexible Validation
DESCRIPTION: Shows how to combine `AliasChoices` and `AliasPath` in Pydantic to create highly flexible validation rules. This allows a field to be mapped to either a direct alias or a specific element within a nested structure, accommodating diverse input data formats.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_2

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, AliasPath, AliasChoices


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasChoices('first_name', AliasPath('names', 0)))
    last_name: str = Field(validation_alias=AliasChoices('last_name', AliasPath('names', 1)))


user = User.model_validate({'first_name': 'John', 'last_name': 'Doe'})
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'names': ['John', 'Doe']})
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'names': ['John'], 'last_name': 'Doe'})
print(user)
#> first_name='John' last_name='Doe'
```

---

TITLE: Define Pydantic Models and Instantiate with Nested Dict (Strict Error Example)
DESCRIPTION: Defines two Pydantic models, `Knight` and `Quest`, where `Quest` contains a `Knight`. Shows how instantiating `Quest` by passing a dictionary for the nested `knight` field is valid for Pydantic (which coerces it) but triggers a strict type error in editors like VS Code/Pylance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Knight(BaseModel):
    title: str
    age: int
    color: str = 'blue'


class Quest(BaseModel):
    title: str
    knight: Knight


quest = Quest(
    title='To seek the Holy Grail', knight={'title': 'Sir Lancelot', 'age': 23}
)
```

---

TITLE: Validating INI Data with Pydantic in Python
DESCRIPTION: This snippet demonstrates how to read an INI configuration file using Python's `configparser` module and validate a specific section's key-value pairs against a Pydantic model. This is useful for ensuring the correctness of application configurations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_12

LANGUAGE: ini
CODE:

```
[PERSON]
name = John Doe
age = 30
email = john@example.com
```

LANGUAGE: python
CODE:

```
import configparser

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


config = configparser.ConfigParser()
config.read('person.ini')
person = Person.model_validate(config['PERSON'])
print(person)
#> name='John Doe' age=30 email='john@example.com'
```

---

TITLE: Global Pydantic Configuration via Class Inheritance
DESCRIPTION: Shows how to establish global Pydantic behavior by creating a custom parent `BaseModel` with a `model_config`. Subclasses inherit this configuration, as demonstrated with `extra='allow'` to permit additional fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_6

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class Parent(BaseModel):
    model_config = ConfigDict(extra='allow')


class Model(Parent):
    x: str


m = Model(x='foo', y='bar')
print(m.model_dump())
#> {'x': 'foo', 'y': 'bar'}
```

---

TITLE: Customize Pydantic Model Serialization with Field and Model Serializers
DESCRIPTION: Illustrates the use of `@field_serializer` to customize the serialization of a specific field and `@model_serializer` to customize the serialization of an entire model. The example shows how to serialize a datetime field to a timestamp and a timedelta to ISO 8601 format, as well as a custom model-wide serialization.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_3

LANGUAGE: python
CODE:

```
from datetime import datetime, timedelta, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer, model_serializer


class WithCustomEncoders(BaseModel):
    model_config = ConfigDict(ser_json_timedelta='iso8601')

    dt: datetime
    diff: timedelta

    @field_serializer('dt')
    def serialize_dt(self, dt: datetime, _info):
        return dt.timestamp()


m = WithCustomEncoders(
    dt=datetime(2032, 6, 1, tzinfo=timezone.utc), diff=timedelta(hours=100)
)
print(m.model_dump_json())
#> {"dt":1969660800.0,"diff":"P4DT4H"}


class Model(BaseModel):
    x: str

    @model_serializer
    def ser_model(self) -> dict[str, Any]:
        return {'x': f'serialized {self.x}'}


print(Model(x='test value').model_dump_json())
#> {"x":"serialized test value"}
```

---

TITLE: Customize Pydantic Validation with Wrap Validators
DESCRIPTION: This example illustrates the use of Pydantic V2's 'wrap validators' for advanced customization. It demonstrates how to intercept and modify validation logic for a field, specifically handling a 'now' string input and ensuring timezone-naive datetimes are treated as UTC.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_6

LANGUAGE: python
CODE:

```
from datetime import datetime, timezone
from typing import Any

from pydantic_core.core_schema import ValidatorFunctionWrapHandler

from pydantic import BaseModel, field_validator


class Meeting(BaseModel):
    when: datetime

    @field_validator('when', mode='wrap')
    def when_now(
        cls, input_value: Any, handler: ValidatorFunctionWrapHandler
    ) -> datetime:
        if input_value == 'now':
            return datetime.now()
        when = handler(input_value)
        # in this specific application we know tz naive datetimes are in UTC
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return when


print(Meeting(when='2020-01-01T12:00+01:00'))
#> when=datetime.datetime(2020, 1, 1, 12, 0, tzinfo=TzInfo(3600))
print(Meeting(when='now'))
#> when=datetime.datetime(2032, 1, 2, 3, 4, 5, 6)
print(Meeting(when='2020-01-01T12:00'))
#> when=datetime.datetime(2020, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
```

---

TITLE: Integrating Third-Party Types with Pydantic Annotated (Python)
DESCRIPTION: Shows how to create a Pydantic annotation class (`_ThirdPartyTypePydanticAnnotation`) for a hypothetical `ThirdPartyType`. It implements `__get_pydantic_core_schema__` to define parsing logic (from int or instance) and serialization logic (to int), then applies it using `Annotated` for use in a `BaseModel`. Requires `pydantic`, `pydantic_core`, and `typing`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_14

LANGUAGE: python
CODE:

```
from typing import Annotated, Any

from pydantic_core import core_schema

from pydantic import (
    BaseModel,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    ValidationError,
)
from pydantic.json_schema import JsonSchemaValue


class ThirdPartyType:
    """
    This is meant to represent a type from a third-party library that wasn't designed with Pydantic
    integration in mind, and so doesn't have a `pydantic_core.CoreSchema` or anything.
    """

    x: int

    def __init__(self):
        self.x = 0


class _ThirdPartyTypePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_int(value: int) -> ThirdPartyType:
            result = ThirdPartyType()
            result.x = value
            return result

        from_int_schema = core_schema.chain_schema(
            [
                core_schema.int_schema(),
                core_schema.no_info_plain_validator_function(validate_from_int),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_int_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ThirdPartyType),
                    from_int_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.x
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.int_schema())


# We now create an `Annotated` wrapper that we'll use as the annotation for fields on `BaseModel`s, etc.
PydanticThirdPartyType = Annotated[
    ThirdPartyType, _ThirdPartyTypePydanticAnnotation
]


# Create a model class that uses this annotation as a field
class Model(BaseModel):
    third_party_type: PydanticThirdPartyType


# Demonstrate that this field is handled correctly, that ints are parsed into `ThirdPartyType`, and that
# these instances are also "dumped" directly into ints as expected.
m_int = Model(third_party_type=1)
assert isinstance(m_int.third_party_type, ThirdPartyType)
assert m_int.third_party_type.x == 1
assert m_int.model_dump() == {'third_party_type': 1}
```

---

TITLE: Pydantic BaseModel with Union Type for ID
DESCRIPTION: This snippet demonstrates a Pydantic `BaseModel` named `User` with an `id` field defined as a `Union` of `int`, `str`, or `UUID`. It illustrates how Pydantic's smart mode handles different input types for the `id` field, successfully validating and casting them as appropriate, showcasing the flexibility of union types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_2

LANGUAGE: Python
CODE:

```
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: Union[int, str, UUID]
    name: str


user_01 = User(id=123, name='John Doe')
print(user_01)
#> id=123 name='John Doe'
print(user_01.id)
#> 123
user_02 = User(id='1234', name='John Doe')
print(user_02)
#> id='1234' name='John Doe'
print(user_02.id)
#> 1234
user_03_uuid = UUID('cf57432e-809e-4353-adbd-9d5c0d733868')
user_03 = User(id=user_03_uuid, name='John Doe')
print(user_03)
#> id=UUID('cf57432e-809e-4353-adbd-9d5c0d733868') name='John Doe'
print(user_03.id)
#> cf57432e-809e-4353-adbd-9d5c0d733868
print(user_03_uuid.int)
#> 275603287559914445491632874575877060712
```

---

TITLE: Define Positive Integer Type using Pydantic Field
DESCRIPTION: This snippet demonstrates how to create a reusable custom type for positive integers using Python's `Annotated` and Pydantic's `Field` for validation. It shows how to validate a valid input and handle a validation error for an invalid input.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_0

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import Field, TypeAdapter, ValidationError

PositiveInt = Annotated[int, Field(gt=0)]

ta = TypeAdapter(PositiveInt)

print(ta.validate_python(1))

try:
    ta.validate_python(-1)
except ValidationError as exc:
    print(exc)
```

---

TITLE: Enhancing Function Parameter Validation with Pydantic Field
DESCRIPTION: This snippet demonstrates using `pydantic.Field` within `Annotated` or as a default value to add extra validation rules (e.g., `gt=10`) or provide default values for function parameters decorated with `validate_call`. It shows how `Field` integrates with type checking and validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validation_decorator.md#_snippet_4

LANGUAGE: Python
CODE:

```
from typing import Annotated

from pydantic import Field, ValidationError, validate_call


@validate_call
def how_many(num: Annotated[int, Field(gt=10)]):
    return num


try:
    how_many(1)
except ValidationError as e:
    print(e)
    """
    1 validation error for how_many
    0
      Input should be greater than 10 [type=greater_than, input_value=1, input_type=int]
    """


@validate_call
def return_value(value: str = Field(default='default value')):
    return value


print(return_value())
#> default value
```

---

TITLE: Advanced Field Inclusion and Exclusion with model_dump
DESCRIPTION: Illustrates the flexible use of `include` and `exclude` parameters in Pydantic's `model_dump` and `model_dump_json` methods. It shows how to specify fields for export using sets and dictionaries, including nested field selection, and special handling for lists or tuples of submodels using integer keys and the `__all__` key for universal exclusion.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_19

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, SecretStr


class User(BaseModel):
    id: int
    username: str
    password: SecretStr


class Transaction(BaseModel):
    id: str
    user: User
    value: int


t = Transaction(
    id='1234567890',
    user=User(id=42, username='JohnDoe', password='hashedpassword'),
    value=9876543210,
)

# using a set:
print(t.model_dump(exclude={'user', 'value'}))
#> {'id': '1234567890'}

# using a dict:
print(t.model_dump(exclude={'user': {'username', 'password'}, 'value': True}))
#> {'id': '1234567890', 'user': {'id': 42}}

print(t.model_dump(include={'id': True, 'user': {'id'}}))
#> {'id': '1234567890', 'user': {'id': 42}}

import datetime

from pydantic import BaseModel, SecretStr


class Country(BaseModel):
    name: str
    phone_code: int


class Address(BaseModel):
    post_code: int
    country: Country


class CardDetails(BaseModel):
    number: SecretStr
    expires: datetime.date


class Hobby(BaseModel):
    name: str
    info: str


class User(BaseModel):
    first_name: str
    second_name: str
    address: Address
    card_details: CardDetails
    hobbies: list[Hobby]


user = User(
    first_name='John',
    second_name='Doe',
    address=Address(
        post_code=123456, country=Country(name='USA', phone_code=1)
    ),
    card_details=CardDetails(
        number='4212934504460000', expires=datetime.date(2020, 5, 1)
    ),
    hobbies=[
        Hobby(name='Programming', info='Writing code and stuff'),
        Hobby(name='Gaming', info='Hell Yeah!!!'),
    ],
)

exclude_keys = {
    'second_name': True,
    'address': {'post_code': True, 'country': {'phone_code'}},
    'card_details': True,
    # You can exclude fields from specific members of a tuple/list by index:
    'hobbies': {-1: {'info'}},
}

include_keys = {
    'first_name': True,
    'address': {'country': {'name'}},
    'hobbies': {0: True, -1: {'name'}},
}

# would be the same as user.model_dump(exclude=exclude_keys) in this case:
print(user.model_dump(include=include_keys))
"""
{
    'first_name': 'John',
    'address': {'country': {'name': 'USA'}},
    'hobbies': [
        {'name': 'Programming', 'info': 'Writing code and stuff'},
        {'name': 'Gaming'},
    ],
}
"""

# To exclude a field from all members of a nested list or tuple, use "__all__":
print(user.model_dump(exclude={'hobbies': {'__all__': {'info'}}}))
"""
{
    'first_name': 'John',
    'second_name': 'Doe',
    'address': {
        'post_code': 123456,
        'country': {'name': 'USA', 'phone_code': 1},
    },
    'card_details': {
        'number': SecretStr('**********'),
        'expires': datetime.date(2020, 5, 1),
    },
    'hobbies': [{'name': 'Programming'}, {'name': 'Gaming'}],
}
"""
```

---

TITLE: Validating JSON Lines Data with Pydantic in Python
DESCRIPTION: This Python snippet demonstrates how to process and validate data from a JSON Lines (`.jsonl`) file. It reads the file, splits its content into individual lines, and then iteratively validates each line as a `Person` model using `Person.model_validate_json()`, collecting all valid objects into a list.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_7

LANGUAGE: python
CODE:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


json_lines = pathlib.Path('people.jsonl').read_text().splitlines()
people = [Person.model_validate_json(line) for line in json_lines]
print(people)
#> [Person(name='John Doe', age=30, email='john@example.com'), Person(name='Jane Doe', age=25, email='jane@example.com')]
```

---

TITLE: Pydantic: Resolve 'class-not-fully-defined' using model_rebuild()
DESCRIPTION: Shows how to resolve the 'class-not-fully-defined' error for `BaseModel` subclasses by defining the referenced type and then explicitly calling `.model_rebuild()` on the model to re-evaluate its fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_2

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel


class Foo(BaseModel):
    a: Optional['Bar'] = None


class Bar(BaseModel):
    b: 'Foo'


Foo.model_rebuild()

foo = Foo(a={'b': {'a': None}})
```

---

TITLE: Rebuilding Pydantic Model Schema with Forward References - Python
DESCRIPTION: Illustrates the use of `model_rebuild()` to resolve forward references in model definitions. Shows the error encountered before rebuilding and the successful schema generation after defining the referenced class and calling the method. Requires `pydantic.BaseModel` and `pydantic.PydanticUserError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_10

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError


class Foo(BaseModel):
    x: 'Bar'  # (1)!


try:
    Foo.model_json_schema()
except PydanticUserError as e:
    print(e)
    """
    `Foo` is not fully defined; you should define `Bar`, then call `Foo.model_rebuild()`.

    For further information visit https://errors.pydantic.dev/2/u/class-not-fully-defined
    """


class Bar(BaseModel):
    pass


Foo.model_rebuild()
print(Foo.model_json_schema())
"""
{
    '$defs': {'Bar': {'properties': {}, 'title': 'Bar', 'type': 'object'}},
    'properties': {'x': {'$ref': '#/$defs/Bar'}},
    'required': ['x'],
    'title': 'Foo',
    'type': 'object',
}
"""
```

---

TITLE: Pydantic Default Error Message Examples
DESCRIPTION: Demonstrates various default error messages generated by Pydantic for different validation and usage scenarios, including missing fields, value constraints, type parsing failures, and custom value errors. This snippet shows the structure and content of typical Pydantic error dictionaries.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/errors.md#_snippet_3

LANGUAGE: python
CODE:

```
"""
            'url': 'https://errors.pydantic.dev/2/v/missing',
        },
        {
            'type': 'greater_than',
            'loc': ('gt_int',),
            'msg': 'Input should be greater than 42',
            'input': 21,
            'ctx': {'gt': 42},
            'url': 'https://errors.pydantic.dev/2/v/greater_than',
        },
        {
            'type': 'int_parsing',
            'loc': ('list_of_ints', 2),
            'msg': 'Input should be a valid integer, unable to parse string as an integer',
            'input': 'bad',
            'url': 'https://errors.pydantic.dev/2/v/int_parsing',
        },
        {
            'type': 'value_error',
            'loc': ('a_float',),
            'msg': 'Value error, Invalid float value',
            'input': 3.0,
            'ctx': {'error': ValueError('Invalid float value')},
            'url': 'https://errors.pydantic.dev/2/v/value_error',
        },
        {
            'type': 'float_parsing',
            'loc': ('recursive_model', 'lng'),
            'msg': 'Input should be a valid number, unable to parse string as a number',
            'input': 'New York',
            'url': 'https://errors.pydantic.dev/2/v/float_parsing',
        },
    ]
    """
```

---

TITLE: Validating List of JSON Objects with Pydantic TypeAdapter in Python
DESCRIPTION: This Python snippet shows how to validate a list of Pydantic models from a JSON array using `TypeAdapter`. It defines a `Person` model and then uses `TypeAdapter(list[Person])` to validate an entire JSON string containing an array of person objects, returning a list of `Person` instances.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_5

LANGUAGE: python
CODE:

```
import pathlib

from pydantic import BaseModel, EmailStr, PositiveInt, TypeAdapter


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


person_list_adapter = TypeAdapter(list[Person])  # (1)!

json_string = pathlib.Path('people.json').read_text()
people = person_list_adapter.validate_json(json_string)
print(people)
#> [Person(name='John Doe', age=30, email='john@example.com'), Person(name='Jane Doe', age=25, email='jane@example.com')]
```

---

TITLE: Pydantic Model Validation Error Handling
DESCRIPTION: This snippet illustrates how Pydantic raises a `ValidationError` when input data does not conform to the model's schema, providing a detailed list of errors. It demonstrates how to catch and inspect validation errors, showing the specific error types, locations, messages, and problematic input values for debugging.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/index.md#_snippet_2

LANGUAGE: python
CODE:

```
# continuing the above example...

from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {'id': 'not an int', 'tastes': {}}

try:
    User(**external_data)
except ValidationError as e:
    print(e.errors())
    """
    [
        {
            'type': 'int_parsing',
            'loc': ('id',),
            'msg': 'Input should be a valid integer, unable to parse string as an integer',
            'input': 'not an int',
            'url': 'https://errors.pydantic.dev/2/v/int_parsing',
        },
        {
            'type': 'missing',
            'loc': ('signup_ts',),
            'msg': 'Field required',
            'input': {'id': 'not an int', 'tastes': {}},
            'url': 'https://errors.pydantic.dev/2/v/missing',
        },
    ]
    """
```

---

TITLE: Customizing Pydantic Validation with **get_pydantic_core_schema** (Python)
DESCRIPTION: Implements the `__get_pydantic_core_schema__` class method on a custom `Username` type, which subclasses `str`. This method customizes how Pydantic validates instances of `Username` by wrapping the default string validation using `pydantic_core.core_schema.no_info_after_validator_function`. The example shows how to use `pydantic.TypeAdapter` to validate an input string and assert that the result is an instance of the custom `Username` class.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_12

LANGUAGE: Python
CODE:

```
from typing import Any

from pydantic_core import CoreSchema, core_schema

from pydantic import GetCoreSchemaHandler, TypeAdapter


class Username(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


ta = TypeAdapter(Username)
res = ta.validate_python('abc')
assert isinstance(res, Username)
assert res == 'abc'
```

---

TITLE: Using Pydantic Field for Default Values
DESCRIPTION: Demonstrates how to use 'pydantic.Field' to define default values for model fields. It highlights that type checkers like Pylance/Pyright require 'default' to be a keyword argument to correctly infer optional fields, showing an example where passing the default as a positional argument causes a type error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md#_snippet_8

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Knight(BaseModel):
    title: str = Field(default='Sir Lancelot')  # this is okay
    age: int = Field(
        23
    )  # this works fine at runtime but will case an error for pyright


lance = Knight()  # error: Argument missing for parameter "age"
```

---

TITLE: Pydantic Field Validator: Using Context with ValidationInfo.context
DESCRIPTION: Illustrates how to pass a context dictionary to Pydantic's validation methods and access it within a `field_validator` using `info.context`. This example shows filtering stopwords from a text field based on a list provided in the validation context.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_15

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationInfo, field_validator


class Model(BaseModel):
    text: str

    @field_validator('text', mode='after')
    @classmethod
    def remove_stopwords(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(info.context, dict):
            stopwords = info.context.get('stopwords', set())
            v = ' '.join(w for w in v.split() if w.lower() not in stopwords)
        return v


data = {'text': 'This is an example document'}
print(Model.model_validate(data))
print(Model.model_validate(data, context={'stopwords': ['this', 'is', 'an']}))
```

---

TITLE: Pydantic String Type Handling and Sequence Validation
DESCRIPTION: Describes how Pydantic handles `str`, `bytes`, `bytearray`, and `Enum` types for string fields, including conversion rules. It also highlights a warning about `str` and `bytes` not being treated as `Sequence[str]` or `Sequence[bytes]` to prevent common bugs, demonstrating this with a `ValidationError` example.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_27

LANGUAGE: python
CODE:

```
from typing import Optional, Sequence

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    sequence_of_strs: Optional[Sequence[str]] = None
    sequence_of_bytes: Optional[Sequence[bytes]] = None


print(Model(sequence_of_strs=['a', 'bc']).sequence_of_strs)
# ['a', 'bc']
print(Model(sequence_of_strs=('a', 'bc')).sequence_of_strs)
# ('a', 'bc')
print(Model(sequence_of_bytes=[b'a', b'bc']).sequence_of_bytes)
# [b'a', b'bc']
print(Model(sequence_of_bytes=(b'a', b'bc')).sequence_of_bytes)
# (b'a', b'bc')


try:
    Model(sequence_of_strs='abc')
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    sequence_of_strs
      'str' instances are not allowed as a Sequence value [type=sequence_str, input_value='abc', input_type=str]
    """
try:
    Model(sequence_of_bytes=b'abc')
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    sequence_of_bytes
      'bytes' instances are not allowed as a Sequence value [type=sequence_str, input_value=b'abc', input_type=bytes]
    """
```

---

TITLE: Separating Argument Validation from Function Execution with Pydantic `validate_call`
DESCRIPTION: This snippet provides a workaround for scenarios where argument validation needs to be separated from the actual function execution, which can be useful for costly or time-consuming operations. It demonstrates how `validate_call` can be applied to a wrapper function that returns the actual function, ensuring arguments are validated upfront before the inner function is called.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validation_decorator.md#_snippet_10

LANGUAGE: Python
CODE:

```
from pydantic import validate_call


@validate_call
def validate_foo(a: int, b: int):
    def foo():
        return a + b

    return foo


foo = validate_foo(a=1, b=2)
print(foo())
#> 3

```

---

TITLE: Excluding Pydantic Fields from Model Export
DESCRIPTION: Demonstrates using the `exclude=True` parameter on a `Field` to prevent it from being included in the model's exported representation, such as the output of `model_dump()`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_30

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    age: int = Field(exclude=True)


user = User(name='John', age=42)
print(user.model_dump())
```

---

TITLE: Generate JSON Schema from Pydantic TypeAdapter
DESCRIPTION: This example illustrates how to generate a JSON schema for an arbitrary type using Pydantic's `TypeAdapter` class. The `TypeAdapter.json_schema()` method provides a flexible way to obtain schema for types like lists, tuples, or unions, serving as a replacement for deprecated V1 functionality.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_2

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
print(adapter.json_schema())
#> {'items': {'type': 'integer'}, 'type': 'array'}
```

---

TITLE: Validating CSV Data with Pydantic in Python
DESCRIPTION: This snippet demonstrates how to load data from a CSV file using Python's `csv.DictReader` and then validate each row against a Pydantic `BaseModel`. It requires the `csv` module and Pydantic types like `EmailStr` and `PositiveInt` for robust validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_8

LANGUAGE: csv
CODE:

```
name,age,email
John Doe,30,john@example.com
Jane Doe,25,jane@example.com
```

LANGUAGE: python
CODE:

```
import csv

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


with open('people.csv') as f:
    reader = csv.DictReader(f)
    people = [Person.model_validate(row) for row in reader]

print(people)
#> [Person(name='John Doe', age=30, email='john@example.com'), Person(name='Jane Doe', age=25, email='jane@example.com')]
```

---

TITLE: Pydantic Model with Forward Annotations (future import)
DESCRIPTION: Demonstrates how Pydantic supports forward annotations using `from __future__ import annotations` for type hints that refer to types defined later in the code. This allows for cleaner type definitions without needing to quote type names.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/forward_annotations.md#_snippet_0

LANGUAGE: python
CODE:

```
from __future__ import annotations

from pydantic import BaseModel

MyInt = int


class Model(BaseModel):
    a: MyInt
    # Without the future import, equivalent to:
    # a: 'MyInt'


print(Model(a='1'))
#> a=1
```

---

TITLE: Enable Strict Mode with Pydantic @validate_call Decorator
DESCRIPTION: Shows how to use `ConfigDict(strict=True)` with the `@validate_call` decorator to enforce strict type checking on function arguments, preventing implicit type coercion for inputs like '1' for an integer.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_17

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict, ValidationError, validate_call


@validate_call(config=ConfigDict(strict=True))
def foo(x: int) -> int:
    return x


try:
    foo('1')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for foo
    0
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    """
```

---

TITLE: Pydantic After Validator: Doubling a Number
DESCRIPTION: Illustrates an 'After' validator in Pydantic that transforms an integer value by doubling it. This example shows how validators can modify the input value without raising exceptions. Both Annotated pattern and `field_validator` decorator implementations are provided.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_2

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel


def double_number(value: int) -> int:
    return value * 2


class Model(BaseModel):
    number: Annotated[int, AfterValidator(double_number)]


print(Model(number=2))
#> number=4
```

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, field_validator


class Model(BaseModel):
    number: int

    @field_validator('number', mode='after')
    @classmethod
    def double_number(cls, value: int) -> int:
        return value * 2


print(Model(number=2))
#> number=4
```

---

TITLE: Pydantic Standard Library Number Type Definitions
DESCRIPTION: This section outlines Pydantic's behavior for standard Python numeric types: `int`, `float`, and `enum.IntEnum`. It details the coercion mechanisms for integers and floats, and the validation rules for `IntEnum` instances and their subclasses, emphasizing how Pydantic ensures type correctness.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_5

LANGUAGE: APIDOC
CODE:

```
Number Types:
  int:
    Description: Pydantic uses `int(v)` to coerce types to an `int`. Refer to Data conversion for details on loss of information during data conversion.
  float:
    Description: Pydantic uses `float(v)` to coerce values to floats.
  enum.IntEnum:
    Validation: Pydantic checks that the value is a valid `IntEnum` instance.
    Subclass Validation: For subclasses of `enum.IntEnum`, checks that the value is a valid member of the integer enum. Refer to Enums and Choices for more details.
```

---

TITLE: Pydantic Union with Left-to-Right - Unexpected Results
DESCRIPTION: Illustrates a potential pitfall of 'left_to_right' union mode where the order of union members significantly impacts validation. If a string input can be coerced into an earlier type in the union (e.g., '456' to int), it will be validated against that type, potentially leading to unexpected type conversions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing import Union

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Union[int, str] = Field(union_mode='left_to_right')


print(User(id=123))  # (1)
#> id=123
print(User(id='456'))  # (2)
#> id=456
```

---

TITLE: Pydantic Strict Mode and JSON Parsing
DESCRIPTION: Explains Pydantic's default data coercion and the 'strict mode' for exact type matching. It demonstrates how `model_validate` handles coercion and how `model_validate_json` provides performant, sensible data conversion for JSON strings, even in strict contexts.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_4

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel, ValidationError


class Meeting(BaseModel):
    when: datetime
    where: bytes


m = Meeting.model_validate({'when': '2020-01-01T12:00', 'where': 'home'})
print(m)
#> when=datetime.datetime(2020, 1, 1, 12, 0) where=b'home'
try:
    m = Meeting.model_validate(
        {'when': '2020-01-01T12:00', 'where': 'home'}, strict=True
    )
except ValidationError as e:
    print(e)
    """
    2 validation errors for Meeting
    when
      Input should be a valid datetime [type=datetime_type, input_value='2020-01-01T12:00', input_type=str]
    where
      Input should be a valid bytes [type=bytes_type, input_value='home', input_type=str]
    """

m_json = Meeting.model_validate_json(
    '{"when": "2020-01-01T12:00", "where": "home"}'
)
print(m_json)
#> when=datetime.datetime(2020, 1, 1, 12, 0) where=b'home'
```

---

TITLE: Using BaseModel for Extra Information (Good Example) - Python
DESCRIPTION: This snippet shows the recommended way to associate additional information with a primitive type by encapsulating it within a Pydantic `BaseModel`. This approach provides clear data structure, leverages Pydantic's validation and serialization capabilities, and is more robust and performant than subclassing primitives.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_4

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class CompletedModel(BaseModel):
    s: str
    done: bool = False
```

---

TITLE: Accessing Configuration and Field Information with Pydantic V2 @field_validator
DESCRIPTION: This Python example demonstrates how to use the new `@field_validator` in Pydantic V2 to access model configuration and field metadata. It shows how `ValidationInfo` provides access to `info.config` and `info.field_name`, replacing the deprecated `config` and `field` arguments from V1's `@validator`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_15

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationInfo, field_validator


class Model(BaseModel):
    x: int

    @field_validator('x')
    def val_x(cls, v: int, info: ValidationInfo) -> int:
        assert info.config is not None
        print(info.config.get('title'))
        #> Model
        print(cls.model_fields[info.field_name].is_required())
        #> True
        return v


Model(x=1)
```

---

TITLE: Applying Decimal Constraints with Pydantic Field
DESCRIPTION: This example demonstrates using `max_digits` and `decimal_places` arguments within `pydantic.Field` to constrain `Decimal` fields in a Pydantic `BaseModel`. It shows defining a model and instantiating it with a `Decimal` value that meets the specified precision requirements.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_23

LANGUAGE: python
CODE:

```
from decimal import Decimal

from pydantic import BaseModel, Field


class Foo(BaseModel):
    precise: Decimal = Field(max_digits=5, decimal_places=2)


foo = Foo(precise=Decimal('123.45'))
print(foo)
```

---

TITLE: Pydantic Error: Removed Keyword Arguments
DESCRIPTION: This error indicates that a keyword argument previously available in Pydantic V1 is no longer supported in Pydantic V2. The example illustrates this with the 'regex' argument for 'Field', which was removed in V2.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_17

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, PydanticUserError

try:

    class Model(BaseModel):
        x: str = Field(regex='test')

except PydanticUserError as exc_info:
    assert exc_info.code == 'removed-kwargs'
```

---

TITLE: Pydantic Serialization Context with field_serializer
DESCRIPTION: This snippet shows how to pass a context object to serialization methods, which can then be accessed via `SerializationInfo` within a `field_serializer`. This allows for dynamic modification of serialization behavior, such as conditionally removing stopwords from a text field based on context-provided values.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_22

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, SerializationInfo, field_serializer


class Model(BaseModel):
    text: str

    @field_serializer('text')
    def remove_stopwords(self, v: str, info: SerializationInfo):
        context = info.context
        if context:
            stopwords = context.get('stopwords', set())
            v = ' '.join(w for w in v.split() if w.lower() not in stopwords)
        return v


model = Model.model_construct(**{'text': 'This is an example document'})
print(model.model_dump())  # no context
#> {'text': 'This is an example document'}
print(model.model_dump(context={'stopwords': ['this', 'is', 'an']}))
#> {'text': 'example document'}
print(model.model_dump(context={'stopwords': ['document']}))
#> {'text': 'This is an example'}
```

---

TITLE: Define and Validate Pydantic Models with Python Enums
DESCRIPTION: This example illustrates how to integrate Python's `Enum` and `IntEnum` classes with Pydantic models for type validation. It shows how to define enum fields, instantiate models with enum members or their raw values, and demonstrates Pydantic's validation error handling for invalid enum inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_7

LANGUAGE: python
CODE:

```
from enum import Enum, IntEnum

from pydantic import BaseModel, ValidationError


class FruitEnum(str, Enum):
    pear = 'pear'
    banana = 'banana'


class ToolEnum(IntEnum):
    spanner = 1
    wrench = 2


class CookingModel(BaseModel):
    fruit: FruitEnum = FruitEnum.pear
    tool: ToolEnum = ToolEnum.spanner


print(CookingModel())
print(CookingModel(tool=2, fruit='banana'))
try:
    CookingModel(fruit='other')
except ValidationError as e:
    print(e)
```

---

TITLE: Pydantic V2 Valid model_serializer Signatures
DESCRIPTION: This section provides examples of correct and valid signatures for `model_serializer` functions in Pydantic V2. It covers instance methods for both `plain` and `wrap` modes, demonstrating the correct usage of `self`, `info`, and `SerializerFunctionWrapHandler` parameters.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_34

LANGUAGE: python
CODE:

```
from pydantic import SerializerFunctionWrapHandler, SerializationInfo, model_serializer

# an instance method with the default mode or `mode='plain'`
@model_serializer  # or model_serializer(mode='plain')
def mod_ser(self, info: SerializationInfo): ...

# an instance method with `mode='wrap'`
@model_serializer(mode='wrap')
def mod_ser(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo):

# For all of these, you can also choose to omit the `info` argument, for example:
@model_serializer(mode='plain')
def mod_ser(self): ...

@model_serializer(mode='wrap')
def mod_ser(self, handler: SerializerFunctionWrapHandler): ...
```

---

TITLE: Pydantic Before Model Validator Example
DESCRIPTION: Illustrates a 'before' model validator in Pydantic, executed prior to model instantiation. This validator checks the raw input data for the presence of a 'card_number' field, raising a `ValueError` if found. It highlights the need to handle `Any` type input.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_11

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel, model_validator


class UserModel(BaseModel):
    username: str

    @model_validator(mode='before')
    @classmethod
    def check_card_number_not_present(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if 'card_number' in data:
                raise ValueError("'card_number' should not be included")
        return data
```

---

TITLE: Implementing Custom After Validator with Pydantic Annotated (Python)
DESCRIPTION: Defines a custom validator `MyAfterValidator` using a dataclass and the `__get_pydantic_core_schema__` method. It shows how to apply this validator to a type hint (`Username`) using `Annotated` and use it within a Pydantic `BaseModel`. Requires `pydantic`, `pydantic_core`, `dataclasses`, and `typing`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_13

LANGUAGE: python
CODE:

```
from dataclasses import dataclass
from typing import Annotated, Any, Callable

from pydantic_core import CoreSchema, core_schema

from pydantic import BaseModel, GetCoreSchemaHandler


@dataclass(frozen=True)  # (1)!
class MyAfterValidator:
    func: Callable[[Any], Any]

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            self.func, handler(source_type)
        )


Username = Annotated[str, MyAfterValidator(str.lower)]


class Model(BaseModel):
    name: Username


assert Model(name='ABC').name == 'abc'  # (2)!
```

---

TITLE: Override Pydantic model_dump return type with model_serializer
DESCRIPTION: Demonstrates how to use the `@model_serializer` decorator to change the return type of a Pydantic model's `.model_dump()` method from the default dictionary to a custom type, such as a string.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_10

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, model_serializer


class Model(BaseModel):
    x: str

    @model_serializer
    def ser_model(self) -> str:
        return self.x


print(Model(x='not a dict').model_dump())
#> not a dict
```

---

TITLE: Modify Pydantic JSON Schema using `typing.Annotated` with `Field`
DESCRIPTION: This example demonstrates how to use `typing.Annotated` in conjunction with `pydantic.fields.Field` to apply JSON schema modifications to model fields. It shows how to set `default_factory` and `max_length` for fields in a `Foo` model, and then prints the generated JSON Schema, illustrating the effect of `Annotated`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_12

LANGUAGE: python
CODE:

```
import json
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class Foo(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    name: Annotated[str, Field(max_length=256)] = Field(
        'Bar', title='CustomName'
    )


print(json.dumps(Foo.model_json_schema(), indent=2))
"""
{
  "properties": {
    "id": {
      "title": "Id",
      "type": "string"
    },
    "name": {
      "default": "Bar",
      "maxLength": 256,
      "title": "CustomName",
      "type": "string"
    }
  },
  "title": "Foo",
  "type": "object"
}
"""
```

---

TITLE: Pydantic Reusable Validators with Annotated Pattern
DESCRIPTION: Demonstrates how the `Annotated` pattern facilitates creating reusable validators. It defines an `EvenNumber` type that ensures an integer is even, and then applies this reusable type to multiple model fields, including list items.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_7

LANGUAGE: Python
CODE:

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel


def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value


EvenNumber = Annotated[int, AfterValidator(is_even)]


class Model1(BaseModel):
    my_number: EvenNumber


class Model2(BaseModel):
    other_number: Annotated[EvenNumber, AfterValidator(lambda v: v + 2)]


class Model3(BaseModel):
    list_of_even_numbers: list[EvenNumber]  # (1)!
```

---

TITLE: Pydantic Config Alias Generator with a Callable Function
DESCRIPTION: Demonstrates how to configure a Pydantic model to use a custom callable function as an `alias_generator` via `model_config`. This function automatically generates aliases for all fields, enabling consistent naming conventions (e.g., uppercase) for input data without explicitly defining each field's alias.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class Tree(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.upper()
    )

    age: int
    height: float
    kind: str


t = Tree.model_validate({'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'})
print(t.model_dump(by_alias=True))
#> {'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'}
```

---

TITLE: Define Nested Discriminated Unions in Pydantic
DESCRIPTION: This example demonstrates creating hierarchical data models using Pydantic's nested discriminated unions. It defines `BlackCat`, `WhiteCat`, `Cat`, `Dog`, and `Pet` models, showcasing how to use `Annotated` and `Field(discriminator='...')` to validate complex structures and handle specific validation errors for missing fields or incorrect discriminator values.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_8

LANGUAGE: python
CODE:

```
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, ValidationError


class BlackCat(BaseModel):
    pet_type: Literal['cat']
    color: Literal['black']
    black_name: str


class WhiteCat(BaseModel):
    pet_type: Literal['cat']
    color: Literal['white']
    white_name: str


Cat = Annotated[Union[BlackCat, WhiteCat], Field(discriminator='color')]


class Dog(BaseModel):
    pet_type: Literal['dog']
    name: str


Pet = Annotated[Union[Cat, Dog], Field(discriminator='pet_type')]


class Model(BaseModel):
    pet: Pet
    n: int


m = Model(pet={'pet_type': 'cat', 'color': 'black', 'black_name': 'felix'}, n=1)
print(m)
# pet=BlackCat(pet_type='cat', color='black', black_name='felix') n=1
try:
    Model(pet={'pet_type': 'cat', 'color': 'red'}, n='1')
except ValidationError as e:
    print(e)
    # 1 validation error for Model
    # pet.cat
    #   Input tag 'red' found using 'color' does not match any of the expected tags: 'black', 'white' [type=union_tag_invalid, input_value={'pet_type': 'cat', 'color': 'red'}, input_type=dict]
try:
    Model(pet={'pet_type': 'cat', 'color': 'black'}, n='1')
except ValidationError as e:
    print(e)
    # 1 validation error for Model
    # pet.cat.black.black_name
    #   Field required [type=missing, input_value={'pet_type': 'cat', 'color': 'black'}, input_type=dict]
```

---

TITLE: Pydantic Error: Model Field Missing Annotation
DESCRIPTION: This error occurs when a field within a Pydantic model lacks a type annotation, which is required for Pydantic to correctly process it. The first example shows the error, while subsequent examples provide solutions like using 'ClassVar' or 'model_config['ignored_types']' to prevent the field from being treated as a model field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_15

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, PydanticUserError

try:

    class Model(BaseModel):
        a = Field('foobar')
        b = None

except PydanticUserError as exc_info:
    assert exc_info.code == 'model-field-missing-annotation'
```

LANGUAGE: python
CODE:

```
from typing import ClassVar

from pydantic import BaseModel


class Model(BaseModel):
    a: ClassVar[str]
```

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class IgnoredType:
    pass


class MyModel(BaseModel):
    model_config = ConfigDict(ignored_types=(IgnoredType,))

    _a = IgnoredType()
    _b: int = IgnoredType()
    _c: IgnoredType
    _d: IgnoredType = IgnoredType()
```

---

TITLE: Defining Pydantic Model with validation_alias - Python
DESCRIPTION: This snippet demonstrates defining a Pydantic model where a field uses `validation_alias`. This alias is used for parsing input data but the field is serialized using its original name.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_16

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class MyModel(BaseModel):
    my_field: int = Field(validation_alias='myValidationAlias')
```

---

TITLE: Conditional Pydantic V1 Import for Broad Compatibility
DESCRIPTION: Shows a robust `try-except` pattern for importing Pydantic V1 features, compatible with all versions of Pydantic V1 and V2. This allows code to adapt whether the `.v1` namespace is available or not.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_8

LANGUAGE: python
CODE:

```
try:
    from pydantic.v1.fields import ModelField
except ImportError:
    from pydantic.fields import ModelField
```

---

TITLE: Avoiding Repeated TypeAdapter Instantiation (Bad Example) - Python
DESCRIPTION: This snippet demonstrates an inefficient way to use `TypeAdapter` by instantiating it inside a function. This leads to repeated construction of validators and serializers every time the function is called, which can negatively impact performance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter

def my_func():
    adapter = TypeAdapter(list[int])
    # do something with adapter
```

---

TITLE: Pydantic Field Parameters for JSON Schema Customization
DESCRIPTION: This API documentation outlines the key parameters of the `pydantic.fields.Field` function that are used to provide extra information and validations, specifically for customizing the generated JSON Schema. These parameters allow developers to define metadata such as titles, descriptions, examples, and additional JSON Schema properties for individual fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_9

LANGUAGE: APIDOC
CODE:

```
Field Parameters:
  title: string
    The title of the field.
  description: string
    The description of the field.
  examples: list
    The examples of the field.
  json_schema_extra: dict
    Extra JSON Schema properties to be added to the field.
  field_title_generator: function
    A function that programmatically sets the field's title, based on its name and info.
```

---

TITLE: Define and Instantiate Pydantic Dataclass
DESCRIPTION: This Python snippet demonstrates how to define a Pydantic dataclass using the `@dataclass` decorator. It shows how Pydantic automatically validates and coerces input types during instantiation, converting a string ID to an integer and a string timestamp to a datetime object.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_1

LANGUAGE: python
CODE:

```
from datetime import datetime
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None


user = User(id='42', signup_ts='2032-06-21T12:00')
print(user)
"""
User(id=42, name='John Doe', signup_ts=datetime.datetime(2032, 6, 21, 12, 0))
"""
```

---

TITLE: Configure Pydantic Dataclass with ConfigDict
DESCRIPTION: Shows how to configure Pydantic dataclasses using the `config` argument in the `@dataclass` decorator. It includes an example with `str_max_length` and `validate_assignment` to demonstrate validation on assignment and the resulting `ValidationError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_2

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict, ValidationError
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(str_max_length=10, validate_assignment=True))
class User:
    name: str


user = User(name='John Doe')
try:
    user.name = 'x' * 20
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    name
      String should have at most 10 characters [type=string_too_long, input_value='xxxxxxxxxxxxxxxxxxxx', input_type=str]
    """
```

---

TITLE: Generate Pydantic Models from JSON Schema using datamodel-code-generator CLI
DESCRIPTION: This command-line utility call uses datamodel-code-generator to process a JSON Schema file ("person.json") and output a Python file ("model.py") containing the generated Pydantic models. The `--input-file-type jsonschema` flag specifies the input format.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/datamodel_code_generator.md#_snippet_1

LANGUAGE: bash
CODE:

```
datamodel-codegen  --input person.json --input-file-type jsonschema --output model.py
```

---

TITLE: Pydantic Runtime Validation Methods API
DESCRIPTION: API documentation for Pydantic methods that support runtime alias control during validation. These methods allow specifying whether to validate by alias, by attribute name, or both, using the `by_alias` and `by_name` flags.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_17

LANGUAGE: APIDOC
CODE:

```
BaseModel.model_validate(data: Any, *, by_alias: bool = True, by_name: bool = False, ...)
BaseModel.model_validate_json(json_data: Union[str, bytes], *, by_alias: bool = True, by_name: bool = False, ...)
BaseModel.model_validate_strings(data: Any, *, by_alias: bool = True, by_name: bool = False, ...)
TypeAdapter.validate_python(obj: Any, *, by_alias: bool = True, by_name: bool = False, ...)
TypeAdapter.validate_json(json_data: Union[str, bytes], *, by_alias: bool = True, by_name: bool = False, ...)
TypeAdapter.validate_strings(obj: Any, *, by_alias: bool = True, by_name: bool = False, ...)

Parameters:
  by_alias: bool (default: True) - If True, validate using field aliases.
  by_name: bool (default: False) - If True, validate using field attribute names.

Note: You cannot set both by_alias and by_name to False.
```

---

TITLE: Pydantic Nested Model Serialization with `serialize_as_any`
DESCRIPTION: This snippet shows the impact of `serialize_as_any` on nested and recursive Pydantic models. It demonstrates that the flag consistently applies to all levels of the model hierarchy, controlling whether subclass-specific fields are included in the serialized output for nested instances.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_16

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class User(BaseModel):
    name: str
    friends: list['User']


class UserLogin(User):
    password: str


class OuterModel(BaseModel):
    user: User


user = UserLogin(
    name='samuel',
    password='pydantic-pw',
    friends=[UserLogin(name='sebastian', password='fastapi-pw', friends=[])],
)

print(OuterModel(user=user).model_dump(serialize_as_any=True))
"""
{
    'user': {
        'name': 'samuel',
        'friends': [
            {'name': 'sebastian', 'friends': [], 'password': 'fastapi-pw'}
        ],
        'password': 'pydantic-pw',
    }
}
"""

print(OuterModel(user=user).model_dump(serialize_as_any=False))
"""
{'user': {'name': 'samuel', 'friends': [{'name': 'sebastian', 'friends': []}]}}
"""
```

---

TITLE: Pydantic WithJsonSchema API Reference
DESCRIPTION: API documentation for the `pydantic.json_schema.WithJsonSchema` annotation, which allows overriding the generated JSON schema for a given type. It is preferred over implementing `__get_pydantic_json_schema__` for custom types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_17

LANGUAGE: APIDOC
CODE:

```
pydantic.json_schema.WithJsonSchema
```

---

TITLE: Using Annotated with Generics in Pydantic
DESCRIPTION: This snippet demonstrates how to use `typing.Annotated` with a `typing.TypeVar` to define generic types with validation constraints in Pydantic. It shows two examples: one using `annotated_types.Len` to constrain the length of a list and another using `annotated_types.Gt` to constrain the value of elements within a list. It uses `pydantic.TypeAdapter` to apply these types and validates both successful and failing cases, printing `ValidationError` messages.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_3

LANGUAGE: python
CODE:

```
from typing import Annotated, TypeVar

from annotated_types import Gt, Len

from pydantic import TypeAdapter, ValidationError

T = TypeVar('T')


ShortList = Annotated[list[T], Len(max_length=4)]


ta = TypeAdapter(ShortList[int])

v = ta.validate_python([1, 2, 3, 4])
assert v == [1, 2, 3, 4]

try:
    ta.validate_python([1, 2, 3, 4, 5])
except ValidationError as exc:
    print(exc)
    """
    1 validation error for list[int]
      List should have at most 4 items after validation, not 5 [type=too_long, input_value=[1, 2, 3, 4, 5], input_type=list]
    """


PositiveList = list[Annotated[T, Gt(0)]]

ta = TypeAdapter(PositiveList[float])

v = ta.validate_python([1.0])
assert type(v[0]) is float


try:
    ta.validate_python([-1.0])
except ValidationError as exc:
    print(exc)
    """
    1 validation error for list[constrained-float]
    0
      Input should be greater than 0 [type=greater_than, input_value=-1.0, input_type=float]
    """

```

---

TITLE: Configure Pydantic TypeAdapter with ConfigDict
DESCRIPTION: Explains how to apply configuration to a `TypeAdapter` instance by providing a `config` argument during initialization. The example demonstrates `coerce_numbers_to_str` to convert numbers in a list to strings during validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict, TypeAdapter

ta = TypeAdapter(list[str], config=ConfigDict(coerce_numbers_to_str=True))

print(ta.validate_python([1, 2]))
#> ['1', '2']
```

---

TITLE: Customize JSON Schema $ref Paths with Pydantic
DESCRIPTION: This Python example demonstrates how to use the 'ref_template' argument with Pydantic's 'json_schema' method (via TypeAdapter) to alter the '$ref' paths in the generated JSON schema. This is useful for aligning with specific schema conventions, such as those found in OpenAPI's 'components/schemas' section.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_33

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel
from pydantic.type_adapter import TypeAdapter


class Foo(BaseModel):
    a: int


class Model(BaseModel):
    a: Foo


adapter = TypeAdapter(Model)

print(
    json.dumps(
        adapter.json_schema(ref_template='#/components/schemas/{model}'),
        indent=2,
    )
)
"""
{
  "$defs": {
    "Foo": {
      "properties": {
        "a": {
          "title": "A",
          "type": "integer"
        }
      },
      "required": [
        "a"
      ],
      "title": "Foo",
      "type": "object"
    }
  },
  "properties": {
    "a": {
      "$ref": "#/components/schemas/Foo"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
"""
```

---

TITLE: Pydantic V2 Float to Integer Type Conversion
DESCRIPTION: Explains the stricter float-to-integer conversion in Pydantic V2, where floats are only accepted for `int` fields if their decimal part is zero. Demonstrates successful conversion for `10.0` and a `ValidationError` for `10.2`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_23

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: int


print(Model(x=10.0))
#> x=10
try:
    Model(x=10.2)
except ValidationError as err:
    print(err)
    """
    1 validation error for Model
    x
      Input should be a valid integer, got a number with a fractional part [type=int_from_float, input_value=10.2, input_type=float]
    """
```

---

TITLE: Define Positive Integer Type using annotated-types Gt
DESCRIPTION: This snippet shows an alternative way to define a positive integer type using `Annotated` in conjunction with the `Gt` constraint from the `annotated-types` library, making the type definition potentially Pydantic-agnostic.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_1

LANGUAGE: python
CODE:

```
from annotated_types import Gt

PositiveInt = Annotated[int, Gt(0)]
```

---

TITLE: Pydantic AliasChoices for Multiple Field Aliases
DESCRIPTION: Illustrates the use of `AliasChoices` in Pydantic's `Field` `validation_alias` to allow a field to be validated against multiple possible input keys. This provides flexibility when deserializing data that might use different naming conventions for the same logical field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_1

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, AliasChoices


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasChoices('first_name', 'fname'))
    last_name: str = Field(validation_alias=AliasChoices('last_name', 'lname'))

user = User.model_validate({'fname': 'John', 'lname': 'Doe'}) # (1)!
print(user)
#> first_name='John' last_name='Doe'
user = User.model_validate({'first_name': 'John', 'lname': 'Doe'}) # (2)!
print(user)
#> first_name='John' last_name='Doe'
```

---

TITLE: Pydantic TypeAdapter Strict Validation for Dataclass
DESCRIPTION: Illustrates strict mode validation with `TypeAdapter` for a custom `dataclass`. When `strict=True`, Pydantic expects an exact instance of `MyDataclass`, not a dictionary that could be coerced into it.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_4

LANGUAGE: python
CODE:

```
from dataclasses import dataclass

from pydantic import TypeAdapter, ValidationError


@dataclass
class MyDataclass:
    x: int


try:
    TypeAdapter(MyDataclass).validate_python({'x': '123'}, strict=True)
except ValidationError as exc:
    print(exc)
    """
    1 validation error for MyDataclass
      Input should be an instance of MyDataclass [type=dataclass_exact_type, input_value={'x': '123'}, input_type=dict]
    """
```

---

TITLE: Defining a Pydantic Model for Mypy Testing - Python
DESCRIPTION: Defines a Pydantic BaseModel with various field types and defaults to demonstrate Mypy's type checking capabilities, both with and without the Pydantic plugin. Includes examples of instantiation that would cause validation or type errors.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md#_snippet_0

LANGUAGE: python
CODE:

```
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):
    age: int
    first_name = 'John'
    last_name: Optional[str] = None
    signup_ts: Optional[datetime] = None
    list_of_ints: list[int]


m = Model(age=42, list_of_ints=[1, '2', b'3'])
print(m.middle_name)  # not a model field!
Model()  # will raise a validation error for age and list_of_ints
```

---

TITLE: Pydantic JSON Schema Module Reference
DESCRIPTION: This API documentation references the `pydantic.json_schema` module, which is central to Pydantic's functionality for generating and customizing JSON schemas from data models. The generated schemas are compliant with modern JSON Schema and OpenAPI specifications.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
Module: pydantic.json_schema

Purpose: Enables automatic creation and customization of JSON schemas directly from Pydantic models.

Compliance:
  - JSON Schema Draft 2020-12
  - OpenAPI Specification v3.1.0
```

---

TITLE: Pydantic JSON Schema Generation Methods API Reference
DESCRIPTION: Reference for Pydantic methods used to generate JSON schemas from models and types, distinguishing them from serialization methods. These methods return a dictionary representation of the schema, which can then be converted to a JSON string.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_3

LANGUAGE: APIDOC
CODE:

```
BaseModel.model_json_schema():
  description: Returns a jsonable dict representing the JSON schema of a BaseModel.
  returns: dict (jsonable)

TypeAdapter.json_schema():
  description: Returns a jsonable dict representing the JSON schema of an adapted type.
  returns: dict (jsonable)
```

---

TITLE: Pydantic Discriminator Field Syntax Examples
DESCRIPTION: This section provides various syntax options for applying discriminators to fields in Pydantic, showcasing how to use both string-based discriminators and callable `Discriminator` instances, often in combination with `Annotated` and `Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_7

LANGUAGE: python
CODE:

```
some_field: Union[...] = Field(discriminator='my_discriminator')
some_field: Annotated[Union[...], Field(discriminator='my_discriminator')]
```

LANGUAGE: python
CODE:

```
some_field: Union[...] = Field(discriminator=Discriminator(...))
some_field: Annotated[Union[...], Discriminator(...)]
some_field: Annotated[Union[...], Field(discriminator=Discriminator(...))]
```

---

TITLE: Configure Pydantic Model with Class Arguments (frozen)
DESCRIPTION: Shows an alternative way to set model configuration, specifically 'frozen=True', by passing it as a keyword argument directly in the class definition. This method is noted to provide better support for type checkers like Pylance/Pyright.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Knight(BaseModel, frozen=True):
    title: str
    age: int
    color: str = 'blue'
```

---

TITLE: Handle Pydantic datetime_from_date_parsing Validation Error
DESCRIPTION: This error is raised when a string input value cannot be parsed into a `datetime` field, typically due to an invalid date or time format.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_19

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: datetime


try:
    # there is no 13th month
    Model(x='2023-13-01')
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'datetime_from_date_parsing'
```

---

TITLE: Pydantic After Validator: Checking for Even Numbers
DESCRIPTION: Demonstrates an 'After' validator in Pydantic that checks if an integer value is even. It raises a `ValueError` if the condition is not met and returns the value unchanged otherwise. Examples show both the Annotated pattern and the `field_validator` decorator.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ValidationError


def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value


class Model(BaseModel):
    number: Annotated[int, AfterValidator(is_even)]


try:
    Model(number=1)
except ValidationError as err:
    print(err)
    """
    1 validation error for Model
    number
      Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]
    """
```

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    number: int

    @field_validator('number', mode='after')
    @classmethod
    def is_even(cls, value: int) -> int:
        if value % 2 == 1:
            raise ValueError(f'{value} is not an even number')
        return value


try:
    Model(number=1)
except ValidationError as err:
    print(err)
    """
    1 validation error for Model
    number
      Value error, 1 is not an even number [type=value_error, input_value=1, input_type=int]
    """
```

---

TITLE: Pydantic V1 to V2 API Path Changes and Deprecations
DESCRIPTION: This snippet provides a mapping of API elements (modules, functions, and utilities) that have been deprecated or moved in Pydantic V2. Developers migrating from V1 to V2 can use this list to identify the new locations of previously used components.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_31

LANGUAGE: APIDOC
CODE:

```
Pydantic V1 Path -> Pydantic V2 Path
pydantic.tools.schema_of -> pydantic.deprecated.tools.schema_of
pydantic.tools.parse_obj_as -> pydantic.deprecated.tools.parse_obj_as
pydantic.tools.schema_json_of -> pydantic.deprecated.tools.schema_json_of
pydantic.json.pydantic_encoder -> pydantic.deprecated.json.pydantic_encoder
pydantic.validate_arguments -> pydantic.deprecated.decorator.validate_arguments
pydantic.json.custom_pydantic_encoder -> pydantic.deprecated.json.custom_pydantic_encoder
pydantic.json.ENCODERS_BY_TYPE -> pydantic.deprecated.json.ENCODERS_BY_TYPE
pydantic.json.timedelta_isoformat -> pydantic.deprecated.json.timedelta_isoformat
pydantic.decorator.validate_arguments -> pydantic.deprecated.decorator.validate_arguments
pydantic.class_validators.validator -> pydantic.deprecated.class_validators.validator
pydantic.class_validators.root_validator -> pydantic.deprecated.class_validators.root_validator
pydantic.utils.deep_update -> pydantic.v1.utils.deep_update
pydantic.utils.GetterDict -> pydantic.v1.utils.GetterDict
pydantic.utils.lenient_issubclass -> pydantic.v1.utils.lenient_issubclass
pydantic.utils.lenient_isinstance -> pydantic.v1.utils.lenient_isinstance
pydantic.utils.is_valid_field -> pydantic.v1.utils.is_valid_field
pydantic.utils.update_not_none -> pydantic.v1.utils.update_not_none
pydantic.utils.import_string -> pydantic.v1.utils.import_string
pydantic.utils.Representation -> pydantic.v1.utils.Representation
pydantic.utils.ROOT_KEY -> pydantic.v1.utils.ROOT_KEY
pydantic.utils.smart_deepcopy -> pydantic.v1.utils.smart_deepcopy
pydantic.utils.sequence_like -> pydantic.v1.utils.sequence_like
```

---

TITLE: Pydantic AliasPath for Nested Field Validation
DESCRIPTION: Demonstrates how to use `AliasPath` within Pydantic's `Field` `validation_alias` to map a model field to a specific element within a nested structure (e.g., a list item in a dictionary). This allows validating input data where field values are deeply nested.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, AliasPath


class User(BaseModel):
    first_name: str = Field(validation_alias=AliasPath('names', 0))
    last_name: str = Field(validation_alias=AliasPath('names', 1))

user = User.model_validate({'names': ['John', 'Doe']})
print(user)
#> first_name='John' last_name='Doe'
```

---

TITLE: Validate Unions Directly with Pydantic TypeAdapter
DESCRIPTION: This snippet demonstrates using Pydantic's `TypeAdapter` to validate data against a union type directly, without requiring a `BaseModel` inheritance. It shows how to validate a dictionary against the `Pet` union, illustrating `TypeAdapter`'s utility for standalone union validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_9

LANGUAGE: python
CODE:

```
type_adapter = TypeAdapter(Pet)

pet = type_adapter.validate_python(
    {'pet_type': 'cat', 'color': 'black', 'black_name': 'felix'}
)
print(repr(pet))
# BlackCat(pet_type='cat', color='black', black_name='felix')
```

---

TITLE: Applying Strict Mode to Pydantic Fields
DESCRIPTION: Illustrates the `strict` parameter on `Field`. Shows how `strict=True` prevents type coercion (`name`), while `strict=False` (the default) allows it (`age`), preventing validation errors for non-strict fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_28

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(strict=True)
    age: int = Field(strict=False)


user = User(name='John', age='42')
print(user)
```

---

TITLE: Pydantic V2 Valid field_serializer Signatures
DESCRIPTION: This section provides examples of correct and valid signatures for `field_serializer` functions in Pydantic V2. It covers instance methods and static methods/functions for both `plain` and `wrap` modes, demonstrating the correct usage of `value`, `info`, and `SerializerFunctionWrapHandler` parameters.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_32

LANGUAGE: python
CODE:

```
from pydantic import FieldSerializationInfo, SerializerFunctionWrapHandler, field_serializer

# an instance method with the default mode or `mode='plain'`
@field_serializer('x')  # or @field_serializer('x', mode='plain')
def ser_x(self, value: Any, info: FieldSerializationInfo): ...

# a static method or function with the default mode or `mode='plain'`
@field_serializer('x')  # or @field_serializer('x', mode='plain')
@staticmethod
def ser_x(value: Any, info: FieldSerializationInfo): ...

# equivalent to
def ser_x(value: Any, info: FieldSerializationInfo): ...
serializer('x')(ser_x)

# an instance method with `mode='wrap'`
@field_serializer('x', mode='wrap')
def ser_x(self, value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ...

# a static method or function with `mode='wrap'`
@field_serializer('x', mode='wrap')
@staticmethod
def ser_x(value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ...

# equivalent to
def ser_x(value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo): ...
serializer('x')(ser_x)

# For all of these, you can also choose to omit the `info` argument, for example:
@field_serializer('x')
def ser_x(self, value: Any): ...

@field_serializer('x', mode='wrap')
def ser_x(self, value: Any, handler: SerializerFunctionWrapHandler): ...
```

---

TITLE: Accessing Validated Data in default_factory in Pydantic Python
DESCRIPTION: Illustrates how a `default_factory` callable can accept a single argument, which will be a dictionary containing the already validated data for the model instance. This allows default values to depend on other fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    username: str = Field(default_factory=lambda data: data['email'])


user = User(email='user@example.com')
print(user.username)
```

---

TITLE: Pydantic Wrap Model Validator Example for Error Logging
DESCRIPTION: Shows a 'wrap' model validator in Pydantic, offering the most flexibility by allowing code execution before or after Pydantic's processing. This example wraps the validation process in a `try-except` block to log `ValidationError` instances before re-raising them.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_12

LANGUAGE: python
CODE:

```
import logging
from typing import Any

from typing_extensions import Self

from pydantic import BaseModel, ModelWrapValidatorHandler, ValidationError, model_validator


class UserModel(BaseModel):
    username: str

    @model_validator(mode='wrap')
    @classmethod
    def log_failed_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        try:
            return handler(data)
        except ValidationError:
            logging.error('Model %s failed to validate with data %s', cls, data)
            raise
```

---

TITLE: Using Parametrized Generics in Nested Models (Pydantic Python)
DESCRIPTION: Illustrates how to use a parametrized generic model (`ResponseModel[T]`) as a field type within another Pydantic model (`Order`), demonstrating how nesting works with generics.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_26

LANGUAGE: python
CODE:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    content: T


class Product(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    id: int
    product: ResponseModel[Product]


product = Product(name='Apple', price=0.5)
response = ResponseModel[Product](content=product)
order = Order(id=1, product=response)
print(repr(order))
```

---

TITLE: Pydantic V2: Demonstrating Input Type Non-Preservation for Mappings
DESCRIPTION: This snippet illustrates that Pydantic V2 no longer preserves the exact input type for generic collections like `Mapping`, instead returning a plain `dict` even when a `MyDict` subclass is provided. This is a change from V1 behavior, where efforts were made to preserve the original input type.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_17

LANGUAGE: python
CODE:

```
from typing import Mapping

from pydantic import TypeAdapter


class MyDict(dict):
    pass


ta = TypeAdapter(Mapping[str, int])
v = ta.validate_python(MyDict())
print(type(v))
#> <class 'dict'>
```

---

TITLE: Pass fields as separate string arguments to `field_validator`
DESCRIPTION: This error is raised when `field_validator` is used with non-string fields, such as a list of strings. Fields should be passed as separate string arguments, not as a single collection.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_25

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: str
        b: str

        @field_validator(['a', 'b'])
        def check_fields(cls, v):
            return v

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-invalid-fields'
```

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, field_validator


class Model(BaseModel):
    a: str
    b: str

    @field_validator('a', 'b')
    def check_fields(cls, v):
        return v
```

---

TITLE: Pydantic Model JSON Parsing with Strict Mode
DESCRIPTION: This example demonstrates Pydantic's `model_validate_json` method for parsing JSON data into a `BaseModel` with `strict` configuration enabled. It shows how Pydantic handles type conversions for JSON inputs (e.g., string to date, array to tuple) and contrasts it with `model_validate` which raises validation errors under strict mode for non-native types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md#_snippet_1

LANGUAGE: python
CODE:

```
from datetime import date

from pydantic import BaseModel, ConfigDict, ValidationError


class Event(BaseModel):
    model_config = ConfigDict(strict=True)

    when: date
    where: tuple[int, int]


json_data = '{"when": "1987-01-28", "where": [51, -1]}'
print(Event.model_validate_json(json_data))  # (1)!
#> when=datetime.date(1987, 1, 28) where=(51, -1)

try:
    Event.model_validate({'when': '1987-01-28', 'where': [51, -1]})  # (2)!
except ValidationError as e:
    print(e)
    """
    2 validation errors for Event
    when
      Input should be a valid date [type=date_type, input_value='1987-01-28', input_type=str]
    where
      Input should be a valid tuple [type=tuple_type, input_value=[51, -1], input_type=list]
    """
```

---

TITLE: Pydantic @model_serializer Decorator
DESCRIPTION: Decorator to customize the serialization of an entire Pydantic model. It allows defining a custom serialization function for the model's output.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_7

LANGUAGE: APIDOC
CODE:

```
@model_serializer(*args, **kwargs)
  args, kwargs: Additional arguments passed to the serializer function.
```

---

TITLE: Run Pydantic Migration Tool
DESCRIPTION: Demonstrates how to run the `bump-pydantic` tool on a Python package within a repository. This command initiates the automated code transformation process for Pydantic V1 to V2.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_3

LANGUAGE: bash
CODE:

```
cd /path/to/repo_folder
bump-pydantic my_package
```

---

TITLE: Demonstrating Pydantic Allowing Extra Arguments (init_forbid_extra)
DESCRIPTION: Shows Pydantic's default behavior of allowing and ignoring extra arguments during model instantiation, demonstrating why the `init_forbid_extra` setting is useful for preventing unexpected inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md#_snippet_6

LANGUAGE: python
CODE:

```
class Model(BaseModel):
    a: int = 1


Model(unrelated=2)
```

---

TITLE: Validating XML Data with Pydantic in Python
DESCRIPTION: This snippet illustrates how to parse an XML file using Python's `xml.etree.ElementTree` module, extract relevant data into a dictionary, and then validate it using a Pydantic model. This approach allows Pydantic to enforce schema and types on XML content.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/files.md#_snippet_11

LANGUAGE: xml
CODE:

```
<?xml version="1.0"?>
<person>
    <name>John Doe</name>
    <age>30</age>
    <email>john@example.com</email>
</person>
```

LANGUAGE: python
CODE:

```
import xml.etree.ElementTree as ET

from pydantic import BaseModel, EmailStr, PositiveInt


class Person(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr


tree = ET.parse('person.xml').getroot()
data = {child.tag: child.text for child in tree}
person = Person.model_validate(data)
print(person)
#> name='John Doe' age=30 email='john@example.com'
```

---

TITLE: Configuring Pydantic Mypy Plugin in pyproject.toml
DESCRIPTION: Example `pyproject.toml` configuration file showing how to enable the pydantic-mypy plugin and configure its specific settings under the `[tool.mypy]` and `[tool.pydantic-mypy]` sections.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md#_snippet_4

LANGUAGE: toml
CODE:

```
[tool.mypy]
plugins = ["pydantic.mypy"]

follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
disallow_any_generics = true
no_implicit_reexport = true
disallow_untyped_defs = true

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
```

---

TITLE: Pydantic JSON Validation API References
DESCRIPTION: References to Pydantic methods for JSON validation, including `model_validate_json` for BaseModel instances, `validate_json` for TypeAdapter, and `from_json` from pydantic_core.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
pydantic.main.BaseModel.model_validate_json
pydantic.type_adapter.TypeAdapter.validate_json
pydantic_core.from_json
```

---

TITLE: Pydantic Model with Typing Sequence of Integers
DESCRIPTION: This example shows how Pydantic handles `typing.Sequence` fields. Pydantic ensures the validated value meets `Sequence` ABC requirements, potentially changing the container type (e.g., to a `list`) during eager validation, while preserving the order and item types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_14

LANGUAGE: python
CODE:

```
from typing import Sequence

from pydantic import BaseModel


class Model(BaseModel):
    sequence_of_ints: Sequence[int] = None


print(Model(sequence_of_ints=[1, 2, 3, 4]).sequence_of_ints)
#> [1, 2, 3, 4]
print(Model(sequence_of_ints=(1, 2, 3, 4)).sequence_of_ints)
#> (1, 2, 3, 4)
```

---

TITLE: Pydantic Strict Field Validation with Annotated and TypedDict
DESCRIPTION: Demonstrates how to apply `Field(strict=True)` as an annotation within `TypedDict` using `typing.Annotated`. This allows for strict validation of fields in dictionary-like structures validated by `TypeAdapter`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_8

LANGUAGE: python
CODE:

```
from typing import Annotated

from typing_extensions import TypedDict

from pydantic import Field, TypeAdapter, ValidationError


class MyDict(TypedDict):
    x: Annotated[int, Field(strict=True)]


try:
    TypeAdapter(MyDict).validate_python({'x': '1'})
except ValidationError as exc:
    print(exc)
    """
    1 validation error for MyDict
    x
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    """
```

---

TITLE: Pydantic Validator Ordering with Annotated Pattern
DESCRIPTION: This snippet demonstrates the order in which BeforeValidator, WrapValidator, and AfterValidator are applied when using the Annotated pattern in Pydantic. Before and Wrap validators run right-to-left, followed by After validators running left-to-right.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_17

LANGUAGE: python
CODE:

```
from pydantic import AfterValidator, BaseModel, BeforeValidator, WrapValidator


class Model(BaseModel):
    name: Annotated[
        str,
        AfterValidator(runs_3rd),
        AfterValidator(runs_4th),
        BeforeValidator(runs_2nd),
        WrapValidator(runs_1st),
    ]
```

---

TITLE: Handling Third-Party Type Instances in Pydantic
DESCRIPTION: This snippet demonstrates how to pass an instance of a custom third-party type (ThirdPartyType) to a Pydantic model (Model) and validate it. It shows successful validation with an instance and demonstrates how ValidationError is raised for invalid inputs, along with the expected JSON schema generated by Pydantic.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_15

LANGUAGE: python
CODE:

```
instance = ThirdPartyType()
assert instance.x == 0
instance.x = 10

m_instance = Model(third_party_type=instance)
assert isinstance(m_instance.third_party_type, ThirdPartyType)
assert m_instance.third_party_type.x == 10
assert m_instance.model_dump() == {'third_party_type': 10}

# Demonstrate that validation errors are raised as expected for invalid inputs
try:
    Model(third_party_type='a')
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    third_party_type.is-instance[ThirdPartyType]
      Input should be an instance of ThirdPartyType [type=is_instance_of, input_value='a', input_type=str]
    third_party_type.chain[int,function-plain[validate_from_int()]]
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
    """


assert Model.model_json_schema() == {
    'properties': {
        'third_party_type': {'title': 'Third Party Type', 'type': 'integer'}
    },
    'required': ['third_party_type'],
    'title': 'Model',
    'type': 'object',
}
```

---

TITLE: Map Pydantic Pipeline API to Legacy Validators
DESCRIPTION: This Python snippet illustrates how the experimental `validate_as` method from the Pipeline API offers a more type-safe and unified approach compared to Pydantic's legacy `BeforeValidator`, `AfterValidator`, and `WrapValidator`. It provides clear examples for pre-processing (stripping whitespace), post-processing (multiplying values), and combined wrap validation, simplifying complex data transformations within type annotations.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md#_snippet_3

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic.experimental.pipeline import transform, validate_as

# BeforeValidator
Annotated[int, validate_as(str).str_strip().validate_as(...)]  # (1)!
# AfterValidator
Annotated[int, transform(lambda x: x * 2)]  # (2)!
# WrapValidator
Annotated[
    int,
    validate_as(str)
    .str_strip()
    .validate_as(...)
    .transform(lambda x: x * 2),  # (3)!
]
```

---

TITLE: Define Alias for Validation Only with Pydantic
DESCRIPTION: This snippet illustrates using `Field(validation_alias='...')` in Pydantic. The alias is used only during model validation (instance creation), while the original field name is used for serialization, even when `model_dump(by_alias=True)` is specified. It requires `pydantic.BaseModel` and `pydantic.Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_11

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(validation_alias='username')


user = User(username='johndoe')  # (1)!
print(user)
#> name='johndoe'
print(user.model_dump(by_alias=True))  # (2)!
#> {'name': 'johndoe'}
```

---

TITLE: Apply PlainSerializer for Simple Pydantic Field Serialization
DESCRIPTION: Demonstrates `PlainSerializer` for modifying the output of serialization using a simple function. It accepts optional `return_type` and `when_used` arguments. The example formats an integer with commas when serialized to JSON mode.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_4

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel
from pydantic.functional_serializers import PlainSerializer

FancyInt = Annotated[
    int, PlainSerializer(lambda x: f'{x:,}', return_type=str, when_used='json')
]


class MyModel(BaseModel):
    x: FancyInt


print(MyModel(x=1234).model_dump())
#> {'x': 1234}

print(MyModel(x=1234).model_dump(mode='json'))
#> {'x': '1,234'}
```

---

TITLE: Define and Validate Discriminated Unions in Pydantic
DESCRIPTION: This Python code demonstrates how to set up and use discriminated unions in Pydantic. It defines multiple BaseModel classes (Cat, Dog, Lizard) with a common 'pet_type' field using Literal types. A main Model then uses a Union of these classes with 'pet_type' as the discriminator. The example shows successful validation and error handling for missing fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_3

LANGUAGE: python
CODE:

```
from typing import Literal, Union

from pydantic import BaseModel, Field, ValidationError


class Cat(BaseModel):
    pet_type: Literal['cat']
    meows: int


class Dog(BaseModel):
    pet_type: Literal['dog']
    barks: float


class Lizard(BaseModel):
    pet_type: Literal['reptile', 'lizard']
    scales: bool


class Model(BaseModel):
    pet: Union[Cat, Dog, Lizard] = Field(discriminator='pet_type')
    n: int


print(Model(pet={'pet_type': 'dog', 'barks': 3.14}, n=1))
# pet=Dog(pet_type='dog', barks=3.14) n=1
try:
    Model(pet={'pet_type': 'dog'}, n=1)
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    pet.dog.barks
      Field required [type=missing, input_value={'pet_type': 'dog'}, input_type=dict]
    """
```

---

TITLE: Pydantic Custom Error Example in Field Validator
DESCRIPTION: Demonstrates how to raise a `PydanticCustomError` within a Pydantic field validator. This example validates an integer `x`, raising a custom error with a specific message and context if `x` is a multiple of 42. It also shows how to catch and print the `ValidationError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_13

LANGUAGE: python
CODE:

```
from pydantic_core import PydanticCustomError

from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    x: int

    @field_validator('x', mode='after')
    @classmethod
    def validate_x(cls, v: int) -> int:
        if v % 42 == 0:
            raise PydanticCustomError(
                'the_answer_error',
                '{number} is the answer!',
                {'number': v},
            )
        return v


try:
    Model(x=42 * 2)
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    x
      84 is the answer! [type=the_answer_error, input_value=84, input_type=int]
    """
```

---

TITLE: Pydantic V2 URL Type Behavior Change
DESCRIPTION: Pydantic V2's `Url` and `Dsn` types no longer inherit from `str`, unlike V1. This change means explicit conversion using `str(url)` is now required when interacting with APIs expecting string types. The new `Url` types, built on Rust's `Url` crate, may append slashes to validated URLs if no path is included, even if not specified in the constructor.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_27

LANGUAGE: python
CODE:

```
from pydantic import AnyUrl

assert str(AnyUrl(url='https://google.com')) == 'https://google.com/'
assert str(AnyUrl(url='https://google.com/')) == 'https://google.com/'
assert str(AnyUrl(url='https://google.com/api')) == 'https://google.com/api'
assert str(AnyUrl(url='https://google.com/api/')) == 'https://google.com/api/'
```

---

TITLE: Define Named Type Alias with 'type' Syntax (Python 3.12+)
DESCRIPTION: Demonstrates defining a named type alias `PositiveIntList` using the new `type` statement (PEP 695) available in Python 3.12 and above. Shows its usage in a Pydantic model and the resulting JSON schema with a `$defs` entry, preventing definition duplication.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_5

LANGUAGE: python
CODE:

```
from typing import Annotated

from annotated_types import Gt

from pydantic import BaseModel

type PositiveIntList = list[Annotated[int, Gt(0)]]


class Model(BaseModel):
    x: PositiveIntList
    y: PositiveIntList


print(Model.model_json_schema())
```

LANGUAGE: json
CODE:

```
{
    '$defs': {
        'PositiveIntList': {
            'items': {'exclusiveMinimum': 0, 'type': 'integer'},
            'type': 'array'
        }
    },
    'properties': {
        'x': {'$ref': '#/$defs/PositiveIntList'},
        'y': {'$ref': '#/$defs/PositiveIntList'}
    },
    'required': ['x', 'y'],
    'title': 'Model',
    'type': 'object'
}
```

---

TITLE: Pydantic V2: Custom JSON Schema with **get_pydantic_json_schema**
DESCRIPTION: Illustrates the new `__get_pydantic_json_schema__` method in Pydantic V2 for customizing JSON schema. It receives `CoreSchema` and a `handler` callable, allowing for more flexible schema manipulation and resolution.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_4

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic_core import CoreSchema

from pydantic import BaseModel, GetJsonSchemaHandler


class Model(BaseModel):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = super().__get_pydantic_json_schema__(core_schema, handler)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(examples=['example'])
        return json_schema


print(Model.model_json_schema())
"""
{'examples': ['example'], 'properties': {}, 'title': 'Model', 'type': 'object'}
"""
```

---

TITLE: Pydantic Model Validation by Alias (Runtime)
DESCRIPTION: Illustrates how to validate a Pydantic model using aliases at runtime by setting `by_alias=True` on validation methods like `model_validate()`. This is the default behavior for validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_12

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')


m = Model.model_validate(
    {'my_alias': 'foo'},  # (1)!
    by_alias=True,
    by_name=False,
)
print(repr(m))
#> Model(my_field='foo')
```

---

TITLE: Pydantic Field Exclusion Priority with model_dump
DESCRIPTION: This snippet demonstrates how `Field(exclude=True)` takes precedence over the `include` argument in `model_dump` and `model_dump_json`. It shows that a field explicitly marked for exclusion at the model definition level will always be excluded, regardless of `include` parameters during dumping.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_20

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, SecretStr


class User(BaseModel):
    id: int
    username: str
    password: SecretStr = Field(exclude=True)


class Transaction(BaseModel):
    id: str
    value: int = Field(exclude=True)


t = Transaction(
    id='1234567890',
    value=9876543210,
)

print(t.model_dump())
#> {'id': '1234567890'}
print(t.model_dump(include={'id': True, 'value': True}))
#> {'id': '1234567890'}
```

---

TITLE: Handle Pydantic `bool_type` Validation Error
DESCRIPTION: This error is raised when the input value's type is not valid for a `bool` field. This error is also raised for strict fields when the input value is not an instance of `bool`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: bool


try:
    Model(x=None)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'bool_type'
```

---

TITLE: Modify Pydantic JSON Schema with **get_pydantic_json_schema**
DESCRIPTION: This Python example demonstrates how to customize the generated JSON schema for a Pydantic model or type. By implementing `__get_pydantic_json_schema__`, you can modify the `JsonSchemaValue` returned by the default handler, for instance, by adding `examples` or changing the `title`. This only affects the JSON schema output and does not impact the core validation logic.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_24

LANGUAGE: python
CODE:

```
import json
from typing import Any

from pydantic_core import core_schema as cs

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, TypeAdapter
from pydantic.json_schema import JsonSchemaValue


class Person:
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> cs.CoreSchema:
        return cs.typed_dict_schema(
            {
                'name': cs.typed_dict_field(cs.str_schema()),
                'age': cs.typed_dict_field(cs.int_schema()),
            },
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: cs.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema['examples'] = [
            {
                'name': 'John Doe',
                'age': 25,
            }
        ]
        json_schema['title'] = 'Person'
        return json_schema


print(json.dumps(TypeAdapter(Person).json_schema(), indent=2))
"""
{
  "examples": [
    {
      "age": 25,
      "name": "John Doe"
    }
  ],
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "age": {
      "title": "Age",
      "type": "integer"
    }
  },
  "required": [
    "name",
    "age"
  ],
  "title": "Person",
  "type": "object"
}
"""
```

---

TITLE: Configure Strict Mode with Pydantic TypeAdapter
DESCRIPTION: Demonstrates how to apply strict mode to a `TypeAdapter` instance using `ConfigDict(strict=True)` to enforce strict type validation, catching invalid inputs like 'yes' for a boolean.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_16

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict, TypeAdapter, ValidationError

adapter = TypeAdapter(bool, config=ConfigDict(strict=True))

try:
    adapter.validate_python('yes')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for bool
      Input should be a valid boolean [type=bool_type, input_value='yes', input_type=str]
    """
```

---

TITLE: Defining a Pydantic Model Using Generic Types - Python
DESCRIPTION: Defines a Pydantic `BaseModel` named `Model` which includes fields that use the custom generic `Owner` class. It demonstrates how to use the generic class with specific Pydantic models (`Car` and `House`) as type arguments.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_21

LANGUAGE: Python
CODE:

```
class Model(BaseModel):
    car_owner: Owner[Car]
    home_owner: Owner[House]
```

---

TITLE: Pydantic JSON Schema Generation Methods
DESCRIPTION: Documentation for key methods used to generate JSON schemas from Pydantic models and type adapters, including parameter details and return types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_7

LANGUAGE: APIDOC
CODE:

```
BaseModel.model_json_schema(mode: JsonSchemaMode = 'validation')
  mode: JsonSchemaMode
    Description: Specifies the mode of JSON schema generation.
    Default: 'validation'
    Options: 'validation', 'serialization'
  Returns: dict (JSON Schema)

TypeAdapter.json_schema(mode: JsonSchemaMode = 'validation')
  mode: JsonSchemaMode
    Description: Specifies the mode of JSON schema generation.
    Default: 'validation'
    Options: 'validation', 'serialization'
  Returns: dict (JSON Schema)
```

---

TITLE: Pydantic WithJsonSchema Annotation Example
DESCRIPTION: Demonstrates how to use `Annotated` with `WithJsonSchema` to customize the JSON schema for a type (`MyInt`) within a Pydantic `BaseModel`. The example shows how to add `examples` and explicitly set the `type` for the generated schema, overriding the default JSON Schema generation process for the field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_18

LANGUAGE: python
CODE:

```
import json
from typing import Annotated

from pydantic import BaseModel, WithJsonSchema

MyInt = Annotated[
    int,
    WithJsonSchema({'type': 'integer', 'examples': [1, 0, -1]}),
]


class Model(BaseModel):
    a: MyInt


print(json.dumps(Model.model_json_schema(), indent=2))
```

LANGUAGE: json
CODE:

```
{
  "properties": {
    "a": {
      "examples": [
        1,
        0,
        -1
      ],
      "title": "A",
      "type": "integer"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
```

---

TITLE: Configure Pydantic Model with model_config (frozen)
DESCRIPTION: Demonstrates setting Pydantic model configuration, specifically 'frozen=True', using the 'model_config' attribute within the model class definition. This makes instances of the model immutable after creation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md#_snippet_6

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Knight(BaseModel):
    model_config = dict(frozen=True)
    title: str
    age: int
    color: str = 'blue'
```

---

TITLE: Type Coercion with `validate_call` and Date Types (Python)
DESCRIPTION: This example illustrates how `@validate_call` automatically coerces input types to match function annotations, specifically converting a string to a `datetime.date` object. It also highlights that unannotated parameters default to `Any`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validation_decorator.md#_snippet_1

LANGUAGE: python
CODE:

```
from datetime import date

from pydantic import validate_call


@validate_call
def greater_than(d1: date, d2: date, *, include_equal=False) -> date:  # (1)!
    if include_equal:
        return d1 >= d2
    else:
        return d1 > d2


d1 = '2000-01-01'  # (2)!
d2 = date(2001, 1, 1)
greater_than(d1, d2, include_equal=True)
```

---

TITLE: Pydantic Date Field Handling with `datetime.date`
DESCRIPTION: This snippet shows Pydantic's ability to parse and validate `datetime.date` fields. It specifically demonstrates the conversion of a Unix timestamp (float) into a `date` object, showcasing Pydantic's flexible input handling for date types within a `BaseModel`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_2

LANGUAGE: python
CODE:

```
from datetime import date

from pydantic import BaseModel


class Birthday(BaseModel):
    d: date = None


my_birthday = Birthday(d=1679616000.0)

print(my_birthday.model_dump())
```

---

TITLE: Pydantic Error: Config and model_config Both Defined
DESCRIPTION: This error is raised when both the legacy 'class Config' and the modern 'model_config' attribute are simultaneously defined within a Pydantic model. Pydantic V2 deprecates 'class Config' in favor of 'model_config', and using both causes a conflict.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_16

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, PydanticUserError

try:

    class Model(BaseModel):
        model_config = ConfigDict(from_attributes=True)

        a: str

        class Config:
            from_attributes = True

except PydanticUserError as exc_info:
    assert exc_info.code == 'config-both'
```

---

TITLE: Pydantic V1 vs V2: JSON Serialization of Non-String Dictionary Keys
DESCRIPTION: This Python code demonstrates the difference in JSON serialization behavior for dictionary keys that are not strings (specifically `None`) between Pydantic V1's `json()` method and Pydantic V2's `model_dump_json()` method. V1 serializes `None` to 'null', while V2 serializes it to 'None'.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_10

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel as V2BaseModel
from pydantic.v1 import BaseModel as V1BaseModel


class V1Model(V1BaseModel):
    a: dict[Optional[str], int]


class V2Model(V2BaseModel):
    a: dict[Optional[str], int]


v1_model = V1Model(a={None: 123})
v2_model = V2Model(a={None: 123})

# V1
print(v1_model.json())
#> {"a": {"null": 123}}

# V2
print(v2_model.model_dump_json())
#> {"a":{"None":123}}
```

---

TITLE: Illustrating Data Loss in Pydantic Unparametrized Bounded Generics (Python)
DESCRIPTION: This snippet demonstrates a potential pitfall when validating data against an unparametrized generic model whose type variable has a bound that is a base class of the actual data type. It shows that without explicit parametrization, validation uses the base class bound, leading to data loss from the more specific subtype.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_32

LANGUAGE: python
CODE:

```
from typing import Generic, TypeVar

from pydantic import BaseModel

ItemT = TypeVar('ItemT', bound='ItemBase')


class ItemBase(BaseModel): ...


class IntItem(ItemBase):
    value: int


class ItemHolder(BaseModel, Generic[ItemT]):
    item: ItemT


loaded_data = {'item': {'value': 1}}


print(ItemHolder(**loaded_data))  # (1)!
#> item=ItemBase()

print(ItemHolder[IntItem](**loaded_data))  # (2)!
#> item=IntItem(value=1)
```

---

TITLE: Improving Pydantic Union Error Clarity with Tags
DESCRIPTION: This example demonstrates how `Tag` can be used with `TypeAdapter` to make validation error messages for union types more informative. It compares error outputs when `Tag` is not used versus when it is, highlighting how tags provide clearer context for which union member failed validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_12

LANGUAGE: python
CODE:

```
from typing import Annotated, Union

from pydantic import AfterValidator, Tag, TypeAdapter, ValidationError

DoubledList = Annotated[list[int], AfterValidator(lambda x: x * 2)]
StringsMap = dict[str, str]


# Not using any `Tag`s for each union case, the errors are not so nice to look at
adapter = TypeAdapter(Union[DoubledList, StringsMap])

try:
    adapter.validate_python(['a'])
except ValidationError as exc_info:
    print(exc_info)

tag_adapter = TypeAdapter(
    Union[
        Annotated[DoubledList, Tag('DoubledList')],
        Annotated[StringsMap, Tag('StringsMap')],
    ]
)

try:
    tag_adapter.validate_python(['a'])
except ValidationError as exc_info:
    print(exc_info)
```

---

TITLE: Pydantic Field Validator for Type Coercion
DESCRIPTION: This snippet shows how a field_validator with mode='before' can be used to coerce input types, specifically converting integers to strings for a field annotated as str. It highlights that the actual accepted input type can differ from the field's type hint.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_21

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel, field_validator


class Model(BaseModel):
    value: str

    @field_validator('value', mode='before')
    @classmethod
    def cast_ints(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value


print(Model(value='a'))
# > value='a'
print(Model(value=1))
# > value='1'
```

---

TITLE: Benchmarking TypedDict vs Nested BaseModel - Python
DESCRIPTION: This snippet provides a performance benchmark comparing `TypedDict` with nested Pydantic `BaseModel` for data validation. It uses `timeit` to demonstrate that `TypedDict` can be significantly faster (approximately 2.5x) for simple nested data structures, suggesting its use for performance-critical scenarios where full `BaseModel` features are not required.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_6

LANGUAGE: python
CODE:

```
from timeit import timeit

from typing_extensions import TypedDict

from pydantic import BaseModel, TypeAdapter


class A(TypedDict):
    a: str
    b: int


class TypedModel(TypedDict):
    a: A


class B(BaseModel):
    a: str
    b: int


class Model(BaseModel):
    b: B


ta = TypeAdapter(TypedModel)
result1 = timeit(
    lambda: ta.validate_python({'a': {'a': 'a', 'b': 2}}), number=10000
)
result2 = timeit(
    lambda: Model.model_validate({'b': {'a': 'a', 'b': 2}}), number=10000
)
print(result2 / result1)
```

---

TITLE: Pydantic Field Validator with JSON Schema Input Type
DESCRIPTION: This example demonstrates using json_schema_input_type with a field_validator to accurately represent the accepted input types in the generated JSON Schema. This ensures that the schema correctly reflects that both integers and strings are valid inputs for the value field, even though its type hint is str.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_22

LANGUAGE: python
CODE:

```
from typing import Any, Union

from pydantic import BaseModel, field_validator


class Model(BaseModel):
    value: str

    @field_validator(
        'value', mode='before', json_schema_input_type=Union[int, str]
    )
    @classmethod
    def cast_ints(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value


print(Model.model_json_schema()['properties']['value'])
# > {'anyOf': [{'type': 'integer'}, {'type': 'string'}], 'title': 'Value'}
```

---

TITLE: Configure Pydantic Model with Class Arguments
DESCRIPTION: Illustrates how to apply configuration to a Pydantic `BaseModel` directly via class arguments, such as `frozen=True`. This method allows static type checkers to recognize the configuration, flagging instance mutations as type checking errors.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_1

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Model(BaseModel, frozen=True):
    a: str  # (1)!
```

---

TITLE: Validating Default Values in Pydantic Python
DESCRIPTION: Demonstrates how to enable validation for default values using the `validate_default=True` argument in `pydantic.Field`. By default, Pydantic does not validate default values, but this setting forces validation, potentially raising a `ValidationError` if the default is invalid.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_8

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    age: int = Field(default='twelve', validate_default=True)


try:
    user = User()
except ValidationError as e:
    print(e)
```

---

TITLE: Generating Model Signature with inspect.signature (Python)
DESCRIPTION: Shows how Pydantic automatically generates a function signature for a BaseModel based on its fields, useful for introspection and integration with libraries like FastAPI or hypothesis.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_50

LANGUAGE: python
CODE:

```
import inspect

from pydantic import BaseModel, Field


class FooModel(BaseModel):
    id: int
    name: str = None
    description: str = 'Foo'
    apple: int = Field(alias='pear')


print(inspect.signature(FooModel))
```

---

TITLE: Pydantic Self-Referencing (Recursive) Model Definition
DESCRIPTION: Illustrates how to define Pydantic models with self-referencing fields, allowing a model to contain instances of itself. The example shows how to use string-wrapped type hints for recursive definitions and demonstrates model instantiation with and without a sibling.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/forward_annotations.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel


class Foo(BaseModel):
    a: int = 123
    sibling: 'Optional[Foo]' = None


print(Foo())
#> a=123 sibling=None
print(Foo(sibling={'a': '321'}))
#> a=123 sibling=Foo(a=321, sibling=None)
```

---

TITLE: Pydantic: Correct Usage of `validate_call` with Class/Static Methods and Properties
DESCRIPTION: This snippet demonstrates the correct order of decorators when using `validate_call` with `@classmethod`, `@staticmethod`, or `@property`. It shows an incorrect example where `validate_call` is applied before the method type decorator, leading to an error, and then the correct approach where `validate_call` is placed after.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_45

LANGUAGE: python
CODE:

```
from pydantic import PydanticUserError, validate_call

# Incorrect usage: @validate_call before @classmethod
try:

    class A:
        @validate_call
        @classmethod
        def f1(cls): ...

except PydanticUserError as exc_info:
    assert exc_info.code == 'validate-call-type'


# Correct usage: @classmethod before @validate_call
@classmethod
@validate_call
def f2(cls): ...
```

---

TITLE: Pydantic Model Validation by Alias or Attribute Name (Runtime)
DESCRIPTION: Demonstrates how to allow validation by both alias and attribute name simultaneously at runtime by setting both `by_alias=True` and `by_name=True` on validation methods. This provides flexibility, accepting input matching either the alias or the attribute name.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_14

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')


m = Model.model_validate(
    {'my_alias': 'foo'}, by_alias=True, by_name=True  # (1)!
)
print(repr(m))
#> Model(my_field='foo')

m = Model.model_validate(
    {'my_field': 'foo'}, by_alias=True, by_name=True  # (2)!
)
print(repr(m))
#> Model(my_field='foo')
```

---

TITLE: Pydantic Plain Validator: Terminate Validation and Bypass Type Checking
DESCRIPTION: The `PlainValidator` allows immediate termination of the validation process, preventing any further validators from being called and bypassing Pydantic's internal type validation. This example demonstrates how a `PlainValidator` can modify an integer value or accept an invalid type without raising a `ValidationError`, as Pydantic's default validation is skipped. Both the `Annotated` pattern and the `@field_validator` decorator are shown.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_4

LANGUAGE: python
CODE:

```
from typing import Annotated, Any

from pydantic import BaseModel, PlainValidator


def val_number(value: Any) -> Any:
    if isinstance(value, int):
        return value * 2
    else:
        return value


class Model(BaseModel):
    number: Annotated[int, PlainValidator(val_number)]


print(Model(number=4))
print(Model(number='invalid'))
```

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel, field_validator


class Model(BaseModel):
    number: int

    @field_validator('number', mode='plain')
    @classmethod
    def val_number(cls, value: Any) -> Any:
        if isinstance(value, int):
            return value * 2
        else:
            return value


print(Model(number=4))
print(Model(number='invalid'))
```

---

TITLE: Pydantic JSON Serialization API Methods
DESCRIPTION: Lists key API methods available in Pydantic for serializing data to JSON format, providing options for different use cases like BaseModel instances or TypeAdapter usage.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md#_snippet_6

LANGUAGE: APIDOC
CODE:

```
pydantic.main.BaseModel.model_dump_json
pydantic.type_adapter.TypeAdapter.dump_json
pydantic_core.to_json
```

---

TITLE: Pydantic V2 TypeError Handling in Validators
DESCRIPTION: This Python snippet illustrates the change in Pydantic V2 where `TypeError` exceptions raised within validator functions are no longer converted to `ValidationError`. It demonstrates that a `TypeError` will propagate directly, preventing unintended user-facing validation errors from internal type mismatches.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_16

LANGUAGE: python
CODE:

```
import pytest

from pydantic import BaseModel, field_validator


class Model(BaseModel):
    x: int

    @field_validator('x')
    def val_x(cls, v: int) -> int:
        return str.lower(v)  # raises a TypeError


with pytest.raises(TypeError):
    Model(x=1)
```

---

TITLE: Pydantic Error: BaseModel Instantiated Directly
DESCRIPTION: This error occurs when 'BaseModel' is instantiated directly instead of being inherited by a custom model. Pydantic models should always inherit from 'BaseModel' to define their structure and behavior.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_20

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError

try:
    BaseModel()
except PydanticUserError as exc_info:
    assert exc_info.code == 'base-model-instantiated'
```

---

TITLE: JSON Schema for Numeric Constraints
DESCRIPTION: This JSON snippet shows the schema generated by Pydantic for the `Foo` model defined with numeric constraints. It illustrates how Pydantic translates `gt`, `lt`, `ge`, `le`, and `multiple_of` into standard JSON Schema keywords like `exclusiveMinimum`, `exclusiveMaximum`, `minimum`, `maximum`, and `multipleOf`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_19

LANGUAGE: json
CODE:

```
{
  "title": "Foo",
  "type": "object",
  "properties": {
    "positive": {
      "title": "Positive",
      "type": "integer",
      "exclusiveMinimum": 0
    },
    "non_negative": {
      "title": "Non Negative",
      "type": "integer",
      "minimum": 0
    },
    "negative": {
      "title": "Negative",
      "type": "integer",
      "exclusiveMaximum": 0
    },
    "non_positive": {
      "title": "Non Positive",
      "type": "integer",
      "maximum": 0
    },
    "even": {
      "title": "Even",
      "type": "integer",
      "multipleOf": 2
    },
    "love_for_pydantic": {
      "title": "Love For Pydantic",
      "type": "number"
    }
  },
  "required": [
    "positive",
    "non_negative",
    "negative",
    "non_positive",
    "even",
    "love_for_pydantic"
  ]
}
```

---

TITLE: JSON Schema for Pydantic String Constraints
DESCRIPTION: This JSON snippet shows the schema generated by Pydantic for the `Foo` model defined with string constraints (`min_length`, `max_length`, `pattern`). It illustrates how Pydantic translates these constraints into standard JSON Schema properties.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_22

LANGUAGE: json
CODE:

```
{
  "title": "Foo",
  "type": "object",
  "properties": {
    "short": {
      "title": "Short",
      "type": "string",
      "minLength": 3
    },
    "long": {
      "title": "Long",
      "type": "string",
      "maxLength": 10
    },
    "regex": {
      "title": "Regex",
      "type": "string",
      "pattern": "^\\d*$"
    }
  },
  "required": [
    "short",
    "long",
    "regex"
  ]
}
```

---

TITLE: Pydantic Multi-Field Validators with Decorator Pattern
DESCRIPTION: Shows how to use the `@field_validator` decorator to apply a single validator function to multiple fields (`f1`, `f2`) in a Pydantic model. It capitalizes the string values of the specified fields before validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_8

LANGUAGE: Python
CODE:

```
from pydantic import BaseModel, field_validator


class Model(BaseModel):
    f1: str
    f2: str

    @field_validator('f1', 'f2', mode='before')
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()
```

---

TITLE: Pydantic Validation with `TypedDict` for Structured Dictionaries
DESCRIPTION: Explains how Pydantic validates `TypedDict` instances, ensuring all required keys are present and their values conform to the specified types. It demonstrates successful validation and a `ValidationError` for a missing required field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_18

LANGUAGE: python
CODE:

```
from typing_extensions import TypedDict

from pydantic import TypeAdapter, ValidationError


class User(TypedDict):
    name: str
    id: int


ta = TypeAdapter(User)

print(ta.validate_python({'name': 'foo', 'id': 1}))
#> {'name': 'foo', 'id': 1}

try:
    ta.validate_python({'name': 'foo'})
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    id
      Field required [type=missing, input_value={'name': 'foo'}, input_type=dict]
    """
```

---

TITLE: Type Checking with Pydantic Annotated Alias
DESCRIPTION: This snippet shows how to use `typing.Annotated` with `Field(alias='...')` and `ConfigDict(validate_by_name=True, validate_by_alias=True)` to make static type checkers accept instance creation using the original field name, while Pydantic runtime accepts both. Type checkers will _not_ accept the alias in this configuration. It requires `typing.Annotated`, `pydantic.BaseModel`, `pydantic.ConfigDict`, and `pydantic.Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_15

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    name: Annotated[str, Field(alias='username')]


user = User(name='johndoe')  # (1)!
user = User(username='johndoe')  # (2)!
```

---

TITLE: Demonstrating Pydantic Data Conversion (init_typed)
DESCRIPTION: Illustrates Pydantic's default data conversion behavior where a string can be assigned to an integer field at runtime, highlighting the need for the `init_typed` setting for stricter type checking.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md#_snippet_5

LANGUAGE: python
CODE:

```
class Model(BaseModel):
    a: int


Model(a='1')
```

---

TITLE: Rebuilding Pydantic Model to Resolve Forward Reference
DESCRIPTION: This Python snippet shows how to resolve a previously undefined forward reference ('MyType') in a Pydantic model. By defining 'MyType' and then calling `Foo.model_rebuild()`, the model's core schema is successfully regenerated, as evidenced by the updated `__pydantic_core_schema__`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/resolving_annotations.md#_snippet_8

LANGUAGE: python
CODE:

```
type MyType = int

Foo.model_rebuild()
Foo.__pydantic_core_schema__
#> {'type': 'model', 'schema': {...}, ...}
```

---

TITLE: Handling Custom Types in Pydantic Dataclasses with `arbitrary_types_allowed`
DESCRIPTION: This example explains how Pydantic handles custom types within standard library dataclasses when they are used in a `BaseModel`. It demonstrates the `PydanticSchemaGenerationError` that occurs without proper configuration and shows how to resolve it by setting `arbitrary_types_allowed=True` in the `model_config`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_7

LANGUAGE: python
CODE:

```
import dataclasses

from pydantic import BaseModel, ConfigDict
from pydantic.errors import PydanticSchemaGenerationError


class ArbitraryType:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'ArbitraryType(value={self.value!r})'


@dataclasses.dataclass
class DC:
    a: ArbitraryType
    b: str


# valid as it is a stdlib dataclass without validation:
my_dc = DC(a=ArbitraryType(value=3), b='qwe')

try:

    class Model(BaseModel):
        dc: DC
        other: str

    # invalid as dc is now validated with pydantic, and ArbitraryType is not a known type
    Model(dc=my_dc, other='other')

except PydanticSchemaGenerationError as e:
    print(e.message)
    """
    Unable to generate pydantic-core schema for <class '__main__.ArbitraryType'>. Set `arbitrary_types_allowed=True` in the model_config to ignore this error or implement `__get_pydantic_core_schema__` on your type to fully support it.

    If you got this error by calling handler(<some type>) within `__get_pydantic_core_schema__` then you likely need to call `handler.generate_schema(<some type>)` since we do not call `__get_pydantic_core_schema__` on `<some type>` otherwise to avoid infinite recursion.
    """


# valid as we set arbitrary_types_allowed=True, and that config pushes down to the nested vanilla dataclass
class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    dc: DC
    other: str


m = Model(dc=my_dc, other='other')
print(repr(m))
#|> Model(dc=DC(a=ArbitraryType(value=3), b='qwe'), other='other')
```

---

TITLE: Using Standard Library Dataclasses as Fields in Pydantic BaseModel
DESCRIPTION: This snippet demonstrates how standard library dataclasses are validated when used as fields within a Pydantic `BaseModel`. It highlights the importance of `model_config = ConfigDict(revalidate_instances='always')` for revalidation and shows how Pydantic applies validation to nested dataclass fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_6

LANGUAGE: python
CODE:

```
import dataclasses
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError


@dataclasses.dataclass(frozen=True)
class User:
    name: str


class Foo(BaseModel):
    # Required so that pydantic revalidates the model attributes:
    model_config = ConfigDict(revalidate_instances='always')

    user: Optional[User] = None


# nothing is validated as expected:
user = User(name=['not', 'a', 'string'])
print(user)
#|> User(name=['not', 'a', 'string'])


try:
    Foo(user=user)
except ValidationError as e:
    print(e)
    """
    1 validation error for Foo
    user.name
      Input should be a valid string [type=string_type, input_value=['not', 'a', 'string'], input_type=list]
    """

foo = Foo(user=User(name='pika'))
try:
    foo.user.name = 'bulbi'
except dataclasses.FrozenInstanceError as e:
    print(e)
    #|> cannot assign to field 'name'
```

---

TITLE: Pydantic JSON Schema Customization Options
DESCRIPTION: Overview of methods and annotations available for customizing JSON schema generation at both field and model levels in Pydantic, including options for custom types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_8

LANGUAGE: APIDOC
CODE:

```
JSON Schema Customization:
  Field-level customization:
    - Field constructor (pydantic.fields.Field)
  Model-level customization:
    - model_config (pydantic.config.ConfigDict)
  Common option:
    - json_schema_extra: Add extra information to the JSON schema.
  Custom types specific tools:
    - WithJsonSchema annotation
    - SkipJsonSchema annotation
    - Implementing __get_pydantic_core_schema__
    - Implementing __get_pydantic_json_schema__
```

---

TITLE: Using Pydantic Field and Stdlib Dataclass Field in Pydantic Dataclasses
DESCRIPTION: This example illustrates how to combine Pydantic's `Field` function with the standard library's `dataclasses.field` within a Pydantic dataclass. It demonstrates setting default values, metadata, and validation constraints like `ge` (greater than or equal) and `le` (less than or equal) for fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_2

LANGUAGE: python
CODE:

```
import dataclasses
from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str = 'John Doe'
    friends: list[int] = dataclasses.field(default_factory=lambda: [0])
    age: Optional[int] = dataclasses.field(
        default=None,
        metadata={'title': 'The age of the user', 'description': 'do not lie!'},
    )
    height: Optional[int] = Field(
        default=None, title='The height in cm', ge=50, le=300
    )


user = User(id='42', height='250')
print(user)
#> User(id=42, name='John Doe', friends=[0], age=None, height=250)
```

---

TITLE: Access Field Name in Pydantic Annotated Validator Python
DESCRIPTION: Demonstrates accessing the field name (`info.field_name`) within a validator function applied via `Annotated` and `AfterValidator`. This provides context about the field being validated directly to the validator function, enabling field-specific logic or data storage.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_28

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ValidationInfo


def my_validators(value: int, info: ValidationInfo):
    return f'<{value} {info.field_name!r}>'


class MyModel(BaseModel):
    my_field: Annotated[int, AfterValidator(my_validators)]


m = MyModel(my_field=1)
print(m.my_field)
# <1 'my_field'>

```

---

TITLE: Creating Pydantic Models Dynamically with create_model
DESCRIPTION: Shows how to use the pydantic.create_model function to dynamically create a Pydantic model at runtime with specified fields and types, including a field with a default value.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_37

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, create_model

DynamicFoobarModel = create_model('DynamicFoobarModel', foo=str, bar=(int, 123))
```

---

TITLE: Validate Pydantic List Types with Optional Generics
DESCRIPTION: This snippet demonstrates how Pydantic handles `list` types, including optional lists and lists with generic type parameters. It shows how Pydantic automatically casts input values to the specified list item type during validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_8

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):
    simple_list: Optional[list] = None
    list_of_ints: Optional[list[int]] = None


print(Model(simple_list=['1', '2', '3']).simple_list)
print(Model(list_of_ints=['1', '2', '3']).list_of_ints)
```

---

TITLE: Understand Non-Recursive Strict Mode in Pydantic Nested Models
DESCRIPTION: Explains that `ConfigDict(strict=True)` on an outer Pydantic `BaseModel` does not recursively apply strict validation to nested models. This means nested model fields will still allow type coercion unless explicitly configured for strictness.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_13

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, ValidationError


class Inner(BaseModel):
    y: int


class Outer(BaseModel):
    model_config = ConfigDict(strict=True)

    x: int
    inner: Inner


print(Outer(x=1, inner=Inner(y='2')))
# x=1 inner=Inner(y=2)

try:
    Outer(x='1', inner=Inner(y='2'))
except ValidationError as exc:
    print(exc)
    """
    1 validation error for Outer
    x
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    """
```

---

TITLE: Pydantic PlainSerializer Class
DESCRIPTION: A functional serializer that uses a simple function to modify the output of serialization. It provides direct control over the serialized value.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_8

LANGUAGE: APIDOC
CODE:

```
PlainSerializer(func: Callable, return_type: Any = None, when_used: Literal['always', 'unless-none', 'json', 'json-unless-none'] = 'always')
  func: The serialization function to apply.
  return_type: Specifies the return type for the function. If omitted, it's inferred from the type annotation.
  when_used: Specifies when this serializer should be used. Accepts 'always', 'unless-none', 'json', and 'json-unless-none'. Defaults to 'always'.
```

---

TITLE: Pydantic Configuration Boundary Example
DESCRIPTION: Demonstrates that `ConfigDict` settings applied to a parent Pydantic model (e.g., `Parent`) do not propagate to nested models (e.g., `User`) used as field annotations. The `str_max_length` on `Parent` does not affect the `name` field in `User`, showing independent configuration boundaries.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_8

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    name: str


class Parent(BaseModel):
    user: User

    model_config = ConfigDict(str_max_length=2)


print(Parent(user={'name': 'John Doe'}))
#> user=User(name='John Doe')
```

---

TITLE: Defining Private Attributes in Pydantic Models (Python)
DESCRIPTION: Explains how to define attributes that are not treated as model fields using a leading underscore or `PrivateAttr`. Shows how `PrivateAttr` can be initialized with `default_factory` or in `model_post_init`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_49

LANGUAGE: python
CODE:

```
from datetime import datetime
from random import randint
from typing import Any

from pydantic import BaseModel, PrivateAttr


class TimeAwareModel(BaseModel):
    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)
    _secret_value: str

    def model_post_init(self, context: Any) -> None:
        # this could also be done with `default_factory`:
        self._secret_value = randint(1, 5)


m = TimeAwareModel()
print(m._processed_at)
#> 2032-01-02 03:04:05.000006
print(m._secret_value)
#> 3
```

---

TITLE: Pydantic Model Discrimination with `typing.Literal` and `Union`
DESCRIPTION: Illustrates how `typing.Literal` can be used with `typing.Union` to create discriminated unions in Pydantic, allowing the model to correctly parse different object types based on a literal field value. Shows successful parsing of `Cake` and `IceCream` types and a `ValidationError` for an unmatched type.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_29

LANGUAGE: python
CODE:

```
from typing import ClassVar, Literal, Union

from pydantic import BaseModel, ValidationError


class Cake(BaseModel):
    kind: Literal['cake']
    required_utensils: ClassVar[list[str]] = ['fork', 'knife']


class IceCream(BaseModel):
    kind: Literal['icecream']
    required_utensils: ClassVar[list[str]] = ['spoon']


class Meal(BaseModel):
    dessert: Union[Cake, IceCream]


print(type(Meal(dessert={'kind': 'cake'}).dessert).__name__)
#> Cake
print(type(Meal(dessert={'kind': 'icecream'}).dessert).__name__)
#> IceCream
try:
    Meal(dessert={'kind': 'pie'})
except ValidationError as e:
    print(str(e))
    """
    2 validation errors for Meal
    dessert.Cake.kind
      Input should be 'cake' [type=literal_error, input_value='pie', input_type=str]
    dessert.IceCream.kind
      Input should be 'icecream' [type=literal_error, input_value='pie', input_type=str]
    """
```

---

TITLE: Handle Pydantic union_tag_invalid Error
DESCRIPTION: This error is raised when the discriminator value provided in the input for a Pydantic Union field does not match any of the expected values defined by the union's constituent types. The example demonstrates how to define a discriminated union using `Field(discriminator='pet_type')` and triggers this error by supplying an unrecognized `pet_type`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_89

LANGUAGE: python
CODE:

```
from typing import Literal, Union

from pydantic import BaseModel, Field, ValidationError


class BlackCat(BaseModel):
    pet_type: Literal['blackcat']


class WhiteCat(BaseModel):
    pet_type: Literal['whitecat']


class Model(BaseModel):
    cat: Union[BlackCat, WhiteCat] = Field(discriminator='pet_type')


try:
    Model(cat={'pet_type': 'dog'})
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'union_tag_invalid'
```

---

TITLE: Pydantic Field Validator API References
DESCRIPTION: References to key Pydantic functional validators and the `field_validator` decorator, providing an overview of available tools for custom field validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
pydantic.functional_validators.WrapValidator
pydantic.functional_validators.PlainValidator
pydantic.functional_validators.BeforeValidator
pydantic.functional_validators.AfterValidator
pydantic.functional_validators.field_validator
```

---

TITLE: Pydantic Model Validator API Reference
DESCRIPTION: Reference for the `pydantic.functional_validators.model_validator` decorator, used for performing validation on the entire model's data.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_9

LANGUAGE: APIDOC
CODE:

```
`pydantic.functional_validators.model_validator`
```

---

TITLE: Applying Pydantic Dataclass Decorator to Stdlib Dataclasses
DESCRIPTION: This example illustrates how to directly apply the `pydantic.dataclasses.dataclass` decorator to an existing standard library dataclass. This creates a new subclass that benefits from Pydantic's validation capabilities.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_5

LANGUAGE: python
CODE:

```
import dataclasses

import pydantic


@dataclasses.dataclass
class A:
    a: int


PydanticA = pydantic.dataclasses.dataclass(A)
print(PydanticA(a='1'))
#|> A(a=1)
```

---

TITLE: Pydantic Strict Validation for JSON Data with TypeAdapter and BaseModel
DESCRIPTION: Shows how `strict=True` affects `validate_json` for `TypeAdapter` and `model_validate_json` for `BaseModel`. It highlights that string representations of numbers are not valid integers in strict mode when parsed from JSON, but UUID strings are valid for `UUID` types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_5

LANGUAGE: python
CODE:

```
import json
from uuid import UUID

from pydantic import BaseModel, TypeAdapter, ValidationError

try:
    TypeAdapter(list[int]).validate_json('["1", 2, "3"]', strict=True)
except ValidationError as exc:
    print(exc)
    """
    2 validation errors for list[int]
    0
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    2
      Input should be a valid integer [type=int_type, input_value='3', input_type=str]
    """


class Model(BaseModel):
    x: int
    y: UUID


data = {'x': '1', 'y': '12345678-1234-1234-1234-123456789012'}
try:
    Model.model_validate(data, strict=True)
except ValidationError as exc:
    # Neither x nor y are valid in strict mode from python:
    print(exc)
    """
    2 validation errors for Model
    x
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    y
      Input should be an instance of UUID [type=is_instance_of, input_value='12345678-1234-1234-1234-123456789012', input_type=str]
    """

json_data = json.dumps(data)
try:
    Model.model_validate_json(json_data, strict=True)
except ValidationError as exc:
    # From JSON, x is still not valid in strict mode, but y is:
    print(exc)
    """
    1 validation error for Model
    x
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    """
```

---

TITLE: Pydantic Union with Left-to-Right Mode
DESCRIPTION: Demonstrates how to configure a Pydantic field to use 'left_to_right' union mode. It shows successful validation for both string and integer inputs and how validation errors are aggregated from all union members when input is invalid.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_0

LANGUAGE: python
CODE:

```
from typing import Union

from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    id: Union[str, int] = Field(union_mode='left_to_right')


print(User(id=123))
#> id=123
print(User(id='hello'))
#> id='hello'

try:
    User(id=[])
except ValidationError as e:
    print(e)
    """
    2 validation errors for User
    id.str
      Input should be a valid string [type=string_type, input_value=[], input_type=list]
    id.int
      Input should be a valid integer [type=int_type, input_value=[], input_type=list]
    """
```

---

TITLE: Enable Strict Mode for Individual Fields with Pydantic Annotated
DESCRIPTION: Demonstrates how to apply strict validation to specific fields in a Pydantic `BaseModel` using `typing.Annotated` and `pydantic.types.Strict`. This ensures that inputs strictly match the annotated type, preventing implicit type coercion.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_10

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, Strict, ValidationError


class User(BaseModel):
    name: str
    age: int
    is_active: Annotated[bool, Strict()]


User(name='David', age=33, is_active=True)
try:
    User(name='David', age=33, is_active='True')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for User
    is_active
      Input should be a valid boolean [type=bool_type, input_value='True', input_type=str]
    """
```

---

TITLE: Pydantic Model Serialization by Alias using ConfigDict
DESCRIPTION: Demonstrates how to enable serialization by alias for a Pydantic model using `ConfigDict.serialize_by_alias`. This sets the default behavior for the model, causing fields with `serialization_alias` to be output using that alias.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_11

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    my_field: str = Field(serialization_alias='my_alias')

    model_config = ConfigDict(serialize_by_alias=True)


m = Model(my_field='foo')
print(m.model_dump())  # (1)!
#> {'my_alias': 'foo'}
```

---

TITLE: Instantiating Pydantic Model with Valid Generic Data - Python
DESCRIPTION: Shows how to create an instance of the `Model` class using valid Python objects for the nested generic `Owner` types. The output confirms successful validation and instantiation of the model.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_22

LANGUAGE: Python
CODE:

```
model = Model(
    car_owner=Owner(name='John', item=Car(color='black')),
    home_owner=Owner(name='James', item=House(rooms=3)),
)
print(model)
```

---

TITLE: Type Checking with Pydantic Alias and validate_by_name
DESCRIPTION: This snippet demonstrates that when `ConfigDict(validate_by_name=True)` is used along with `Field(alias='...')`, static type checkers will _not_ accept instance creation using the original field name, even though Pydantic runtime validation might allow it. It requires `pydantic.BaseModel`, `pydantic.ConfigDict`, and `pydantic.Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_14

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    name: str = Field(alias='username')


user = User(name='johndoe')  # (1)!
```

---

TITLE: Invalid Field Metadata in Named Alias ('type' Syntax, Python 3.12+)
DESCRIPTION: Illustrates that field-specific metadata like `pydantic.Field` cannot be used directly within a named type alias defined with the new `type` statement. Only metadata applicable to the type itself (like validation constraints) is supported.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_7

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, Field

type MyAlias = Annotated[int, Field(default=1)]


class Model(BaseModel):
    x: MyAlias  # This is not allowed
```

---

TITLE: Install Pydantic Migration Tool
DESCRIPTION: Provides the command to install `bump-pydantic`, a beta tool designed to assist with automated code migration from Pydantic V1 to V2. This tool can help streamline the update process.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_2

LANGUAGE: bash
CODE:

```
pip install bump-pydantic
```

---

TITLE: Configure Pydantic Dataclasses with ConfigDict
DESCRIPTION: This snippet shows two methods to configure Pydantic dataclasses using `ConfigDict`. Configuration can be applied either directly as an argument to the `@dataclass` decorator or by defining a `__pydantic_config__` attribute within the dataclass, enabling features like `validate_assignment`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass


# Option 1 -- using the decorator argument:
@dataclass(config=ConfigDict(validate_assignment=True))  # (1)!
class MyDataclass1:
    a: int


# Option 2 -- using an attribute:
@dataclass
class MyDataclass2:
    a: int

    __pydantic_config__ = ConfigDict(validate_assignment=True)
```

---

TITLE: Pydantic TypeAdapter Strict Boolean Validation
DESCRIPTION: Demonstrates how to use `TypeAdapter` for boolean validation. It highlights the difference between lax (default) and strict mode, where strict mode raises a `ValidationError` for non-boolean string inputs like 'yes'.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter, ValidationError

print(TypeAdapter(bool).validate_python('yes'))  # OK: lax
#> True

try:
    TypeAdapter(bool).validate_python('yes', strict=True)  # Not OK: strict
except ValidationError as exc:
    print(exc)
    """
    1 validation error for bool
      Input should be a valid boolean [type=bool_type, input_value='yes', input_type=str]
    """
```

---

TITLE: Inheriting and Validating Standard Library Dataclasses with Pydantic
DESCRIPTION: This snippet demonstrates how Pydantic automatically validates fields when inheriting from standard library dataclasses, including nested ones. It shows an example of a class hierarchy where Pydantic validates inherited fields and catches type errors.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_4

LANGUAGE: python
CODE:

```
import dataclasses

import pydantic


@dataclasses.dataclass
class Z:
    z: int


@dataclasses.dataclass
class Y(Z):
    y: int = 0


@pydantic.dataclasses.dataclass
class X(Y):
    x: int = 0


foo = X(x=b'1', y='2', z='3')
print(foo)
#|> X(z=3, y=2, x=1)

try:
    X(z='pika')
except pydantic.ValidationError as e:
    print(e)
    """
    1 validation error for X
    z
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='pika', input_type=str]
    """
```

---

TITLE: Validate Pydantic Model with `type[T]` for Subclasses
DESCRIPTION: Demonstrates how to use `type[T]` in Pydantic to specify that a field must accept only classes that are subclasses of `T`. Includes an example of `ValidationError` when an invalid class is provided.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_24

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Foo:
    pass


class Bar(Foo):
    pass


class Other:
    pass


class SimpleModel(BaseModel):
    just_subclasses: type[Foo]


SimpleModel(just_subclasses=Foo)
SimpleModel(just_subclasses=Bar)
try:
    SimpleModel(just_subclasses=Other)
except ValidationError as e:
    print(e)
```

---

TITLE: Customizing Pydantic Validation Errors with Discriminated Unions
DESCRIPTION: This snippet defines a `DiscriminatedModel` using `Annotated` and `Discriminator` to manage a union of `str` and a recursive `DiscriminatedModel`. It demonstrates how to provide `custom_error_type`, `custom_error_message`, and `custom_error_context` for validation failures, showing the resulting `ValidationError` output. It also illustrates successful validation of nested data and its dumped output.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/unions.md#_snippet_11

LANGUAGE: python
CODE:

```
def model_x_discriminator(v):
    if isinstance(v, str):
        return 'str'
    if isinstance(v, (dict, BaseModel)):
        return 'model'


class DiscriminatedModel(BaseModel):
    x: Annotated[
        Union[
            Annotated[str, Tag('str')],
            Annotated['DiscriminatedModel', Tag('model')],
        ],
        Discriminator(
            model_x_discriminator,
            custom_error_type='invalid_union_member',  # (1)!
            custom_error_message='Invalid union member',  # (2)!
            custom_error_context={'discriminator': 'str_or_model'},  # (3)!
        ),
    ]


try:
    DiscriminatedModel.model_validate({'x': {'x': {'x': 1}}})
except ValidationError as e:
    print(e)

try:
    DiscriminatedModel.model_validate({'x': {'x': {'x': {}}}})
except ValidationError as e:
    print(e)

# The data is still handled properly when valid:
data = {'x': {'x': {'x': 'a'}}}
m = DiscriminatedModel.model_validate(data)
print(m.model_dump())
```

---

TITLE: Validate Pydantic Model by Alias or Name
DESCRIPTION: Illustrates configuring `ConfigDict` with both `validate_by_alias=True` and `validate_by_name=True`, allowing model fields to be populated using either their alias or their attribute name during validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_9

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)


print(repr(Model(my_alias='foo')))  # (1)!
#> Model(my_field='foo')

print(repr(Model(my_field='foo')))  # (2)!
#> Model(my_field='foo')
```

---

TITLE: Handle Unenforced Pydantic Field Constraints
DESCRIPTION: This snippet illustrates how Pydantic handles unenforced constraints when using `Field` with types like `PositiveInt`. It shows that direct `Field` constraints might be ignored if the type hint takes precedence, leading to a `ValueError`. It then provides an alternative by declaring constraints directly in `Field` for `int` to ensure both are enforced and correctly reflected in the JSON Schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_11

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, PositiveInt

try:
    # this won't work since `PositiveInt` takes precedence over the
    # constraints defined in `Field`, meaning they're ignored
    class Model(BaseModel):
        foo: PositiveInt = Field(lt=10)

except ValueError as e:
    print(e)


# if you find yourself needing this, an alternative is to declare
# the constraints in `Field` (or you could use `conint()`)
# here both constraints will be enforced:
class ModelB(BaseModel):
    # Here both constraints will be applied and the schema
    # will be generated correctly
    foo: int = Field(gt=0, lt=10)


print(ModelB.model_json_schema())
"""
{
    'properties': {
        'foo': {
            'exclusiveMaximum': 10,
            'exclusiveMinimum': 0,
            'title': 'Foo',
            'type': 'integer',
        }
    },
    'required': ['foo'],
    'title': 'ModelB',
    'type': 'object',
}
"""
```

---

TITLE: Demonstrate `int_type` Pydantic Validation Error
DESCRIPTION: This error occurs when an input value's type is incompatible with an `int` field in a Pydantic model. The snippet illustrates this by attempting to assign `None` to an integer field, which results in a `ValidationError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_45

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: int


try:
    Model(x=None)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'int_type'
```

---

TITLE: Pydantic Dictionary Type Validation with `dict`
DESCRIPTION: Shows how to validate a dictionary where both keys and values have specific types using `dict[str, int]`. The example demonstrates successful validation and a `ValidationError` when a value type is incorrect.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_17

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: dict[str, int]


m = Model(x={'foo': 1})
print(m.model_dump())
#> {'x': {'foo': 1}}

try:
    Model(x={'foo': '1'})
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    x
      Input should be a valid dictionary [type=dict_type, input_value='test', input_type=str]
    """
```

---

TITLE: Define Pydantic BaseModel with Custom Field Serializer
DESCRIPTION: This Python code demonstrates how to define a custom serialization function for a field in a Pydantic `BaseModel` using the `@field_serializer` decorator. The `serialize_foo` method is applied to the `foo` field, with `mode='plain'`, indicating how custom serialization logic is integrated.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/architecture.md#_snippet_3

LANGUAGE: python
CODE:

```
class Model(BaseModel):
    foo: bool = Field(strict=True)

    @field_serializer('foo', mode='plain')
    def serialize_foo(self, value: bool) -> Any:
        ...
```

---

TITLE: Pydantic V2: Changes to Generic Models and `GenericModel` Removal
DESCRIPTION: In Pydantic V2, `pydantic.generics.GenericModel` is removed. Generic `BaseModel` subclasses are now created by directly inheriting from `BaseModel` and `Generic`. This section also advises against using parametrized generics in `isinstance` checks directly, suggesting subclassing instead.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_12

LANGUAGE: APIDOC
CODE:

```
pydantic.generics.GenericModel:
  - Removed in V2.
  - V2 equivalent: Inherit `BaseModel` and `Generic[T]` directly.
    Example: `class MyGenericModel(BaseModel, Generic[T]): ...`
  - `isinstance` checks with parametrized generics (e.g., `MyGenericModel[int]`) are discouraged.
    Recommended: Subclass the parametrized generic (e.g., `class MyIntModel(MyGenericModel[int]): ...`) then check `isinstance(my_model, MyIntModel)`.
```

---

TITLE: Validate Pydantic Model by Alias Only
DESCRIPTION: Demonstrates how to configure `ConfigDict` with `validate_by_alias=True` and `validate_by_name=False` to ensure that model fields are populated exclusively using their defined aliases during validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=False)


print(repr(Model(my_alias='foo')))  # (1)!
#> Model(my_field='foo')
```

---

TITLE: Use `json_schema_input_type` with compatible `field_validator` modes
DESCRIPTION: This error occurs when `json_schema_input_type` is explicitly specified for a `field_validator` where `mode` is not set to `'before'`, `'plain'`, or `'wrap'`. This argument is incompatible with `after` validators because the value is already validated against the type annotation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_27

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: int = 1

        @field_validator('a', mode='after', json_schema_input_type=int)
        @classmethod
        def check_a(self, value):
            return value

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-input-type'
```

---

TITLE: Inspecting Pydantic Models with `python-devtools.debug()`
DESCRIPTION: This Python code demonstrates how to use `devtools.debug()` to inspect a Pydantic `User` model. Unlike `print()`, `debug()` leverages Pydantic's `__pretty__` method implementation to format complex model output in a highly readable way, including type information and structure. It also provides file and line number context, making debugging Pydantic models significantly easier.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/devtools.md#_snippet_0

LANGUAGE: python
CODE:

```
from datetime import datetime

from devtools import debug

from pydantic import BaseModel


class Address(BaseModel):
    street: str
    country: str
    lat: float
    lng: float


class User(BaseModel):
    id: int
    name: str
    signup_ts: datetime
    friends: list[int]
    address: Address


user = User(
    id='123',
    name='John Doe',
    signup_ts='2019-06-01 12:22',
    friends=[1234, 4567, 7890],
    address=dict(street='Testing', country='uk', lat=51.5, lng=0),
)
debug(user)
print('\nshould be much easier read than:\n')
print('user:', user)
```

---

TITLE: Pydantic Handling of `pathlib.Path`
DESCRIPTION: Describes Pydantic's validation for `pathlib.Path` types, which involves simply passing the input value directly to the `Path(v)` constructor for instantiation and validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_35

LANGUAGE: APIDOC
CODE:

```
pathlib.Path:
  Behavior: Simply uses the type itself for validation by passing the value to `Path(v)`.
```

---

TITLE: Pydantic PydanticUseDefault for Conditional Default Values
DESCRIPTION: This example demonstrates how PydanticUseDefault can be raised within a BeforeValidator to instruct Pydantic to use the field's default value. It's useful for scenarios where a specific input (e.g., None) should trigger the use of a predefined default.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_20

LANGUAGE: python
CODE:

```
from typing import Annotated, Any

from pydantic_core import PydanticUseDefault

from pydantic import BaseModel, BeforeValidator


def default_if_none(value: Any) -> Any:
    if value is None:
        raise PydanticUseDefault()
    return value


class Model(BaseModel):
    name: Annotated[str, BeforeValidator(default_if_none)] = 'default_name'


print(Model(name=None))
# > name='default_name'
```

---

TITLE: Pydantic: Resolving Invalid Annotated Type Error
DESCRIPTION: This error is raised when an `Annotated` type cannot properly annotate another type, often due to incompatible type hints or Pydantic validators. It results in a `PydanticUserError` with code 'invalid-annotated-type'.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_36

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, FutureDate, PydanticUserError

try:

    class Model(BaseModel):
        foo: Annotated[str, FutureDate()]

except PydanticUserError as exc_info:
    assert exc_info.code == 'invalid-annotated-type'
```

---

TITLE: Override Generated Aliases with Field Alias
DESCRIPTION: Illustrates that an explicit `alias` set on a `Field` takes precedence over a generated alias from `ConfigDict.alias_generator` by default, allowing fine-grained control over field naming.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_6

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


class Voice(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: str
    language_code: str = Field(alias='lang')


voice = Voice(Name='Filiz', lang='tr-TR')
print(voice.language_code)
#> tr-TR
print(voice.model_dump(by_alias=True))
#> {'Name': 'Filiz', 'lang': 'tr-TR'}
```

---

TITLE: Access Field Name in Pydantic Core Schema Python
DESCRIPTION: Illustrates how to access the field name (`info.field_name`) within a custom type's `__get_pydantic_core_schema__` method and its validator function. This allows the custom type instance to store information about the field it was used in, as shown by the `CustomType` example.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_27

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler, ValidationInfo


class CustomType:
    """Custom type that stores the field it was used in."""

    def __init__(self, value: int, field_name: str):
        self.value = value
        self.field_name = field_name

    def __repr__(self):
        return f'CustomType<{self.value} {self.field_name!r}>'

    @classmethod
    def validate(cls, value: int, info: ValidationInfo):
        return cls(value, info.field_name)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate, handler(int)
        )


class MyModel(BaseModel):
    my_field: CustomType


m = MyModel(my_field=1)
print(m.my_field)
# CustomType<1 'my_field'>

```

---

TITLE: Validate Pydantic Models with TypedDict and TypeAdapter
DESCRIPTION: Demonstrates how to define Pydantic models using `TypedDict` for structured data, including optional fields (`total=False`) and strict extra field handling (`ConfigDict(extra='forbid')`). It shows how to use `TypeAdapter` for validation and illustrates common validation errors for incorrect types or forbidden extra fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_19

LANGUAGE: python
CODE:

```
from typing import Optional, TypedDict

from pydantic import ConfigDict, TypeAdapter, ValidationError


# `total=False` means keys are non-required
class UserIdentity(TypedDict, total=False):
    name: Optional[str]
    surname: str


class User(TypedDict):
    __pydantic_config__ = ConfigDict(extra='forbid')

    identity: UserIdentity
    age: int

ta = TypeAdapter(User)

print(
    ta.validate_python(
        {'identity': {'name': 'Smith', 'surname': 'John'}, 'age': 37}
    )
)

print(
    ta.validate_python(
        {'identity': {'name': None, 'surname': 'John'}, 'age': 37}
    )
)

print(ta.validate_python({'identity': {}, 'age': 37}))


try:
    ta.validate_python(
        {'identity': {'name': ['Smith'], 'surname': 'John'}, 'age': 24}
    )
except ValidationError as e:
    print(e)

try:
    ta.validate_python(
        {
            'identity': {'name': 'Smith', 'surname': 'John'},
            'age': '37',
            'email': 'john.smith@me.com',
        }
    )
except ValidationError as e:
    print(e)
```

---

TITLE: Handle Pydantic value_error from Custom Validator
DESCRIPTION: This error is raised when a `ValueError` is explicitly thrown within a Pydantic field validator or a custom model validator. Pydantic catches these standard Python errors and converts them into its own validation error type. The example demonstrates defining a custom `field_validator` that unconditionally raises a `ValueError`, showing how Pydantic processes this into a `value_error`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_99

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError, field_validator


class Model(BaseModel):
    x: str

    @field_validator('x')
    @classmethod
    def repeat_b(cls, v):
        raise ValueError()


try:
    Model(x='test')
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'value_error'
```

---

TITLE: Pydantic Field-Level Strict Validation
DESCRIPTION: Demonstrates how to apply strict validation to individual fields using `Field(strict=True)`. This ensures that only the specified field adheres to strict type checking, even if the overall validation method is not called with `strict=True`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_6

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    name: str
    age: int
    n_pets: int


user = User(name='John', age='42', n_pets='1')
print(user)
#> name='John' age=42 n_pets=1


class AnotherUser(BaseModel):
    name: str
    age: int = Field(strict=True)
    n_pets: int


try:
    anotheruser = AnotherUser(name='John', age='42', n_pets='1')
except ValidationError as e:
    print(e)
    """
    1 validation error for AnotherUser
    age
      Input should be a valid integer [type=int_type, input_value='42', input_type=str]
    """
```

---

TITLE: Using typing.TypeVar with Pydantic Models
DESCRIPTION: Demonstrates how Pydantic supports `TypeVar` (unconstrained, constrained, or with a bound) and illustrates its usage within a `BaseModel` with examples of valid and `None` assignments.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_26

LANGUAGE: python
CODE:

```
from typing import TypeVar

from pydantic import BaseModel

Foobar = TypeVar('Foobar')
BoundFloat = TypeVar('BoundFloat', bound=float)
IntStr = TypeVar('IntStr', int, str)


class Model(BaseModel):
    a: Foobar  # equivalent of ": Any"
    b: BoundFloat  # equivalent of ": float"
    c: IntStr  # equivalent of ": Union[int, str]"


print(Model(a=[1], b=4.2, c='x'))
# a=[1] b=4.2 c='x'

# a may be None
print(Model(a=None, b=1, c=1))
# a=None b=1.0 c=1
```

---

TITLE: Configuring Pydantic Model Immutability with frozen (Python)
DESCRIPTION: Demonstrates how to make a Pydantic model instance immutable by setting `model_config['frozen'] = True`. Shows that direct attribute assignment fails, but mutation of nested mutable objects (like dictionaries) is still possible.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_45

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, ValidationError


class FooBarModel(BaseModel):
    model_config = ConfigDict(frozen=True)

    a: str
    b: dict


foobar = FooBarModel(a='hello', b={'apple': 'pear'})

try:
    foobar.a = 'different'
except ValidationError as e:
    print(e)
    """
    1 validation error for FooBarModel
    a
      Instance is frozen [type=frozen_instance, input_value='different', input_type=str]
    """

print(foobar.a)
#> hello
print(foobar.b)
#> {'apple': 'pear'}
foobar.b['apple'] = 'grape'
print(foobar.b)
#> {'apple': 'grape'}
```

---

TITLE: Override Global Strict Mode for Pydantic BaseModel Fields
DESCRIPTION: Shows how to selectively disable strict validation for individual fields within a Pydantic `BaseModel` when a global `ConfigDict(strict=True)` is applied. This is achieved by using `Field(strict=False)` on the specific field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_12

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    age: int = Field(strict=False)
```

---

TITLE: Merge Pydantic Configuration in Subclasses
DESCRIPTION: Explains how configuration defined in subclasses merges with inherited parent configurations. Specific settings in the subclass's `model_config` override or combine with parent settings, as shown with `str_to_lower`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict


class Parent(BaseModel):
    model_config = ConfigDict(extra='allow', str_to_lower=False)


class Model(Parent):
    model_config = ConfigDict(str_to_lower=True)

    x: str


m = Model(x='FOO', y='bar')
print(m.model_dump())
#> {'x': 'foo', 'y': 'bar'}
print(Model.model_config)
#> {'extra': 'allow', 'str_to_lower': True}
```

---

TITLE: Marking Field as Deprecated with Boolean Flag
DESCRIPTION: Illustrates how to mark a field as deprecated in a Pydantic model using the boolean `deprecated=True` argument in `Field`. Also shows how this is reflected in the generated JSON schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_34

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, Field


class Model(BaseModel):
    deprecated_field: Annotated[int, Field(deprecated=True)]


print(Model.model_json_schema()['properties']['deprecated_field'])
#> {'deprecated': True, 'title': 'Deprecated Field', 'type': 'integer'}
```

---

TITLE: Enabling Pydantic Mypy Plugin in pyproject.toml - TOML
DESCRIPTION: Shows how to enable the Pydantic Mypy plugin by adding `pydantic.mypy` to the `plugins` list under the `[tool.mypy]` section in a `pyproject.toml` configuration file.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md#_snippet_2

LANGUAGE: toml
CODE:

```
[tool.mypy]
plugins = ['pydantic.mypy']
```

---

TITLE: Controlling Pydantic Generic Model Serialization with SerializeAsAny
DESCRIPTION: Demonstrates how Pydantic serializes generic models with default types, showing that by default it uses the serializer of the default type, but this can be overridden using SerializeAsAny to serialize the actual runtime type.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_36

LANGUAGE: python
CODE:

```
from typing import Generic

from typing_extensions import TypeVar

from pydantic import BaseModel, SerializeAsAny


class ErrorDetails(BaseModel):
    foo: str


ErrorDataT = TypeVar('ErrorDataT', default=ErrorDetails)


class Error(BaseModel, Generic[ErrorDataT]):
    message: str
    details: ErrorDataT


class MyErrorDetails(ErrorDetails):
    bar: str


# serialized using the default's serializer
error = Error(
    message='We just had an error',
    details=MyErrorDetails(foo='var', bar='var2'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
    },
}
# If `ErrorDataT` was using an upper bound, `bar` would be present in `details`.


class SerializeAsAnyError(BaseModel, Generic[ErrorDataT]):
    message: str
    details: SerializeAsAny[ErrorDataT]


# serialized as Any
error = SerializeAsAnyError(
    message='We just had an error',
    details=MyErrorDetails(foo='var', bar='baz'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
        'bar': 'baz',
    },
}
```

---

TITLE: Pydantic Handling of `typing.Any`
DESCRIPTION: Describes Pydantic's behavior when encountering `typing.Any`, indicating it allows any value, including `None`, without performing specific validation beyond basic type checking.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_31

LANGUAGE: APIDOC
CODE:

```
typing.Any:
  Description: Allows any value, including `None`.
```

---

TITLE: Customize Pydantic Error Location (loc) Format
DESCRIPTION: This Python code shows how to modify the 'loc' field of Pydantic validation errors from a tuple representation to a dot-separated string with array indexing. It defines a 'loc_to_dot_sep' function to transform the location tuple and then applies this transformation to the errors list. This can improve readability for nested data structures.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/errors.md#_snippet_5

LANGUAGE: python
CODE:

```
from typing import Any, Union

from pydantic import BaseModel, ValidationError


def loc_to_dot_sep(loc: tuple[Union[str, int], ...]) -> str:
    path = ''
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += '.'
            path += x
        elif isinstance(x, int):
            path += f'[{x}]'
        else:
            raise TypeError('Unexpected type')
    return path


def convert_errors(e: ValidationError) -> list[dict[str, Any]]:
    new_errors: list[dict[str, Any]] = e.errors()
    for error in new_errors:
        error['loc'] = loc_to_dot_sep(error['loc'])
    return new_errors


class TestNestedModel(BaseModel):
    key: str
    value: str


class TestModel(BaseModel):
    items: list[TestNestedModel]


data = {'items': [{'key': 'foo', 'value': 'bar'}, {'key': 'baz'}]}

try:
    TestModel.model_validate(data)
except ValidationError as e:
    print(e.errors())  # (1)!
    """
    [
        {
            'type': 'missing',
            'loc': ('items', 1, 'value'),
            'msg': 'Field required',
            'input': {'key': 'baz'},
            'url': 'https://errors.pydantic.dev/2/v/missing',
        }
    ]
    """
    pretty_errors = convert_errors(e)
    print(pretty_errors)  # (2)!
    """
    [
        {
            'type': 'missing',
            'loc': 'items[1].value',
            'msg': 'Field required',
            'input': {'key': 'baz'},
            'url': 'https://errors.pydantic.dev/2/v/missing',
        }
    ]
    """
```

---

TITLE: Pydantic Model Parsing with `Union` and `Literal` for Type Specificity
DESCRIPTION: Shows how to order types in a `typing.Union` with `typing.Literal` to parse data into the most specific matching Pydantic model. Demonstrates how Pydantic resolves types based on the order in the union and literal values, allowing for hierarchical parsing.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_30

LANGUAGE: python
CODE:

```
from typing import Literal, Optional, Union

from pydantic import BaseModel


class Dessert(BaseModel):
    kind: str


class Pie(Dessert):
    kind: Literal['pie']
    flavor: Optional[str]


class ApplePie(Pie):
    flavor: Literal['apple']


class PumpkinPie(Pie):
    flavor: Literal['pumpkin']


class Meal(BaseModel):
    dessert: Union[ApplePie, PumpkinPie, Pie, Dessert]


print(type(Meal(dessert={'kind': 'pie', 'flavor': 'apple'}).dessert).__name__)
#> ApplePie
print(type(Meal(dessert={'kind': 'pie', 'flavor': 'pumpkin'}).dessert).__name__)
#> PumpkinPie
print(type(Meal(dessert={'kind': 'pie'}).dessert).__name__)
#> Dessert
print(type(Meal(dessert={'kind': 'cake'}).dessert).__name__)
#> Dessert
```

---

TITLE: Handle Pydantic `int_from_float` Validation Error
DESCRIPTION: This error is raised when you provide a `float` value for an `int` field. It indicates that Pydantic does not automatically coerce float values to integers for strict type validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_42

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: int


try:
    Model(x=0.5)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'int_from_float'
```

---

TITLE: Applying Pydantic validate_call to Asynchronous Functions
DESCRIPTION: This example illustrates that the `pydantic.validate_call` decorator can also be applied to asynchronous functions and methods, ensuring argument validation works seamlessly with `async def` syntax.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validation_decorator.md#_snippet_7

LANGUAGE: Python
CODE:

```
class Connection:
    async def execute(self, sql, *args):
        return 'testing@example.com'


conn = Connection()
```

---

TITLE: Inspecting Pydantic Core Schema with Unresolved Forward Reference
DESCRIPTION: This Python snippet demonstrates how Pydantic's core schema generation fails silently when a model contains a forward reference ('MyType') that is not yet defined. Inspecting `__pydantic_core_schema__` shows a `MockCoreSchema` object, indicating the schema could not be fully built.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/resolving_annotations.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Foo(BaseModel):
    f: 'MyType'


Foo.__pydantic_core_schema__
#> <pydantic._internal._mock_val_ser.MockCoreSchema object at 0x73cd0d9e6d00>
```

---

TITLE: Generate JSON Schema for Union Types with TypeAdapter
DESCRIPTION: This Python example demonstrates how to use Pydantic's `TypeAdapter` to generate a JSON schema for a `Union` of `BaseModel` classes. It shows how `TypeAdapter.json_schema()` combines schemas for `Cat` and `Dog` into an `anyOf` structure, which is useful for validating polymorphic data.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_4

LANGUAGE: python
CODE:

```
import json
from typing import Union

from pydantic import BaseModel, TypeAdapter


class Cat(BaseModel):
    name: str
    color: str


class Dog(BaseModel):
    name: str
    breed: str


ta = TypeAdapter(Union[Cat, Dog])
ta_schema = ta.json_schema()
print(json.dumps(ta_schema, indent=2))
"""
{
  "$defs": {
    "Cat": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "color": {
          "title": "Color",
          "type": "string"
        }
      },
      "required": [
        "name",
        "color"
      ],
      "title": "Cat",
      "type": "object"
    },
    "Dog": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "breed": {
          "title": "Breed",
          "type": "string"
        }
      },
      "required": [
        "name",
        "breed"
      ],
      "title": "Dog",
      "type": "object"
    }
  },
  "anyOf": [
    {
      "$ref": "#/$defs/Cat"
    },
    {
      "$ref": "#/$defs/Dog"
    }
  ]
}
"""
```

---

TITLE: Pydantic ConfigDict.serialize_by_alias API
DESCRIPTION: API documentation for the `ConfigDict.serialize_by_alias` setting. This boolean flag controls whether aliases are used for serialization by default for a Pydantic model. When `True`, fields with `serialization_alias` will use that alias in the dumped output. It is `False` by default.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_16

LANGUAGE: APIDOC
CODE:

```
ConfigDict.serialize_by_alias: bool
  Description: Controls whether aliases are used for serialization by default.
  Default: False
```

---

TITLE: Use WrapSerializer for Advanced Pydantic Field Serialization
DESCRIPTION: Illustrates `WrapSerializer`, which receives raw inputs and a handler function to apply standard serialization logic, allowing modification of the resulting value. It also accepts optional `return_type` and `when_used` arguments. The example increments an integer and formats it with commas when serialized to JSON mode.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_5

LANGUAGE: python
CODE:

```
from typing import Annotated, Any

from pydantic import BaseModel, SerializerFunctionWrapHandler
from pydantic.functional_serializers import WrapSerializer


def ser_wrap(v: Any, nxt: SerializerFunctionWrapHandler) -> str:
    return f'{nxt(v + 1):,}'


FancyInt = Annotated[int, WrapSerializer(ser_wrap, when_used='json')]


class MyModel(BaseModel):
    x: FancyInt


print(MyModel(x=1234).model_dump())
#> {'x': 1234}

print(MyModel(x=1234).model_dump(mode='json'))
#> {'x': '1,235'}
```

---

TITLE: Pydantic IP Address Type Validation
DESCRIPTION: Pydantic supports various `ipaddress` types for validation. Validation is performed by passing the input value directly to the respective `ipaddress` type constructor.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_21

LANGUAGE: APIDOC
CODE:

```
ipaddress.IPv4Address: Uses the type itself for validation by passing the value to IPv4Address(v).
ipaddress.IPv4Interface: Uses the type itself for validation by passing the value to IPv4Address(v).
ipaddress.IPv4Network: Uses the type itself for validation by passing the value to IPv4Network(v).
ipaddress.IPv6Address: Uses the type itself for validation by passing the value to IPv6Address(v).
ipaddress.IPv6Interface: Uses the type itself for validation by passing the value to IPv6Interface(v).
ipaddress.IPv6Network: Uses the type itself for validation by passing the value to IPv6Network(v).
```

---

TITLE: Pydantic: Avoiding 'model_config' as a Model Field Name
DESCRIPTION: Pydantic reserves the name `model_config` for internal configuration. Using `model_config` as a field name in a `BaseModel` subclass will raise a `PydanticUserError`, preventing conflicts with Pydantic's internal mechanisms.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_42

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError

try:

    class Model(BaseModel):
        model_config: str

except PydanticUserError as exc_info:
    assert exc_info.code == 'model-config-invalid-field-name'
```

---

TITLE: Pydantic Instance Revalidation with 'never' (Python)
DESCRIPTION: This example shows the default behavior when `revalidate_instances` is not set or set to 'never'. An invalid value assigned to a model instance field does not cause `model_validate` to raise an error when validating the instance itself.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_15

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Model(BaseModel):
    a: int


m = Model(a=0)
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior.
m.a = 'not an int'

# doesn't raise a validation error even though m is invalid
m2 = Model.model_validate(m)
```

---

TITLE: Avoid applying `field_validator` on instance methods
DESCRIPTION: This error is raised when you apply a `field_validator` on an instance method. Field validators should typically be class methods or static methods, not bound to an instance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_26

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: int = 1

        @field_validator('a')
        def check_a(self, value):
            return value

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-instance-method'
```

---

TITLE: Pydantic: Applying `validate_call` to Class Constructors
DESCRIPTION: This snippet explains why `validate_call` cannot be applied directly to a class and how to correctly validate a class's constructor. It shows an erroneous attempt to decorate a class with `validate_call` and then the correct method of applying it to the `__init__` or `__new__` methods.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_46

LANGUAGE: python
CODE:

```
from pydantic import PydanticUserError, validate_call

# Incorrect usage: @validate_call on a class
try:

    @validate_call
    class A1: ...

except PydanticUserError as exc_info:
    assert exc_info.code == 'validate-call-type'


# Correct usage: @validate_call on __init__ or __new__
class A2:
    @validate_call
    def __init__(self): ...

    @validate_call
    def __new__(cls): ...
```

---

TITLE: Pydantic BaseModel.model_copy API Reference
DESCRIPTION: API documentation for the `model_copy` method of `pydantic.main.BaseModel`. This method allows duplicating a model instance, optionally updating some fields, and supports both shallow and deep copies.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_24

LANGUAGE: APIDOC
CODE:

```
pydantic.main.BaseModel.model_copy
```

---

TITLE: Enabling Duck-Typing Serialization with Pydantic's SerializeAsAny Annotation
DESCRIPTION: This Python example demonstrates how to use the `SerializeAsAny` annotation to achieve duck-typing serialization behavior in Pydantic V2. It shows a `User` base model and a `UserLogin` subclass. When an `OuterModel` contains fields annotated with `SerializeAsAny[User]` and plain `User`, passing a `UserLogin` instance reveals that `SerializeAsAny` includes subclass-specific fields (like 'password') in the serialized output, while the plain `User` field only includes base class fields. Validation and type-checking behave as if the field was the original type, but serialization treats it as `Any`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_14

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, SerializeAsAny


class User(BaseModel):
    name: str


class UserLogin(User):
    password: str


class OuterModel(BaseModel):
    as_any: SerializeAsAny[User]
    as_user: User


user = UserLogin(name='pydantic', password='password')

print(OuterModel(as_any=user, as_user=user).model_dump())
"""
{
    'as_any': {'name': 'pydantic', 'password': 'password'},
    'as_user': {'name': 'pydantic'},
}
"""
```

---

TITLE: Attribute Copying During BaseModel Construction (Python)
DESCRIPTION: Compares how a standard class and a Pydantic BaseModel handle a mutable input (a list), showing that Pydantic copies the input during validation, resulting in different object IDs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_53

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class C1:
    arr = []

    def __init__(self, in_arr):
        self.arr = in_arr


class C2(BaseModel):
    arr: list[int]


arr_orig = [1, 9, 10, 3]


c1 = C1(arr_orig)
c2 = C2(arr=arr_orig)
print(f'{id(c1.arr) == id(c2.arr)=}')
```

---

TITLE: Configure JSON Schema Generation Mode in Pydantic
DESCRIPTION: This Python example illustrates how to control the JSON schema generation mode using the `mode` parameter in `model_json_schema`. It compares the schemas produced by `'validation'` mode, which includes `anyOf` for type coercion, and `'serialization'` mode, which strictly defines the serialized output type.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_5

LANGUAGE: python
CODE:

```
from decimal import Decimal

from pydantic import BaseModel


class Model(BaseModel):
    a: Decimal = Decimal('12.34')


print(Model.model_json_schema(mode='validation'))
"""
{
    'properties': {
        'a': {
            'anyOf': [{'type': 'number'}, {'type': 'string'}],
            'default': '12.34',
            'title': 'A',
        }
    },
    'title': 'Model',
    'type': 'object',
}
"""

print(Model.model_json_schema(mode='serialization'))
"""
{
    'properties': {'a': {'default': '12.34', 'title': 'A', 'type': 'string'}},
    'title': 'Model',
    'type': 'object',
}
"""
```

---

TITLE: Type Checking with Pydantic Field Alias
DESCRIPTION: This snippet shows that when using `Field(alias='...')`, static type checkers will synthesize the `__init__` method using the alias name, accepting instance creation with the alias. It requires `pydantic.BaseModel` and `pydantic.Field`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_13

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(alias='username')


user = User(username='johndoe')  # (1)!
```

---

TITLE: Instantiate Pydantic Model Using typing.Any
DESCRIPTION: Defines a Pydantic `Knight` model. Shows how to assign the string value `'23'` to a variable `age_str` explicitly typed as `Any`. This variable is then passed to the `age` field during instantiation, causing the type checker to ignore the type mismatch for that specific value. Requires importing `Any` from `typing`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/visual_studio_code.md#_snippet_4

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel


class Knight(BaseModel):
    title: str
    age: int
    color: str = 'blue'


age_str: Any = '23'
lancelot = Knight(title='Sir Lancelot', age=age_str)
```

---

TITLE: Pydantic Validation Error: datetime_object_invalid
DESCRIPTION: This error is raised when a `datetime` object is invalid, specifically when its `tzinfo` is not properly implemented (e.g., `utcoffset` is missing). It demonstrates how Pydantic's `AwareDatetime` type catches such issues.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_21

LANGUAGE: python
CODE:

```
from datetime import datetime, tzinfo

from pydantic import AwareDatetime, BaseModel, ValidationError


class CustomTz(tzinfo):
    # utcoffset is not implemented!

    def tzname(self, _dt):
        return 'CustomTZ'


class Model(BaseModel):
    x: AwareDatetime


try:
    Model(x=datetime(2023, 1, 1, tzinfo=CustomTz()))
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'datetime_object_invalid'
```

---

TITLE: Configure Pydantic Mypy Plugins
DESCRIPTION: Pydantic V2 includes a mypy plugin in `pydantic.mypy`. If using V1 features, the `pydantic.v1.mypy` plugin may also be required. This snippet shows how to configure both plugins in `mypy.ini` and `pyproject.toml` to ensure proper type checking.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_29

LANGUAGE: ini
CODE:

```
[mypy]
plugins = pydantic.mypy, pydantic.v1.mypy  # include `.v1.mypy` if required.
```

LANGUAGE: toml
CODE:

```
[tool.mypy]
plugins = [
    "pydantic.mypy",
    "pydantic.v1.mypy",  # include `.v1.mypy` if required.
]
```

---

TITLE: Validate Pydantic Model by Name Only
DESCRIPTION: Shows how to configure `ConfigDict` with `validate_by_alias=False` and `validate_by_name=True` to enforce that model fields are populated solely by their attribute names during validation, ignoring aliases.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_8

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')

    model_config = ConfigDict(validate_by_alias=False, validate_by_name=True)


print(repr(Model(my_field='foo')))  # (1)!
#> Model(my_field='foo')
```

---

TITLE: Pydantic InstanceOf for Type Validation
DESCRIPTION: This example shows how to use InstanceOf to validate that elements in a list are instances of a specific base class (Fruit). It demonstrates successful validation with correct types and a ValidationError when an incorrect type is provided.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validators.md#_snippet_18

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, InstanceOf, ValidationError


class Fruit:
    def __repr__(self):
        return self.__class__.__name__


class Banana(Fruit): ...


class Apple(Fruit): ...


class Basket(BaseModel):
    fruits: list[InstanceOf[Fruit]]


print(Basket(fruits=[Banana(), Apple()]))
# > fruits=[Banana, Apple]
try:
    Basket(fruits=[Banana(), 'Apple'])
except ValidationError as e:
    print(e)
    """
    1 validation error for Basket
    fruits.1
      Input should be an instance of Fruit [type=is_instance_of, input_value='Apple', input_type=str]
    """
```

---

TITLE: Specify Generic Parameters for Pydantic TypeAdapter for Proper Typing
DESCRIPTION: This Python example illustrates how to explicitly specify generic parameters for `TypeAdapter` (e.g., `str | int`) to ensure proper type inference and avoid limitations with common type checkers, especially in complex scenarios.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_25

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter

adapter = TypeAdapter[str | int](str | int)
...
```

---

TITLE: Pydantic Boolean Type Validation and Coercion
DESCRIPTION: This snippet demonstrates how Pydantic's `bool` field handles various input types, including standard booleans, integers 0/1, and specific string/bytes representations. It also shows how invalid inputs raise a `ValidationError`, highlighting Pydantic's flexible yet robust type coercion for booleans.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_0

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class BooleanModel(BaseModel):
    bool_value: bool


print(BooleanModel(bool_value=False))
print(BooleanModel(bool_value='False'))
print(BooleanModel(bool_value=1))
try:
    BooleanModel(bool_value=[])
except ValidationError as e:
    print(str(e))
```

---

TITLE: Pydantic Model with Optional Set and Set of Integers
DESCRIPTION: This example illustrates Pydantic's handling of `set` and `typing.Set` fields. It shows how Pydantic casts input iterables to a `set` and applies validation to all items when a generic type parameter is provided, converting string numbers to integers in `Set[int]`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_12

LANGUAGE: python
CODE:

```
from typing import Optional, Set

from pydantic import BaseModel


class Model(BaseModel):
    simple_set: Optional[set] = None
    set_of_ints: Optional[Set[int]] = None


print(Model(simple_set={'1', '2', '3'}).simple_set)
#> {'1', '2', '3'}
print(Model(simple_set=['1', '2', '3']).simple_set)
#> {'1', '2', '3'}
print(Model(set_of_ints=['1', '2', '3']).set_of_ints)
#> {1, 2, 3}
```

---

TITLE: Handling and Suppressing Pydantic Cyclic Validation Errors
DESCRIPTION: Provides a robust method to handle and optionally suppress `ValidationError` caused by cyclic references in Pydantic models. It includes a utility function to check for `recursion_loop` errors and a `field_validator` that demonstrates how to drop cyclic references during validation, allowing partial validation of recursive structures.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/forward_annotations.md#_snippet_3

LANGUAGE: python
CODE:

```
from contextlib import contextmanager
from dataclasses import field
from typing import Iterator

from pydantic import BaseModel, ValidationError, field_validator


def is_recursion_validation_error(exc: ValidationError) -> bool:
    errors = exc.errors()
    return len(errors) == 1 and errors[0]['type'] == 'recursion_loop'


@contextmanager
def suppress_recursion_validation_error() -> Iterator[None]:
    try:
        yield
    except ValidationError as exc:
        if not is_recursion_validation_error(exc):
            raise exc


class Node(BaseModel):
    id: int
    children: list['Node'] = field(default_factory=list)

    @field_validator('children', mode='wrap')
    @classmethod
    def drop_cyclic_references(cls, children, h):
        try:
            return h(children)
        except ValidationError as exc:
            if not (
                is_recursion_validation_error(exc)
                and isinstance(children, list)
            ):
                raise exc

            value_without_cyclic_refs = []
            for child in children:
                with suppress_recursion_validation_error():
                    value_without_cyclic_refs.extend(h([child]))
            return h(value_without_cyclic_refs)


# Create data with cyclic references representing the graph 1 -> 2 -> 3 -> 1
node_data = {'id': 1, 'children': [{'id': 2, 'children': [{'id': 3}]}]}
node_data['children'][0]['children'][0]['children'] = [node_data]

print(Node.model_validate(node_data))
#> id=1 children=[Node(id=2, children=[Node(id=3, children=[])])]
```

---

TITLE: Demonstrate `list_type` Pydantic Validation Error
DESCRIPTION: This error is raised when an input value's type is not valid for a `list` field. The snippet defines a model with a `list[int]` field and demonstrates that attempting to assign a non-list type (e.g., an integer `1`) to it results in a `list_type` validation error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_55

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: list[int]


try:
    Model(x=1)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'list_type'
```

---

TITLE: Serialize Pydantic subclasses of standard types
DESCRIPTION: Shows how Pydantic automatically handles the serialization of subclasses derived from standard Python types (e.g., `datetime.date`), demonstrating a custom date type and its integration into a `BaseModel` for proper dumping.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_12

LANGUAGE: python
CODE:

```
from datetime import date, timedelta
from typing import Any

from pydantic_core import core_schema

from pydantic import BaseModel, GetCoreSchemaHandler


class DayThisYear(date):
    """
    Contrived example of a special type of date that
    takes an int and interprets it as a day in the current year
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.int_schema(),
            serialization=core_schema.format_ser_schema('%Y-%m-%d'),
        )

    @classmethod
    def validate(cls, v: int):
        return date(2023, 1, 1) + timedelta(days=v)


class FooModel(BaseModel):
    date: DayThisYear


m = FooModel(date=300)
print(m.model_dump_json())
#> {"date":"2023-10-28"}
```

---

TITLE: Making Pydantic Fields Immutable with Frozen
DESCRIPTION: Shows how the `frozen=True` parameter on a `Field` makes the field immutable after model creation. Attempts to reassign the field (`user.name = 'Jane'`) result in a `ValidationError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_29

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    name: str = Field(frozen=True)
    age: int


user = User(name='John', age=42)

try:
    user.name = 'Jane'
except ValidationError as e:
    print(e)
```

---

TITLE: Handle Pydantic date_past Validation Error
DESCRIPTION: This error is raised when a `PastDate` field receives an input value that is not in the past relative to the current date.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_17

LANGUAGE: python
CODE:

```
from datetime import date, timedelta

from pydantic import BaseModel, PastDate, ValidationError


class Model(BaseModel):
    x: PastDate


try:
    Model(x=date.today() + timedelta(1))
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'date_past'
```

---

TITLE: Configure Standard Dataclass with **pydantic_config**
DESCRIPTION: Demonstrates configuring standard library dataclasses by setting the `__pydantic_config__` class attribute to a `ConfigDict` instance. This example uses `strict=True` for stricter validation rules.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/config.md#_snippet_4

LANGUAGE: python
CODE:

```
from dataclasses import dataclass

from pydantic import ConfigDict


@dataclass
class User:
    __pydantic_config__ = ConfigDict(strict=True)

    id: int
    name: str = 'John Doe'
```

---

TITLE: Demonstrate `less_than` Pydantic Validation Error
DESCRIPTION: This error is raised when an input value does not satisfy a `lt` (less than) constraint defined on a field. The snippet defines an integer field with `lt=10` and shows that providing a value equal to or greater than 10 (e.g., `10`) triggers the `less_than` validation error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_53

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: int = Field(lt=10)


try:
    Model(x=10)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'less_than'
```

---

TITLE: Pydantic Model Serialization with `serialize_as_any` Flag
DESCRIPTION: This example illustrates how the `serialize_as_any` flag affects Pydantic model serialization. When `True`, subclass fields (like `password`) are included, mimicking V1 behavior. When `False` (the default), only fields defined in the base schema are serialized, ignoring subclass-specific additions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_15

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class User(BaseModel):
    name: str


class UserLogin(User):
    password: str


class OuterModel(BaseModel):
    user1: User
    user2: User


user = UserLogin(name='pydantic', password='password')

outer_model = OuterModel(user1=user, user2=user)
print(outer_model.model_dump(serialize_as_any=True))
"""
{
    'user1': {'name': 'pydantic', 'password': 'password'},
    'user2': {'name': 'pydantic', 'password': 'password'},
}
"""

print(outer_model.model_dump(serialize_as_any=False))
#> {'user1': {'name': 'pydantic'}, 'user2': {'name': 'pydantic'}}
```

---

TITLE: Pydantic Handling of `typing.Annotated`
DESCRIPTION: Details Pydantic's support for `typing.Annotated` as per PEP-593, noting that it allows arbitrary metadata but typically only processes a single call to the `Field` function, ignoring other additional metadata.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_33

LANGUAGE: APIDOC
CODE:

```
typing.Annotated:
  Description: Allows wrapping another type with arbitrary metadata, as per [PEP-593](https://www.python.org/dev/peps/pep-0593/).
  Behavior: The `Annotated` hint may contain a single call to the `Field` function, but otherwise the additional metadata is ignored and the root type is used.
```

---

TITLE: Customize Pydantic JSON Schema with `json_schema_extra` Dictionary
DESCRIPTION: This snippet demonstrates how to use the `json_schema_extra` option within Pydantic's `ConfigDict` to add static, extra information to the generated JSON schema. By providing a dictionary, you can include custom fields like 'examples' directly into the schema output for a `BaseModel`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_14

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    a: str

    model_config = ConfigDict(json_schema_extra={'examples': [{'a': 'Foo'}]})


print(json.dumps(Model.model_json_schema(), indent=2))
"""
{
  "examples": [
    {
      "a": "Foo"
    }
  ],
  "properties": {
    "a": {
      "title": "A",
      "type": "string"
    }
  },
  "required": [
    "a"
  ],
  "title": "Model",
  "type": "object"
}
"""
```

---

TITLE: Avoiding Subclasses of Primitives (Bad Example) - Python
DESCRIPTION: This snippet demonstrates an anti-pattern where a custom class directly inherits from a primitive type like `str` and attempts to add extra attributes via `__init__`. This approach is generally discouraged in Pydantic for adding extra information, as it can lead to unexpected behavior and is less performant than using a `BaseModel`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_3

LANGUAGE: python
CODE:

```
class CompletedStr(str):
    def __init__(self, s: str):
        self.s = s
        self.done = False
```

---

TITLE: Pydantic WrapSerializer Class
DESCRIPTION: A functional serializer that receives the raw inputs along with a handler function. This handler applies the standard serialization logic, allowing the `WrapSerializer` to modify the resulting value before returning it as the final output.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_9

LANGUAGE: APIDOC
CODE:

```
WrapSerializer(func: Callable, return_type: Any = None, when_used: Literal['always', 'unless-none', 'json', 'json-unless-none'] = 'always')
  func: The wrapping serialization function. It receives the raw value and a handler function.
  return_type: Specifies the return type for the function. If omitted, it's inferred from the type annotation.
  when_used: Specifies when this serializer should be used. Accepts 'always', 'unless-none', 'json', and 'json-unless-none'. Defaults to 'always'.
```

---

TITLE: Pydantic Timedelta Field Handling with `datetime.timedelta`
DESCRIPTION: This snippet illustrates Pydantic's support for `datetime.timedelta` fields, including parsing from ISO 8601 duration strings. It demonstrates how a string representing a duration is automatically converted into a `timedelta` object, correctly calculating the total days and seconds.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_4

LANGUAGE: python
CODE:

```
from datetime import timedelta

from pydantic import BaseModel


class Model(BaseModel):
    td: timedelta = None


m = Model(td='P3DT12H30M5S')

print(m.model_dump())
```

---

TITLE: Pickling Pydantic Models for Serialization
DESCRIPTION: Demonstrates how Pydantic models can be serialized into a byte stream using Python's `pickle.dumps` and deserialized back into model instances using `pickle.loads`, showcasing their compatibility with standard Python pickling.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_18

LANGUAGE: python
CODE:

```
import pickle

from pydantic import BaseModel


class FooBarModel(BaseModel):
    a: str
    b: int


m = FooBarModel(a='hello', b=123)
print(m)
#> a='hello' b=123
data = pickle.dumps(m)
print(data[:20])
#> b'\x80\x04\x95\x95\x00\x00\x00\x00\x00\x00\x00\x8c\x08__main_'
m2 = pickle.loads(data)
print(m2)
#> a='hello' b=123
```

---

TITLE: Handle Pydantic V2 field_validator Signature Error
DESCRIPTION: This snippet illustrates a `PydanticUserError` (code 'validator-signature') triggered by an incorrect signature for a `field_validator` function in Pydantic V2. The example shows a `field_validator` decorated method that incorrectly omits the `value` parameter.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_30

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError, field_validator

try:

    class Model(BaseModel):
        a: str

        @field_validator('a')
        @classmethod
        def check_a(cls):
            return 'a'

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-signature'
```

---

TITLE: Pydantic Error: Model Parent Field Overridden
DESCRIPTION: This error is raised when a field defined on a base Pydantic model class is unintentionally overridden by a non-annotated attribute in a subclass. The example demonstrates how defining 'a = 123.0' in 'Bar' overrides 'a: float' from 'Foo', leading to this error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_14

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError


class Foo(BaseModel):
    a: float


try:

    class Bar(Foo):
        x: float = 12.3
        a = 123.0

except PydanticUserError as exc_info:
    assert exc_info.code == 'model-field-overridden'
```

---

TITLE: Handle Pydantic datetime_future Validation Error
DESCRIPTION: This error is raised when a `FutureDatetime` field receives an input value that is not in the future relative to the current date and time.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_20

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import BaseModel, FutureDatetime, ValidationError


class Model(BaseModel):
    x: FutureDatetime


try:
    Model(x=datetime(2000, 1, 1))
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'datetime_future'
```

---

TITLE: Pydantic Dataclass: Disallowing `extra='allow'` with `init=False` Fields
DESCRIPTION: Pydantic dataclasses do not permit the `extra='allow'` configuration when any field has `init=False`. This combination leads to a `PydanticUserError` during schema building, as it creates an ambiguous state for initialization and extra field handling.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_40

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


@dataclass(config=ConfigDict(extra='allow'))
class A:
    a: int = Field(init=False, default=1)
```

---

TITLE: Enabling Pydantic Mypy Plugin in mypy.ini - INI
DESCRIPTION: Shows how to enable the Pydantic Mypy plugin by adding `pydantic.mypy` to the `plugins` list in the `[mypy]` section of a `mypy.ini` configuration file.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/mypy.md#_snippet_1

LANGUAGE: ini
CODE:

```
[mypy]
plugins = pydantic.mypy
```

---

TITLE: Pydantic Model Validation by Attribute Name (Runtime)
DESCRIPTION: Shows how to validate a Pydantic model using attribute names at runtime by setting `by_name=True` on validation methods like `model_validate()`. This overrides the default alias-based validation, allowing input to match the attribute name.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/alias.md#_snippet_13

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Model(BaseModel):
    my_field: str = Field(validation_alias='my_alias')


m = Model.model_validate(
    {'my_field': 'foo'}, by_alias=False, by_name=True  # (1)!
)
print(repr(m))
#> Model(my_field='foo')
```

---

TITLE: Handle Pydantic date_parsing Validation Error for JSON
DESCRIPTION: This error is raised when validating JSON data where the input string for a `date` field cannot be parsed into a valid date, especially when `strict=True` is applied to the field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_16

LANGUAGE: python
CODE:

```
import json
from datetime import date

from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: date = Field(strict=True)


try:
    Model.model_validate_json(json.dumps({'x': '1'}))
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'date_parsing'
```

---

TITLE: Handle Pydantic date_from_datetime_parsing Validation Error
DESCRIPTION: This error is raised when a string input value cannot be successfully parsed into a `date` field, indicating an invalid date string format.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_14

LANGUAGE: python
CODE:

```
from datetime import date

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: date


try:
    Model(x='XX1494012000')
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'date_from_datetime_parsing'
```

---

TITLE: Pydantic Strict Field Validation During Model Instantiation
DESCRIPTION: Shows that setting `strict=True` on a `Field` also affects validation when directly instantiating the `BaseModel` class, not just when using validation methods.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/strict_mode.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: int = Field(strict=True)
    y: int = Field(strict=False)


try:
    Model(x='1', y='2')
except ValidationError as exc:
    print(exc)
    """
    1 validation error for Model
    x
      Input should be a valid integer [type=int_type, input_value='1', input_type=str]
    """
```

---

TITLE: Validate Pydantic Tuple Types with Mixed Generics
DESCRIPTION: This example illustrates Pydantic's handling of `tuple` types, including simple tuples and tuples with specific type annotations for each element. It demonstrates how Pydantic validates and casts input values to the defined tuple element types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_9

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):
    simple_tuple: Optional[tuple] = None
    tuple_of_different_types: Optional[tuple[int, float, bool]] = None


print(Model(simple_tuple=[1, 2, 3, 4]).simple_tuple)
print(Model(tuple_of_different_types=[3, 2, 1]).tuple_of_different_types)
```

---

TITLE: Pydantic: Reproduce 'class-not-fully-defined' with Post-Definition
DESCRIPTION: Illustrates the 'class-not-fully-defined' error when a type is used in a `BaseModel` annotation before its actual definition, showing that Pydantic fails validation until the type is fully defined.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_1

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel, PydanticUserError


class Foo(BaseModel):
    a: Optional['Bar'] = None


try:
    # this doesn't work, see raised error
    foo = Foo(a={'b': {'a': None}})
except PydanticUserError as exc_info:
    assert exc_info.code == 'class-not-fully-defined'


class Bar(BaseModel):
    b: 'Foo'


# this works, though
foo = Foo(a={'b': {'a': None}})
```

---

TITLE: Handle Pydantic date_type Validation Error
DESCRIPTION: This error is raised when the input value's type is not valid for a `date` field. It also occurs for strict fields if the input is not an instance of `date`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_18

LANGUAGE: python
CODE:

```
from datetime import date

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: date


try:
    Model(x=None)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'date_type'
```

---

TITLE: Modifying Pydantic Model Fields (Python)
DESCRIPTION: Illustrates that Pydantic models are mutable by default, allowing field values to be changed directly via attribute assignment after instantiation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_4

LANGUAGE: python
CODE:

```
user.id = 321
assert user.id == 321
```

---

TITLE: Handle Pydantic `timezone_aware` Datetime Error
DESCRIPTION: This error is raised when a `datetime` value provided for a timezone-aware `datetime` field lacks timezone information. The example demonstrates how to trigger this error by passing a naive datetime to an `AwareDatetime` field.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_82

LANGUAGE: python
CODE:

```
from datetime import datetime

from pydantic import AwareDatetime, BaseModel, ValidationError


class Model(BaseModel):
    x: AwareDatetime


try:
    Model(x=datetime.now())
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'timezone_aware'
```

---

TITLE: Pydantic Error: Undefined Annotation
DESCRIPTION: This error is raised when Pydantic encounters an undefined type annotation during 'CoreSchema' generation, typically due to a forward reference that cannot be resolved. The example shows a forward reference to an undefined type 'B'.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_21

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUndefinedAnnotation


class Model(BaseModel):
    a: 'B'  # noqa F821


try:
    Model.model_rebuild()
except PydanticUndefinedAnnotation as exc_info:
    assert exc_info.code == 'undefined-annotation'
```

---

TITLE: Pydantic Performance Comparison for JSON and URL Validation
DESCRIPTION: This example compares the performance of Pydantic's `TypeAdapter` for JSON parsing and URL validation against a pure Python implementation. It demonstrates Pydantic's significant speed advantage (over 300% faster) when handling common data validation tasks, leveraging its Rust-implemented core.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/why.md#_snippet_1

LANGUAGE: python
CODE:

```
import json
import timeit
from urllib.parse import urlparse

import requests

from pydantic import HttpUrl, TypeAdapter

reps = 7
number = 100
r = requests.get('https://api.github.com/emojis')
r.raise_for_status()
emojis_json = r.content


def emojis_pure_python(raw_data):
    data = json.loads(raw_data)
    output = {}
    for key, value in data.items():
        assert isinstance(key, str)
        url = urlparse(value)
        assert url.scheme in ('https', 'http')
        output[key] = url


emojis_pure_python_times = timeit.repeat(
    'emojis_pure_python(emojis_json)',
    globals={
        'emojis_pure_python': emojis_pure_python,
        'emojis_json': emojis_json,
    },
    repeat=reps,
    number=number,
)
print(f'pure python: {min(emojis_pure_python_times) / number * 1000:0.2f}ms')
#> pure python: 5.32ms

type_adapter = TypeAdapter(dict[str, HttpUrl])
emojis_pydantic_times = timeit.repeat(
    'type_adapter.validate_json(emojis_json)',
    globals={
        'type_adapter': type_adapter,
        'HttpUrl': HttpUrl,
        'emojis_json': emojis_json,
    },
    repeat=reps,
    number=number,
)
print(f'pydantic: {min(emojis_pydantic_times) / number * 1000:0.2f}ms')
#> pydantic: 1.54ms

print(
    f'Pydantic {min(emojis_pure_python_times) / min(emojis_pydantic_times):0.2f}x faster'
)
#> Pydantic 3.45x faster
```

---

TITLE: Debug Missing Pydantic-Core Module by Checking Package Files
DESCRIPTION: This Python snippet helps diagnose the `no module named pydantic_core._pydantic_core` error by inspecting the installed `pydantic-core` package. It uses `importlib.metadata.files` to list the package's contents, verifying the presence of both the compiled library (e.g., `.so`, `.pyd`) and its type stubs (`.pyi`), which are essential for correct Pydantic operation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/aws_lambda.md#_snippet_1

LANGUAGE: python
CODE:

```
from importlib.metadata import files
print([file for file in files('pydantic-core') if file.name.startswith('_pydantic_core')])
"""
[PackagePath('pydantic_core/_pydantic_core.pyi'), PackagePath('pydantic_core/_pydantic_core.cpython-312-x86_64-linux-gnu.so')]
"""
```

---

TITLE: Enforcing Type Relationships with Nested Generics (Pydantic Python)
DESCRIPTION: Shows nested generic models (`InnerT[T]` inside `OuterT[T]`) using the same type variable `T` to enforce type consistency. Includes a `try...except` block demonstrating validation errors when types mismatch.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_27

LANGUAGE: python
CODE:

```
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar('T')


class InnerT(BaseModel, Generic[T]):
    inner: T


class OuterT(BaseModel, Generic[T]):
    outer: T
    nested: InnerT[T]


nested = InnerT[int](inner=1)
print(OuterT[int](outer=1, nested=nested))
try:
    print(OuterT[int](outer='a', nested=InnerT(inner='a')))
except ValidationError as e:
    print(e)
```

---

TITLE: Excluding Class Variables from Pydantic Fields (Python)
DESCRIPTION: Demonstrates that attributes defined with `typing.ClassVar` are treated as class variables by Pydantic and are not included as model fields on instances.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_48

LANGUAGE: python
CODE:

```
from typing import ClassVar

from pydantic import BaseModel


class Model(BaseModel):
    x: ClassVar[int] = 1

    y: int = 2


m = Model()
print(m)
#> y=2
print(Model.x)
#> 1
```

---

TITLE: Using Any to Skip Validation - Python
DESCRIPTION: This snippet illustrates how to use `typing.Any` in a Pydantic `BaseModel` to explicitly bypass validation for a specific field. This is useful when a value does not require Pydantic's validation and should be kept unchanged, improving performance by avoiding unnecessary processing.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_2

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel


class Model(BaseModel):
    a: Any


model = Model(a=1)
```

---

TITLE: Using Pydantic Models with Python ABCs (Python)
DESCRIPTION: Shows how to combine Pydantic models with Python's `abc.ABC` to create abstract base classes that also function as Pydantic models, including defining abstract methods.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_46

LANGUAGE: python
CODE:

```
import abc

from pydantic import BaseModel


class FooBarModel(BaseModel, abc.ABC):
    a: str
    b: int

    @abc.abstractmethod
    def my_abstract_method(self):
        pass
```

---

TITLE: Pydantic: Configuring TypeAdapter with BaseModel, TypedDict, or Dataclass
DESCRIPTION: This error occurs when attempting to pass a `config` argument directly to `TypeAdapter` for types like `BaseModel`, `TypedDict`, or `dataclass` that manage their own configuration. The configuration must be set directly on the type itself, not via `TypeAdapter`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_37

LANGUAGE: python
CODE:

```
from typing_extensions import TypedDict

from pydantic import ConfigDict, PydanticUserError, TypeAdapter


class MyTypedDict(TypedDict):
    x: int


try:
    TypeAdapter(MyTypedDict, config=ConfigDict(strict=True))
except PydanticUserError as exc_info:
    assert exc_info.code == 'type-adapter-config-unused'
```

LANGUAGE: python
CODE:

```
from typing_extensions import TypedDict

from pydantic import ConfigDict, TypeAdapter


class MyTypedDict(TypedDict):
    x: int

    # or `model_config = ...` for BaseModel
    __pydantic_config__ = ConfigDict(strict=True)


TypeAdapter(MyTypedDict)  # ok
```

---

TITLE: Pydantic Cyclic Reference Detection in Validation
DESCRIPTION: Demonstrates Pydantic's ability to detect and handle cyclic references during model validation, preventing `RecursionError` and instead raising a specific `ValidationError`. The example defines two mutually recursive models and shows how a cyclic data structure triggers the `recursion_loop` error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/forward_annotations.md#_snippet_2

LANGUAGE: python
CODE:

```
from typing import Optional

from pydantic import BaseModel, ValidationError


class ModelA(BaseModel):
    b: 'Optional[ModelB]' = None


class ModelB(BaseModel):
    a: Optional[ModelA] = None


cyclic_data = {}
cyclic_data['a'] = {'b': cyclic_data}
print(cyclic_data)
#> {'a': {'b': {...}}}

try:
    ModelB.model_validate(cyclic_data)
except ValidationError as exc:
    print(exc)
    """
    1 validation error for ModelB
    a.b
      Recursion error - cyclic reference detected [type=recursion_loop, input_value={'a': {'b': {...}}}, input_type=dict]
    """
```

---

TITLE: Install datamodel-code-generator
DESCRIPTION: This command installs the datamodel-code-generator library using pip, the Python package installer. It ensures the utility is available in your environment for generating Pydantic models.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/datamodel_code_generator.md#_snippet_0

LANGUAGE: bash
CODE:

```
pip install datamodel-code-generator
```

---

TITLE: Workaround Pydantic Discriminator Validator Error with Union
DESCRIPTION: Provides a workaround for the `discriminator-validator` error by using a standard `Union` instead of a discriminator. This approach allows custom validation logic on the field without interfering with Pydantic's internal type determination for discriminated unions.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_12

LANGUAGE: python
CODE:

```
from typing import Literal, Union

from pydantic import BaseModel, field_validator


class Cat(BaseModel):
    pet_type: Literal['cat']

    @field_validator('pet_type', mode='before')
    @classmethod
    def validate_pet_type(cls, v):
        if v == 'kitten':
            return 'cat'
        return v


class Dog(BaseModel):
    pet_type: Literal['dog']


class Model(BaseModel):
    pet: Union[Cat, Dog]


assert Model(pet={'pet_type': 'kitten'}).pet.pet_type == 'cat'
```

---

TITLE: Pydantic Validation Error Output Example
DESCRIPTION: Shows the typical format of the output printed by a Pydantic `ValidationError`, detailing the model, field, error type, input value, and input type.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_18

LANGUAGE: text
CODE:

```
1 validation error for Model
a
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not an int', input_type=str]
```

---

TITLE: Extending Base Model with create_model - Pydantic Python
DESCRIPTION: Shows how to create a new Pydantic model dynamically using `create_model` that inherits fields from an existing `BaseModel` by using the `__base__` argument, effectively extending the base model with additional fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_40

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, create_model


class FooModel(BaseModel):
    foo: str
    bar: int = 123


BarModel = create_model(
    'BarModel',
    apple=(str, 'russet'),
    banana=(str, 'yellow'),
    __base__=FooModel,
)
print(BarModel)
#> <class '__main__.BarModel'>
print(BarModel.model_fields.keys())
#> dict_keys(['foo', 'bar', 'apple', 'banana'])
```

---

TITLE: Python: Reference Example for Class Annotation Resolution
DESCRIPTION: This simple Python module serves as a reference for understanding how Pydantic resolves annotations at class definition time. It defines a type alias `MyType` and a `Base` class with a forward-referenced annotation `f1: 'MyType'`, illustrating a common pattern for annotation evaluation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/resolving_annotations.md#_snippet_2

LANGUAGE: python
CODE:

```
# module1.py:
type MyType = int

class Base:
    f1: 'MyType'
```

---

TITLE: Handle PydanticUserError for Overlapping TypedDict Unpack Fields in Python
DESCRIPTION: This snippet demonstrates how Pydantic raises a `PydanticUserError` when a `TypedDict` used for variadic keyword parameters (`**kwargs: Unpack[TD]`) has field names that overlap with other function parameters. It shows catching the specific `overlapping-unpack-typed-dict` error code.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_50

LANGUAGE: python
CODE:

```
from typing_extensions import TypedDict, Unpack

from pydantic import PydanticUserError, validate_call


class TD(TypedDict):
    a: int


try:

    @validate_call
    def func(a: int, **kwargs: Unpack[TD]):
        pass

except PydanticUserError as exc_info:
    assert exc_info.code == 'overlapping-unpack-typed-dict'
```

---

TITLE: API Reference for Pydantic Dataclass Decorator
DESCRIPTION: This section provides API documentation for the `@pydantic.dataclasses.dataclass` decorator, which enables Pydantic's data validation features on standard Python dataclasses. It serves as an alternative to `BaseModel` for data validation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_0

LANGUAGE: APIDOC
CODE:

```
pydantic.dataclasses.dataclass:
  Decorator to add Pydantic validation to standard Python dataclasses.
```

---

TITLE: Pydantic Dataclass Model Validators and Post-Initialization Hooks
DESCRIPTION: Illustrates the execution order of `@model_validator` (both `before` and `after` modes) and the `__post_init__` method in a Pydantic dataclass, showing how `ArgsKwargs` is used for `before` validators.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/dataclasses.md#_snippet_10

LANGUAGE: python
CODE:

```
from pydantic_core import ArgsKwargs
from typing_extensions import Self

from pydantic import model_validator
from pydantic.dataclasses import dataclass


@dataclass
class Birth:
    year: int
    month: int
    day: int


@dataclass
class User:
    birth: Birth

    @model_validator(mode='before')
    @classmethod
    def before(cls, values: ArgsKwargs) -> ArgsKwargs:
        print(f'First: {values}')  # (1)!
        """
        First: ArgsKwargs((), {'birth': {'year': 1995, 'month': 3, 'day': 2}})
        """
        return values

    @model_validator(mode='after')
    def after(self) -> Self:
        print(f'Third: {self}')
        # Third: User(birth=Birth(year=1995, month=3, day=2))
        return self

    def __post_init__(self):
        print(f'Second: {self.birth}')
        # Second: Birth(year=1995, month=3, day=2)


user = User(**{'birth': {'year': 1995, 'month': 3, 'day': 2}})
```

---

TITLE: Pydantic V1 vs V2: `model_dump_json()` Output Compactness and `json.dumps()` Alignment
DESCRIPTION: This Python code illustrates how Pydantic V2's `model_dump_json()` produces compacted JSON output compared to Pydantic V1's `json()` and standard `json.dumps()`. It also shows how to modify `json.dumps()` separators to match the compacted output of `model_dump_json()`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_11

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel as V2BaseModel
from pydantic.v1 import BaseModel as V1BaseModel


class V1Model(V1BaseModel):
    a: list[str]


class V2Model(V2BaseModel):
    a: list[str]


v1_model = V1Model(a=['fancy', 'sushi'])
v2_model = V2Model(a=['fancy', 'sushi'])

# V1
print(v1_model.json())
#> {"a": ["fancy", "sushi"]}

# V2
print(v2_model.model_dump_json())
#> {"a":["fancy","sushi"]}

# Plain json.dumps
print(json.dumps(v2_model.model_dump()))
#> {"a": ["fancy", "sushi"]}

# Modified json.dumps
print(json.dumps(v2_model.model_dump(), separators=(',', ':')))
#> {"a":["fancy","sushi"]}
```

---

TITLE: Implementing FailFast Validation with Pydantic TypeAdapter (Python)
DESCRIPTION: This snippet demonstrates how to use the `FailFast` annotation with Pydantic's `TypeAdapter` to stop validation immediately upon the first error in a sequence. It shows validating a list of booleans where an invalid item triggers an early `ValidationError`, preventing further checks on subsequent items. This approach trades full error visibility for improved performance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/performance.md#_snippet_7

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import FailFast, TypeAdapter, ValidationError

ta = TypeAdapter(Annotated[list[bool], FailFast()])
try:
    ta.validate_python([True, 'invalid', False, 'also invalid'])
except ValidationError as exc:
    print(exc)
    """
    1 validation error for list[bool]
    1
      Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='invalid', input_type=str]
    """
```

---

TITLE: Validating Keyword Parameters with Unpack and TypedDict in Pydantic
DESCRIPTION: This example illustrates how to use `typing.Unpack` with `TypedDict` to annotate variable keyword parameters (`**kwargs`) for validation by `pydantic.validate_call`, allowing for structured validation of dictionary-like arguments.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/validation_decorator.md#_snippet_3

LANGUAGE: Python
CODE:

```
from typing_extensions import TypedDict, Unpack

from pydantic import validate_call


class Point(TypedDict):
    x: int
    y: int


@validate_call
def add_coords(**kwargs: Unpack[Point]) -> int:
    return kwargs['x'] + kwargs['y']


add_coords(x=1, y=2)
```

---

TITLE: Install Pydantic for AWS Lambda with pip
DESCRIPTION: This `pip install` command is tailored for AWS Lambda environments, ensuring `pydantic` is installed with platform-compatible binary wheels. It specifies the target directory, CPython implementation, and Python version, making it suitable for packaging dependencies in .zip files or Lambda Layers.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/aws_lambda.md#_snippet_0

LANGUAGE: Bash
CODE:

```
pip install \
    --platform manylinux2014_x86_64 \
    --target=<your_package_dir> \
    --implementation cp \
    --python-version 3.10 \
    --only-binary=:all: \
    --upgrade pydantic
```

---

TITLE: Adding Validators with create_model - Pydantic Python
DESCRIPTION: Illustrates how to add custom field validators to a dynamically created Pydantic model using the `__validators__` argument and the `field_validator` decorator. Includes an example of successful validation and handling a validation failure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_41

LANGUAGE: python
CODE:

```
from pydantic import ValidationError, create_model, field_validator


def alphanum(cls, v):
    assert v.isalnum(), 'must be alphanumeric'
    return v


validators = {
    'username_validator': field_validator('username')(alphanum)  # (1)!
}

UserModel = create_model(
    'UserModel', username=(str, ...), __validators__=validators
)

user = UserModel(username='scolvin')
print(user)
#> username='scolvin'

try:
    UserModel(username='scolvi%n')
except ValidationError as e:
    print(e)
    """
    1 validation error for UserModel
    username
      Assertion failed, must be alphanumeric [type=assertion_error, input_value='scolvi%n', input_type=str]
    """
```

---

TITLE: Define Pydantic BaseModel with Strict Boolean Field
DESCRIPTION: This Python code defines a Pydantic `BaseModel` named `Model` with a single field `foo` of type `bool`. The `Field(strict=True)` ensures strict boolean validation for this field, demonstrating how Pydantic models are defined before core schema generation.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/architecture.md#_snippet_1

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field


class Model(BaseModel):
    foo: bool = Field(strict=True)
```

---

TITLE: Pydantic BaseModel field serialization with subclass instances
DESCRIPTION: Explains Pydantic's behavior when a `BaseModel` field is annotated with a superclass type but instantiated with a subclass. It demonstrates that only fields defined in the _annotated_ type are included in the dumped output, ensuring predictable serialization and preventing unintended data exposure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_13

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class User(BaseModel):
    name: str


class UserLogin(User):
    password: str


class OuterModel(BaseModel):
    user: User


user = UserLogin(name='pydantic', password='hunter2')

m = OuterModel(user=user)
print(m)
#> user=UserLogin(name='pydantic', password='hunter2')
print(m.model_dump())  # note: the password field is not included
#> {'user': {'name': 'pydantic'}}
```

---

TITLE: Subclassing Parametrized Generics for isinstance (Pydantic Python)
DESCRIPTION: Provides an example of subclassing a parametrized generic model (`MyGenericModel[int]`) to create a concrete type (`MyIntModel`) that can be reliably used in `isinstance` checks, as recommended by Pydantic.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_28

LANGUAGE: python
CODE:

```
class MyIntModel(MyGenericModel[int]): ...

isinstance(my_model, MyIntModel)
```

---

TITLE: Ignoring Flake8 Pydantic Rules (INI)
DESCRIPTION: This configuration snippet demonstrates how to ignore specific flake8-pydantic rules (e.g., PYD001, PYD002) within your Flake8 configuration file. By adding rule codes to the 'extend-ignore' option under the '[flake8]' section, you can customize which linting errors are reported.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/linting.md#_snippet_1

LANGUAGE: ini
CODE:

```
[flake8]
extend-ignore = PYD001,PYD002
```

---

TITLE: Handle Pydantic `extra_forbidden` Validation Error
DESCRIPTION: This error is raised when the input value contains extra fields, but `model_config['extra'] == 'forbid'`. It indicates that the model configuration explicitly disallows additional fields not defined in the schema.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_32

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    x: str

    model_config = ConfigDict(extra='forbid')


try:
    Model(x='test', y='test')
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'extra_forbidden'
```

---

TITLE: Handle Missing Fields with Default Values in Partial JSON Parsing
DESCRIPTION: Provides an advanced example demonstrating how to use a custom `WrapValidator` (`default_on_error`) to set default values for fields that are missing due to partial JSON parsing. This prevents `ValidationError` for missing fields, allowing successful model validation even with truncated input.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json.md#_snippet_5

LANGUAGE: python
CODE:

```
from typing import Annotated, Any, Optional

import pydantic_core

from pydantic import BaseModel, ValidationError, WrapValidator


def default_on_error(v, handler) -> Any:
    """
    Raise a PydanticUseDefault exception if the value is missing.

    This is useful for avoiding errors from partial
    JSON preventing successful validation.
    """
    try:
        return handler(v)
    except ValidationError as exc:
        # there might be other types of errors resulting from partial JSON parsing
        # that you allow here, feel free to customize as needed
        if all(e['type'] == 'missing' for e in exc.errors()):
            raise pydantic_core.PydanticUseDefault()
        else:
            raise


class NestedModel(BaseModel):
    x: int
    y: str


class MyModel(BaseModel):
    foo: Optional[str] = None
    bar: Annotated[
        Optional[tuple[str, int]], WrapValidator(default_on_error)
    ] = None
    nested: Annotated[
        Optional[NestedModel], WrapValidator(default_on_error)
    ] = None


m = MyModel.model_validate(
    pydantic_core.from_json('{"foo": "x", "bar": ["world",', allow_partial=True)
)
print(repr(m))
# > MyModel(foo='x', bar=None, nested=None)


m = MyModel.model_validate(
    pydantic_core.from_json(
        '{"foo": "x", "bar": ["world", 1], "nested": {"x":', allow_partial=True
    )
)
print(repr(m))
# > MyModel(foo='x', bar=('world', 1), nested=None)
```

---

TITLE: Pydantic: Resolving Unevaluable Type Annotation Conflicts
DESCRIPTION: This error arises when a type annotation's name clashes with a field name, leading to evaluation issues because annotations are processed after assignments. A `PydanticUserError` is raised to prevent unexpected behavior. Workarounds include aliasing the import or changing the import statement.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_39

LANGUAGE: python
CODE:

```
from datetime import date

from pydantic import BaseModel, Field


class Model(BaseModel):
    date: date = Field(description='A date')
```

LANGUAGE: python
CODE:

```
import datetime
# Or `from datetime import date as _date`

from pydantic import BaseModel, Field


class Model(BaseModel):
    date: datetime.date = Field(description='A date')
```

---

TITLE: Handle Pydantic union_tag_not_found Error
DESCRIPTION: This error is raised when Pydantic cannot extract a discriminator value from the input for a Union field, typically because the expected discriminator key is missing. The provided code illustrates a discriminated union and shows how this error occurs when the `pet_type` field, designated as the discriminator, is absent from the input data.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_90

LANGUAGE: python
CODE:

```
from typing import Literal, Union

from pydantic import BaseModel, Field, ValidationError


class BlackCat(BaseModel):
    pet_type: Literal['blackcat']


class WhiteCat(BaseModel):
    pet_type: Literal['whitecat']


class Model(BaseModel):
    cat: Union[BlackCat, WhiteCat] = Field(discriminator='pet_type')


try:
    Model(cat={'name': 'blackcat'})
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'union_tag_not_found'
```

---

TITLE: Define Named Type Alias with TypeAliasType (Python 3.9+)
DESCRIPTION: Demonstrates defining a named type alias `PositiveIntList` using `typing_extensions.TypeAliasType` for Python versions 3.9 and above. Shows how it's used in a Pydantic model and the resulting JSON schema with a `$defs` entry, preventing definition duplication.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_4

LANGUAGE: python
CODE:

```
from typing import Annotated

from annotated_types import Gt
from typing_extensions import TypeAliasType

from pydantic import BaseModel

PositiveIntList = TypeAliasType('PositiveIntList', list[Annotated[int, Gt(0)]])


class Model(BaseModel):
    x: PositiveIntList
    y: PositiveIntList


print(Model.model_json_schema())
```

LANGUAGE: json
CODE:

```
{
    '$defs': {
        'PositiveIntList': {
            'items': {'exclusiveMinimum': 0, 'type': 'integer'},
            'type': 'array'
        }
    },
    'properties': {
        'x': {'$ref': '#/$defs/PositiveIntList'},
        'y': {'$ref': '#/$defs/PositiveIntList'}
    },
    'required': ['x', 'y'],
    'title': 'Model',
    'type': 'object'
}
```

---

TITLE: Validate Nested Pydantic Model Fields with Context-Based Field Validator
DESCRIPTION: Illustrates an alternative method for validating nested model fields using a @field_validator within the nested model itself. It shows how to pass data from the parent model (e.g., forbidden passwords) into the nested validator via the ValidationInfo.context, allowing for context-aware validation. A warning is included about potential complexity.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/examples/custom_validators.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator


class User(BaseModel):
    username: str
    password: str

    @field_validator('password', mode='after')
    @classmethod
    def validate_user_passwords(
        cls, password: str, info: ValidationInfo
    ) -> str:
        """Check that user password is not in forbidden list."""
        forbidden_passwords = (
            info.context.get('forbidden_passwords', []) if info.context else []
        )
        if password in forbidden_passwords:
            raise ValueError(f'Password {password} is forbidden.')
        return password


class Organization(BaseModel):
    forbidden_passwords: list[str]
    users: list[User]

    @field_validator('forbidden_passwords', mode='after')
    @classmethod
    def add_context(cls, v: list[str], info: ValidationInfo) -> list[str]:
        if info.context is not None:
            info.context.update({'forbidden_passwords': v})
        return v


data = {
    'forbidden_passwords': ['123'],
    'users': [
        {'username': 'Spartacat', 'password': '123'},
        {'username': 'Iceburgh', 'password': '87'},
    ],
}

try:
    org = Organization.model_validate(data, context={})
except ValidationError as e:
    print(e)
    """
    1 validation error for Organization
    users.0.password
      Value error, Password 123 is forbidden. [type=value_error, input_value='123', input_type=str]
    """

```

---

TITLE: Merge `json_schema_extra` from Annotated Types in Pydantic v2.9+
DESCRIPTION: This snippet demonstrates the additive merging behavior of `json_schema_extra` dictionaries when used with `Annotated` types in Pydantic v2.9 and later. It shows how `json_schema_extra` definitions from multiple nested `Field` annotations are combined into a single, unified schema, resolving previous override behaviors.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_16

LANGUAGE: python
CODE:

```
import json
from typing import Annotated

from typing_extensions import TypeAlias

from pydantic import Field, TypeAdapter

ExternalType: TypeAlias = Annotated[
    int, Field(json_schema_extra={'key1': 'value1'})
]

ta = TypeAdapter(
    Annotated[ExternalType, Field(json_schema_extra={'key2': 'value2'})]
)
print(json.dumps(ta.json_schema(), indent=2))
"""
{
  "key1": "value1",
  "key2": "value2",
  "type": "integer"
}
"""
```

---

TITLE: Marking a Required Field with Ellipsis and Field()
DESCRIPTION: Illustrates using the ellipsis (`...`) as the first argument to `Field` to indicate that a field is required and has no default value, while still applying other constraints like `frozen=True`. Note that this usage is discouraged due to static type checker compatibility issues.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/fields.md#_snippet_1

LANGUAGE: python
CODE:

```
class Model(BaseModel):
    name: str = Field(..., frozen=True)
```

---

TITLE: Deferring and Rebuilding TypeAdapter Schemas
DESCRIPTION: This example shows how to initialize a `TypeAdapter` with `defer_build=True` to postpone schema generation, which is beneficial for types with forward references or expensive schema builds. It also demonstrates how to manually trigger the schema build using the `rebuild` method.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/type_adapter.md#_snippet_3

LANGUAGE: python
CODE:

```
from pydantic import ConfigDict, TypeAdapter

ta = TypeAdapter('MyInt', config=ConfigDict(defer_build=True))

```

---

TITLE: Pydantic Time Field Handling with `datetime.time`
DESCRIPTION: This example demonstrates how Pydantic handles `datetime.time` fields, accepting existing `time` objects. It shows the direct assignment of a `time` object to a model field and how Pydantic correctly serializes it when dumping the model, preserving the time components.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_3

LANGUAGE: python
CODE:

```
from datetime import time

from pydantic import BaseModel


class Meeting(BaseModel):
    t: time = None


m = Meeting(t=time(4, 8, 16))

print(m.model_dump())
```

---

TITLE: Handle Pydantic Callable Discriminator No Tag Error
DESCRIPTION: Illustrates the `callable-discriminator-no-tag` error in Pydantic, which occurs when a `Union` using a callable `Discriminator` lacks `Tag` annotations for all its cases. The snippet provides multiple scenarios demonstrating how missing tags lead to a `PydanticUserError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_13

LANGUAGE: python
CODE:

```
from typing import Annotated, Union

from pydantic import BaseModel, Discriminator, PydanticUserError, Tag


def model_x_discriminator(v):
    if isinstance(v, str):
        return 'str'
    if isinstance(v, (dict, BaseModel)):
        return 'model'


# tag missing for both union choices
try:

    class DiscriminatedModel(BaseModel):
        x: Annotated[
            Union[str, 'DiscriminatedModel'],
            Discriminator(model_x_discriminator),
        ]

except PydanticUserError as exc_info:
    assert exc_info.code == 'callable-discriminator-no-tag'

# tag missing for `'DiscriminatedModel'` union choice
try:

    class DiscriminatedModel(BaseModel):
        x: Annotated[
            Union[Annotated[str, Tag('str')], 'DiscriminatedModel'],
            Discriminator(model_x_discriminator),
        ]

except PydanticUserError as exc_info:
    assert exc_info.code == 'callable-discriminator-no-tag'

# tag missing for `str` union choice
try:

    class DiscriminatedModel(BaseModel):
        x: Annotated[
            Union[str, Annotated['DiscriminatedModel', Tag('model')]],
            Discriminator(model_x_discriminator),
        ]

except PydanticUserError as exc_info:
    assert exc_info.code == 'callable-discriminator-no-tag'
```

---

TITLE: Comprehensive Pydantic Partial Validation Examples with TypeAdapter
DESCRIPTION: This extensive example demonstrates Pydantic's `experimental_allow_partial` flag across various scenarios using `TypeAdapter.validate_json()` and `TypeAdapter.validate_python()`. It defines a `Foobar` TypedDict with required and optional fields, showcasing how incomplete JSON and Python objects are processed, including cases where fields are omitted due to validation failures or incompleteness, and the distinct behavior of the `'trailing-strings'` mode.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/experimental.md#_snippet_8

LANGUAGE: python
CODE:

```
from typing import Annotated

from annotated_types import MinLen
from typing_extensions import NotRequired, TypedDict

from pydantic import TypeAdapter


class Foobar(TypedDict):  # (1)!
    a: int
    b: NotRequired[float]
    c: NotRequired[Annotated[str, MinLen(5)]]


ta = TypeAdapter(list[Foobar])

v = ta.validate_json('[{"a": 1, "b"', experimental_allow_partial=True)  # (2)!
print(v)
#> [{'a': 1}]

v = ta.validate_json(
    '[{"a": 1, "b": 1.0, "c": "abcd', experimental_allow_partial=True  # (3)!
)
print(v)
#> [{'a': 1, 'b': 1.0}]

v = ta.validate_json(
    '[{"b": 1.0, "c": "abcde"', experimental_allow_partial=True  # (4)!
)
print(v)
#> []

v = ta.validate_json(
    '[{"a": 1, "b": 1.0, "c": "abcde"},{"a": ', experimental_allow_partial=True
)
print(v)
#> [{'a': 1, 'b': 1.0, 'c': 'abcde'}]

v = ta.validate_python([{'a': 1}], experimental_allow_partial=True)  # (5)!
print(v)
#> [{'a': 1}]

v = ta.validate_python(
    [{'a': 1, 'b': 1.0, 'c': 'abcd'}], experimental_allow_partial=True  # (6)!
)
print(v)
#> [{'a': 1, 'b': 1.0}]

v = ta.validate_json(
    '[{"a": 1, "b": 1.0, "c": "abcdefg',
    experimental_allow_partial='trailing-strings',  # (7)!
)
print(v)
#> [{'a': 1, 'b': 1.0, 'c': 'abcdefg'}]
```

---

TITLE: Pydantic V2: Custom Validator to Preserve Input Type for Generic Collections
DESCRIPTION: This example provides a custom `restore_input_type` validator using `WrapValidator` and `Annotated` to explicitly preserve the original input type for generic collections. This demonstrates a workaround for the default V2 behavior where input types are not always preserved.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/migration.md#_snippet_18

LANGUAGE: python
CODE:

```
from typing import Annotated, Any, Mapping, TypeVar

from pydantic import (
    TypeAdapter,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)


def restore_input_type(
    value: Any, handler: ValidatorFunctionWrapHandler, _info: ValidationInfo
) -> Any:
    return type(value)(handler(value))


T = TypeVar('T')
PreserveType = Annotated[T, WrapValidator(restore_input_type)]


ta = TypeAdapter(PreserveType[Mapping[str, int]])


class MyDict(dict):
    pass


v = ta.validate_python(MyDict())
assert type(v) is MyDict
```

---

TITLE: Pydantic GenerateJsonSchema API Reference
DESCRIPTION: Provides API documentation for the `pydantic.json_schema.GenerateJsonSchema` class. This class is the core mechanism for customizing JSON schema generation, allowing users to override specific methods to alter the schema output.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/json_schema.md#_snippet_29

LANGUAGE: APIDOC
CODE:

```
pydantic.json_schema.GenerateJsonSchema
  Description: Base class for customizing JSON schema generation.
  Methods: Implements methods for translating pydantic-core schema into JSON schema, designed for easy overriding in subclasses.
```

---

TITLE: Generated Pydantic Models from JSON Schema
DESCRIPTION: This Python code represents the Pydantic models automatically generated by datamodel-code-generator from the provided `person.json` JSON Schema. It includes `Pet` and `Person` models with type hints, default values, and field descriptions derived from the schema, demonstrating type-safe data structures for Python applications.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/datamodel_code_generator.md#_snippet_3

LANGUAGE: python
CODE:

```
# generated by datamodel-codegen:
#   filename:  person.json
#   timestamp: 2020-05-19T15:07:31+00:00
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, conint


class Pet(BaseModel):
    name: str | None = None
    age: int | None = None


class Person(BaseModel):
    first_name: str = Field(description="The person's first name.")
    last_name: str = Field(description="The person's last name.")
    age: conint(ge=0) | None = Field(None, description='Age in years.')
    pets: list[Pet] | None = None
    comment: Any | None = None
```

---

TITLE: Preserving Field Order in Pydantic Models (Python)
DESCRIPTION: Illustrates how Pydantic preserves the order of fields as defined in the model class. Shows this preservation in `model_fields.keys()`, `model_dump()`, and the order of errors in `ValidationError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_47

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    a: int
    b: int = 2
    c: int = 1
    d: int = 0
    e: float


print(Model.model_fields.keys())
#> dict_keys(['a', 'b', 'c', 'd', 'e'])
m = Model(e=2, a=1)
print(m.model_dump())
#> {'a': 1, 'b': 2, 'c': 1, 'd': 0, 'e': 2.0}
try:
    Model(a='x', b='x', c='x', d='x', e='x')
except ValidationError as err:
    error_locations = [e['loc'] for e in err.errors()]

print(error_locations)
#> [('a',), ('b',), ('c',), ('d',), ('e',)]
```

---

TITLE: Customizing Pydantic Core Schema with **get_pydantic_core_schema**
DESCRIPTION: This Python code demonstrates how to customize Pydantic's core schema generation using the **get_pydantic_core_schema** class method. It illustrates a wrapper pattern where `MyStrict` and `MyGt` classes modify the schema for an annotated integer type, adding `strict` and `gt` constraints respectively.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/internals/architecture.md#_snippet_6

LANGUAGE: python
CODE:

```
from typing import Annotated, Any

from pydantic_core import CoreSchema

from pydantic import GetCoreSchemaHandler, TypeAdapter


class MyStrict:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        schema = handler(source) # (1)!
        schema['strict'] = True
        return schema


class MyGt:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        schema = handler(source) # (2)!
        schema['gt'] = 1
        return schema


ta = TypeAdapter(Annotated[int, MyStrict(), MyGt()])
```

---

TITLE: Dynamic vs Static Model Definition with create_model - Pydantic Python
DESCRIPTION: Demonstrates creating a Pydantic model dynamically using `create_model` and compares it to an equivalent static `BaseModel` definition, showing how to handle aliases, descriptions using `Annotated` and `Field`, and private attributes.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_39

LANGUAGE: python
CODE:

```
from typing import Annotated

from pydantic import BaseModel, Field, PrivateAttr, create_model

DynamicModel = create_model(
    'DynamicModel',
    foo=(str, Field(alias='FOO')),
    bar=Annotated[str, Field(description='Bar field')],
    _private=(int, PrivateAttr(default=1)),
)


class StaticModel(BaseModel):
    foo: str = Field(alias='FOO')
    bar: Annotated[str, Field(description='Bar field')]
    _private: int = PrivateAttr(default=1)
```

---

TITLE: Ignoring Extra Data in Pydantic Model (Default) - Python
DESCRIPTION: Demonstrates the default behavior of Pydantic models where extra data provided during instantiation is ignored and not included in the model's dictionary representation. Requires `pydantic.BaseModel`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_7

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Model(BaseModel):
    x: int


m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1}
```

---

TITLE: Automatic Pydantic Model Validation Instrumentation (Python)
DESCRIPTION: This example shows how to enable automatic logging of Pydantic model validation events using `logfire.instrument_pydantic()`. Once configured, Logfire automatically records details for all successful and failed model validations, providing comprehensive insights into data integrity and parsing without explicit logging calls per model.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/logfire.md#_snippet_1

LANGUAGE: python
CODE:

```
from datetime import date

import logfire

from pydantic import BaseModel

logfire.configure()
logfire.instrument_pydantic()  # (1)!


class User(BaseModel):
    name: str
    country_code: str
    dob: date


User(name='Anne', country_code='USA', dob='2000-01-01')
User(name='David', country_code='GBR', dob='invalid-dob')
```

---

TITLE: Pydantic Model with Infinite Iterable Validation
DESCRIPTION: Demonstrates how to define a Pydantic model field using `typing.Iterable` to handle infinite generators or remote data loaders without eager consumption. The example shows an `infinite_ints` generator and how its values are accessed lazily.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_15

LANGUAGE: python
CODE:

```
from typing import Iterable

from pydantic import BaseModel


class Model(BaseModel):
    infinite: Iterable[int]


def infinite_ints():
    i = 0
    while True:
        yield i
        i += 1


m = Model(infinite=infinite_ints())
print(m)
"""
infinite=ValidatorIterator(index=0, schema=Some(Int(IntValidator { strict: false })))
"""

for i in m.infinite:
    print(i)
    #> 0
    #> 1
    #> 2
    #> 3
    #> 4
    #> 5
    #> 6
    #> 7
    #> 8
    #> 9
    #> 10
    if i == 10:
        break
```

---

TITLE: Define Named Generic Type Alias with 'type' Syntax (Python 3.12+)
DESCRIPTION: Demonstrates defining a named generic type alias `ShortList` using the new `type` statement (PEP 695) that accepts a type variable `T`. This allows the alias to be parameterized, similar to generic types.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/types.md#_snippet_9

LANGUAGE: python
CODE:

```
from typing import Annotated, TypeVar

from annotated_types import Len

type ShortList[T] = Annotated[list[T], Len(max_length=4)]
```

---

TITLE: Configure Serverless Framework to Include Email-Validator Metadata
DESCRIPTION: This YAML configuration snippet for `serverless.yml` addresses the 'No package metadata was found for `email-validator`' error in AWS Lambda deployments using the Serverless Framework. Setting `slim: false` under `pythonRequirements` ensures that `serverless-python-requirements` includes the necessary `dist-info` metadata directory for `email-validator` in the deployment package, resolving versioning issues.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/integrations/aws_lambda.md#_snippet_3

LANGUAGE: yaml
CODE:

```
pythonRequirements:
    dockerizePip: non-linux
    slim: false
    fileName: requirements.txt
```

---

TITLE: Pydantic: Resolve 'decorator-missing-field' with check_fields=False
DESCRIPTION: Demonstrates how to suppress the 'decorator-missing-field' error by setting `check_fields=False` in the `@field_validator`. This is useful when inheriting models and the field might be defined in a subclass or dynamically.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_6

LANGUAGE: python
CODE:

```
from typing import Any

from pydantic import BaseModel, create_model, field_validator


class Model(BaseModel):
    @field_validator('a', check_fields=False)
    def check_a(cls, v: Any):
        return v


model = create_model('FooModel', a=(str, 'cake'), __base__=Model)
```

---

TITLE: Handle Pydantic `get_attribute_error` Validation Error
DESCRIPTION: This error is raised when `model_config['from_attributes'] == True` and an error occurs while Pydantic attempts to read attributes from the input object. This typically happens if an attribute or property raises an exception during access.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_39

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ConfigDict, ValidationError


class Foobar:
    def __init__(self):
        self.x = 1

    @property
    def y(self):
        raise RuntimeError('intentional error')


class Model(BaseModel):
    x: int
    y: str

    model_config = ConfigDict(from_attributes=True)


try:
    Model.model_validate(Foobar())
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'get_attribute_error'
```

---

TITLE: Structural Pattern Matching with BaseModel (Python)
DESCRIPTION: Demonstrates using Python's structural pattern matching (match/case), introduced in Python 3.10 (PEP 636), with a Pydantic BaseModel instance.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_52

LANGUAGE: python
CODE:

```
from pydantic import BaseModel


class Pet(BaseModel):
    name: str
    species: str


a = Pet(name='Bones', species='dog')

match a:
    # match `species` to 'dog', declare and initialize `dog_name`
    case Pet(species='dog', name=dog_name):
        print(f'{dog_name} is a dog')
    # default case
    case _:
        print('No dog matched')
```

---

TITLE: Handle Pydantic Discriminator Alias Type Error
DESCRIPTION: Illustrates the `discriminator-alias-type` error in Pydantic, which occurs when a non-string alias is defined on a discriminator field. The example demonstrates how this misconfiguration leads to a `PydanticUserError`.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_8

LANGUAGE: python
CODE:

```
from typing import Literal, Union

from pydantic import AliasChoices, BaseModel, Field, PydanticUserError


class Cat(BaseModel):
    pet_type: Literal['cat'] = Field(
        validation_alias=AliasChoices('Pet', 'PET')
    )
    c: str


class Dog(BaseModel):
    pet_type: Literal['dog']
    d: str


try:

    class Model(BaseModel):
        pet: Union[Cat, Dog] = Field(discriminator='pet_type')
        number: int

except PydanticUserError as exc_info:
    assert exc_info.code == 'discriminator-alias-type'
```

---

TITLE: Ensure proper type-checking for Pydantic model_dump override
DESCRIPTION: Illustrates how to maintain correct type-checking for a Pydantic model's `.model_dump()` method when its return type has been customized, by overriding the method within an `if TYPE_CHECKING:` block.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/serialization.md#_snippet_11

LANGUAGE: python
CODE:

```
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, model_serializer


class Model(BaseModel):
    x: str

    @model_serializer
    def ser_model(self) -> str:
        return self.x

    if TYPE_CHECKING:
        # Ensure type checkers see the correct return type
        def model_dump(
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: Any = None,
            exclude: Any = None,
            by_alias: bool | None = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
        ) -> str: ...
```

---

TITLE: Handle Pydantic `model_attributes_type` Validation Error
DESCRIPTION: This error is raised when the input value is not a valid dictionary, model instance, or an instance from which fields can be extracted using `from_attributes=True`. The example shows successful validation from a dictionary and a custom object, then demonstrates how a non-object string triggers the 'model_attributes_type' error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_62

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    a: int
    b: int


# simply validating a dict
print(Model.model_validate({'a': 1, 'b': 2}))
#> a=1 b=2


class CustomObj:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# using from attributes to extract fields from an objects
print(Model.model_validate(CustomObj(3, 4), from_attributes=True))
#> a=3 b=4

try:
    Model.model_validate('not an object', from_attributes=True)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'model_attributes_type'
```

---

TITLE: Serializing Pydantic Generic Model with Default Type
DESCRIPTION: Demonstrates the default serialization behavior of a Pydantic model with a generic type variable that has a default type, showing that fields not present in the default type are omitted during model_dump.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md#_snippet_34

LANGUAGE: python
CODE:

```
error = Error[ErrorDetails](
    message='We just had an error',
    details=ErrorDetails(foo='var'),
)
assert error.model_dump() == {
    'message': 'We just had an error',
    'details': {
        'foo': 'var',
    },
}
```

---

TITLE: Pydantic: Reproduce 'class-not-fully-defined' with ForwardRef
DESCRIPTION: Demonstrates how Pydantic raises a 'class-not-fully-defined' error when a type is referenced using `ForwardRef` but not properly resolved or defined later, leading to validation failure.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_0

LANGUAGE: python
CODE:

```
from typing import ForwardRef

from pydantic import BaseModel, PydanticUserError

UndefinedType = ForwardRef('UndefinedType')


class Foobar(BaseModel):
    a: UndefinedType


try:
    Foobar(a=1)
except PydanticUserError as exc_info:
    assert exc_info.code == 'class-not-fully-defined'
```

---

TITLE: Handle Pydantic V1 Validator Signature Error
DESCRIPTION: This snippet demonstrates a `PydanticUserError` (code 'validator-v1-signature') raised when an unsupported signature is used for a Pydantic V1-style validator. It shows a `validator` decorated method with an extra `foo` parameter, which is not allowed.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_29

LANGUAGE: python
CODE:

```
import warnings

from pydantic import BaseModel, PydanticUserError, validator

warnings.filterwarnings('ignore', category=DeprecationWarning)

try:

    class Model(BaseModel):
        a: int

        @validator('a')
        def check_a(cls, value, foo):
            return value

except PydanticUserError as exc_info:
    assert exc_info.code == 'validator-v1-signature'
```

---

TITLE: Pydantic: Avoiding `dataclass` Decorator on `BaseModel` Subclass
DESCRIPTION: This example illustrates the `PydanticUserError` that occurs when the Pydantic `dataclass` decorator is used on a class which is already a `BaseModel` subclass. It provides the code that leads to the 'dataclass-on-model' error.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_44

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, PydanticUserError
from pydantic.dataclasses import dataclass

try:

    @dataclass
    class Model(BaseModel):
        bar: str

except PydanticUserError as exc_info:
    assert exc_info.code == 'dataclass-on-model'
```

---

TITLE: Handle Pydantic `string_pattern_mismatch` Error
DESCRIPTION: This error occurs when a string input value does not conform to the regular expression `pattern` constraint defined for a Pydantic `Field`. The example shows a string failing to match a simple 'test' pattern.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_72

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: str = Field(pattern='test')


try:
    Model(x='1')
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'string_pattern_mismatch'
```

---

TITLE: Demonstrate `int_parsing_size` Pydantic Validation Error
DESCRIPTION: This error is raised when attempting to parse a Python or JSON string value into an integer that exceeds Python's maximum `str` to `int` parsing range. The example shows successful parsing for a valid length string and then demonstrates the error for an excessively long string, both from direct Python assignment and JSON deserialization.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_44

LANGUAGE: python
CODE:

```
import json

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: int


# from Python
assert Model(x='1' * 4_300).x == int('1' * 4_300)  # OK

too_long = '1' * 4_301
try:
    Model(x=too_long)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'int_parsing_size'

# from JSON
try:
    Model.model_validate_json(json.dumps({'x': too_long}))
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'int_parsing_size'
```

---

TITLE: Validate Pydantic Models with Python NamedTuple
DESCRIPTION: This snippet shows how Pydantic integrates with `typing.NamedTuple` subclasses for structured data validation. It demonstrates defining a `NamedTuple` as a field in a `BaseModel` and how Pydantic performs type checking on the `NamedTuple`'s elements, raising `ValidationError` for invalid inputs.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/api/standard_library_types.md#_snippet_10

LANGUAGE: python
CODE:

```
from typing import NamedTuple

from pydantic import BaseModel, ValidationError


class Point(NamedTuple):
    x: int
    y: int


class Model(BaseModel):
    p: Point


try:
    Model(p=('1.3', '2'))
except ValidationError as e:
    print(e)
```

---

TITLE: Pydantic: Preventing 'extra' Field Configuration in RootModel
DESCRIPTION: Pydantic's `RootModel` is designed to wrap a single root value and does not support extra fields. Specifying `model_config['extra']` (e.g., 'allow') for a `RootModel` subclass will raise a `PydanticUserError` with code 'root-model-extra'.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_38

LANGUAGE: python
CODE:

```
from pydantic import PydanticUserError, RootModel

try:

    class MyRootModel(RootModel):
        model_config = {'extra': 'allow'}
        root: int

except PydanticUserError as exc_info:
    assert exc_info.code == 'root-model-extra'
```

---

TITLE: Pydantic: Validating Callable Instances with `validate_call`
DESCRIPTION: This snippet demonstrates the current limitation of `validate_call` when applied directly to an instance of a class that implements a `__call__` method. It shows the incorrect attempt and then the recommended correct approach of applying `validate_call` directly to the `__call__` method itself.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/usage_errors.md#_snippet_47

LANGUAGE: python
CODE:

```
from pydantic import PydanticUserError, validate_call

# Incorrect usage: validate_call on an instance
try:

    class A1:
        def __call__(self): ...

    validate_call(A1())

except PydanticUserError as exc_info:
    assert exc_info.code == 'validate-call-type'


# Correct usage: @validate_call on the __call__ method
class A2:
    @validate_call
    def __call__(self): ...
```

---

TITLE: Pydantic Cyclic Reference Detection During Serialization
DESCRIPTION: Introduces Pydantic's behavior when encountering cyclic references during model serialization, where it raises a `ValueError` immediately to prevent `RecursionError`. This snippet is an incomplete example demonstrating the setup for such a scenario.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/concepts/forward_annotations.md#_snippet_4

LANGUAGE: python
CODE:

```
from pydantic import TypeAdapter
```

---

TITLE: Handle Pydantic `greater_than` Validation Error
DESCRIPTION: This error is raised when the value is not strictly greater than the field's `gt` constraint. It enforces a minimum exclusive value for numerical fields.
SOURCE: https://github.com/pydantic/pydantic/blob/main/docs/errors/validation_errors.md#_snippet_40

LANGUAGE: python
CODE:

```
from pydantic import BaseModel, Field, ValidationError


class Model(BaseModel):
    x: int = Field(gt=10)


try:
    Model(x=10)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'greater_than'
```
