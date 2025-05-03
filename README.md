# Floresta Limpa PgSTAC + STAC-FastAPI Service
## Overview
Project containing the following:
- Docker Compose that sets up a container network with a PgSTAC database with migrations applied to work with STAC FastAPI and the STAC Fast-API itself. 
- Python script (stac_collection_item_agg.py) to aggregate all items and collections into two singular JSON files from a static catalog. This format is needed to import STAC items into the PgSTAC database. 
- Python script (stac_pgstac_importer.py) to import STAC items and collections to a PgSTAC database by providing a items.json and a collections.json. 

## Setup 
1. Set up environment variables (See variable config section) through a .env file. 
2. Set up the docker containers (`docker compose up -d`)
3. Provide the `items.json` and `collections.json` files that contain the STAC items and collections respectively. Possible to generate these with the `stac_collection_item_agg.py` (`$ python stac_collection_item_agg.py`) by providing a static STAC catalog.  
4. Import the STAC items and collections using the `stac_pgstac_importer.py` script. (`$ python stac_pgstac_importer.py`)
5. Access the STAC API (default host is localhost:6006)

## Variables Configuration
### .env file 
* CATALOG_PATH - Path where the static STAC catalog is located. 
* COLLECTIONS_OUTPUT_FILE - Output location and name of the JSON file with the collections.
* ITEMS_OUTPUT_FILE - Output location and name of the JSON file with the items.
* PGSTAC_DATABASE_URI - PgSTAC DSN URI, used to connect to the database. Format is the following: postgresql://{USERNAME}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}

### docker-compose.yml Default Environment Variables
If needed, the docker compose yaml file can be altered to change the default variables.

PgSTAC database variables:
* POSTGRES_USER=postgres
* POSTGRES_PASSWORD=pgpass
* POSTGRES_DB=pgstac
* ports: "6005:5432" (Note: Only change the first port if outside access needs to be changed, not the second one since that is used for docker internal network.)

PyPgSTAC Migrate (Has to have the same as the variables in the pgstac container to connect):
* POSTGRES_USER=postgres
* POSTGRES_PASS=pgpass
* POSTGRES_DBNAME=pgstac
* POSTGRES_HOST=pgstac-db
* POSTGRES_PORT=5432

STAC-FastAPI (Has to have the same as the variables in the pgstac container to connect):
- APP_HOST=0.0.0.0
- APP_PORT=8080
- ENVIRONMENT=production
- POSTGRES_HOST_READER=pgstac-db
- POSTGRES_HOST_WRITER=pgstac-db
- POSTGRES_PORT=5432
- POSTGRES_USER=postgres
- POSTGRES_PASS=pgpass
- POSTGRES_DBNAME=pgstac
- ENABLED_EXTENSIONS=filter,transactions,sort,query
- ports: "6006:8080" (Note: Only change the first port if outside access needs to be changed, not the second one since that is used for docker internal network.)

