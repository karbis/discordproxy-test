from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(root_path="https://discord.com")

# CORS Configuration
origins = ["*",
    # Add more allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return RedirectResponse(url="https://discord.com")