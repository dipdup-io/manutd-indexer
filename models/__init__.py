from tortoise.queryset import QuerySet
from manutd_indexer.const import ResolveTokenMetadataConst as Const

from dipdup import fields
from dipdup.models import Model


class Metadata(Model):
    id = fields.UUIDField(pk=True)
    network = fields.CharField(51)
    key = fields.CharField(max_length=64)
    value = fields.TextField()


class TokenMetadata(Model):
    id = fields.UUIDField(pk=True)
    network = fields.CharField(51)
    contract = fields.CharField(max_length=36)
    token_id = fields.CharField(max_length=16)
    metadata_key = fields.CharField(max_length=64)
    resolved = fields.BooleanField(default=False, index=True)
    failures_count = fields.IntField(default=0, index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)


    @classmethod
    def get_unresolved_chunk(cls) -> QuerySet:
        return (
            cls.filter(
                resolved=False,
                failures_count__lt=Const.failures_limit,
            )
            .order_by("created_at")
            .limit(Const.select_chunk_size)
        )

    async def set_resolved(self):
        if self.resolved:
            return
        self.resolved = True
        await self.save()

    async def set_failed(self):
        self.failures_count += 1
        await self.save()

    def __str__(self):
        return f"{self.token_id}"
