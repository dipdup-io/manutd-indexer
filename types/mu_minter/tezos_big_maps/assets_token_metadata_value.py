# generated by DipDup 8.0.0b4

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, ConfigDict


class AssetsTokenMetadataValue(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    token_id: str
    token_info: Dict[str, str]
