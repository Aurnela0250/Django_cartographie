TITLE: Working with Tortoise ORM Models and Relationships
DESCRIPTION: Comprehensive example of using Tortoise ORM to create objects, manage relationships, query with filters, and use prefetching for optimized data retrieval. Demonstrates both single and many-to-many relationship handling.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/getting_started.rst#2025-04-20_snippet_3

LANGUAGE: python
CODE:

```
async def main():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

    # Creating an instance with .save()
    tournament = Tournament(name='New Tournament')
    await tournament.save()

    # Or with .create()
    await Event.create(name='Without participants', tournament=tournament)
    event = await Event.create(name='Test', tournament=tournament)
    participants = []
    for i in range(2):
        team = await Team.create(name='Team {}'.format(i + 1))
        participants.append(team)

    # Many to Many Relationship management is quite straightforward
    # (there are .remove(...) and .clear() too)
    await event.participants.add(*participants)

    # Iterate over related entities with the async context manager
    async for team in event.participants:
        print(team.name)

    # The related entities are cached and can be iterated in the synchronous way afterwards
    for team in event.participants:
        pass

    # Use prefetch_related to fetch related objects
    selected_events = await Event.filter(
        participants=participants[0].id
    ).prefetch_related('participants', 'tournament')
    for event in selected_events:
        print(event.tournament.name)
        print([t.name for t in event.participants])

    # Prefetch multiple levels of related entities
    await Team.all().prefetch_related('events__tournament')

    # Filter and order by related models too
    await Tournament.filter(
        events__name__in=['Test', 'Prod']
    ).order_by('-events__participants__name').distinct()

run_async(main())
```

---

TITLE: Initializing Tortoise ORM with SQLite Database
DESCRIPTION: Demonstrates how to initialize Tortoise ORM with a SQLite database connection and generate database schemas. Uses the db_url parameter to specify SQLite connection and modules parameter to define model locations. Includes schema generation which should be run once during initial setup.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/setup.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise import Tortoise

async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
```

---

TITLE: Using Tortoise ORM Models (Python)
DESCRIPTION: Demonstrates various operations with Tortoise ORM models, including creating instances, managing relationships, querying with filters and prefetch_related, and working with many-to-many relationships.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/README.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
async def main():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

    # Creating an instance with .save()
    tournament = Tournament(name='New Tournament')
    await tournament.save()

    # Or with .create()
    await Event.create(name='Without participants', tournament=tournament)
    event = await Event.create(name='Test', tournament=tournament)
    participants = []
    for i in range(2):
        team = await Team.create(name='Team {}'.format(i + 1))
        participants.append(team)

    # Many to Many Relationship management is quite straightforward
    # (there are .remove(...) and .clear() too)
    await event.participants.add(*participants)

    # Iterate over related entities with the async context manager
    async for team in event.participants:
        print(team.name)

    # The related entities are cached and can be iterated in the synchronous way afterwards
    for team in event.participants:
        pass

    # Use prefetch_related to fetch related objects
    selected_events = await Event.filter(
        participants=participants[0].id
    ).prefetch_related('participants', 'tournament')
    for event in selected_events:
        print(event.tournament.name)
        print([t.name for t in event.participants])

    # Prefetch multiple levels of related entities
    await Team.all().prefetch_related('events__tournament')

    # Filter and order by related models too
    await Tournament.filter(
        events__name__in=['Test', 'Prod']
    ).order_by('-events__participants__name').distinct()

run_async(main())
```

---

TITLE: Defining Models in Tortoise ORM
DESCRIPTION: Example of defining models in Tortoise ORM by inheriting from Model class. Demonstrates creating Tournament, Event, and Team models with various field types and relationships like ForeignKey and ManyToMany.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/getting_started.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in the tortoise config
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
```

---

TITLE: Defining Models in Tortoise ORM (Python)
DESCRIPTION: Demonstrates how to define database models by inheriting from tortoise.models.Model. It shows the creation of Tournament, Event, and Team models with various field types including foreign keys and many-to-many relationships.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/README.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
```

---

TITLE: Different primary key field types in Tortoise ORM
DESCRIPTION: Shows examples of different field types that can be used as primary keys, including IntField, CharField, and UUIDField.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_4

LANGUAGE: python
CODE:

```
id = fields.IntField(primary_key=True)

checksum = fields.CharField(primary_key=True)

guid = fields.UUIDField(primary_key=True)
```

---

TITLE: Using Nested Transactions with Savepoints in Tortoise ORM
DESCRIPTION: This example demonstrates how to use nested transactions with savepoints in Tortoise ORM. The outer transaction will commit changes on successful completion, while inner transactions create savepoints that can be rolled back to if exceptions occur, without affecting the outer transaction.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/transactions.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
# this block will commit changes on exit
async with in_transaction():
    await MyModel.create(name='foo')
    try:
        # this block will create a savepoint and rollback to it if an exception is raised
        async with in_transaction():
            await MyModel.create(name='bar')
            # this will rollback to the savepoint, meaning that
            # the 'bar' record will not be created, however,
            # the 'foo' record will be created
            raise Exception()
    except Exception:
        pass
```

---

TITLE: Initializing Tortoise ORM and Generating Schema
DESCRIPTION: Example of initializing Tortoise ORM with a SQLite database connection and generating the database schema. This demonstrates the basic setup needed before working with models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/getting_started.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
from tortoise import Tortoise, run_async

async def main():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

run_async(main())
```

---

TITLE: Creating and Serializing Tortoise ORM Objects with Pydantic
DESCRIPTION: Example showing how to create Tournament and Event objects and serialize them using Pydantic integration. Demonstrates relationship handling and computed fields like name_length and events_num.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_17

LANGUAGE: python
CODE:

```
# Create objects
tournament = await Tournament.create(name="New Tournament")
await Event.create(name="Event 1", tournament=tournament)
await Event.create(name="Event 2", tournament=tournament)

# Serialise Tournament
tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)

>>> print(tourpy.model_dump_json())
{
    "id": 1,
    "name": "New Tournament",
    "events": [
        {
            "id": 1,
            "name": "Event 1"
        },
        {
            "id": 2,
            "name": "Event 2"
        }
    ],
    "name_length": 14,
    "events_num": 2
}
```

---

TITLE: Performing Database Operations with Tortoise ORM in Python
DESCRIPTION: This snippet shows various database operations using Tortoise ORM, including creating records, searching with filters, and performing complex aggregation queries with case statements and grouping.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/index.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
# Creating a record
await Tournament.create(name='Another Tournament')

# Searching for a record
tour = await Tournament.filter(name__contains='Another').first()
print(tour.name)

# Count groups of records with a complex condition
await Tournament.annotate(
    name_prefix=Case(
        When(name__startswith="One", then="1"),
        When(name__startswith="Two", then="2"),
        default="0",
    ),
).annotate(
    count=Count(F("name_prefix")),
).group_by(
    "name_prefix"
).values("name_prefix", "count")
```

---

TITLE: Initializing Tortoise ORM (Python)
DESCRIPTION: Shows how to initialize Tortoise ORM, establish database connections, and generate schema. This example uses SQLite and is intended for development purposes.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/README.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from tortoise import Tortoise, run_async

async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

run_async(main())
```

---

TITLE: Defining Primary Keys in Tortoise-ORM Models
DESCRIPTION: Illustrates different ways to define primary keys in Tortoise-ORM models. Shows how to create primary keys of different field types by setting the pk parameter to True.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_18

LANGUAGE: python
CODE:

```
id = fields.IntField(pk=True)

checksum = fields.CharField(pk=True)

guid = fields.UUIDField(pk=True)
```

---

TITLE: Defining basic Tortoise ORM models with relationships
DESCRIPTION: Demonstrates how to define multiple related models in Tortoise ORM with various field types including primary keys, foreign keys, and many-to-many relationships.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
class Tournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    tournament = fields.ForeignKeyField('models.Tournament', related_name='events')
    participants = fields.ManyToManyField('models.Team', related_name='events', through='event_team')
    modified = fields.DatetimeField(auto_now=True)
    prize = fields.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    def __str__(self):
        return self.name
```

---

TITLE: Model inheritance and mixins in Tortoise ORM
DESCRIPTION: Demonstrates how to use inheritance and mixins to share fields between models, including abstract base models and non-model mixins for common fields.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_5

LANGUAGE: python
CODE:

```
from tortoise import fields
from tortoise.models import Model

class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)

class NameMixin():
    name = fields.CharField(40, unique=True)

class MyAbstractBaseModel(Model):
    id = fields.IntField(primary_key=True)

    class Meta:
        abstract = True

class UserModel(TimestampMixin, MyAbstractBaseModel):
    # Overriding the id definition
    # from MyAbstractBaseModel
    id = fields.UUIDField(primary_key=True)

    # Adding additional fields
    first_name = fields.CharField(20, null=True)

    class Meta:
        table = "user"


class RoleModel(TimestampMixin, NameMixin, MyAbstractBaseModel):

    class Meta:
        table = "role"
```

---

TITLE: Creating an abstract model in Tortoise ORM
DESCRIPTION: Demonstrates how to create an abstract model that can be used as a base class for other models but won't create a database table itself. Uses the Meta class with abstract=True.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_3

LANGUAGE: python
CODE:

```
class AbstractTournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
```

---

TITLE: Model Definitions with Type Hints
DESCRIPTION: Complete example showing model definitions with proper type hints for relationships, improving IDE autocomplete support.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_21

LANGUAGE: python3
CODE:

```
from tortoise.models import Model
from tortoise import fields


class Tournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)

    events: fields.ReverseRelation["Event"]

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    tournament: fields.ForeignKeyRelation[Tournament] = fields.ForeignKeyField(
        "models.Tournament", related_name="events"
    )
    participants: fields.ManyToManyRelation["Team"] = fields.ManyToManyField(
        "models.Team", related_name="events", through="event_team"
    )

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)

    events: fields.ManyToManyRelation[Event]

    def __str__(self):
        return self.name
```

---

TITLE: Initializing Tortoise ORM with Configuration in Python
DESCRIPTION: Demonstrates how to initialize Tortoise ORM with a SQLite database and specify application models. This code shows the new initialization pattern that replaced the previous model discovery approach.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_20

LANGUAGE: python
CODE:

```
async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
```

---

TITLE: Prefetching related models in Tortoise ORM
DESCRIPTION: Demonstrates how to fetch related models using the prefetch_related method, using a ForeignKeyField's related_name to access related objects.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_11

LANGUAGE: python
CODE:

```
await Tournament.first().prefetch_related("events")
```

---

TITLE: Querying Events Using Q Expressions in Python
DESCRIPTION: Demonstrates how to use Q objects to construct complex queries in Tortoise ORM. This example shows filtering events with specific names using OR conditions.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
found_events = await Event.filter(
    Q(name='Event 1') | Q(name='Event 2')
)
```

---

TITLE: Creating a Custom EnumField by Extending CharField
DESCRIPTION: Demonstrates how to create a custom field by subclassing existing fields. This example creates an EnumField that extends CharField to store and query Enum types, converting between Enum objects and their string representations.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/fields.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from enum import Enum
from typing import Type

