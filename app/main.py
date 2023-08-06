from typing import Dict

from fastapi import FastAPI, Depends

from app.db.connection import set_up_postgres
from app.db.repositories.json_dump_repository import JSONDumpRepository


def create_app() -> FastAPI:
    app = FastAPI()
    set_up_postgres(app)

    return app


app = create_app()


@app.get("/dumps/{dump_id}")
async def read_dump(dump_id: int, dump_repository: JSONDumpRepository = Depends(JSONDumpRepository)):
    return dump_repository.get_by_id(dump_id=dump_id)


@app.post("/dumps")
async def write_dump(dump: Dict[str, str], dump_repository: JSONDumpRepository = Depends(JSONDumpRepository)):
    return dump_repository.add(data=dump)
