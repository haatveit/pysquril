# pysquril tests

This directory contains the test suite for pysquril, including tests for both synchronous and asynchronous backends.

## Prerequisites

### Python dependencies

Install the development dependencies:

```bash
poetry install -E async
```

This installs:

* `pytest` - Test framework
* `pytest-asyncio` - Async test support
* `pytest-postgresql` - Automatic PostgreSQL test server
* `psycopg2` - PostgreSQL driver (sync)
* `aiosqlite` - Async SQLite support
* `psycopg` + `psycopg-pool` - Async PostgreSQL support

### PostgreSQL binaries

**IMPORTANT:** PostgreSQL binaries must be in your `$PATH` for the test fixtures to work.

The following binaries are required:

* `pg_ctl` - PostgreSQL server control
* `initdb` - Database cluster initialization
* `postgres` - PostgreSQL server

#### macOS (Homebrew)

```bash
brew install postgresql@16

# Add to PATH (add this to your ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"

# Verify
which pg_ctl
# Should output: /opt/homebrew/opt/postgresql@16/bin/pg_ctl
```

#### Linux (Debian/Ubuntu)

```bash
sudo apt install postgresql-16

# Add to PATH if needed
export PATH="/usr/lib/postgresql/16/bin:$PATH"

# Verify
which pg_ctl
# Should output: /usr/lib/postgresql/16/bin/pg_ctl
```

#### Linux (Fedora/RHEL)

```bash
sudo dnf install postgresql-server

# PATH is usually configured automatically
# Verify
which pg_ctl
```

## Running tests

### Run all tests

```bash
poetry run pytest tests/
```

### Run with verbose output

```bash
poetry run pytest tests/ -v
```

### Run specific test file

```bash
poetry run pytest tests/test_backends.py
```

### Run specific test class or method

```bash
poetry run pytest tests/test_backends.py::TestSqliteBackend
poetry run pytest tests/test_backends.py::TestSqliteBackend::test_audit
```

### Run with coverage

```bash
poetry run pytest tests/ --cov=pysquril --cov-report=html
```

## Test structure

* **`test_backends.py`** - Main test suite for sync backends (SQLite & PostgreSQL)
* **`test_data.py`** - Sample data used across tests
* **`conftest.py`** - Pytest fixtures and configuration

## How PostgreSQL testing works

The test suite uses `pytest-postgresql` to automatically:

1. **Start a temporary PostgreSQL server** on a random port when tests begin
2. **Create a test database** for each test module
3. **Clean up and shutdown** the server when tests complete

This means:

* No manual database setup required
* Tests run in complete isolation
* No conflicts with your local PostgreSQL installation
* Automatic cleanup - no leftover test data

The temporary server runs with optimized settings for speed:

* `fsync=off` - Skip disk syncs (safe for disposable test data)
* `synchronous_commit=off` - Async commits for faster tests
* `full_page_writes=off` - Skip full page writes

## Troubleshooting

### "pg_ctl: command not found"

PostgreSQL binaries are not in your PATH. Follow the installation instructions above and ensure `which pg_ctl` works.

### Tests fail with "connection refused"

The temporary PostgreSQL server failed to start. Check:

1. PostgreSQL binaries are in PATH
2. No other PostgreSQL instance is blocking the random port
3. You have permissions to create temp directories

### Import errors

Make sure you installed with the async extras:

```bash
poetry install -E async
```

## Writing new tests

When adding new tests:

1. **For sync backends**: Follow the pattern in `TestSqliteBackend` or `TestPostgresBackend`
2. **For async backends**: Create new test files with `@pytest.mark.asyncio` decorators
3. **Use fixtures**: `postgresql_proc`, `postgresql`, or `postgres_config` for PostgreSQL tests
4. **Test data**: Import from `test_data.py` for consistency

Example async test:

```python
import pytest
from pysquril import AsyncSqliteBackend

class TestAsyncSqliteBackend:
    @pytest.mark.asyncio
    async def test_insert_select(self):
        from pysquril._connection import async_sqlite_init

        backend = AsyncSqliteBackend()
        backend.engine = await async_sqlite_init(':memory:')
        await backend.initialise()

        await backend.table_insert('test', {'id': 1, 'name': 'Alice'})

        results = []
        async for row in backend.table_select('test', ''):
            results.append(row)

        assert len(results) == 1
        assert results[0]['name'] == 'Alice'
```
