from typing import Any, Dict, Optional

from sqlalchemy import select

from app.db.connection import get_db_sess
from app.db.models.json_dump import JSONDump
from app.models.json_dump_dto import JSONDumpDTO, JSONDumpDTOs


class JSONDumpRepository:
    async def get_all(self) -> JSONDumpDTOs:
        async with get_db_sess() as session:
            stmt = select(JSONDump)
            results = await session.execute(stmt)
            dumps = list(results.scalars())
            return [JSONDumpDTO(id=dump.id, data=dump.data) for dump in dumps]

    async def get_by_id(self, dump_id: int) -> Optional[JSONDumpDTO]:
        async with get_db_sess() as session:
            stmt = select(JSONDump).where(JSONDump.id == dump_id)
            results = await session.execute(stmt)
            dump = results.scalar_one_or_none()
            if dump is None:
                return None
            else:
                return JSONDumpDTO(id=dump.id, data=dump.data)

    async def add(self, data: Dict[str, Any]) -> int:
        async with get_db_sess() as session:
            entry = JSONDump(data=data)
            session.add(entry)
            await session.flush()
            await session.refresh(entry)

            return entry.id
