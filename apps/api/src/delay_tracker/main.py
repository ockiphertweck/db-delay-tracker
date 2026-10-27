from delay_tracker.core.middleware import request_id_middleware
from delay_tracker.core.config import settings
from delay_tracker.core.logging import setup_logging
from delay_tracker.timetables.client import TimetablesClient
from fastapi import FastAPI, Response

import os

PRODUCTION = settings.env == "production"

setup_logging(settings.debug)

app = FastAPI(
    title="DB Delay Tracker API",
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json"
)
app.middleware("http")(request_id_middleware)


@app.get("/")
async def root():
    # TODO: Implement a proper root endpoint that returns useful information about the API.
    async with TimetablesClient() as client:
        return await client.get_stations("*")
