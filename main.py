from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time

ALLOWED_ORIGIN = "https://dash-mu1aya.example.com"
EMAIL = "tanishkaurmehta@gmail.com"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response

@app.get("/stats")
def stats(values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]
    s = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": s,
        "min": min(nums),
        "max": max(nums),
        "mean": s / len(nums),
    }