import logging
from types import TracebackType
from typing import Self
from urllib.parse import quote

import httpx

from delay_tracker.core.config import settings

logger = logging.getLogger(__name__)


class TimetablesClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.timetables.base_url,
            headers={
                "DB-Api-Key": settings.timetables.client_secret.get_secret_value(),
                "DB-Client-ID": settings.timetables.client_id,
                "Accept": "application/xml",
            },
            timeout=httpx.Timeout(10.0, connect=5.0),
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def get_stations(self, station: str) -> str:
        path = f"/station/{quote(station, safe='')}"
        response = await self._client.get(path)
        response.raise_for_status()
        logger.info(f"Retrieved station information for {station}")
        logger.debug(f"Response content: {response.text}")
        return response.text

    async def get_plan(self, station_eva: str, day: str, hour: str) -> str:
        path = f"/plan/{quote(station_eva, safe='')}/{quote(day, safe='')}/{quote(hour, safe='')}"
        response = await self._client.get(path)
        response.raise_for_status()
        logger.info("Retrieved plan information for %s", station_eva)
        logger.debug("Response content: %s", response.text)
        return response.text