from tortoise import ConfigurationError
from tortoise.fields import CharField


class EnumField(CharField):
    """
    An example extension to CharField that serializes Enums
    to and from a str representation in the DB.
    """

    def __init__(self, enum_type: Type[Enum], **kwargs):
        super().__init__(128, **kwargs)
        if not issubclass(enum_type, Enum):
            raise ConfigurationError("{} is not a subclass of Enum!".format(enum_type))
        self._enum_type = enum_type

    def to_db_value(self, value: Enum, instance) -> str:
        return value.value

    def to_python_value(self, value: str) -> Enum:
        try:
            return self._enum_type(value)
        except Exception:
            raise ValueError(
                "Database value {} does not exist on Enum {}.".format(value, self._enum_type)
            )
```

---

TITLE: Complex Prefetching in Tortoise ORM
DESCRIPTION: Illustrates how to use the Prefetch object for complex prefetching in Tortoise ORM. This example demonstrates fetching only certain related records by applying a filter to the prefetch query.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_14

LANGUAGE: python
CODE:

```
tournament_with_filtered = await Tournament.all().prefetch_related(
    Prefetch('events', queryset=Event.filter(name='First'))
).first()
```

---

TITLE: Filtering with POSIX Regex in Tortoise ORM for PostgreSQL, MySQL, and SQLite
DESCRIPTION: Demonstrates how to use POSIX regular expressions for filtering in Tortoise ORM across different database systems. It shows both case-sensitive and case-insensitive regex comparisons using the posix_regex and iposix_regex operators.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_13

LANGUAGE: python
CODE:

```
class DemoModel:
  demo_text = fields.TextField()

await DemoModel.create(demo_text="Hello World")
obj = await DemoModel.filter(demo_text__posix_regex="^Hello World$").first()
obj = await DemoModel.filter(demo_text__iposix_regex="^hello world$").first()
```

---

TITLE: Filtering by Related Entity Fields in Tortoise ORM
DESCRIPTION: Demonstrates how to filter records based on related entity fields. Shows three different examples of filtering across relationships.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_5

LANGUAGE: python
CODE:

```
# getting all events, which tournament name is "World Cup"
await Event.filter(tournament__name='World Cup')

# Gets all teams participating in events with ids 1, 2, 3
await Team.filter(events__id__in=[1,2,3])

# Gets all tournaments where teams with "junior" in their name are participating
await Tournament.filter(event__participants__name__icontains='junior').distinct()
```

---

TITLE: JSON Field Filtering in Tortoise ORM
DESCRIPTION: Shows advanced JSON field filtering using contains, contained_by, and filter modifiers. Demonstrates various ways to query JSON data structures in PostgreSQL and MySQL.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_12

LANGUAGE: python
CODE:

```
class JSONModel:
    data = fields.JSONField[list]()

await JSONModel.create(data=["text", 3, {"msg": "msg2"}])
obj = await JSONModel.filter(data__contains=[{"msg": "msg2"}]).first()

await JSONModel.create(data=["text"])
await JSONModel.create(data=["tortoise", "msg"])
await JSONModel.create(data=["tortoise"])

objects = await JSONModel.filter(data__contained_by=["text", "tortoise", "msg"])

await JSONModel.create(data={"breed": "labrador",
                             "owner": {
                                 "name": "Boby",
                                 "last": None,
                                 "other_pets": [
                                     {
                                         "name": "Fishy",
                                     }
                                 ],
                             },
                         })

obj1 = await JSONModel.filter(data__filter={"breed": "labrador"}).first()
obj2 = await JSONModel.filter(data__filter={"owner__name": "Boby"}).first()
obj3 = await JSONModel.filter(data__filter={"owner__other_pets__0__name": "Fishy"}).first()
obj4 = await JSONModel.filter(data__filter={"breed__not": "a"}).first()
obj5 = await JSONModel.filter(data__filter={"owner__name__isnull": True}).first()
obj6 = await JSONModel.filter(data__filter={"owner__last__not_isnull": False}).first()
```

---

TITLE: Generating Database Schema with Tortoise ORM
DESCRIPTION: Method to generate database schemas for Tortoise ORM models. The safe parameter can be set to True to only create tables if they don't already exist.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/schema.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
await Tortoise.generate_schemas(safe=True)
```

---

TITLE: Closing Tortoise ORM Connections
DESCRIPTION: Shows how to properly close Tortoise ORM database connections to prevent asyncio connection leaks. This cleanup step is crucial for proper application shutdown and resource management.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/setup.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
await Tortoise.close_connections()
```

---

TITLE: Creating a Pydantic Model from Tortoise Model
DESCRIPTION: Generating a Pydantic model from a Tortoise model using the pydantic_model_creator function. This creates a Pydantic model that can be used for schema representation and serialization of Tortoise model instances.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from tortoise.contrib.pydantic import pydantic_model_creator

Tournament_Pydantic = pydantic_model_creator(Tournament)
```

---

TITLE: Implementing Custom Manager in Tortoise ORM Model
DESCRIPTION: Shows how to create a custom StatusManager that filters queryset results and implement it in a model. Also demonstrates how to define multiple managers including a default manager and additional named managers.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/manager.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise.manager import Manager

class StatusManager(Manager):
    def get_queryset(self):
        return super(StatusManager, self).get_queryset().filter(status=1)


class ManagerModel(Model):
    status = fields.IntField(default=0)
    all_objects = Manager()

    class Meta:
        manager = StatusManager()
```

---

TITLE: Serializing Event Objects with Tournament Relationship in Python
DESCRIPTION: Shows how to serialize an Event object to JSON in an async context, including its relationship to a Tournament. The serialized output includes the full Tournament object data.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_13

LANGUAGE: python
CODE:

```
eventpy = await Event_Pydantic.from_tortoise_orm(event)

>>> print(eventpy.model_dump_json())
{
    "id": 1,
    "name": "The Event",
    "created_at": "2020-03-02T07:23:27.732492",
    "tournament": {
        "id": 1,
        "name": "New Tournament",
        "created_at": "2020-03-02T07:23:27.731656"
    }
}
```

---

TITLE: Filtering Related Objects in Tortoise ORM
DESCRIPTION: Shows how to filter related objects for a specific model instance. Returns a QuerySet with a predefined filter for related objects.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
await team.events.filter(name='First')
```

---

TITLE: Executing Raw SQL Queries with RawSQL in Tortoise ORM
DESCRIPTION: Shows how to use RawSQL to execute raw SQL queries within filter() and annotate() operations. This provides maximum flexibility for complex database operations.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_7

LANGUAGE: python
CODE:

```
await Tournament.filter(pk=1).annotate(count=RawSQL('count(*)')).values("count")
await Tournament.filter(pk=1).annotate(idp=RawSQL('id + 1')).filter(idp=2).values("idp")
await Tournament.filter(pk=RawSQL("id + 1"))
```

---

TITLE: Nesting Q Expressions for Complex Queries in Python
DESCRIPTION: Shows how to nest Q objects to create equivalent complex queries. This example demonstrates an alternative way to filter events with specific names using nested Q objects.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
found_events = await Event.filter(
    Q(Q(name='Event 1'), Q(name='Event 2'), join_type="OR")
)
```

---

TITLE: Creating objects with foreign keys in Tortoise ORM
DESCRIPTION: Shows different approaches to specify foreign key values when creating model instances, either by passing the object directly or by using the database backing field.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_12

LANGUAGE: python
CODE:

```
await SomeModel.create(tournament=the_tournament)
# or
somemodel.tournament=the_tournament
```

---

TITLE: Using Annotations and Database Functions in Tortoise ORM
DESCRIPTION: Shows how to use the annotate() method with various database functions like Count, Trim, Lower, Upper, and Coalesce to perform aggregations and transformations in queries.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_8

LANGUAGE: python
CODE:

```
from tortoise.functions import Count, Trim, Lower, Upper, Coalesce

# This query will fetch all tournaments with 10 or more events, and will
# populate filed `.events_count` on instances with corresponding value
await Tournament.annotate(events_count=Count('events')).filter(events_count__gte=10)
await Tournament.annotate(clean_name=Trim('name')).filter(clean_name='tournament')
await Tournament.annotate(name_upper=Upper('name')).filter(name_upper='TOURNAMENT')
await Tournament.annotate(name_lower=Lower('name')).filter(name_lower='tournament')
await Tournament.annotate(desc_clean=Coalesce('desc', '')).filter(desc_clean='')
```

---

TITLE: Async Many-to-Many Relationship Query
DESCRIPTION: Shows how to asynchronously fetch all related participants using a Many-to-Many relationship.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_18

LANGUAGE: python3
CODE:

```
participants = await tournament.participants.all()
```

---

TITLE: Advanced Filtering and Ordering in Tortoise ORM
DESCRIPTION: Shows how to filter by related model fields and order by nested relationships in Tortoise ORM. This example demonstrates filtering tournaments by event names and ordering by participant names.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_23

LANGUAGE: python
CODE:

```
await Tournament.filter(
    events__name__in=['1', '3']
).order_by('-events__participants__name').distinct()
```

---

TITLE: Using NOT Operation with Q Expressions in Python
DESCRIPTION: Illustrates how to use the negation operator (~) with Q objects to create NOT conditions in queries. This example filters events that do not have the name '3'.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
not_third_events = await Event.filter(~Q(name='3'))
```

---

TITLE: Using Case-When Expressions for Conditional Logic in Tortoise ORM
DESCRIPTION: Demonstrates the use of Case-When expressions to construct conditional logic using CASE WHEN ... THEN ... ELSE ... END SQL statements. This example categorizes IntModel instances based on their 'intnum' value.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_8

LANGUAGE: python
CODE:

```
results = await IntModel.all().annotate(
    category=Case(
        When(intnum__gte=8, then='big'),
        When(intnum__lte=2, then='small'),
        default='middle'
    )
)
```

---

TITLE: Async Iteration Over Many-to-Many Relationship
DESCRIPTION: Demonstrates how to asynchronously iterate over participants in a Many-to-Many relationship.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_19

LANGUAGE: python3
CODE:

```
async for participant in tournament.participants:
    ...
```

---

TITLE: Using MySQL FullTextIndex and SpatialIndex in Tortoise ORM Model
DESCRIPTION: Demonstrates how to apply specialized MySQL indexes in a Tortoise ORM model by defining them in the Meta class. Shows implementation of FullTextIndex with a custom parser and SpatialIndex for geometry data.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/indexes.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise import Model, fields
from tortoise.contrib.mysql.fields import GeometryField
from tortoise.contrib.mysql.indexes import FullTextIndex, SpatialIndex


class Index(Model):
    full_text = fields.TextField()
    geometry = GeometryField()

    class Meta:
        indexes = [
            FullTextIndex(fields={"full_text"}, parser_name="ngram"),
            SpatialIndex(fields={"geometry"}),
        ]
```

---

TITLE: Updating User Balance Using F Expressions in Python
DESCRIPTION: Demonstrates the use of F expressions for atomic field operations in Tortoise ORM. This example shows how to update a user's balance without loading the value into Python memory.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_3

LANGUAGE: python
CODE:

```
from tortoise.expressions import F

