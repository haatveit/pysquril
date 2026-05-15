"""
Legacy imports for pysquril sync database backends, to support imports
like this:
    from pysquril.backends import SqliteBackend, PostgresBackend

The actual implementations are in internal modules:
- _backends_core: Shared business logic
- _backends_sync: Synchronous I/O implementations
- _connection: Connection management

This module re-exports everything to maintain backwards compatibility.
It will be removed in pysquril 2.0.
"""

# Import from internal modules
from pysquril import (
    AuditTransaction,
    DatabaseBackend,
    GenericBackend,
    SqliteBackend,
    PostgresBackend,
    sqlite_init,
    postgres_init,
    sqlite_session,
    postgres_session,
)

# Re-export functions and classes that used to be here for backwards compatibility
__all__ = [
    # Connection utilities
    "sqlite_init",
    "postgres_init",
    "sqlite_session",
    "postgres_session",
    # Core classes
    "AuditTransaction",
    "DatabaseBackend",
    # Sync backends
    "GenericBackend",
    "SqliteBackend",
    "PostgresBackend",
]
