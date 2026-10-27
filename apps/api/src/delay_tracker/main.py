from fastapi import FastAPI, Response

from delay_tracker.core.config import Environment, settings
from delay_tracker.core.lifespan import lifespan
from delay_tracker.core.logging import setup_logging
from delay_tracker.core.middleware import request_id_middleware
from delay_tracker.routers import timetables

PRODUCTION = settings.env == Environment.PRODUCTION

setup_logging(settings.debug)


app = FastAPI(
    title="DB Delay Tracker API",
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
    lifespan=lifespan,
)
app.middleware("http")(request_id_middleware)

app.include_router(timetables.router)


@app.get("/health")
async def health() -> Response:
    return Response(content="OK", media_type="text/plain")
