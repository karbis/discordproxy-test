from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS configuration
origins = ["*"]  # Add specific origins if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def proxy_discord(request, call_next):
    url = f"https://discord.com{request.url.path}"
    headers = dict(request.headers)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                request.method, url, headers=headers, data=await request.body()
            )
            response.raise_for_status()
            return response.content
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code)
