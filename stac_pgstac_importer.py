import json
from pypgstac.db import PgstacDB
from pypgstac.load import Loader
import os

# CONFIG
# DB_DSN = "postgresql://postgres:pgpass@localhost:6005/pgstac"  # Database URI
# COLLECTIONS_JSON_PATH = "collections.json"  # Path to your collections JSON file
# ITEMS_JSON_PATH = "items.json"  # Path to your items JSON file
# os.environ["PGSTAC_DATABASE_URI"] = DB_DSN
DB_DSN = os.getenv("PGSTAC_DATABASE_URI", "postgresql://postgres:pgpass@localhost:6005/pgstac")
COLLECTIONS_JSON_PATH = os.getenv("COLLECTIONS_OUTPUT_FILE", "collections.json")
ITEMS_JSON_PATH = os.getenv("ITEMS_OUTPUT_FILE", "items.json")


# LOAD THE DATABASE
pgstac = PgstacDB(dsn=DB_DSN)
pgstac.connect()  # Connect to the database
pgstac.open()  # Open the database connection

# LOAD COLLECTIONS
with open(COLLECTIONS_JSON_PATH, 'r', encoding='utf-8') as f:
    collections_data = json.load(f)

if isinstance(collections_data, list):
    loader = Loader(pgstac)
    loader.load_collections(COLLECTIONS_JSON_PATH)
    print(f"Loaded {len(collections_data)} collections.")
else:
    print("Error: The collections data is not in the expected format.")

# LOAD ITEMS
with open(ITEMS_JSON_PATH, 'r', encoding='utf-8') as f:
    items_data = json.load(f)

if isinstance(items_data, list):
    loader.load_items(ITEMS_JSON_PATH)
    print(f"Loaded {len(items_data)} items.")
else:
    print("Error: The items data is not in the expected format.")

pgstac.close()  # Close the connection
