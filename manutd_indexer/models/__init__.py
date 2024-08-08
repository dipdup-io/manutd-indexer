import uuid

from dipdup import fields
from dipdup.models import Model
from tortoise.fields import DatetimeField

TEZOS_STORAGE_PREFIX = 'tezos-storage:'

UUID_NAME_DELIMITER = '-'


class DatetimeModelMixin:
    created_at = DatetimeField(index=True, auto_now_add=True)
    updated_at = DatetimeField(index=True, auto_now=True)


class Test(Model):
    class Meta:
        table = 'test'
        model = 'models.Test'

    def __post_init__(self):
        self.pk = 'df4495c8-1111-2222-3333-ef7c54617da8'

    id = fields.UUIDField(pk=True)
    level = fields.IntField(index=True)

class AbstractTezosOperation(Model):
    class Meta:
        abstract = True
        indexes = (('network', 'timestamp'), ('network', 'level'))

    id = fields.UUIDField(pk=True)
    timestamp = fields.DatetimeField(index=True)
    network = fields.CharField(max_length=51, index=True)
    level = fields.IntField(index=True)


class MetadataBigMapHistory(AbstractTezosOperation, DatetimeModelMixin):
    class Meta:
        table = 'metadata'
        model = 'models.MetadataBigMapHistory'

    key = fields.CharField(max_length=64, index=True)
    value = fields.JSONField()

    join_key = fields.UUIDField(index=True)


class TokenMetadataBigMapHistory(AbstractTezosOperation, DatetimeModelMixin):
    class Meta:
        table = 'token_metadata'
        model = 'models.TokenMetadataBigMapHistory'
        indexes = (('network', 'contract', 'token_id'))

    contract = fields.CharField(max_length=36)
    token_id = fields.CharField(max_length=16)
    metadata_key = fields.CharField(max_length=64, index=True)

    join_key = fields.UUIDField(index=True)
    #
    # @classmethod
    # def get_pk(cls, pool_from: Pool, pool_to: Pool) -> uuid.UUID:
    #     return uuid.uuid5(
    #         namespace=uuid.NAMESPACE_OID,
    #         name=UUID_NAME_DELIMITER.join(
    #             [
    #                 *cls.sort_pair_items(
    #                     pool_from,
    #                     pool_to,
    #                 ),
    #             ]
    #         ),
    #     )


class ContinuousHelper:
    @staticmethod
    def make_join_key(network: str, metadata_key: str) -> uuid.UUID:
        return uuid.uuid5(
            namespace=uuid.NAMESPACE_OID,
            name=UUID_NAME_DELIMITER.join(
                [
                    network,
                    metadata_key.removeprefix(TEZOS_STORAGE_PREFIX),
                ]
            )
        )
