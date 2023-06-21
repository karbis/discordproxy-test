import httpx
from httpx import AsyncClient
from fastapi import Request, FastAPI
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

app = FastAPI()

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

HTTP_SERVER = AsyncClient(base_url="https://discord.com/")

async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = HTTP_SERVER.build_request(
        request.method, url, headers=request.headers.raw, content=await request.body()
    )
    rp_resp = await HTTP_SERVER.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )

app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])