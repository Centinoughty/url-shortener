from cassandra.cluster import Cluster
import os

cluster = Cluster([os.getenv("CASSANDRA_HOST", "cassandra")])
session = cluster.connect()

def init_db():
  session.execute("""
    CREATE KEYSPACE IF NOT EXISTS url_shortener
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
  """)

  session.set_keyspace("url_shortener")

  session.execute("""
    CREATE TABLE IF NOT EXISTS urls (
      short_url text PRIMARY KEY,
      original_url text,
      created_at timestamp
    )
  """)