await User.filter(id=1).update(balance = F('balance') - 10)

await User.filter(id=1).update(balance = F('balance') + F('award'), award = 0)

# Using F expressions with .save()
user = await User.get(id=1)
user.balance = F('balance') - 10
await user.save(update_fields=['balance'])
```

---

TITLE: Querying with Raw SQL in Tortoise ORM
DESCRIPTION: Using the Model.raw() method to execute raw SQL queries directly against the database. This allows for complex queries that might not be expressible through the standard ORM interface.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
Model.raw("SELECT * FROM table WHERE condition")
```

---

TITLE: Using F Expression in Tortoise ORM Annotations
DESCRIPTION: F expressions allow referring to model field values directly in database queries. This example shows using F expressions with annotations to create computations at the database level.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_3

LANGUAGE: python
CODE:

```
queryset.annotate(field_expression=F("field_name"))
```

---

TITLE: Serializing a Tortoise Model Instance with Pydantic
DESCRIPTION: Converting a Tortoise ORM model instance to a Pydantic model and serializing it. This shows how to create a Tournament instance and then convert it to a Pydantic object that can be exported as a dictionary or JSON.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
tournament = await Tournament.create(name="New Tournament")
tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)
```

---

TITLE: Defining Model Fields in Tortoise ORM
DESCRIPTION: Demonstrates how to define fields as properties of a Model class object. The example shows a Tournament model with integer ID (primary key) and character name fields.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/fields.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
```

---

TITLE: Defining Tortoise Models with PydanticMeta Configuration in Python
DESCRIPTION: Shows how to define Tortoise ORM models with computed properties and PydanticMeta configuration. The PydanticMeta class controls which fields are included/excluded and adds computed fields to the Pydantic model.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_14

LANGUAGE: python
CODE:

```
class Tournament(Model):
    """
    This references a Tournament
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    # It is useful to define the reverse relations manually so that type checking
    #  and auto completion work
    events: fields.ReverseRelation["Event"]

    def name_length(self) -> int:
        """
        Computed length of name
        """
        return len(self.name)

    def events_num(self) -> int:
        """
        Computed team size
        """
        try:
            return len(self.events)
        except NoValuesFetched:
            return -1

    class PydanticMeta:
        # Let's exclude the created timestamp
        exclude = ("created_at",)
        # Let's include two callables as computed columns
        computed = ("name_length", "events_num")


class Event(Model):
    """
    This references an Event in a Tournament
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    tournament = fields.ForeignKeyField(
        "models.Tournament", related_name="events", description="The Tournament this happens in"
    )

    class Meta:
        ordering = ["name"]

    class PydanticMeta:
        exclude = ("created_at",)
```

---

TITLE: Using Validators with Tortoise ORM Model Fields
DESCRIPTION: Demonstrates how to use validators with Tortoise ORM model fields. It shows a CharField with a RegexValidator to ensure the field value matches a specific pattern.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/validators.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
class ValidatorModel(Model):
    regex = fields.CharField(max_length=100, null=True, validators=[RegexValidator("abc.+", re.I)])

# oh no, this will raise ValidationError!
await ValidatorModel.create(regex="ccc")
# this is great!
await ValidatorModel.create(regex="abcd")
```

---

TITLE: Querying with Nested Values in Tortoise ORM
DESCRIPTION: Shows how to perform nested queries using the values() and values_list() methods in Tortoise ORM. This allows retrieving specific fields including those from related models in a single query.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_21

LANGUAGE: python
CODE:

```
result = await Event.filter(id=event.id).values('id', 'name', tournament='tournament__name')
result = await Event.filter(id=event.id).values_list('id', 'participants__name')
```

---

TITLE: Setting foreign keys directly with IDs in Tortoise ORM
DESCRIPTION: Shows how to set a foreign key value by directly accessing the database backing field with the \_id suffix, which can be more efficient when the related object isn't needed.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_13

LANGUAGE: python
CODE:

```
await SomeModel.create(tournament_id=the_tournament.pk)
# or
somemodel.tournament_id=the_tournament.pk
```

---

TITLE: Using Pydantic Serialization Methods
DESCRIPTION: Demonstrating Pydantic's serialization methods on a converted Tortoise model. Shows how to use model_dump() to get a dictionary representation and model_dump_json() to get a JSON string representation of the model.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_3

LANGUAGE: python
CODE:

```
>>> print(tourpy.model_dump())
{
    'id': 1,
    'name': 'New Tournament',
    'created_at': datetime.datetime(2020, 3, 1, 20, 28, 9, 346808)
}
>>> print(tourpy.model_dump_json())
{
    "id": 1,
    "name": "New Tournament",
    "created_at": "2020-03-01T20:28:09.346808"
}
```

---

TITLE: Using Select Related in Tortoise ORM
DESCRIPTION: The select_related() method optimizes queries by fetching related objects in a single database query. This reduces the number of database queries needed when accessing related objects.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_11

LANGUAGE: python
CODE:

```
queryset.select_related("related_field")
```

---

TITLE: Using Nested Queries with Values Method in Tortoise ORM
DESCRIPTION: Examples of using nested queries with the values() and values_list() methods in Tortoise ORM. This allows fetching related model fields in a single query, introduced in version 0.9.0.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_14

LANGUAGE: python
CODE:

```
result = await Event.filter(id=event.id).values('id', 'name', tournament='tournament__name')
result = await Event.filter(id=event.id).values_list('id', 'participants__name')
```

---

TITLE: Tortoise-ORM Configuration with Aerich
DESCRIPTION: Example configuration for Tortoise-ORM including Aerich models, showing database connection and app settings.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
TORTOISE_ORM = {
    "connections": {"default": "mysql://root:123456@127.0.0.1:3306/test"},
    "apps": {
        "models": {
            "models": ["tests.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
```

---

TITLE: Sync Usage of Foreign Key Relationship
DESCRIPTION: Shows how to use Foreign Key relationships synchronously after fetching related data, including common operations like listing, length checking, and indexing.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_16

LANGUAGE: python3
CODE:

```
await tournament.fetch_related('events')
events = list(tournament.events)
eventlen = len(tournament.events)
if SomeEvent in tournament.events:
    ...
if tournament.events:
    ...
firstevent = tournament.events[0]
```

---

TITLE: Initializing and Finalizing Tortoise ORM Test Environment
DESCRIPTION: Shows how to properly set up and tear down the test environment for Tortoise ORM tests using the initializer and finalizer functions.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/unittest.rst#2025-04-20_snippet_1

LANGUAGE: python3
CODE:

```
from tortoise.contrib.test import initializer, finalizer

# In setup
initializer(['module.a', 'module.b.c'])
# With optional db_url, app_label and loop parameters
initializer(['module.a', 'module.b.c'], db_url='...', app_label="someapp", loop=loop)
# Or env-var driven → See Green test runner section below.
env_initializer()

# In teardown
finalizer()
```

---

TITLE: Excluding Teams by Name Pattern in Tortoise ORM
DESCRIPTION: Shows how to use the exclude method to filter out records matching certain criteria. Returns all teams that don't have 'junior' in their name (case-insensitive).
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_4

LANGUAGE: python
CODE:

```
await Team.exclude(name__icontains='junior')
```

---

TITLE: Defining a Basic Tortoise Model
DESCRIPTION: Creating a simple Tortoise ORM model class that will be used as the basis for Pydantic model generation. This model represents a Tournament entity with basic fields including an ID, name, and created_at timestamp.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise import fields
from tortoise.models import Model

class Tournament(Model):
    """
    This references a Tournament
    """
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    #: The date-time the Tournament record was created at
    created_at = fields.DatetimeField(auto_now_add=True)
```

---

TITLE: Defining Tortoise Models with Relationships
DESCRIPTION: Creating Tortoise ORM models with a foreign key relationship. This example defines Tournament and Event models where Event has a foreign key relationship to Tournament, demonstrating how relationships are handled in serialization.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_8

LANGUAGE: python
CODE:

```
from tortoise import fields
from tortoise.models import Model

