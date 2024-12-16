from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.redis import init_redis, close_redis

from src.api import utils, contacts, auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_url = "redis://redis:6379"
    await init_redis(app)
    yield
    await close_redis()


app = FastAPI(
    title="Contacts API",
    description="goit-pythonweb-hw-12",
    version="1.0.1",
    lifespan=lifespan,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded, try again later."},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
