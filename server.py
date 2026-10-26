"""DuckDB HTTP server with the compose Postgres instance attached as `pg`."""
import os
import threading

import duckdb

con = duckdb.connect("/data/local.duckdb")
con.load_extension("postgres")
con.execute("SET allow_extension_repositories = 'allowed'")
con.execute("CREATE EXTENSION REPOSITORY IF NOT EXISTS query_farm WITH PREFIX 'https://duckdb-extensions.query.farm'")
con.execute("LOAD httpserver FROM query_farm")

# DATABASE_URL is a libpq URI (postgresql://user:pass@host:port/db?sslmode=...).
# If unset, libpq falls back to PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE.
con.execute("ATTACH ? AS pg (TYPE postgres)", [os.environ.get("DATABASE_URL", "")])

con.execute("SELECT httpserve_start('0.0.0.0', 9999, ?)", [os.environ.get("DUCKDB_HTTP_AUTH", "")])
print("DuckDB HTTP server listening on :9999 (postgres attached as 'pg')", flush=True)
threading.Event().wait()
