from typing import Any, Optional

from fastapi import FastAPI, Depends, Body

from app.db.connection import lifespan
from app.db.repositories.json_dump_repository import JSONDumpRepository
from app.models.JSONDumpDTO import JSONDumpDTO, JSONDumpDTOs


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app


app = create_app()


@app.get("/")
async def health():
    return {"status": "ok"}


@app.get("/dumps")
async def read_dump(dump_repository: JSONDumpRepository = Depends(JSONDumpRepository)) -> JSONDumpDTOs:
    return dump_repository.get_all()


@app.get("/dumps/{dump_id}")
async def read_one_dump(
    dump_id: Optional[int] = None,
    dump_repository: JSONDumpRepository = Depends(JSONDumpRepository),
) -> Optional[JSONDumpDTO]:
    return dump_repository.get_by_id(dump_id=dump_id)


@app.post("/dumps")
async def write_dump(payload: Any = Body(...), dump_repository: JSONDumpRepository = Depends(JSONDumpRepository)):
    return dump_repository.add(data=payload)
