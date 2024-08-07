
from dipdup import fields
from dipdup.models import Model
from tortoise.fields.relational import ForeignKeyFieldInstance


class Metadata(Model):
    class Meta:
        table = 'metadata'
        model = 'models.Metadata'

    id = fields.UUIDField(pk=True)
    network = fields.CharField(51)
    key = fields.CharField(max_length=64, unique=True, index=True)
    value = fields.TextField()


class TokenMetadata(Model):
    class Meta:
        table = 'token_metadata'
        model = 'models.TokenMetadata'

    id = fields.UUIDField(pk=True)
    network = fields.CharField(51)
    contract = fields.CharField(max_length=36)
    token_id = fields.CharField(max_length=16)
    metadata: ForeignKeyFieldInstance[Metadata] = fields.ForeignKeyField(
        model_name=Metadata.Meta.model,
        source_field='metadata_id',
        to_field='key',
    )
    resolved = fields.BooleanField(default=False, index=True)
    failures_count = fields.IntField(default=0, index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)


    # @classmethod
    # def get_unresolved_chunk(cls) -> QuerySet:
    #     return (
    #         cls.filter(
    #             resolved=False,
    #             failures_count__lt=Const.failures_limit,
    #         )
    #         .order_by("created_at")
    #         .limit(Const.select_chunk_size)
    #     )
    #
    # async def set_resolved(self):
    #     if self.resolved:
    #         return
    #     self.resolved = True
    #     await self.save()
    #
    # async def set_failed(self):
    #     self.failures_count += 1
    #     await self.save()
    #
    # def __str__(self):
    #     return f"{self.token_id}"
