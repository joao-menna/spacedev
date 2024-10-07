from app import chat, index
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = os.path.join(Path(os.getcwd()).parent, ".env")
load_dotenv(dotenv_path)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat")
app.include_router(index.router, prefix="/api/index")