class Tournament(Model):
    """
    This references a Tournament
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    #: The date-time the Tournament record was created at
    created_at = fields.DatetimeField(auto_now_add=True)

class Event(Model):
    """
    This references an Event in a Tournament
    """

    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    tournament = fields.ForeignKeyField(
        "models.Tournament", related_name="events", description="The Tournament this happens in"
    )
```

---

TITLE: Setting a custom manager in Tortoise ORM
DESCRIPTION: Shows how to override the default manager with a custom manager class instance using the manager option in the Meta class.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_10

LANGUAGE: python
CODE:

```
manager = CustomManager()
```

---

TITLE: Prefetching Related Data in Tortoise ORM
DESCRIPTION: Shows how to prefetch related data to reduce the number of database queries. Demonstrates prefetching a single relationship and multiple levels of related models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_6

LANGUAGE: python
CODE:

```
# This will fetch events, and for each of events ``.tournament`` field will be populated with
# corresponding ``Tournament`` instance
await Event.all().prefetch_related('tournament')

# This will fetch tournament with their events and teams for each event
tournament_list = await Tournament.all().prefetch_related('events__participants')

# Fetched result for m2m and backward fk relations are stored in list-like containe#r
for tournament in tournament_list:
    print([e.name for e in tournament.events])
```

---

TITLE: Filtering and Ordering by Related Models Fields in Tortoise ORM
DESCRIPTION: Example of filtering and ordering by related model fields in Tortoise ORM. This demonstrates the ability to query across relationships and order by related fields, introduced in version 0.2.0.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_15

LANGUAGE: python
CODE:

```
await Tournament.filter(
    events__name__in=['1', '3']
).order_by('-events__participants__name').distinct()
```

---

TITLE: Refreshing Model Instance After F Expression Updates in Python
DESCRIPTION: Shows the correct way to access updated field values after using F expressions. This example demonstrates how to refresh a model instance to get the latest balance value.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_4

LANGUAGE: python
CODE:

```
# Incorrect - balance value may be stale
balance = user.balance

# Correct - refresh the balance field first
await user.refresh_from_db(fields=['balance'])
balance = user.balance
```

---

TITLE: Fetching Related Objects with Explicit Query and Async For Loop
DESCRIPTION: Demonstrates how to retrieve related objects using an explicit query with 'async for' syntax. This provides a way to iterate through related objects without loading all of them at once.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
async for team in event.participants:
    print(team.name)
```

---

TITLE: Adding Participants to an Event in Tortoise ORM
DESCRIPTION: Demonstrates how to use the ManyToManyRelation API to add related objects. This example adds two participants to an event using the add() method.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_9

LANGUAGE: python
CODE:

```
await event.participants.add(participant_1, participant_2)
```

---

TITLE: Reverse Foreign Key Relationship Access
DESCRIPTION: Demonstrates how to access the reverse side of a Foreign Key relationship using the sync interface.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_17

LANGUAGE: python3
CODE:

```
await event.fetch_related('tournament')
tournament = event.tournament
```

---

TITLE: Filtering with JSON Field Operators
DESCRIPTION: Example showing usage of contains, contained_by and filter operators with JSONField
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_4

LANGUAGE: Python
CODE:

```
Model.filter(json_field__contains={"key": "value"})
Model.filter(json_field__contained_by={"key": "value"})
```

---

TITLE: Configuring TortoiseORM in Python
DESCRIPTION: Demonstrates how to create a TortoiseORM configuration object in a Python settings file. This configuration specifies database connections and application models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/cli.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://:memory:",
    },
    "apps": {
        "models": {"models": ["examples.models"], "default_connection": "default"},
    },
}
```

---

TITLE: Declaring a class derived from Model in Tortoise ORM
DESCRIPTION: Shows the basic syntax for creating a model class that inherits from the Model base class in Tortoise ORM.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
class Tournament(Model):
```

---

TITLE: Creating Custom Validators in Tortoise ORM
DESCRIPTION: Shows two methods to create custom validators in Tortoise ORM. The first method is by creating a class that inherits from Validator, and the second is by defining a standalone function. Both validate if a number is even.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/validators.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from tortoise.validators import Validator
from tortoise.exceptions import ValidationError

class EvenNumberValidator(Validator):
    """
    A validator to validate whether the given value is an even number or not.
    """
    def __call__(self, value: int):
        if value % 2 != 0:
            raise ValidationError(f"Value '{value}' is not an even number")

# or use function instead of class
def validate_even_number(value:int):
    if value % 2 != 0:
        raise ValidationError(f"Value '{value}' is not an even number")
```

---

TITLE: Model Raw SQL Query Example
DESCRIPTION: Code snippet showing the addition of Model.raw() method for executing raw SQL queries.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_3

LANGUAGE: Python
CODE:

```
Model.raw("sql query")
```

---

TITLE: Creating Custom JsonSet Function for MySQL and SQLite in Tortoise ORM
DESCRIPTION: This snippet demonstrates how to create a custom JsonSet function for use with MySQL and SQLite in Tortoise ORM. It allows for JSON manipulation in update operations using the JSON_SET function.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/functions.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
from tortoise.expressions import F
from tortoise.functions import Function
from pypika_tortoise.terms import Function as PupikaFunction

class JsonSet(Function):
    class PypikaJsonSet(PupikaFunction):
        def __init__(self, field: F, expression: str, value: Any):
            super().__init__("JSON_SET", field, expression, value)

    database_func = PypikaJsonSet

json = await JSONFields.create(data_default={"a": 1})
json.data_default = JsonSet(F("data_default"), "$.a", 2)
await json.save()

# or use queryset.update()
sql = JSONFields.filter(pk=json.pk).update(data_default=JsonSet(F("data_default"), "$.a", 3)).sql()
print(sql)
# UPDATE jsonfields SET data_default=JSON_SET(`data_default`,'$.a',3) where id=1
```

---

TITLE: Using F Expressions in Annotations in Python
DESCRIPTION: Illustrates how F expressions can be used in annotations to perform calculations on field values. This example shows annotating a User model with an incremented ID value.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_5

LANGUAGE: python
CODE:

```
data = await User.annotate(idp=F("id") + 1).values_list("id", "idp")
```

---

TITLE: Setting up compound indexes in Tortoise ORM
DESCRIPTION: Shows the syntax for setting up compound non-unique indexes using the indexes option in the Meta class with different formats of specification.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_8

LANGUAGE: python
CODE:

```
indexes=("field_a", "field_b")
indexes=(("field_a", "field_b"), )
indexes=(("field_a", "field_b"), ("field_c", "field_d", "field_e"))
```

---

TITLE: Using Subquery Expression in Tortoise ORM
DESCRIPTION: The Subquery expression enables creating nested queries within a main query. This is useful for complex data retrieval that requires data from multiple related tables or aggregated results.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_4

LANGUAGE: python
CODE:

```
Subquery("subquery_expression")
```

---

TITLE: Implementing OneToOneField Relation in Python with Tortoise ORM
DESCRIPTION: Example code showing how to define a OneToOneField relation between models in Tortoise ORM. It demonstrates creating a one-to-one relationship between an Event model and an Address model with a cascade deletion policy.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_9

LANGUAGE: python
CODE:

```
event: fields.OneToOneRelation[Event] = fields.OneToOneField(
    "models.Event", on_delete=fields.CASCADE, related_name="address"
)
```

---

TITLE: Creating a Custom FullTextIndex Class in Tortoise ORM
DESCRIPTION: Shows how to extend the base Index class to create a custom FullTextIndex with support for parser specification. The implementation includes type hints and proper inheritance from the base Index class.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/indexes.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from typing import Optional, Set
from pypika_tortoise.terms import Term
from tortoise.indexes import Index

class FullTextIndex(Index):
    INDEX_TYPE = "FULLTEXT"

    def __init__(
        self,
        *expressions: Term,
        fields: Optional[Set[str]] = None,
        name: Optional[str] = None,
        parser_name: Optional[str] = None,
    ):
        super().__init__(*expressions, fields=fields, name=name)
        if parser_name:
            self.extra = f" WITH PARSER {parser_name}"
```

---

TITLE: Printing Pydantic Schema for Tournament Model in Python
DESCRIPTION: Displays the JSON schema of a Tournament Pydantic model created from a Tortoise ORM model. The schema shows the model's properties including relationships to Event models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_10

LANGUAGE: python
CODE:

```
>>> print(Tournament_Pydantic.schema())
{
    'title': 'Tournament',
    'description': 'This references a Tournament',
    'type': 'object',
    'properties': {
        'id': {
            'title': 'Id',
            'type': 'integer'
        },
        'name': {
            'title': 'Name',
            'type': 'string'
        },
        'created_at': {
            'title': 'Created At',
            'description': 'The date-time the Tournament record was created at',
            'type': 'string',
            'format': 'date-time'
        },
        'events': {
            'title': 'Events',
            'description': 'The Tournament this happens in',
            'type': 'array',
            'items': {
                '$ref': '#/definitions/Event'
            }
        }
    },
    'definitions': {
        'Event': {
            'title': 'Event',
            'description': 'This references an Event in a Tournament',
            'type': 'object',
            'properties': {
                'id': {
                    'title': 'Id',
                    'type': 'integer'
                },
                'name': {
                    'title': 'Name',
                    'type': 'string'
                },
                'created_at': {
                    'title': 'Created At',
                    'type': 'string',
                    'format': 'date-time'
                }
            }
        }
    }
}
```

---

TITLE: Initializing Tortoise ORM Models Without Database Connection
DESCRIPTION: Example demonstrating early initialization of Tortoise ORM models without requiring a database connection. This is useful for schema generation or model introspection without a full database setup.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_8

LANGUAGE: python
CODE:

```
# Lets say you defined your models in "some/models.py", and "other/ddef.py"
# And you are going to use them in the "model" namespace:
Tortoise.init_models(["some.models", "other.ddef"], "models")

# Now the models will have relationships built, so introspection of schema will be comprehensive
```

---

TITLE: Sync Usage of Many-to-Many Relationship
DESCRIPTION: Shows how to use Many-to-Many relationships synchronously after fetching related data, including common operations like listing, length checking, and indexing.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_20

LANGUAGE: python3
CODE:

```
await tournament.fetch_related('participants')
participants = list(tournament.participants)
participantlen = len(tournament.participants)
if SomeParticipant in tournament.participants:
    ...
if tournament.participants:
    ...
firstparticipant = tournament.participants[0]
```

---

TITLE: Creating and Displaying Pydantic Model Schema with Custom Configuration in Python
DESCRIPTION: Demonstrates creating a Pydantic model from a Tortoise model with custom PydanticMeta configuration and displaying its JSON schema. The schema includes computed fields and excludes fields specified in PydanticMeta.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_15

LANGUAGE: python
CODE:

```
from tortoise import Tortoise

Tortoise.init_models(["__main__"], "models")
Tournament_Pydantic = pydantic_model_creator(Tournament)
```

---

TITLE: Creating a Pydantic Model for the Event Model in Python
DESCRIPTION: Shows how to create and print the schema for an Event Pydantic model. The schema includes the relationship back to the Tournament model but avoids circular references.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_11

LANGUAGE: python
CODE:

```
Event_Pydantic = pydantic_model_creator(Event)

>>> print(Event_Pydantic.schema())
{
    'title': 'Event',
    'description': 'This references an Event in a Tournament',
    'type': 'object',
    'properties': {
        'id': {
            'title': 'Id',
            'type': 'integer'
        },
        'name': {
            'title': 'Name',
            'type': 'string'
        },
        'created_at': {
            'title': 'Created At',
            'type': 'string',
            'format': 'date-time'
        },
        'tournament': {
            'title': 'Tournament',
            'description': 'The Tournament this happens in',
            'allOf': [
                {
                    '$ref': '#/definitions/Tournament'
                }
            ]
        }
    },
    'definitions': {
        'Tournament': {
            'title': 'Tournament',
            'description': 'This references a Tournament',
            'type': 'object',
            'properties': {
                'id': {
                    'title': 'Id',
                    'type': 'integer'
                },
                'name': {
                    'title': 'Name',
                    'type': 'string'
                },
                'created_at': {
                    'title': 'Created At',
                    'description': 'The date-time the Tournament record was created at',
                    'type': 'string',
                    'format': 'date-time'
                }
            }
        }
    }
}
```

---

TITLE: Implementing OneToOne Relationship in Python with Tortoise ORM
DESCRIPTION: Example showing how to define a OneToOneField relationship between models using Tortoise ORM. The field definition includes cascade delete behavior and a related name for reverse lookup.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_15

LANGUAGE: python
CODE:

```
event: fields.OneToOneRelation[Event] = fields.OneToOneField(
    "models.Event", on_delete=fields.CASCADE, related_name="address"
)
```

---

TITLE: Initializing Tortoise Models for Pydantic Integration in Python
DESCRIPTION: Demonstrates how to initialize Tortoise ORM models for use with Pydantic model creators. This is necessary to establish relationships between models before creating Pydantic models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_9

LANGUAGE: python
CODE:

```
from tortoise import Tortoise

Tortoise.init_models(["__main__"], "models")
# Now lets try again
Tournament_Pydantic = pydantic_model_creator(Tournament)
```

---

TITLE: Creating a Pydantic List Model for Querysets
DESCRIPTION: Generating a Pydantic model to handle querysets (lists of Tortoise models). This uses pydantic_queryset_creator to create a model that can serialize multiple Tournament instances at once.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_5

LANGUAGE: python
CODE:

```
from tortoise.contrib.pydantic import pydantic_queryset_creator

Tournament_Pydantic_List = pydantic_queryset_creator(Tournament)
```

---

TITLE: Creating and Serializing Tortoise ORM Objects to JSON in Python
DESCRIPTION: Demonstrates how to create Tournament and Event objects in an async context and serialize them using the Pydantic models created earlier. Shows how relationships are included in the serialized output.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_12

LANGUAGE: python
CODE:

```
# Create objects
tournament = await Tournament.create(name="New Tournament")
event = await Event.create(name="The Event", tournament=tournament)

# Serialise Tournament
tourpy = await Tournament_Pydantic.from_tortoise_orm(tournament)

>>> print(tourpy.model_dump_json())
{
    "id": 1,
    "name": "New Tournament",
    "created_at": "2020-03-02T07:23:27.731656",
    "events": [
        {
            "id": 1,
            "name": "The Event",
            "created_at": "2020-03-02T07:23:27.732492"
        }
    ]
}
```

---

TITLE: Pytest Configuration for Tortoise ORM
DESCRIPTION: Setting up Tortoise ORM for pytest in a conftest.py file, including database initialization and cleanup using fixtures.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/unittest.rst#2025-04-20_snippet_3

LANGUAGE: python3
CODE:

```
import os
import pytest
from tortoise.contrib.test import finalizer, initializer

@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(["tests.testmodels"], db_url=db_url, app_label="models")
    request.addfinalizer(finalizer)
```

---

TITLE: Date Field Filtering by Year in Tortoise ORM
DESCRIPTION: Demonstrates filtering by date components like year. This example filters Teams created in 2020 using the year filter modifier on the created_at field.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_11

LANGUAGE: python
CODE:

```
await Team.filter(created_at__year=2020)
```

---

TITLE: Using Custom Manager in Tortoise ORM Queries
DESCRIPTION: Demonstrates practical usage of custom managers in Tortoise ORM, showing how different managers affect query results. Examples include creating objects and querying them using both default and custom managers.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/manager.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
m1 = await ManagerModel.create()
m2 = await ManagerModel.create(status=1)

self.assertEqual(await ManagerModel.all().count(), 1)
self.assertEqual(await ManagerModel.all_objects.count(), 2)

self.assertIsNone(await ManagerModel.get_or_none(pk=m1.pk))
self.assertIsNotNone(await ManagerModel.all_objects.get_or_none(pk=m1.pk))
self.assertIsNotNone(await ManagerModel.get_or_none(pk=m2.pk))
```

---

TITLE: Using Subquery Expressions in Tortoise ORM Queries
DESCRIPTION: Demonstrates the use of Subquery expressions in both filter() and annotate() operations. This example shows how to use subqueries to filter and annotate Tournament models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/expressions.rst#2025-04-20_snippet_6

LANGUAGE: python
CODE:

```
from tortoise.expressions import Subquery

await Tournament.annotate(ids=Subquery(Tournament.all().limit(1).values("id"))).values("ids", "id")
await Tournament.filter(pk=Subquery(Tournament.filter(pk=t1.pk).values("id"))).first()
```

---

TITLE: Custom SSL Configuration for PostgreSQL Connection
DESCRIPTION: Shows how to create and configure a custom SSL context for PostgreSQL database connection with verbose initialization
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/databases.rst#2025-04-20_snippet_1

LANGUAGE: python3
CODE:

```
# Here we create a custom SSL context
import ssl
ctx = ssl.create_default_context()
# And in this example we disable validation...
# Please don't do this. Look at the official Python ``ssl`` module documentation
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Here we do a verbose init
await Tortoise.init(
    config={
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "database": None,
                    "host": "127.0.0.1",
                    "password": "moo",
                    "port": 54321,
                    "user": "postgres",
                    "ssl": ctx  # Here we pass in the SSL context
                }
            }
        },
        "apps": {
            "models": {
                "models": ["some.models"],
                "default_connection": "default",
            }
        },
    }
)
```

---

TITLE: Fetching related objects asynchronously in Tortoise ORM
DESCRIPTION: Shows how to fetch related objects using the asynchronous API through a relation defined by a ForeignKeyField's related_name.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_14

LANGUAGE: python
CODE:

```
events = await tournament.events.all()
```

---

TITLE: Accessing and Using Database Connections in Tortoise ORM
DESCRIPTION: This code snippet demonstrates how to access and use database connections in Tortoise ORM. It shows the initialization of Tortoise with a SQLite database, retrieving the connection object, and executing a query. The example also includes error handling for potential operational errors.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/connections.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
# connections is a singleton instance of the ConnectionHandler class and serves as the
# entrypoint to access all connection management APIs.
from tortoise import connections


# Assume that this is the Tortoise configuration used
await Tortoise.init(
    {
        "connections": {
            "default": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {"file_path": "example.sqlite3"},
            }
        },
        "apps": {
            "events": {"models": ["__main__"], "default_connection": "default"}
        },
    }
)

conn: BaseDBAsyncClient = connections.get("default")
try:
    await conn.execute_query('SELECT * FROM "event"')
except OperationalError:
    print("Expected it to fail")
```

---

TITLE: Using Conditional Test Skipping Based on Database Capabilities
DESCRIPTION: Shows how to write tests that only run on specific database dialects using the requireCapability decorator. This allows writing database-specific tests that will be skipped when running against unsupported database types.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_19

LANGUAGE: python
CODE:

```
@requireCapability(dialect='sqlite')
async def test_run_sqlite_only(self):
    ...
```

---

TITLE: Using Select For Update in Tortoise ORM
DESCRIPTION: The select_for_update() method locks selected rows for the duration of a transaction. Optional parameters include nowait, skip_locked, and of to control locking behavior.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_12

LANGUAGE: python
CODE:

```
queryset.select_for_update(nowait=True, skip_locked=False, of=None)
```

---

TITLE: Creating a Custom BloomIndex for PostgreSQL in Tortoise ORM
DESCRIPTION: Example of extending the PostgreSQLIndex class to create a BloomIndex specialized for PostgreSQL. This minimal implementation only requires setting the INDEX_TYPE constant.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/indexes.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
class BloomIndex(PostgreSQLIndex):
    INDEX_TYPE = "BLOOM"
```

---

TITLE: Using Values Method for Efficient Queries in Tortoise ORM
DESCRIPTION: Demonstrates using the values() method to create more efficient queries that return dictionaries instead of model instances. This reduces the number of database queries needed.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_7

LANGUAGE: python
CODE:

```
# This will return list of dicts with keys 'id', 'name', 'tournament_name' and
# 'tournament_name' will be populated by name of related tournament.
# And it will be done in one query
events = await Event.filter(id__in=[1,2,3]).values('id', 'name', tournament_name='tournament__name')
```

---

TITLE: Primary Key Field Definition in Python
DESCRIPTION: Examples of defining different types of primary key fields in Tortoise ORM models including IntField, CharField and UUIDField.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_10

LANGUAGE: python
CODE:

```
id = fields.IntField(pk=True)

checksum = fields.CharField(pk=True)

guid = fields.UUIDField(pk=True)
```

---

TITLE: Setting default ordering in Tortoise ORM
DESCRIPTION: Shows how to set default ordering for model queries using the ordering option in the Meta class with a list of field names.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_9

LANGUAGE: python
CODE:

```
ordering = ["name", "-score"]
```

---

TITLE: Performing Bulk Insert Operations in Tortoise-ORM
DESCRIPTION: Shows how to use the bulk_create method to efficiently insert multiple records at once. This method optimizes insert performance but may result in incomplete references in Python since it only ensures minimum DB field population.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_17

LANGUAGE: python
CODE:

```
User.bulk_create([
    User(name="...", email="..."),
    User(name="...", email="...")
])
```

---

TITLE: Using Command-line Interface with Quart and Tortoise-ORM
DESCRIPTION: Example commands for running a Quart application integrated with Tortoise-ORM. Shows how to view available commands, generate database schemas, and start the development server.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples/quart.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
QUART_APP=main quart
        ...
        Commands:
          generate-schemas  Populate DB with Tortoise-ORM schemas.
          run               Start and run a development server.
          shell             Open a shell within the app context.

# To generate schemas
QUART_APP=main quart generate-schemas

# To run
QUART_APP=main quart run
```

---

TITLE: Defining a Router Class in Python for Tortoise ORM
DESCRIPTION: This snippet demonstrates how to create a basic Router class with db_for_read and db_for_write methods. These methods determine which database connection to use for read and write operations respectively.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/router.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
class Router:
    def db_for_read(self, model: Type[Model]):
        return "slave"

    def db_for_write(self, model: Type[Model]):
        return "master"
```

---

TITLE: Initializing Tortoise ORM with Configuration in Python
DESCRIPTION: Example showing how to initialize Tortoise ORM with a SQLite database and specify app models. The code demonstrates the proper initialization pattern after a breaking change in version 0.10.0, including database connection setup and schema generation.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_13

LANGUAGE: python
CODE:

```
async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
```

---

TITLE: Using RawSQL Expression in Tortoise ORM
DESCRIPTION: The RawSQL expression allows embedding raw SQL within Tortoise ORM queries. This provides flexibility when the standard ORM query builders are insufficient for specific database operations.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
RawSQL("expression")
```

---

TITLE: Running FastAPI Application with Uvicorn
DESCRIPTION: This command starts a FastAPI application using Uvicorn server with auto-reload enabled. It assumes the main application is defined in a file named 'main.py' with an 'app' object.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/examples/fastapi/README.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
uvicorn main:app --reload
```

---

TITLE: Using Case-When in Tortoise ORM
DESCRIPTION: The Case-When support allows for conditional logic directly in database queries, similar to SQL CASE statements. This enables more complex filtering and transformation at the database level.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_5

LANGUAGE: python
CODE:

```
Case().when(condition, then_value).else_(default_value)
```

---

TITLE: Cloning Model Instances in Tortoise ORM
DESCRIPTION: The clone() method creates a copy of a model instance in memory. This is useful for creating new records based on existing ones. The method accepts an optional pk parameter to set a specific primary key value.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_9

LANGUAGE: python
CODE:

```
new_instance = instance.clone()
# or
new_instance = instance.clone(pk=new_value)
```

---

TITLE: Running Tortoise-ORM Starlette Example Application
DESCRIPTION: Command to run the main.py file which demonstrates the Tortoise-ORM integration with Starlette. This executes the example application that likely uses the register_tortoise utility.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/examples/starlette/README.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
python3 main.py
```

---

TITLE: Serializing a Tortoise ORM Queryset with Pydantic
DESCRIPTION: Demonstrating the serialization of a queryset (collection of model instances) using Pydantic. Shows the output of both model_dump() and model_dump_json() methods on a list model, including how default ordering is respected.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_7

LANGUAGE: python
CODE:

```
>>> print(tourpy.model_dump())
{
    'root': [
        {
            'id': 2,
            'name': 'Another',
            'created_at': datetime.datetime(2020, 3, 2, 6, 53, 39, 776504)
        },
        {
            'id': 3,
            'name': 'Last Tournament',
            'created_at': datetime.datetime(2020, 3, 2, 6, 53, 39, 776848)
        },
        {
            'id': 1,
            'name': 'New Tournament',
            'created_at': datetime.datetime(2020, 3, 2, 6, 53, 39, 776211)
        }
    ]
}
>>> print(tourpy.model_dump_json())
[
    {
        "id": 2,
        "name": "Another",
        "created_at": "2020-03-02T06:53:39.776504"
    },
    {
        "id": 3,
        "name": "Last Tournament",
        "created_at": "2020-03-02T06:53:39.776848"
    },
    {
        "id": 1,
        "name": "New Tournament",
        "created_at": "2020-03-02T06:53:39.776211"
    }
]
```

---

TITLE: Case-Insensitive Filtering in Tortoise ORM
DESCRIPTION: Shows how to use filter modifiers for case-insensitive string comparison. This example filters teams whose names contain 'CON' regardless of case.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_10

LANGUAGE: python
CODE:

```
teams = await Team.filter(name__icontains='CON')
```

---

TITLE: Setting up unique_together in Tortoise ORM
DESCRIPTION: Shows the syntax for setting up compound unique indexes using the unique_together option in the Meta class with different formats of specification.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_7

LANGUAGE: python
CODE:

```
unique_together=("field_a", "field_b")
unique_together=(("field_a", "field_b"), )
unique_together=(("field_a", "field_b"), ("field_c", "field_d", "field_e"))
```

---

TITLE: Running Tortoise-ORM Sanic Example
DESCRIPTION: Command to execute the main Python script that demonstrates the Tortoise-ORM and Sanic integration. This command runs the 'main.py' file using Python 3.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/examples/sanic/README.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
python3 main.py
```

---

TITLE: JSON Schema Output for Tournament Model with PydanticMeta Configuration
DESCRIPTION: Shows the JSON schema output of a Tournament Pydantic model with custom PydanticMeta configuration. The schema includes computed fields and excludes the created_at field as specified in PydanticMeta.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_16

LANGUAGE: json
CODE:

```
{
    "title": "Tournament",
    "description": "This references a Tournament",
    "type": "object",
    "properties": {
        "id": {
            "title": "Id",
            "type": "integer"
        },
        "name": {
            "title": "Name",
            "type": "string"
        },
        "events": {
            "title": "Events",
            "description": "The Tournament this happens in",
            "type": "array",
            "items": {
                "$ref": "#/definitions/Event"
            }
        },
        "name_length": {
            "title": "Name Length",
            "description": "Computes length of name",
            "type": "integer"
        },
        "events_num": {
            "title": "Events Num",
            "description": "Computes team size.",
            "type": "integer"
        }
    },
    "definitions": {
        "Event": {
            "title": "Event",
            "description": "This references an Event in a Tournament",
            "type": "object",
            "properties": {
                "id": {
                    "title": "Id",
                    "type": "integer"
                },
                "name": {
                    "title": "Name",
                    "type": "string"
                }
            }
        }
    }
```

---

TITLE: Getting Timezone-Aware Datetime in Tortoise ORM
DESCRIPTION: Example of obtaining a timezone-aware datetime using Tortoise's utility function instead of the native Python datetime. This approach ensures proper timezone handling within the ORM's context.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/timezone.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
tortoise.timezone.now()
```

---

TITLE: Starting TortoiseCLI Interactive Shell with Environment Config
DESCRIPTION: Shows how to start the TortoiseCLI interactive shell after setting the configuration via an environment variable.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/cli.rst#2025-04-20_snippet_4

LANGUAGE: shell
CODE:

```
tortoise-cli shell
```

---

TITLE: Schema Generation with Tortoise ORM
DESCRIPTION: Demonstrates how to set up a SQLite connection, initialize Tortoise ORM, and generate the database schema. This shows the earlier method of schema generation before the simplified API was introduced.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_22

LANGUAGE: python
CODE:

```
from tortoise import Tortoise
from tortoise.backends.sqlite.client import SqliteClient
from tortoise.utils import generate_schema

client = SqliteClient(db_name)
await client.create_connection()
Tortoise.init(client)
await generate_schema(client)
```

---

TITLE: Defining Models in Tortoise ORM with Python
DESCRIPTION: This snippet demonstrates how to define a model class in Tortoise ORM. It shows the creation of a Tournament model with an integer primary key and a text field, following the object-oriented approach of Tortoise ORM.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/index.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise.models import Model
from tortoise import fields

class Tournament(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
```

---

TITLE: Model Update or Create Example
DESCRIPTION: Usage of Model.update_or_create() method for atomic update or insert operations
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_5

LANGUAGE: Python
CODE:

```
await Model.update_or_create(defaults={}, **kwargs)
```

---

TITLE: Using Native Python Datetime (Not Recommended for Tortoise ORM)
DESCRIPTION: Example of using Python's native datetime function, which is not recommended in Tortoise ORM contexts as it lacks timezone awareness.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/timezone.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
datetime.datetime.now()
```

---

TITLE: Using TestCase Class with Tortoise ORM
DESCRIPTION: Example of creating test classes with Tortoise ORM's test utilities, including regular tests, async tests, skipped tests, and tests expected to fail.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/unittest.rst#2025-04-20_snippet_0

LANGUAGE: python3
CODE:

```
from tortoise.contrib import test

class TestSomething(test.TestCase):
    def test_something(self):
        ...

    async def test_something_async(self):
        ...

    @test.skip('Skip this')
    def test_skip(self):
        ...

    @test.expectedFailure
    def test_something(self):
        ...
```

---

TITLE: Importing MySQL-specific Fields in Tortoise ORM
DESCRIPTION: Imports the GeometryField and UUIDField classes from the tortoise.contrib.mysql.fields module. These fields provide MySQL-specific data types for use in Tortoise ORM models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/mysql.rst#2025-04-20_snippet_1

LANGUAGE: Python
CODE:

```
from tortoise.contrib.mysql.fields import GeometryField, UUIDField
```

---

TITLE: Configuring PyLint Plugin for Tortoise ORM
DESCRIPTION: Configuration snippet showing how to enable the Tortoise ORM PyLint plugin in a .pylintrc file. This plugin helps PyLint better understand Tortoise ORM Models and Fields that use MetaClasses.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/linters.rst#2025-04-20_snippet_0

LANGUAGE: ini
CODE:

```
load-plugins=tortoise.contrib.pylint
```

---

TITLE: Defining a Tortoise Model with Default Ordering
DESCRIPTION: Creating a Tortoise ORM model with default ordering metadata. This model includes a Meta class that defines the default ordering by the name field, which will be used by the Pydantic serializer.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_4

LANGUAGE: python
CODE:

```
from tortoise import fields
from tortoise.models import Model

class Tournament(Model):
    """
    This references a Tournament
    """
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100)
    #: The date-time the Tournament record was created at
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        # Define the default ordering
        #  the pydantic serialiser will use this to order the results
        ordering = ["name"]
```

---

TITLE: Configuring Router in Tortoise ORM Initialization
DESCRIPTION: This snippet shows how to configure a router in Tortoise ORM. It includes setting up multiple database connections and specifying the router in the configuration dictionary or as a separate parameter in Tortoise.init().
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/router.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
config = {
    "connections": {"master": "sqlite:///tmp/test.db", "slave": "sqlite:///tmp/test.db"},
    "apps": {
        "models": {
            "models": ["__main__"],
            "default_connection": "master",
        }
    },
    "routers": ["path.Router"],
    "use_tz": False,
    "timezone": "UTC",
}
await Tortoise.init(config=config)
# or
routers = config.pop('routers')
await Tortoise.init(config=config, routers=routers)
```

---

TITLE: Async Iteration Over Foreign Key Relationship
DESCRIPTION: Demonstrates how to asynchronously iterate over related events using a Foreign Key relationship in Tortoise ORM.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_15

LANGUAGE: python3
CODE:

```
async for event in tournament.events:
    ...
```

---

TITLE: Green Test Runner Configuration for Tortoise ORM
DESCRIPTION: Configuration example for the Green test runner using initializer and finalizer in a .green file.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/unittest.rst#2025-04-20_snippet_2

LANGUAGE: ini
CODE:

```
initializer = tortoise.contrib.test.env_initializer
finalizer = tortoise.contrib.test.finalizer
```

---

TITLE: Documenting Tortoise ORM Models with Docstrings and Comments for Schema Generation
DESCRIPTION: Example showing how to add documentation to Tortoise ORM models using docstrings and special comments. These are used as documentation and DDL descriptions in the database schema.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_13

LANGUAGE: python
CODE:

```
class Something(Model):
    """
    A Docstring.

    Some extra info.
    """

    # A regular comment
    name = fields.CharField(max_length=50)
    #: A docstring comment
    chars = fields.CharField(max_length=50, description="Some chars")
    #: A docstring comment
    #: Some more detail
    blip = fields.CharField(max_length=50)

# When looking at the describe model:
{
    "description": "A Docstring.",
    "docstring": "A Docstring.\n\nSome extra info.",
    ...
    "data_fields": [
        {
            "name": "name",
            ...
            "description": null,
            "docstring": null
        },
        {
            "name": "chars",
            ...
            "description": "Some chars",
            "docstring": "A docstring comment"
        },
        {
            "name": "blip",
            ...
            "description": "A docstring comment",
            "docstring": "A docstring comment\nSome more detail"
        }
    ]
}
```

---

TITLE: Using **models** Variable for Model Discovery Override in Python
DESCRIPTION: Demonstrates how to override the automatic model discovery mechanism in Tortoise-ORM by defining a **models** variable in your models module. This allows explicit control over which models are used during schema generation.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_16

LANGUAGE: python
CODE:

```
# In yourapp.models.py
__models__ = [User, Post, Comment]  # Only these models will be used by generate_schema()
```

---

TITLE: Defining Tortoise ORM Examples Table of Contents in reStructuredText
DESCRIPTION: This code snippet defines the structure for the Tortoise ORM examples documentation using reStructuredText. It sets up a table of contents with links to various example pages, including basic usage and integration with frameworks like FastAPI, Quart, Sanic, Starlette, AIOHTTP, and BlackSheep.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples.rst#2025-04-20_snippet_0

LANGUAGE: reStructuredText
CODE:

```
.. _examples:

========
Examples
========

.. toctree::
   :maxdepth: 3

   examples/basic
   examples/pydantic
   examples/fastapi
   examples/quart
   examples/sanic
   examples/starlette
   examples/aiohttp
   examples/blacksheep
```

---

TITLE: Implementing SQL Syntax Highlighting with Pygments in Tortoise Logging
DESCRIPTION: Creates a custom logging formatter that adds SQL syntax highlighting using Pygments library. The formatter specifically targets SQL queries logged by tortoise.db_client and applies PostgreSQL syntax coloring.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/logging.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
import logging

from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.sql import PostgresLexer

postgres = PostgresLexer()
terminal_formatter = TerminalFormatter()


class PygmentsFormatter(logging.Formatter):
    def __init__(
        self,
        fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
        datefmt="%H:%M:%S",
    ):
        self.datefmt = datefmt
        self.fmt = fmt
        logging.Formatter.__init__(self, None, datefmt)

    def format(self, record: logging.LogRecord):
        """Format the logging record with slq's syntax coloration."""
        own_records = {
            attr: val
            for attr, val in record.__dict__.items()
            if not attr.startswith("_")
        }
        message = record.getMessage()
        name = record.name
        asctime = self.formatTime(record, self.datefmt)

        if name == "tortoise.db_client":
            if (
                record.levelname == "DEBUG"
                and not message.startswith("Created connection pool")
                and not message.startswith("Closed connection pool")
            ):
                message = highlight(message, postgres, terminal_formatter).rstrip()

        own_records.update(
            {
                "message": message,
                "name": name,
                "asctime": asctime,
            }
        )

        return self.fmt.format(**own_records)



