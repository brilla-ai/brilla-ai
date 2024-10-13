from fastapi import FastAPI
from uvicorn import run
from  router.user import user_router
import os 
from database import Base, engine
from dotenv import load_dotenv

app = FastAPI()

app.include_router(user_router)


#  Setting up database connection
production_env = os.getenv(key="DEBUG", default="True").lower() == "false"

if production_env:
    env_file = ".env.prod"
else:
    env_file = ".env.dev"
load_dotenv(dotenv_path =env_file)

DOMAIN_NAME = os.getenv(key="DOMAIN_NAME")
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    run(app, host = "0.0.0.0", port = 8000)

