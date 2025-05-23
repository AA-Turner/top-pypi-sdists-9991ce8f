from typing import Any

from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.postgresql.base import DatabaseWrapper

class DatabaseOperations(BaseDatabaseOperations):
    connection: DatabaseWrapper
    explain_options: frozenset[str]

    def compose_sql(self, sql: Any, params: Any) -> Any: ...
    def fetch_returned_insert_rows(self, cursor: Any) -> Any: ...
