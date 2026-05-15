"""
DEPRECATED: This module will be removed in pysquril 2.0.

Import directly from the pysquril package instead:
    from pysquril import SqliteBackend, PostgresBackend

This module contains reexports of pysquril sync database backends symbols,
to support implementing applications with imports like these:
    from pysquril.backends import SqliteBackend, PostgresBackend

The actual implementations are in internal modules:
- _backends_core: Shared business logic
- _backends_sync: Synchronous I/O implementations
- _connection: Connection management

This module re-exports what used to be here to maintain backwards compatibility.
"""

import warnings

# Emit deprecation warning when this module is imported
warnings.warn(
    "Importing from 'pysquril.backends' is deprecated and will be removed in pysquril 2.0. "
    + "Import directly from 'pysquril' instead: from pysquril import SqliteBackend, PostgresBackend",
    DeprecationWarning,
    stacklevel=2,
)

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
