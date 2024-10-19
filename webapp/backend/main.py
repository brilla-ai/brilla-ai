from fastapi import FastAPI
from uvicorn import run
from router.ml_layer import ml_layer
from  router.user import user_router
from router.live_video import live_video
from router.live_video_edit_logs import live_video_edit_logs
from router.ai_operations import ai_operations
from router.websocket import websocket_router
from fastapi.middleware.cors import CORSMiddleware
import os 
from database import Base, engine, get_db
from dotenv import load_dotenv

from helper.seed_data import Seed


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(live_video)
app.include_router(live_video_edit_logs)
app.include_router(ai_operations)

app.include_router(ml_layer)
#  adding websocket route configuration
app.include_router(websocket_router)

#  Setting up database connection
production_env = os.getenv(key="DEBUG", default="True").lower() == "false"

if production_env:
    env_file = ".env.prod"
else:
    env_file = ".env.dev"
load_dotenv(dotenv_path =env_file)

DOMAIN_NAME = os.getenv(key="DOMAIN_NAME")
@app.on_event("startup")
def seed_data():
    # Create the database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Seed data into the AIOperations table
    db = next(get_db())
    seed = Seed(db)
    seed.seed_ai_operations()


if __name__ == "__main__":
    run(app, host = "0.0.0.0", port = 8000)

