from typing import List, Dict, Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.connection import get_db_sess
from app.db.models.json_dump import JSONDump


class JSONDumpRepository:
    def get_all(self) -> List[JSONDump]:
        with get_db_sess() as session:
            stmt = select(JSONDump)
            return list(session.execute(stmt).scalars())

    def get_by_id(self, dump_id: int) -> JSONDump:
        with get_db_sess() as session:
            stmt = select(JSONDump).where(JSONDump.id == dump_id)
            return session.execute(stmt).scalar_one_or_none()

    def add(self, data: Dict[str, str]):
        with get_db_sess() as session:
            entry = JSONDump(data=data)
            session.add(entry)
            session.commit()
