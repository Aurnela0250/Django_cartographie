TITLE: Configuring TortoiseORM with Aerich Models
DESCRIPTION: Example configuration for TortoiseORM including Aerich models. This setup is required before using Aerich commands.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_1

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

TITLE: Configuring TortoiseORM with Aerich
DESCRIPTION: Example configuration for TortoiseORM that includes aerich.models, which is necessary for Aerich to work properly.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_2

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

TITLE: Multi-Database Configuration for TortoiseORM and Aerich
DESCRIPTION: Example configuration for using Aerich with multiple databases in a TortoiseORM setup.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_17

LANGUAGE: python
CODE:

```
tortoise_orm = {
    "connections": {
        "default": expand_db_url(db_url, True),
        "second": expand_db_url(db_url_second, True),
    },
    "apps": {
        "models": {"models": ["tests.models", "aerich.models"], "default_connection": "default"},
        "models_second": {"models": ["tests.models_second"], "default_connection": "second", },
    },
}
```

---

TITLE: Configuring TortoiseORM for Multiple Databases
DESCRIPTION: Example configuration for TortoiseORM with multiple database connections and apps.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_7

LANGUAGE: python
CODE:

```
tortoise_orm = {
    "connections": {
        "default": "postgres://postgres_user:postgres_pass@127.0.0.1:5432/db1",
        "second": "postgres://postgres_user:postgres_pass@127.0.0.1:5432/db2",
    },
    "apps": {
        "models": {"models": ["tests.models", "aerich.models"], "default_connection": "default"},
        "models_second": {"models": ["tests.models_second"], "default_connection": "second", },
    },
}
```

---

TITLE: Using Aerich in Python Application
DESCRIPTION: Example of how to use Aerich programmatically within a Python application using the Command class.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_8

LANGUAGE: python
CODE:

```
from aerich import Command

async with Command(tortoise_config=config, app='models') as command:
    await command.migrate('test')
    await command.upgrade()
```

---

TITLE: Programmatic Usage of Aerich in Python Code
DESCRIPTION: Example of using Aerich programmatically in Python code through the Command class rather than via the command line.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_18

LANGUAGE: python
CODE:

```
from aerich import Command

command = Command(tortoise_config=config, app='models')
await command.init()
await command.migrate('test')
```

---

TITLE: Initializing Aerich Configuration
DESCRIPTION: Shell command to initialize Aerich configuration file and migrations location.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_2

LANGUAGE: shell
CODE:

```
aerich init -t tests.backends.mysql.TORTOISE_ORM
```

---

TITLE: Initializing Aerich Configuration
DESCRIPTION: Example command to initialize Aerich with a specific TortoiseORM configuration module.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_4

LANGUAGE: shell
CODE:

```
> aerich init -t tests.backends.mysql.TORTOISE_ORM

Success create migrate location ./migrations
Success write config to pyproject.toml
```

---

TITLE: Initializing Database Schema with Aerich
DESCRIPTION: Command to initialize the database with the current schema defined in TortoiseORM models.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_5

LANGUAGE: shell
CODE:

```
> aerich init-db

Success create app migrate location ./migrations/models
Success generate schema for app "models"
```

---

TITLE: Initializing Database with Aerich
DESCRIPTION: Command to initialize the database and create migration locations for the specified Tortoise-ORM app.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_3

LANGUAGE: shell
CODE:

```
aerich init-db
```

---

TITLE: Creating a Migration with Aerich
DESCRIPTION: Command to create a new migration file with a specified name.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_4

LANGUAGE: shell
CODE:

```
aerich migrate --name drop_column
```

---

TITLE: Generating a Database Migration
DESCRIPTION: Command to create a migration file based on changes made to TortoiseORM models.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_6

LANGUAGE: shell
CODE:

```
> aerich migrate --name drop_column

Success migrate 1_202029051520102929_drop_column.py
```

---

TITLE: Upgrading Database to Latest Version
DESCRIPTION: Command to apply all pending migrations and upgrade the database to the latest version.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_5

LANGUAGE: shell
CODE:

```
aerich upgrade
```

---

TITLE: Upgrading Database to Latest Version
DESCRIPTION: Command to apply all pending migrations to bring the database to the latest schema version.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_7

LANGUAGE: shell
CODE:

```
> aerich upgrade

Success upgrade 1_202029051520102929_drop_column.py
```

---

TITLE: Downgrading Database to Previous Version
DESCRIPTION: Command to rollback the database to a previous migration version.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_6

LANGUAGE: shell
CODE:

```
aerich downgrade
```

---

TITLE: Downgrading Database Schema
DESCRIPTION: Command to downgrade the database to a specified version or to the previous version.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_9

LANGUAGE: shell
CODE:

```
> aerich downgrade

Success downgrade 1_202029051520102929_drop_column.py
```

---

TITLE: Inspecting a Specific Table
DESCRIPTION: Command to introspect a specific database table and save the generated TortoiseORM model to a file.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_14

