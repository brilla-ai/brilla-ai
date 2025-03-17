import asyncio
from contextlib import asynccontextmanager
import threading
from typing import Annotated
from fastapi import Depends, FastAPI
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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from helper.seed_data import Seed
from job.video_job import check_and_update_live_video_status



@asynccontextmanager
async def lifespan(app: FastAPI):
    global loop
    loop = asyncio.get_running_loop()  # ✅ Store FastAPI's event loop at startup
    scheduler.add_job(job_wrapper, trigger=IntervalTrigger(seconds=10))
    scheduler.start()
    print("Scheduler started.")
    yield
    scheduler.shutdown()
    print("Scheduler stopped.")
    
app = FastAPI(lifespan=lifespan)

scheduler = BackgroundScheduler()
loop = None 


def job_wrapper():
    global loop
    if loop:
        future = asyncio.run_coroutine_threadsafe(check_and_update_live_video_status(), loop)
        future.result() 

# def start_scheduler():
#     scheduler.add_job(
#         lambda: asyncio.get_event_loop(check_and_update_live_video_status()), 
#         trigger=IntervalTrigger(seconds=60)
#     )
#     scheduler.start()

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



@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()

if __name__ == "__main__":
    run(app, host = "0.0.0.0", port = 8000)

