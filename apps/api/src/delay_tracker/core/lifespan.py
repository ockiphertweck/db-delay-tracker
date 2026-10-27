from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from delay_tracker.timetables.client import TimetablesClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    async with TimetablesClient() as client:
        app.state.timetables_client = client
        yield