LANGUAGE: shell
CODE:

```
aerich inspectdb -t user > models.py
```

---

TITLE: Inspecting All Database Tables
DESCRIPTION: Command to introspect all database tables and output TortoiseORM models to the console.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_13

LANGUAGE: shell
CODE:

```
aerich --app models inspectdb
```

---

TITLE: Viewing Pending Migrations
DESCRIPTION: Command to show which migrations should be applied but haven't been yet.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_11

LANGUAGE: shell
CODE:

```
> aerich heads

1_202029051520102929_drop_column.py
```

---

TITLE: Viewing Migration History
DESCRIPTION: Command to list all migration files that have been created.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_10

LANGUAGE: shell
CODE:

```
> aerich history

1_202029051520102929_drop_column.py
```

---

TITLE: Defining Unmanaged Model in TortoiseORM
DESCRIPTION: Example of how to define a model that should be ignored by Aerich migrations using the managed=False option in the Meta class.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_9

LANGUAGE: python
CODE:

```
class MyModel(Model):
    class Meta:
        managed = False
```

---

TITLE: Generated TortoiseORM Model from InspectDB
DESCRIPTION: Example of a TortoiseORM model automatically generated by the inspectdb command from a database table.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_16

LANGUAGE: python
CODE:

```
from tortoise import Model, fields


class Test(Model):
    date = fields.DateField(null=True, )
    datetime = fields.DatetimeField(auto_now=True, )
    decimal = fields.DecimalField(max_digits=10, decimal_places=2, )
    float = fields.FloatField(null=True, )
    id = fields.IntField(pk=True, )
    string = fields.CharField(max_length=200, null=True, )
    time = fields.TimeField(null=True, )
    tinyint = fields.BooleanField(null=True, )
```

---

TITLE: Example SQL Table Definition
DESCRIPTION: SQL definition of a test table with various data types that can be introspected by Aerich.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_15

LANGUAGE: sql
CODE:

```
CREATE TABLE `test`
(
    `id`       int            NOT NULL AUTO_INCREMENT,
    `decimal`  decimal(10, 2) NOT NULL,
    `date`     date                                    DEFAULT NULL,
    `datetime` datetime       NOT NULL                 DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `time`     time                                    DEFAULT NULL,
    `float`    float                                   DEFAULT NULL,
    `string`   varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `tinyint`  tinyint                                 DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `asyncmy_string_index` (`string`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci
```

---

TITLE: Installing Aerich with TOML support
DESCRIPTION: Command to install Aerich package with TOML support using pip.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README.md#2025-04-23_snippet_0

LANGUAGE: shell
CODE:

```
pip install "aerich[toml]"
```

---

TITLE: Installing Aerich via pip
DESCRIPTION: Command to install the Aerich package from PyPI using pip.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_0

LANGUAGE: shell
CODE:

```
pip install aerich
```

---

TITLE: Aerich Command Line Interface Usage
DESCRIPTION: Output of the help command showing all available Aerich commands and options.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_1

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
  heads      Show current available heads in migrate location.
  history    List all migrate items.
  init       Init config file and generate root migrate location.
  init-db    Generate schema and generate app migrate location.
  inspectdb  Introspects the database tables to standard output as...
  migrate    Generate migrate changes file.
  upgrade    Upgrade to specified version.
```

---

TITLE: Aerich Init Command Help
DESCRIPTION: Help output for the 'init' command which initializes the configuration file and migration directory.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_3

LANGUAGE: shell
CODE:

```
> aerich init -h

Usage: aerich init [OPTIONS]

  Init config file and generate root migrate location.

Options:
  -t, --tortoise-orm TEXT  Tortoise-ORM config module dict variable, like
                           settings.TORTOISE_ORM.  [required]
  --location TEXT          Migrate store location.  [default: ./migrations]
  -s, --src_folder TEXT    Folder of the source, relative to the project root.
  -h, --help               Show this message and exit.
```

---

TITLE: Downgrade Command Help
DESCRIPTION: Help output for the 'downgrade' command which reverts the database schema to a specified version.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_8

LANGUAGE: shell
CODE:

```
> aerich downgrade -h

Usage: aerich downgrade [OPTIONS]

  Downgrade to specified version.

Options:
  -v, --version INTEGER  Specified version, default to last.  [default: -1]
  -d, --delete           Delete version files at the same time.  [default:
                         False]

  --yes                  Confirm the action without prompting.
  -h, --help             Show this message and exit.
```

---

TITLE: InspectDB Command Help
DESCRIPTION: Help output for the 'inspectdb' command which generates TortoiseORM models from existing database tables.
SOURCE: https://github.com/tortoise/aerich/blob/dev/README_RU.md#2025-04-23_snippet_12

LANGUAGE: shell
CODE:

```
Usage: aerich inspectdb [OPTIONS]

  Introspects the database tables to standard output as TortoiseORM model.

Options:
  -t, --table TEXT  Which tables to inspect.
  -h, --help        Show this message and exit.
```
