# duckdb-postgres

A [DuckDB Quack](https://duckdb.org/docs/2.0/quack/overview) server with a PostgreSQL database attached as `pg`. Run it with Docker Compose, then connect any number of DuckDB instances to it and query Postgres through DuckDB.

## What's in the box

| Service    | Image / build   | Host port        | Purpose                                                  |
|------------|-----------------|------------------|----------------------------------------------------------|
| `duckdb`   | built from `Dockerfile` | `127.0.0.1:9494` | DuckDB running `quack_serve`, with Postgres attached as `pg` |
| `postgres` | `postgres:18`   | `127.0.0.1:5432` | Postgres, seeded from `initdb/` (`users` and `orders` tables) |

The `duckdb` container reaches Postgres at `postgres:5432` on the compose network. `DATABASE_URL` is built from the `POSTGRES_*` variables in `compose.yaml`. Local DuckDB state lives in the `duckdata` volume (`/data/local.duckdb`).

## Run it

```sh
cp .env.example .env   # set POSTGRES_PASSWORD and QUACK_TOKEN
docker compose up --build
```

Secrets can also come from [fnox](https://github.com/jdx/fnox) instead of `.env`.

| Variable            | Required | Default    | Description                              |
|---------------------|----------|------------|------------------------------------------|
| `POSTGRES_PASSWORD` | yes      |            | Password for the Postgres container      |
| `QUACK_TOKEN`       | yes      |            | Token clients present (min. 4 characters) |
| `POSTGRES_USER`     | no       | `postgres` | Postgres user                            |
| `POSTGRES_DB`       | no       | `postgres` | Postgres database                        |

## Connect a client

From any DuckDB 2.0 instance that can reach the server:

```sql
INSTALL quack; LOAD quack;

ATTACH 'quack:localhost:9494' AS remote (TOKEN 'your-token');
CONNECT remote;                       -- plain SQL now runs on the server
SELECT * FROM pg.public.users LIMIT 5;
DISCONNECT;                           -- back to your local database
```

Or run a one-off query without attaching:

```sql
SELECT * FROM quack_query('quack:localhost:9494', 'SELECT count(*) FROM pg.public.orders', token = 'your-token');
```

All clients share the server's database and the attached `pg` catalog.

## Security

- The Quack port is published on host loopback only, and TLS is disabled (`disable_ssl = true` in `server.py`). The token travels in plaintext, so this setup is for local use.
- To serve clients on other machines, publish the port beyond loopback and turn TLS back on: drop `disable_ssl` for a self-signed certificate, or terminate TLS in a reverse proxy in front. See the [Quack docs](https://duckdb.org/docs/2.0/quack/overview).
- Don't commit `.env`. It is git-ignored.

## Files

- `server.py`: loads `postgres` and `quack`, attaches Postgres as `pg`, and starts `quack_serve` on `:9494`.
- `install_extensions.py`: installs the extensions at image build time so startup needs no network.
- `initdb/`: SQL that seeds the Postgres container on first start.
