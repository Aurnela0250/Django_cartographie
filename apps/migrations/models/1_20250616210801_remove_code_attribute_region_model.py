from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_regions_code_432d51";
        ALTER TABLE "regions" DROP COLUMN "code";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "regions" ADD "code" VARCHAR(50) UNIQUE;
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_regions_code_432d51" ON "regions" ("code");"""
