from datetime import date

from delay_tracker.timetables.client import TimetablesClient


class TimetablesService:
    def __init__(self, client: TimetablesClient):
        self._client = client

    async def get_stations(self, pattern: str) -> str:
        return await self._client.get_stations(pattern)

    async def get_plan(self, station_eva: str, day: date, hour: str) -> str:
        day_str = day.strftime("%y%m%d")
        return await self._client.get_plan(station_eva, day=day_str, hour=hour)
