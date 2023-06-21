from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/channels")
def get_channels(id: int, authorization: str):
    headers = {"Authorization": authorization}
    url = f"https://discord.com/api/v10/guilds/{id}/channels"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.post("/vc")
def join_voice_channel(serverId: int, userId: int, channel_id: int, authorization: str):
    headers = {"Authorization": authorization, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/guilds/{serverId}/members/{userId}"
    body = {"channel_id": channel_id}

    response = requests.patch(url, json=body, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.post("/leave")
def leave_voice_channel(serverId: int, userId: int, authorization: str):
    headers = {"Authorization": authorization, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/guilds/{serverId}/members/{userId}"
    body = {"channel_id": None}

    response = requests.patch(url, json=body, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)