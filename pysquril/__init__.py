"""
pysquril - Python Structured URI Query Language

A library for versioned, queryable, and auditable document-oriented datastores
with support for PostgreSQL and SQLite backends.

Public API:
-----------
Synchronous backends (always available):
    - SqliteBackend: SQLite implementation
    - PostgresBackend: PostgreSQL implementation
    - GenericBackend: Base sync backend

Asynchronous backends (requires: pip install pysquril[async]):
    - AsyncSqliteBackend: Async SQLite implementation
    - AsyncPostgresBackend: Async PostgreSQL implementation
    - AsyncGenericBackend: Base async backend

Query parsing:
    - UriQuery: URI query parser

Example (sync):
    from pysquril import SqliteBackend, sqlite_init

    engine = sqlite_init(":memory:")
    backend = SqliteBackend(engine)
    backend.initialise()
    backend.table_insert("users", {"id": 1, "name": "Alice"})

Example (async):
    from pysquril import AsyncSqliteBackend, async_sqlite_init
    import asyncio

    async def main():
        engine = await async_sqlite_init(":memory:")
        backend = AsyncSqliteBackend(engine)
        await backend.initialise()
        result = await backend.table_insert("users", {"id": 1, "name": "Alice"})
        await backend.engine.close()
        return result

    asyncio.run(main())
"""

# Always available: sync backends
from pysquril.backends import (
    SqliteBackend,
    PostgresBackend,
    GenericBackend,
    AuditTransaction,
    DatabaseBackend,
    BackendCore,
)

# Always available: parser
from pysquril.parser import UriQuery

# Conditional: async backends (only if async dependencies installed)
try:
    from pysquril._backends_async import (
        AsyncSqliteBackend,
        AsyncPostgresBackend,
        AsyncGenericBackend,
    )

    __all__ = [
        # Sync backends
        "SqliteBackend",
        "PostgresBackend",
        "GenericBackend",
        # Async backends
        "AsyncSqliteBackend",
        "AsyncPostgresBackend",
        "AsyncGenericBackend",
        # Core classes
        "AuditTransaction",
        "DatabaseBackend",
        "BackendCore",
        # Parser
        "UriQuery",
    ]
except ImportError:
    # Async dependencies not installed
    __all__ = [
        # Sync backends
        "SqliteBackend",
        "PostgresBackend",
        "GenericBackend",
        # Core classes
        "AuditTransaction",
        "DatabaseBackend",
        "BackendCore",
        # Parser
        "UriQuery",
    ]
