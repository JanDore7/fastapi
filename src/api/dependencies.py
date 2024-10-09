from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page_nuber: Annotated[int, Query(default=1, ge=1)]
    page_size: Annotated[int | None ,Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]