# Then replace the formatter above by the following one
fmt = PygmentsFormatter(
    fmt="{asctime} - {name}:{lineno} - {levelname} - {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

---

TITLE: Annotating QuerySet with Coalesce Function in Python
DESCRIPTION: This snippet demonstrates how to use the Coalesce function to annotate a QuerySet in Tortoise ORM. It adds a new attribute 'clean_desc' to each SomeModel instance, containing the annotated data.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/functions.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
results = await SomeModel.filter(...).annotate(clean_desc=Coalesce("desc", "N/A"))
```

---

TITLE: Model Relationship Definition Example (Python)
DESCRIPTION: Code example from the changelog showing M2M field usage with create_unique_index parameter
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
M2MField(create_unique_index=True)
```

---

TITLE: Simplified model inheritance example in Tortoise ORM
DESCRIPTION: Shows a minimal model definition that inherits from multiple mixins and a base model without defining additional fields or a Meta class.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_6

LANGUAGE: python
CODE:

```
class RoleModel(TimestampMixin, NameMixin, MyAbstractBaseModel):
    pass
```

---

TITLE: URL Encoding Password for Database Connection
DESCRIPTION: Demonstrates how to URL encode special characters in database passwords using urllib
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/databases.rst#2025-04-20_snippet_0

LANGUAGE: python3
CODE:

```
>>> import urllib.parse
>>> urllib.parse.quote_plus("kx%jj5/g")
'kx%25jj5%2Fg'
```

---

TITLE: ReStructuredText Changelog Formatting
DESCRIPTION: ReStructuredText formatted changelog documenting version changes, bug fixes, and new features for Tortoise ORM. The document uses RST headings, sections, and bullet points to organize version information.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_0

LANGUAGE: rst
CODE:

```
=========
Changelog
=========

.. rst-class:: emphasize-children

0.25
====

0.25.0
------
Fixed
^^^^^
- Fix `pydantic_model_creator` incompatibility with Pydantic 2.11 (#1925)

Changed
^^^^^^^
- Skip database selection if the router is not configured to improve performance (#1915)
- `.values()`, `.values_list()` and `.only()` cannot be used together (#1923)

Added
^^^^^
- `.only` supports selecting related fields, e.g. `.only("related__field")` (#1923)
```

---

TITLE: Using Concat Function in Tortoise ORM
DESCRIPTION: The Concat function allows concatenating multiple string fields or values in MySQL and PostgreSQL databases. This is useful for combining text fields in query results.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_6

LANGUAGE: python
CODE:

```
Concat("field1", "field2")
```

---

TITLE: Importing Tortoise-ORM FastAPI Integration Module
DESCRIPTION: This snippet shows how to import the Tortoise-ORM FastAPI integration module. The RegisterTortoise class from this module can be used to set up and clean up Tortoise-ORM in a FastAPI application's lifespan context.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/fastapi.rst#2025-04-20_snippet_0

LANGUAGE: Python
CODE:

```
from tortoise.contrib.fastapi import RegisterTortoise
```

---

TITLE: Schema Generation in Tortoise ORM with SQLite
DESCRIPTION: Example of schema generation in Tortoise ORM using SQLite client. This demonstrates how to create a database connection, initialize Tortoise, and generate the schema, introduced in version 0.3.0.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_16

LANGUAGE: python
CODE:

```
from tortoise import Tortoise
from tortoise.backends.sqlite.client import SqliteClient
from tortoise.utils import generate_schema

client = SqliteClient(db_name)
await client.create_connection()
Tortoise.init(client)
await generate_schema(client)
```

---

TITLE: Defining RST Documentation Structure with TOC Tree
DESCRIPTION: Sphinx documentation configuration using RST format to create a table of contents tree with maximum depth of 4 levels, organizing all major Tortoise ORM documentation sections.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/reference.rst#2025-04-20_snippet_0

LANGUAGE: rst
CODE:

```
.. toctree::
   :maxdepth: 4

   setup
   databases
   models
   fields
   indexes
   timezone
   schema
   query
   manager
   functions
   expressions
   transactions
   connections
   exceptions
   signals
   migration
   validators
   logging
   router
   cli
```

---

TITLE: Importing MySQL-specific Indexes in Tortoise ORM
DESCRIPTION: Imports the FullTextIndex and SpatialIndex classes from the tortoise.contrib.mysql.indexes module. These classes provide MySQL-specific indexing capabilities for Tortoise ORM models.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/mysql.rst#2025-04-20_snippet_0

LANGUAGE: Python
CODE:

```
from tortoise.contrib.mysql.indexes import FullTextIndex, SpatialIndex
```

---

TITLE: Field Definition Example (Python)
DESCRIPTION: Example showing renamed field arguments for primary key and database index
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
Field(primary_key=True, db_index=True)
```

---

TITLE: Configuring RST Documentation for Tortoise ORM Exceptions
DESCRIPTION: ReStructuredText configuration for automatically generating documentation for the tortoise.exceptions module. Includes all members, undocumented members, and inheritance information.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/exceptions.rst#2025-04-20_snippet_0

LANGUAGE: rst
CODE:

```
.. automodule:: tortoise.exceptions
    :members:
    :undoc-members:
    :show-inheritance:
```

---

TITLE: Running Quart Commands with Tortoise-ORM Integration
DESCRIPTION: This snippet demonstrates how to use Quart CLI commands with Tortoise-ORM integration. It shows commands for listing available options, generating schemas, and running the development server.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/quart.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
QUART_APP=main quart
        ...
        Commands:
          generate-schemas  Populate DB with Tortoise-ORM schemas.
          run               Start and run a development server.
          shell             Open a shell within the app context.

# To generate schemas
QUART_APP=main quart generate-schemas

# To run
QUART_APP=main quart run
```

---

TITLE: QuerySet Select For Update Example
DESCRIPTION: Demonstration of select_for_update() method with additional parameters
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_6

LANGUAGE: Python
CODE:

```
queryset.select_for_update(nowait=True, skip_locked=True, of=[])
```

---

TITLE: Configuring Basic Tortoise ORM Logging in Python
DESCRIPTION: Sets up basic logging configuration for Tortoise ORM with custom formatting. Configures both tortoise.db_client for SQL query logging and tortoise for runtime logging at DEBUG level.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/logging.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
import logging

fmt = logging.Formatter(
    fmt="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)

logger_tortoise = logging.getLogger("tortoise")
logger_tortoise.setLevel(logging.DEBUG)
logger_tortoise.addHandler(sh)
```

---

TITLE: Creating Multiple Model Instances for List Serialization
DESCRIPTION: Creating multiple Tournament model instances to demonstrate list serialization. This code creates three different tournament records that will be queried and serialized as a list.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/pydantic.rst#2025-04-20_snippet_6

LANGUAGE: python
CODE:

```
# Create objects
await Tournament.create(name="New Tournament")
await Tournament.create(name="Another")
await Tournament.create(name="Last Tournament")

tourpy = await Tournament_Pydantic_List.from_queryset(Tournament.all())
```

---

TITLE: Aerich Init Command Help
DESCRIPTION: Help information for the init command showing available options for initializing Aerich configuration.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_2

LANGUAGE: shell
CODE:

```
> aerich init -h

Usage: aerich init [OPTIONS]

  Initialize aerich config and create migrations folder.

Options:
  -t, --tortoise-orm TEXT  Tortoise-ORM config dict location, like
                          `settings.TORTOISE_ORM`.  [required]
  --location TEXT          Migrations folder.  [default: ./migrations]
  -s, --src_folder TEXT    Folder of the source, relative to the project root.
  -h, --help               Show this message and exit.
```

---

TITLE: Using Rand/Random Function in Tortoise ORM
DESCRIPTION: The Rand/Random function in the contrib module provides random value generation at the database level. This can be used for random sorting or selection of records.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_7

LANGUAGE: python
CODE:

```
Rand()
```

---

TITLE: Aerich Initialization Example
DESCRIPTION: Example of initializing Aerich with a specific Tortoise-ORM configuration.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_3

LANGUAGE: shell
CODE:

```
> aerich init -t tests.backends.mysql.TORTOISE_ORM

Success create migrate location ./migrations
Success generate config file aerich.ini
```

---

TITLE: Filtering Events with Rating Threshold in Tortoise ORM
DESCRIPTION: A simple query example that returns all events with a rating greater than 5. This demonstrates the basic filtering capability in Tortoise ORM.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
await Event.filter(rating__gt=5)
```

---

TITLE: Early Initialization of Tortoise ORM Models Without Database Connection
DESCRIPTION: Example demonstrating how to initialize Tortoise ORM models without connecting to a database, useful for schema generation or model introspection.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_14

LANGUAGE: python
CODE:

```
# Lets say you defined your models in "some/models.py", and "other/ddef.py"
# And you are going to use them in the "model" namespace:
Tortoise.init_models(["some.models", "other.ddef"], "models")

# Now the models will have relationships built, so introspection of schema will be comprehensive
```

---

TITLE: Aerich Database Initialization
DESCRIPTION: Command to initialize the database and create migration folders.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_4

LANGUAGE: shell
CODE:

```
> aerich init-db

Success create app migrate location ./migrations/models
Success generate schema for app "models"
```

---

TITLE: Using Model Docstrings for Field Documentation in Python
DESCRIPTION: Example showing how docstrings and comments preceding field definitions are used as descriptions in Tortoise ORM models. The model includes regular comments, docstring comments, and explicitly described fields.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_7

LANGUAGE: python
CODE:

```
class Something(Model):
    """
    A Docstring.

    Some extra info.
    """

    # A regular comment
    name = fields.CharField(max_length=50)
    #: A docstring comment
    chars = fields.CharField(max_length=50, description="Some chars")
    #: A docstring comment
    #: Some more detail
    blip = fields.CharField(max_length=50)

# When looking at the describe model:
{
    "description": "A Docstring.",
    "docstring": "A Docstring.\n\nSome extra info.",
    ...
    "data_fields": [
        {
            "name": "name",
            ...
            "description": null,
            "docstring": null
        },
        {
            "name": "chars",
            ...
            "description": "Some chars",
            "docstring": "A docstring comment"
        },
        {
            "name": "blip",
            ...
            "description": "A docstring comment",
            "docstring": "A docstring comment\nSome more detail"
        }
    ]
}
```

---

TITLE: Downgrade Command Help
DESCRIPTION: Help information for the downgrade command showing available options.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_7

LANGUAGE: shell
CODE:

```
> aerich init -h

Usage: aerich downgrade [OPTIONS]

  Downgrade to specified version.

Options:
  -v, --version INTEGER  Specified version, default to last.  [default: -1]
  -h, --help             Show this message and exit.
```

---

TITLE: Importing the Model class in Tortoise ORM
DESCRIPTION: Shows how to import the base Model class from Tortoise ORM, which is required for all model definitions.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/models.rst#2025-04-20_snippet_0

LANGUAGE: python
CODE:

```
from tortoise.models import Model
```

---

TITLE: Importing MySQL Full-Text Search in Tortoise ORM
DESCRIPTION: Imports the SearchCriterion class from the tortoise.contrib.mysql.search module. This class enables full-text search capabilities for MySQL databases in Tortoise ORM.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/mysql.rst#2025-04-20_snippet_2

LANGUAGE: Python
CODE:

```
from tortoise.contrib.mysql.search import SearchCriterion
```

---

TITLE: Downgrade Migration Example
DESCRIPTION: Example of downgrading to a previous migration version.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_8

LANGUAGE: shell
CODE:

```
> aerich downgrade

Success downgrade 1_202029051520102929_drop_column.json
```

---

TITLE: Creating Migration Example
DESCRIPTION: Example of creating a new migration with a specific name.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_5

LANGUAGE: shell
CODE:

```
> aerich migrate --name drop_column

Success migrate 1_202029051520102929_drop_column.json
```

---

TITLE: Installing Optional Dependencies for Tortoise ORM with Bash
DESCRIPTION: Command to install all optional performance-enhancing dependencies for Tortoise ORM using pip.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/getting_started.rst#2025-04-20_snippet_0

LANGUAGE: bash
CODE:

```
pip install tortoise-orm[accel]
```

---

TITLE: Using SQL Method in Tortoise ORM QuerySet
DESCRIPTION: The .sql() method on QuerySet returns the SQL representation of the query without executing it. This is useful for debugging or understanding the actual SQL being generated by the ORM.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_10

LANGUAGE: python
CODE:

```
sql_query = queryset.sql()
```

---

TITLE: Upgrade Migration Example
DESCRIPTION: Example of upgrading to the latest migration version.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_6

LANGUAGE: shell
CODE:

```
> aerich upgrade

Success upgrade 1_202029051520102929_drop_column.json
```

---

TITLE: Running FastAPI with Tortoise ORM using uvicorn
DESCRIPTION: Command to run a FastAPI application with Tortoise ORM using uvicorn server with auto-reload enabled for development.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples/fastapi.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
uvicorn main:app --reload
```

---

TITLE: Nose2 Configuration for Tortoise ORM
DESCRIPTION: Example of configuring Nose2 to work with Tortoise ORM tests, showing both command line options and configuration file setup.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/contrib/unittest.rst#2025-04-20_snippet_4

LANGUAGE: ini
CODE:

```
[unittest]
plugins = tortoise.contrib.test.nose2

[tortoise]
# Must specify at least one module path
db-module =
    tests.testmodels
# You can optionally override the db_url here
db-url = sqlite://testdb-{}.sqlite
```

---

TITLE: Running AIOHTTP Example with Tortoise ORM
DESCRIPTION: Command to execute the AIOHTTP example application that uses Tortoise ORM. This command runs the main.py file which sets up the AIOHTTP server with Tortoise ORM integration.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples/aiohttp.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
python3 main.py
```

---

TITLE: Defining Custom TruncMonth Function in Python for Tortoise ORM
DESCRIPTION: This example shows how to define a custom TruncMonth function in Tortoise ORM. It uses CustomFunction from pypika_tortoise to create a DATE_FORMAT function that can be used in queries.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/functions.rst#2025-04-20_snippet_1

LANGUAGE: python
CODE:

```
from pypika_tortoise import CustomFunction
from tortoise.expressions import F, Function

class TruncMonth(Function):
    database_func = CustomFunction("DATE_FORMAT", ["name", "dt_format"])

sql = Task.all().annotate(date=TruncMonth('created_at', '%Y-%m-%d')).values('date').sql()
print(sql)
# SELECT DATE_FORMAT(`created_at`,'%Y-%m-%d') `date` FROM `task`
```

---

TITLE: Aerich CLI Help Command
DESCRIPTION: Shows the main help menu and available commands for the Aerich CLI tool.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
> aerich -h

Usage: aerich [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version      Show the version and exit.
  -c, --config TEXT  Config file.  [default: pyproject.toml]
  --app TEXT         Tortoise-ORM app name.
  -h, --help         Show this message and exit.

Commands:
  downgrade  Downgrade to specified version.
  heads      Show currently available heads (unapplied migrations).
  history    List all migrations.
  init       Initialize aerich config and create migrations folder.
  init-db    Generate schema and generate app migration folder.
  inspectdb  Prints the current database tables to stdout as Tortoise-ORM...
  migrate    Generate a migration file for the current state of the models.
  upgrade    Upgrade to specified migration version.
```

---

TITLE: Running Starlette Example with Tortoise ORM
DESCRIPTION: Command to execute the Starlette example application that uses Tortoise ORM. This runs the main.py file which sets up the Starlette app with Tortoise ORM integration.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples/starlette.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
python3 main.py
```

---

TITLE: Starting TortoiseCLI Interactive Shell with Config File
DESCRIPTION: Shows how to start an interactive shell for TortoiseORM using a configuration file specified with the -c option.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/cli.rst#2025-04-20_snippet_2

LANGUAGE: shell
CODE:

```
tortoise-cli -c settings.TORTOISE_ORM shell
```

---

TITLE: Running the Sanic Example Application
DESCRIPTION: Command to execute the Sanic example application that demonstrates Tortoise ORM integration.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples/sanic.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
python3 main.py
```

---

TITLE: Running Tortoise-ORM with Quart via Command Line
DESCRIPTION: Shell commands for setting up and running a Quart application integrated with Tortoise-ORM. Demonstrates how to view available commands, generate database schemas, and launch a development server using the QUART_APP environment variable.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/examples/quart/README.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
QUART_APP=main quart
        ...
        Commands:
          generate-schemas  Populate DB with Tortoise-ORM schemas.
          run               Start and run a development server.
          shell             Open a shell within the app context.

    # To generate schemas
    QUART_APP=main quart generate-schemas

    # To run
    QUART_APP=main quart run
```

---

TITLE: Setting TortoiseORM Config via Environment Variable
DESCRIPTION: Demonstrates how to set the TortoiseORM configuration using an environment variable, allowing for easier command execution.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/cli.rst#2025-04-20_snippet_3

LANGUAGE: shell
CODE:

```
export TORTOISE_ORM=settings.TORTOISE_ORM
```

---

TITLE: Running the Tortoise-ORM aiohttp Example in Shell
DESCRIPTION: Command to execute the main application file that demonstrates the Tortoise-ORM aiohttp integration. This runs the example application which likely contains the integration code using register_tortoise.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/examples/aiohttp/README.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
python3 main.py
```

---

TITLE: Filtering Events by Name Prefix in Tortoise ORM
DESCRIPTION: Demonstrates filtering records by a name prefix using the 'startswith' modifier. Returns all events with names starting with 'FIFA'.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/query.rst#2025-04-20_snippet_3

LANGUAGE: python
CODE:

```
await Event.filter(name__startswith='FIFA')
```

---

TITLE: Running a BlackSheep Application with Tortoise ORM
DESCRIPTION: Command to start a BlackSheep server with uvicorn, enabling hot reload for development.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/examples/blacksheep.rst#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
uvicorn server:app --reload
```

---

TITLE: View Pending Migrations
DESCRIPTION: Example of viewing pending migrations that need to be applied.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_10

LANGUAGE: shell
CODE:

```
> aerich heads

1_202029051520102929_drop_column.json
```

---

TITLE: Migration History Example
DESCRIPTION: Example of viewing migration history.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/migration.rst#2025-04-20_snippet_9

LANGUAGE: shell
CODE:

```
> aerich history

1_202029051520102929_drop_column.json
```

---

TITLE: Conditional Test Skip Based on Database Capability
DESCRIPTION: Example of using the requireCapability decorator to conditionally skip tests based on database driver capabilities.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_12

LANGUAGE: python
CODE:

```
@requireCapability(dialect='sqlite')
async def test_run_sqlite_only(self):
    ...
```

---

TITLE: Running a BlackSheep Server with Tortoise-ORM Integration
DESCRIPTION: This command starts a BlackSheep server with Tortoise-ORM integration using Uvicorn. The '--reload' flag enables auto-reloading for development purposes.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/examples/blacksheep/README.md#2025-04-20_snippet_0

LANGUAGE: sh
CODE:

```
uvicorn server:app --reload
```

---

TITLE: Importing Tortoise ORM Signals Module
DESCRIPTION: This code snippet demonstrates how to import the signals module from Tortoise ORM. It uses the automodule directive to automatically generate documentation for the module, including all members, undocumented members, and inheritance information.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/signals.rst#2025-04-20_snippet_0

LANGUAGE: Python
CODE:

```
.. automodule:: tortoise.signals
    :members:
    :undoc-members:
    :show-inheritance:
```

---

TITLE: Displaying TortoiseCLI Help Information
DESCRIPTION: Shows how to use the help command to display usage information, options, and available commands for tortoise-cli.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/cli.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
> tortoise-cli -h                                                                                                                                                                 23:59:38
Usage: tortoise-cli [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version      Show the version and exit.
  -c, --config TEXT  TortoiseORM config dictionary path, like settings.TORTOISE_ORM
  -h, --help         Show this message and exit.

Commands:
  shell  Start an interactive shell.
```

---

TITLE: Running Makefile Commands for Tortoise ORM Development
DESCRIPTION: This snippet shows the output of the Makefile help command, displaying the available targets for common development operations such as updating dependencies, running tests, and formatting code.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CONTRIBUTING.rst#2025-04-20_snippet_0

LANGUAGE: shell
CODE:

```
Tortoise ORM development makefile

usage: make <target>
Targets:
    up          Updates dev/test dependencies
    deps        Ensure dev/test dependencies are installed
    check       Checks that build is sane
    lint        Reports all linter violations
    test        Runs all tests
    docs        Builds the documentation
    style       Auto-formats the code
```

---

TITLE: Defining Documentation Structure with Sphinx toctree in RST
DESCRIPTION: Sphinx table of contents directive that organizes the Tortoise ORM documentation into logical sections. It includes the main index, getting started guide, reference documentation, examples, contribution guidelines, and project information.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/toc.rst#2025-04-20_snippet_0

LANGUAGE: rst
CODE:

```
.. toctree::
   :maxdepth: 5
   :includehidden:

   index
   getting_started
   reference
   examples
   contrib
   CHANGELOG
   roadmap
   CONTRIBUTING
   CONTRIBUTORS
```

---

TITLE: Using ON CONFLICT in Tortoise ORM
DESCRIPTION: ON CONFLICT support in INSERT statements allows for handling duplicate records gracefully. This feature enables 'upsert' operations that update existing records or insert new ones based on conflict detection.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/CHANGELOG.rst#2025-04-20_snippet_8

LANGUAGE: python
CODE:

```
Model.create(**values, on_conflict=["field"])
```

---

TITLE: Bulk Create Model Instances in Python
DESCRIPTION: Example of using bulk_create() to efficiently insert multiple model instances at once. Note that this is optimized for performance but may result in incomplete references.
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_11

LANGUAGE: python
CODE:

```
User.bulk_create([
    User(name="...", email="..."),
    User(name="...", email="...")
])
```

---

TITLE: Array Field Operations Example (Python)
DESCRIPTION: Implementation of array field operations including contains, contained_by, overlap and len
SOURCE: https://github.com/tortoise/tortoise-orm/blob/develop/docs/CHANGELOG.rst#2025-04-20_snippet_2

LANGUAGE: python
CODE:

```
__contains__, __contained_by__, __overlap__ and __len__ for ArrayField
```
