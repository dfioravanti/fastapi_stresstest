from typing import Any, Optional

from fastapi import Body, Depends, FastAPI

from app.db.repositories.json_dump_repository import JSONDumpRepository
from app.lifespan import lifespan
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
    return await dump_repository.get_all()


@app.get("/dumps/{dump_id}")
async def read_one_dump(
    dump_id: Optional[int] = None,
    dump_repository: JSONDumpRepository = Depends(JSONDumpRepository),
) -> Optional[JSONDumpDTO]:
    return await dump_repository.get_by_id(dump_id=dump_id)


@app.post("/dumps")
async def write_dump(payload: Any = Body(...), dump_repository: JSONDumpRepository = Depends(JSONDumpRepository)):
    return await dump_repository.add(data=payload)
