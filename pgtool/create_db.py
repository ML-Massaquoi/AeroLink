import psycopg

conn = psycopg.connect(
    "postgresql://aerolink:aerolink@127.0.0.1:5432/postgres", autocommit=True
)
with conn.cursor() as cur:
    cur.execute("SELECT datname FROM pg_database WHERE datname = 'aerolink'")
    if not cur.fetchone():
        cur.execute("CREATE DATABASE aerolink OWNER aerolink")
        print("database created")
    else:
        print("database exists")
conn.close()
