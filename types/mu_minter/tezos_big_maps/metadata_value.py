# generated by DipDup 8.0.0b4

from __future__ import annotations

from typing import Any

import orjson
from manutd_indexer.models import MetadataBigMapModelMixin
from pydantic import RootModel


class MetadataValue(RootModel[str]):
    root: str

    def as_dict(self) -> dict[str, Any]:
        value = self.root

        try:
            value = bytes.fromhex(value).decode()
        except ValueError:
            pass

        return orjson.loads(value)

    def get_field_dto(self) -> dict[str, Any]:
        name = MetadataBigMapModelMixin.value.model_field_name  # type: ignore[arg-type]
        value = self.as_dict()

        return {name: value}