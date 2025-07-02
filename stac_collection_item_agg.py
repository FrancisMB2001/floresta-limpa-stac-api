# import json
# import pystac
# import os
#
# # CONFIG
# CATALOG_PATH = "C:/Users/Francisco/Desktop/Tese/floresta-limpa-pystac/stac-catalog-generator/stac_catalog_dev/catalog.json"
# COLLECTIONS_OUTPUT_FILE = "collections.json"
# ITEMS_OUTPUT_FILE = "items.json"
#
# # Load the catalog
# catalog = pystac.Catalog.from_file(CATALOG_PATH)
# print("Catalog loaded:", catalog)
#
# # Extract collections and items
# collections = list(catalog.get_all_collections())
# items = list(catalog.get_all_items())
#
# print(f"Number of collections: {len(collections)}")
# print(f"Number of items: {len(items)}")
#
# # Convert collections and items to dictionaries
# collections_dict = [collection.to_dict() for collection in collections]
# items_dict = [item.to_dict() for item in items]
#
# # Save collections to a JSON file
# with open(COLLECTIONS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
#     json.dump(collections_dict, f, indent=4)
#
# # Save items to a JSON file
# with open(ITEMS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
#     json.dump(items_dict, f, indent=4)
#
# print(f"Collections saved to {COLLECTIONS_OUTPUT_FILE}")
# print(f"Items saved to {ITEMS_OUTPUT_FILE}")

import json
import pystac
import os
from dotenv import load_dotenv

load_dotenv()

# CONFIG
# CATALOG_PATH = "C:/Users/Francisco/Desktop/Tese/floresta-limpa-pystac/stac-catalog-generator/stac_catalog_dev/catalog.json"
# COLLECTIONS_OUTPUT_FILE = "collections.json"
# ITEMS_OUTPUT_FILE = "items.json"
CATALOG_PATH = os.getenv("CATALOG_PATH", "/media/servers/STAC/stac_catalog/catalog.json")
COLLECTIONS_OUTPUT_FILE = os.getenv("COLLECTIONS_OUTPUT_FILE", "collections.json")
ITEMS_OUTPUT_FILE = os.getenv("ITEMS_OUTPUT_FILE", "items.json")

# Load the catalog
catalog = pystac.Catalog.from_file(CATALOG_PATH)
print("Catalog loaded:", catalog)

# Extract collections and items
collections = list(catalog.get_all_collections())
items = list(catalog.get_all_items())
# items = catalog.get_all_items()

print(f"Number of collections: {len(collections)}")
print(f"Number of items before removing duplicates: {len(items)}")

# Convert collections to dictionaries
collections_dict = [collection.to_dict() for collection in collections]

unique_items = {each.id : each for each in items}


# Process items and remove duplicates based on 'id'
# seen_ids = set()
# unique_items_dict = []
# 
# for item in items:
#     item_id = item.id
#     if item_id not in seen_ids:
#         seen_ids.add(item_id)
#         unique_items_dict.append(item.to_dict())
#     else:
#         print(f"Duplicate item skipped: {item_id}")

print(f"Number of unique items after removing duplicates: {len(unique_items)}")

# Save collections to a JSON file
with open(COLLECTIONS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(collections_dict, f, indent=4)

# Save unique items to a JSON file
# with open(ITEMS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
#     json.dump(unique_items_dict, f, indent=4)

# Create a list of items using __geo_interface__ for efficiency
item_list = [item.__geo_interface__ for item in unique_items.values()]

# Save unique items to a JSON file using json.dump
with open(ITEMS_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(item_list, f, indent=4)

print(f"Collections saved to {COLLECTIONS_OUTPUT_FILE}")
print(f"Unique items saved to {ITEMS_OUTPUT_FILE}")

