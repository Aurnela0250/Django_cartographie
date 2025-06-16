from tortoise import Tortoise


async def init_tortoise(config):
    await Tortoise.init(
        config=config,
    )
    # Generate the schema only if it doesn't exist
    # await Tortoise.generate_schemas()


async def close_tortoise():
    await Tortoise.close_connections()
