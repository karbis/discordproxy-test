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

@app.post("/channels")
def get_channels(id: int, authorization: str):
    url = f"https://discord.com/api/v10/guilds/{id}/channels"
    headers = {"Authorization": authorization}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/vc")
def set_vc(serverId: int, userId: int, channel_id: int, authorization: str):
    url = f"https://discordapp.com/api/v9/guilds/{serverId}/members/{userId}"
    headers = {"Authorization": authorization}
    json_data = {"channel_id": channel_id}

    response = requests.patch(url, headers=headers, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
