import os
import time
from typing import Any
from cassandra.cluster import Cluster, NoHostAvailable

class DBManager:
  def __init__(
    self,
    keyspace: str = "url_shortener",
    host: str | None = None,
    port: int | None = None
  ):
    """
    Initialize Cassandra connection.

    Args:
      keyspace (str):
        Cassandra keyspace name.

      cassandra_host (str | None):
        Cassandra host.
        Falls back to CASSANDRA_HOST env variable.
    """
    
    self.host = (
      host
      if host is not None
      else os.getenv("CASSANDRA_HOST", "cassandra")
    )

    self.port = (
      port
      if port is not None
      else int(os.getenv("CASSANDRA_PORT", "9042"))
    )

    self.keyspace = keyspace
    self.cluster: Cluster | None = None
    self.session = None


  def connect(self, max_retries: int = 30, delay_seconds: float = 2.0) -> None:
    """
    Connect to Cassandra with retry support for container startup races.
    """

    for attempt in range(1, max_retries + 1):
      try:
        self.cluster = Cluster([self.host], port=self.port)
        self.session = self.cluster.connect()
        return
      except NoHostAvailable:
        if self.cluster is not None:
          self.cluster.shutdown()
          self.cluster = None

        if attempt == max_retries:
          raise RuntimeError(
            f"Unable to connect to Cassandra at {self.host}:{self.port} "
            f"after {max_retries} attempts"
          )

        time.sleep(delay_seconds)


  def _ensure_session(self):
    if self.session is None:
      raise RuntimeError("Database session is not initialized. Call connect() first.")
    return self.session


  def create_keyspace(self, replication_factor: int = 1) -> None:
    """
    Create keyspace if not exists
    """
    
    query = f"""
      CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
      WITH replication = {{
        'class': 'SimpleStrategy',
        'replication_factor': {replication_factor}
      }}
    """

    session = self._ensure_session()
    session.execute(query)
    session.set_keyspace(self.keyspace)


  def use_keyspace(self) -> None:
    session = self._ensure_session()
    session.set_keyspace(self.keyspace)


  def create_table(self, table_name: str, schema: str) -> None:
    """
    Create table dynamically.

    Args:
      table_name (str):
        Table name.

      schema (str):
        Table schema definition.
    """
    
    query = f"""
      CREATE TABLE IF NOT EXISTS {table_name} (
        {schema}
      )
    """

    session = self._ensure_session()
    session.execute(query)


  def insert(self, table_name: str, columns:list[str], values: tuple[Any, ...]) -> None:
    """
    Insert into table dynamically.
    """

    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(values))

    query = f"""
      INSERT INTO {table_name} ({columns_str})
      VALUES ({placeholders})
    """

    session = self._ensure_session()
    session.execute(query, values)


  def select_one(self, table_name: str, where_clause: str, values: tuple[Any, ...]) -> None:
    """
    Fetch single row.
    """

    query = f"""
      SELECT * FROM {table_name}
      WHERE {where_clause}
      LIMIT 1
    """

    session = self._ensure_session()
    result = session.execute(query, values)

    return result.one()
  

  def delete(self, table_name: str, where_clause: str, values: tuple[Any, ...]) -> None:
    """
    Delete rows from table.
    """

    query = f"""
      DELETE FROM {table_name}
      WHERE {where_clause}
    """

    session = self._ensure_session()
    session.execute(query, values)
  

  def shutdown(self) -> None:
    """
    Close Cassandra connection cleanly.
    """

    if self.cluster is not None:
      self.cluster.shutdown()
      self.cluster = None
      self.session = None
