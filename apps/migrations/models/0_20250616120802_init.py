from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "active" BOOL NOT NULL DEFAULT True,
    "email_verified" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "domains" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "establishment_types" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "formation_authorizations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "issued_date" DATE NOT NULL,
    "expiry_date" DATE,
    "status" VARCHAR(10) NOT NULL DEFAULT 'REQUESTED',
    "decree" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "levels" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "acronym" VARCHAR(50) UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "mentions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "domain_id" INT NOT NULL REFERENCES "domains" ("id") ON DELETE CASCADE,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "regions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "code" VARCHAR(50) UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "cities" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "region_id" INT NOT NULL REFERENCES "regions" ("id") ON DELETE CASCADE,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "sectors" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "city_id" INT NOT NULL REFERENCES "cities" ("id") ON DELETE CASCADE,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "establishments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "acronym" VARCHAR(50) UNIQUE,
    "address" VARCHAR(255) NOT NULL,
    "contacts" JSONB,
    "website" VARCHAR(255),
    "description" TEXT,
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "establishment_type_id" INT NOT NULL REFERENCES "establishment_types" ("id") ON DELETE CASCADE,
    "sector_id" INT NOT NULL REFERENCES "sectors" ("id") ON DELETE CASCADE,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "formations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "duration" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "authorization_id" INT REFERENCES "formation_authorizations" ("id") ON DELETE SET NULL,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "establishment_id" INT NOT NULL REFERENCES "establishments" ("id") ON DELETE CASCADE,
    "level_id" INT NOT NULL REFERENCES "levels" ("id") ON DELETE CASCADE,
    "mention_id" INT NOT NULL REFERENCES "mentions" ("id") ON DELETE CASCADE,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "annual_headcounts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "academic_year" INT NOT NULL,
    "students" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "success_rate" DOUBLE PRECISION,
    "created_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    "formation_id" INT NOT NULL REFERENCES "formations" ("id") ON DELETE CASCADE,
    "updated_by_id" BIGINT REFERENCES "users" ("id") ON DELETE SET NULL,
    CONSTRAINT "uid_annual_head_formati_e12728" UNIQUE ("formation_id", "academic_year")
);
CREATE TABLE IF NOT EXISTS "rates" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "rating" DOUBLE PRECISION NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "establishment_id" INT NOT NULL REFERENCES "establishments" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_rates_establi_1a836c" UNIQUE ("establishment_id", "user_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
