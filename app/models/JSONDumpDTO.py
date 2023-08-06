from typing import Any, Dict, List

import pydantic as pyt


class JSONDumpDTO(pyt.BaseModel):
    id: int
    data: Dict[str, Any]


JSONDumpDTOs = List[JSONDumpDTO]
