"""
Pytest configuration and fixtures for pysquril tests.

Provides fixtures for:
- Temporary PostgreSQL database for testing
- Async PostgreSQL database for async tests

Requirements:
- PostgreSQL binaries (pg_ctl, initdb, postgres) must be in your PATH
- Install PostgreSQL and ensure `which pg_ctl` works before running tests

Example setup:
  macOS (Homebrew): brew install postgresql@16
                    export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"
  Linux (Debian):   apt install postgresql-16
                    export PATH="/usr/lib/postgresql/16/bin:$PATH"
  Linux (Fedora):   dnf install postgresql-server
                    PATH usually configured automatically
"""

import os
import pytest
from pytest_postgresql import factories


# Create a PostgreSQL process fixture
# This starts a temporary PostgreSQL server that all tests can use
postgresql_proc = factories.postgresql_proc(
    host="127.0.0.1",  # Force TCP listening (important for macOS)
    port=None,  # Use any available port
    postgres_options="-h 127.0.0.1 -c fsync=off -c full_page_writes=off -c synchronous_commit=off",  # Fast settings for tests
)

postgresql = factories.postgresql("postgresql_proc")


# For backward compatibility with existing tests that use environment variables
@pytest.fixture(scope="module", autouse=True)
def set_postgres_env_vars(postgresql_proc):
    """
    Automatically set PostgreSQL environment variables for all tests in a module.

    This ensures existing tests that read from environment variables
    (like TestPostgresBackend) will use the temporary PostgreSQL instance.

    Uses module scope to set environment variables once per test module.
    """
    import psycopg2

    # Store original values
    original_env = {
        "PYSQURIL_POSTGRES_DB": os.environ.get("PYSQURIL_POSTGRES_DB"),
        "PYSQURIL_POSTGRES_USER": os.environ.get("PYSQURIL_POSTGRES_USER"),
        "PYSQURIL_POSTGRES_PASSWORD": os.environ.get("PYSQURIL_POSTGRES_PASSWORD"),
        "PYSQURIL_POSTGRES_HOST": os.environ.get("PYSQURIL_POSTGRES_HOST"),
        "PYSQURIL_POSTGRES_PORT": os.environ.get("PYSQURIL_POSTGRES_PORT"),
    }

    # Create the "tests" database using psycopg2
    conn = psycopg2.connect(
        host=postgresql_proc.host,
        port=postgresql_proc.port,
        user=postgresql_proc.user,
        dbname="postgres",  # Connect to default postgres database first
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Drop and create tests database
    try:
        cursor.execute("DROP DATABASE IF EXISTS tests")
        cursor.execute("CREATE DATABASE tests")
    except Exception:
        pass  # Database might not exist yet
    finally:
        cursor.close()
        conn.close()

    # Set environment variables to point to temporary database
    os.environ["PYSQURIL_POSTGRES_DB"] = "tests"
    os.environ["PYSQURIL_POSTGRES_USER"] = postgresql_proc.user
    os.environ["PYSQURIL_POSTGRES_PASSWORD"] = ""
    os.environ["PYSQURIL_POSTGRES_HOST"] = postgresql_proc.host
    os.environ["PYSQURIL_POSTGRES_PORT"] = str(postgresql_proc.port)

    yield

    # Restore original values
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture
def postgres_config(postgresql):
    """
    Provide PostgreSQL configuration dict for pysquril tests.

    Args:
        postgresql: The postgresql fixture from pytest-postgresql

    Returns:
        dict: Configuration dict with keys: dbname, user, pw, host
    """
    info = postgresql.info

    return {
        "dbname": info.dbname,
        "user": info.user,
        "pw": info.password or "",
        "host": info.host,
    }


@pytest.fixture
async def async_postgres_config(postgresql):
    """
    Provide PostgreSQL configuration for async tests.

    Same as postgres_config but explicitly marked as async-compatible.
    """
    info = postgresql.info

    return {
        "dbname": info.dbname,
        "user": info.user,
        "pw": info.password or "",
        "host": info.host,
    }
