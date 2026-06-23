import os
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.database.connection import close_db, connect_db

from app.routes.pitch_routes import router as pitch_router
from app.routes.auth_routes import router as auth_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    yield
    close_db()


app = FastAPI(
    title="PitchForge AI",
    description="Transform startup ideas into investor-ready business pitches.",
    version="1.0.0",
    lifespan=lifespan,
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_URLS",
        "http://localhost:5173,http://localhost:3000,https://*.vercel.app",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=os.getenv("CORS_ORIGIN_REGEX", r"https://.*\.vercel\.app"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        host.strip()
        for host in os.getenv(
            "ALLOWED_HOSTS",
            "localhost,127.0.0.1,0.0.0.0,testserver,*.onrender.com,*.railway.app",
        ).split(",")
    ],
)

rate_window = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
rate_limit = int(os.getenv("RATE_LIMIT_REQUESTS", "80"))
request_log: dict[str, deque[float]] = defaultdict(deque)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path in {"/", "/health", "/api/health"}:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = request_log[client_ip]

    while bucket and now - bucket[0] > rate_window:
        bucket.popleft()

    if len(bucket) >= rate_limit:
        return JSONResponse(
            status_code=429,
            content={"success": False, "error": "Rate limit exceeded. Try again shortly."},
        )

    bucket.append(now)
    return await call_next(request)


app.include_router(pitch_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "name": "PitchForge AI",
        "status": "online",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
