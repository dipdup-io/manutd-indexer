from dipdup import fields
from dipdup.models import Model
from dipdup.models.tezos import TezosBigMapAction
from tortoise.fields import DatetimeField

TEZOS_STORAGE_PREFIX = 'tezos-storage:'

UUID_NAME_DELIMITER = '-'


class DatetimeModelMixin:
    created_at = DatetimeField(index=True, auto_now_add=True)
    updated_at = DatetimeField(index=True, auto_now=True)


class AbstractBigMapAction(Model):
    class Meta:
        abstract = True
        indexes = (('network', 'timestamp'), ('network', 'level'))

    id = fields.UUIDField(pk=True)
    timestamp = fields.DatetimeField(index=True)
    network = fields.CharField(max_length=51, index=True)
    level = fields.IntField(index=True)
    action = fields.EnumField(enum_type=TezosBigMapAction, index=True)


class MetadataBigMapModelMixin:
    contract = fields.CharField(max_length=36)
    key = fields.CharField(max_length=64, index=True)
    value = fields.JSONField()

    join_key = fields.UUIDField(index=True)


class TokenMetadataBigMapModelMixin:
    contract = fields.CharField(max_length=36)
    token_id = fields.CharField(max_length=16)
    metadata_key = fields.CharField(max_length=64, index=True)

    join_key = fields.UUIDField(index=True)


class MetadataBigMapState(AbstractBigMapAction, MetadataBigMapModelMixin, DatetimeModelMixin):
    class Meta:
        table = 'big_map_metadata_state'
        model = 'models.MetadataBigMapHistory'


class MetadataBigMapHistory(AbstractBigMapAction, MetadataBigMapModelMixin, DatetimeModelMixin):
    class Meta:
        table = 'big_map_metadata_history'
        model = 'models.MetadataBigMapHistory'


class TokenMetadataBigMapState(AbstractBigMapAction, TokenMetadataBigMapModelMixin, DatetimeModelMixin):
    class Meta:
        table = 'big_map_token_metadata_state'
        model = 'models.TokenMetadataBigMapState'
        indexes = (('network', 'contract', 'token_id'),)


class TokenMetadataBigMapHistory(AbstractBigMapAction, TokenMetadataBigMapModelMixin, DatetimeModelMixin):
    class Meta:
        table = 'big_map_token_metadata_history'
        model = 'models.TokenMetadataBigMapHistory'
        indexes = (('network', 'contract', 'token_id'),)
