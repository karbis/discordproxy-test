from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:5000",
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


@app.route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def proxy_request(path: str, request: Request):
    discord_url = f"https://discord.com/api/{path}"

    headers = {key: value for key, value in request.headers.items()}

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            response = await client.get(discord_url, headers=headers)
        elif request.method == "POST":
            response = await client.post(discord_url, headers=headers, data=request.body())
        elif request.method == "PUT":
            response = await client.put(discord_url, headers=headers, data=request.body())
        elif request.method == "PATCH":
            response = await client.patch(discord_url, headers=headers, data=request.body())
        elif request.method == "DELETE":
            response = await client.delete(discord_url, headers=headers, data=request.body())
        elif request.method == "OPTIONS":
            response = await client.options(discord_url, headers=headers)

    content = response.content
    resp = Response(content, media_type=response.headers["Content-Type"])
    return resp