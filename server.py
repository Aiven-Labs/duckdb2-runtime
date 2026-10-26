"""DuckDB Quack server with the compose Postgres instance attached as `pg`."""
import os
import threading

import duckdb

# /data is a compose volume locally; on platforms without one (Aiven Runtime) it's
# just a directory in the container filesystem, so make sure it exists.
DB_PATH = os.environ.get("DUCKDB_PATH", "/data/local.duckdb")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
con = duckdb.connect(DB_PATH)
con.load_extension("postgres")
con.load_extension("quack")

# DATABASE_URL is a libpq URI (postgresql://user:pass@host:port/db?sslmode=...).
# If unset, libpq falls back to PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE.
con.execute("ATTACH ? AS pg (TYPE postgres)", [os.environ.get("DATABASE_URL", "")])

# Bound to the container's interface; compose only publishes it on host loopback,
# so TLS is off. Put a TLS-terminating proxy in front for anything non-local.
con.execute(
    "CALL quack_serve('quack:0.0.0.0:9494', allow_other_hostname = true, disable_ssl = true, token = ?)",
    [os.environ["QUACK_TOKEN"]],
)
print("DuckDB Quack server listening on :9494 (postgres attached as 'pg')", flush=True)
threading.Event().wait()
