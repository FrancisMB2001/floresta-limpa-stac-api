import json
from pypgstac.db import PgstacDB
from pypgstac.load import Loader
import os
from dotenv import load_dotenv

load_dotenv()
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
pgstac.connect()
pgstac.open() 

try:
    print("Clearing existing items and collections...")
    with pgstac.connection.cursor() as cur:
        print("Clearing items and collections...")
        cur.execute("DELETE FROM items;")
        cur.execute("DELETE FROM collections;")
    pgstac.connection.commit()
    print("Tables cleared successfully.")

    loader = Loader(pgstac)

    # LOAD COLLECTIONS
    print("Loading new collections...")
    with open(COLLECTIONS_JSON_PATH, 'r', encoding='utf-8') as f:
        collections_data = json.load(f)
    
    if isinstance(collections_data, list):
        loader.load_collections(COLLECTIONS_JSON_PATH)
        print(f"Loaded {len(collections_data)} collections.")
    else:
        print("Error: The collections data is not in the expected format.")
        raise ValueError("Collections data is not a list")

    # LOAD ITEMS
    print("Loading new items...")
    with open(ITEMS_JSON_PATH, 'r', encoding='utf-8') as f:
        items_data = json.load(f)
    
    if isinstance(items_data, list):
        # Debug: Check for items missing collection field
        missing_collection_count = 0
        for i, item in enumerate(items_data):
            if 'collection' not in item:
                if missing_collection_count == 0:  # Only print first occurrence
                    print(f"Warning: Item at index {i} missing 'collection' field:")
                    print(f"Item ID: {item.get('id', 'NO_ID')}")
                    print(f"Item keys: {list(item.keys())}")
                missing_collection_count += 1
        
        if missing_collection_count > 0:
            print(f"Warning: {missing_collection_count} items missing 'collection' field")
        
        loader.load_items(ITEMS_JSON_PATH)
        print(f"Loaded {len(items_data)} items.")
    else:
        print("Error: The items data is not in the expected format.")
        raise ValueError("Items data is not a list")
    
    print("Data import completed successfully!")

except Exception as e:
    print(f"Error during data import: {e}")
    # Rollback any partial changes
    pgstac.connection.rollback()
    raise

finally:
    pgstac.close()  # Close the connection
    print("Database connection closed.")
