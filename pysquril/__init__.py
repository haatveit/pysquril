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

from pysquril._backends_sync import (
    SqliteBackend,
    PostgresBackend,
    GenericBackend,
)
from pysquril._backends_core import (
    AuditTransaction,
    DatabaseBackend,
)
from pysquril._connection import (
    sqlite_init,
    postgres_init,
    sqlite_session,
    postgres_session,
)

from pysquril.parser import UriQuery

__all__ = [
    # Sync backends
    "SqliteBackend",
    "PostgresBackend",
    "GenericBackend",
    # Core classes
    "AuditTransaction",
    "DatabaseBackend",
    # Parser
    "UriQuery",
    # Connection util functions
    "sqlite_init",
    "postgres_init",
    "sqlite_session",
    "postgres_session",
]

# Conditional: async backends (only if async dependencies installed)
try:
    from pysquril._backends_async import (
        AsyncSqliteBackend,
        AsyncPostgresBackend,
        AsyncGenericBackend,
    )
    from pysquril._connection import (
        async_sqlite_init,
        async_postgres_init,
        async_sqlite_session,
        async_postgres_session,
    )

    __all__.extend(
        [
            # Classes
            "AsyncSqliteBackend",
            "AsyncPostgresBackend",
            "AsyncGenericBackend",
            # Connection util functions
            "async_sqlite_init",
            "async_postgres_init",
            "async_sqlite_session",
            "async_postgres_session",
        ]
    )
except ImportError:
    pass
