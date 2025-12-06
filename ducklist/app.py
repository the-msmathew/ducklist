from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import lists, tasks
from .db import init_db

app = FastAPI()

init_db()

# app.include_router(lists.router) → tells FastAPI: “Use all endpoints in lists.py with /lists prefix.”
app.include_router(lists.route)
app.include_router(tasks.route)

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for testing only
    allow_credentials=True,
    allow_methods=["*"],    # important for OPTIONS
    allow_headers=["*"],
)