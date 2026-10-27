from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response

from delay_tracker.dependencies import get_timetables_service
from delay_tracker.services.timetables import TimetablesService

router = APIRouter(prefix="/timetables", tags=["timetables"])


@router.get("/stations/{pattern}")
async def read_stations(
    pattern: str,
    timetables_service: Annotated[TimetablesService, Depends(get_timetables_service)],
) -> Response:
    stations = await timetables_service.get_stations(pattern)
    return Response(content=stations, media_type="application/xml")


@router.get("/plan/{station_eva}/{day}/{hour}")
async def read_plan(
    station_eva: Annotated[str, Path(pattern=r"^\d+$")],
    day: date,
    hour: Annotated[str, Path(pattern=r"^([0-1][0-9]|2[0-3])$")],
    timetables_service: Annotated[TimetablesService, Depends(get_timetables_service)],
) -> Response:
    plan = await timetables_service.get_plan(station_eva, day, hour)
    return Response(content=plan, media_type="application/xml")
