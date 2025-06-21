from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "establishments" DROP CONSTRAINT IF EXISTS "fk_establis_sectors_0e3b3afe";
        ALTER TABLE "establishments" RENAME COLUMN "sector_id" TO "city_id";
        ALTER TABLE "establishments" ALTER COLUMN "address" DROP NOT NULL;
        DROP TABLE IF EXISTS "sectors" CASCADE;
        ALTER TABLE "establishments" ADD CONSTRAINT "fk_establis_cities_eb015a75" FOREIGN KEY ("city_id") REFERENCES "cities" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "establishments" DROP CONSTRAINT IF EXISTS "fk_establis_cities_eb015a75";
        ALTER TABLE "establishments" RENAME COLUMN "city_id" TO "sector_id";
        ALTER TABLE "establishments" ALTER COLUMN "address" SET NOT NULL;
        ALTER TABLE "establishments" ADD CONSTRAINT "fk_establis_sectors_0e3b3afe" FOREIGN KEY ("sector_id") REFERENCES "sectors" ("id") ON DELETE CASCADE;"""
