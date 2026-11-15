import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name('.env'))

POSTGRES_HOST = os.environ['PGHOST']
POSTGRES_PORT = int(os.environ['PGPORT'])
POSTGRES_DATABASE = os.environ['PGDATABASE']
POSTGRES_USER = os.environ['PGUSER']
POSTGRES_PASSWORD = os.environ['PGPASSWORD']

MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = int(os.environ['MONGO_PORT'])
MONGO_DATABASE = os.environ['MONGO_DATABASE']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_AUTH_DATABASE = os.environ['MONGO_AUTH_DATABASE']
