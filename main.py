from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def proxy_request(request: Request, call_next):
    try:
        # Modify the URL as per your needs
        url = f"https://discord.com{request.url.path}"

        # Forward the request to Discord
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=dict(request.headers),
                data=await request.body(),
            )

        # Return the response from Discord
        return response.content
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))