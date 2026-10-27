from typing import Annotated, cast

from fastapi import Depends, Request

from delay_tracker.services.timetables import TimetablesService
from delay_tracker.timetables.client import TimetablesClient


def get_timetables_client(request: Request) -> TimetablesClient:
    return cast(TimetablesClient, request.app.state.timetables_client)


def get_timetables_service(
    client: Annotated[TimetablesClient, Depends(get_timetables_client)],
) -> TimetablesService:
    return TimetablesService(client)
