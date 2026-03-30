from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return { "msg": "Hello dev docker", "v": "0.1" }


@app.get("/items/{id}")
def read_item(item_id: int, q: str = None):
    return {"id": id, "q": q}

@app.get("/api/ip")
async def get_ip(request: Request):
    x_forwarded_for = request.headers.get("x-forwarded-for")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host

    return {"ip": ip}