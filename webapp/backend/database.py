from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os 


production_env = os.getenv("DEBUG", "True").lower() == "false"

if production_env:
    env_file = ".env.prod"
else:
    env_file = ".env.dev"

load_dotenv(env_file)

database_url = os.getenv("DATABASE_URL_VALUE")

if not database_url:
    raise Exception("DATABASE_URL is not set")

engine = create_engine(database_url)
sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Dependency 
def get_db():
    database = sessionLocal()
    try:
        yield database
    finally:
        database.close()   