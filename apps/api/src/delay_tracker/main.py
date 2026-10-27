from datetime import date
from typing import Annotated

from fastapi import FastAPI, Path, Response

from delay_tracker.core.config import Environment, settings
from delay_tracker.core.logging import setup_logging
from delay_tracker.core.middleware import request_id_middleware
from delay_tracker.timetables.client import TimetablesClient

PRODUCTION = settings.env == Environment.PRODUCTION

setup_logging(settings.debug)

app = FastAPI(
    title="DB Delay Tracker API",
    docs_url=None if PRODUCTION else "/docs",
    redoc_url=None if PRODUCTION else "/redoc",
    openapi_url=None if PRODUCTION else "/openapi.json",
)
app.middleware("http")(request_id_middleware)


@app.get("/health")
async def health() -> Response:
    return Response(content="OK", media_type="text/plain")


@app.get("/stations/{pattern}")
async def read_stations(pattern: str) -> str:
    # TODO: Implement a proper root endpoint that returns useful information about the API.
    async with TimetablesClient() as client:
        return await client.get_stations(pattern)


@app.get("/plan/{station_eva}/{day}/{hour}")
async def read_plan(
    station_eva: Annotated[str, Path(pattern=r"^\d+$")],
    day: date,
    hour: Annotated[str, Path(pattern=r"^([0-1][0-9]|2[0-3])$")],
) -> Response:
    day_str = day.strftime("%y%m%d")
    async with TimetablesClient() as client:
        resp = await client.get_plan(station_eva, day=day_str, hour=hour)
        return Response(content=resp, media_type="application/xml")
