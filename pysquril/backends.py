"""
Public API for pysquril database backends.

This module provides the public interface for synchronous database backends.
External applications should import from this module, not from internal
modules (those prefixed with underscore).

Usage:
    from pysquril.backends import SqliteBackend, PostgresBackend

The actual implementations are in internal modules:
- _backends_core: Shared business logic
- _backends_sync: Synchronous I/O implementations
- _connection: Connection management

This module re-exports everything to maintain backwards compatibility.
"""

# Import from internal modules
from pysquril._backends_core import (
    AuditTransaction,
    DatabaseBackend,
    BackendCore,
)
from pysquril._backends_sync import (
    GenericBackend,
    SqliteBackend,
    PostgresBackend,
)
from pysquril._connection import (
    sqlite_init,
    postgres_init,
    sqlite_session,
    postgres_session,
)

# Re-export everything for backwards compatibility
__all__ = [
    # Core classes
    "AuditTransaction",
    "DatabaseBackend",
    "BackendCore",
    # Sync backends
    "GenericBackend",
    "SqliteBackend",
    "PostgresBackend",
    # Connection utilities
    "sqlite_init",
    "postgres_init",
    "sqlite_session",
    "postgres_session",
]
