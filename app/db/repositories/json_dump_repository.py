from typing import Dict, Optional

from sqlalchemy import select

from app.db.connection import get_db_sess
from app.db.models.json_dump import JSONDump
from app.models.JSONDumpDTO import JSONDumpDTO, JSONDumpDTOs


class JSONDumpRepository:
    def get_all(self) -> JSONDumpDTOs:
        with get_db_sess() as session:
            stmt = select(JSONDump)
            dumps = list(session.execute(stmt).scalars())
            return [JSONDumpDTO(id=dump.id, data=dump.data) for dump in dumps]

    def get_by_id(self, dump_id: int) -> Optional[JSONDumpDTO]:
        with get_db_sess() as session:
            stmt = select(JSONDump).where(JSONDump.id == dump_id)
            dump = session.execute(stmt).scalar_one_or_none()
            if dump is None:
                return None
            else:
                return JSONDumpDTO(id=dump.id, data=dump.data)

    def add(self, data: Dict[str, str]):
        with get_db_sess() as session:
            entry = JSONDump(data=data)
            session.add(entry)
