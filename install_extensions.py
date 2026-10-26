"""Build-time: bake extensions into the image so startup needs no network."""
import duckdb

con = duckdb.connect()
con.execute("INSTALL postgres")
con.execute("SET allow_extension_repositories = 'allowed'")
con.execute("CREATE EXTENSION REPOSITORY IF NOT EXISTS query_farm WITH PREFIX 'https://duckdb-extensions.query.farm'")
con.execute("INSTALL httpserver FROM query_farm")
