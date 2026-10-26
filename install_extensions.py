"""Build-time: bake extensions into the image so startup needs no network."""
import duckdb

con = duckdb.connect()
con.execute("INSTALL postgres")
con.execute("INSTALL quack")
