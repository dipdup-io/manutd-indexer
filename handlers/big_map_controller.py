import uuid
from typing import Generic
from typing import TypeVar

from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapAction
from dipdup.models.tezos import TezosBigMapDiff

from manutd_indexer.models import TEZOS_STORAGE_PREFIX
from manutd_indexer.models import UUID_NAME_DELIMITER
from manutd_indexer.models import MetadataBigMapState
from manutd_indexer.models import TokenMetadataBigMapState
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_key import MetadataKey

JOIN_KEY_FIELD_NAME = 'join_key'

BigMapDiffType = TypeVar('BigMapDiffType', bound=TezosBigMapDiff)


class BigMapController(Generic[BigMapDiffType]):
    def __init__(self, ctx: HandlerContext, big_map_diff: TezosBigMapDiff) -> None:
        self._big_map_diff = big_map_diff
        self._network: str = ctx.handler_config.parent.datasources[0].name
        self._contract: str = ctx.handler_config.contract.address  # type: ignore[attr-defined]
        self._ctx = ctx

    async def handle_action(self):
        match self._big_map_diff:
            case TezosBigMapDiff(action=TezosBigMapAction.ALLOCATE):
                if self._big_map_diff.action.has_key:
                    raise TypeError
                if self._big_map_diff.action.has_value:
                    raise TypeError
                return
            case TezosBigMapDiff(key=MetadataKey(root=str(''))):
                return
            case TezosBigMapDiff(action=TezosBigMapAction.REMOVE):  # i.e. remove whole big_map
                raise NotImplementedError
            case TezosBigMapDiff(action=TezosBigMapAction.ADD_KEY):
                await self._handle_add_key()
            case TezosBigMapDiff(action=TezosBigMapAction.UPDATE_KEY):
                await self._handle_update_key()
            case TezosBigMapDiff(action=TezosBigMapAction.REMOVE_KEY):
                await self._handle_remove_key()

    async def _handle_add_key(self):
        record_dto = self._build_record_dto()

        state_model = self._big_map_diff.key.get_state_model()
        model = await state_model.create(**record_dto)
        history_model = self._big_map_diff.key.get_history_model()
        await history_model.create(**record_dto)
        key = getattr(model, 'key', None) or getattr(model, 'metadata_key', None)
        await self.handle_token_metadata(key)

    async def _handle_update_key(self):
        defaults, filter_query_dto = self._build_update_parameters_dto()

        state_model = self._big_map_diff.key.get_state_model()
        model, created = await state_model.update_or_create(
            defaults=defaults,
            **filter_query_dto,
        )

        record_dto = self._build_record_dto()

        history_model = self._big_map_diff.key.get_history_model()
        await history_model.create(**record_dto)

        key = getattr(model, 'key', None) or getattr(model, 'metadata_key', None)
        await self.handle_token_metadata(key)

    async def _handle_remove_key(self):
        record_dto = self._build_record_dto()
        defaults, filter_query_dto = self._build_update_parameters_dto()

        state_model = self._big_map_diff.key.get_state_model()
        await state_model.filter(**filter_query_dto).delete()

        history_model = self._big_map_diff.key.get_history_model()
        await history_model.create(**record_dto)

    def _build_record_dto(self) -> dict:
        record_dto = {
            'timestamp': self._big_map_diff.data.timestamp,
            'network': self._network,
            'level': self._big_map_diff.data.level,
            'contract': self._contract,
            'action': self._big_map_diff.data.action,
        }
        record_dto.update(self._big_map_diff.key.get_field_dto())  # type: ignore[union-attr]
        record_dto.update(self._big_map_diff.value.get_field_dto())  # type: ignore[union-attr]
        record_dto.update({JOIN_KEY_FIELD_NAME: self.make_join_key()})

        return record_dto

    def _build_update_parameters_dto(self) -> tuple[dict, dict]:
        defaults = self._build_record_dto()
        fields_list = self._big_map_diff.key.get_composite_key_fields()  # type: ignore[union-attr]
        filter_query_dto = {}
        for field_name in fields_list:
            if field_name in defaults:
                field_value = defaults.pop(field_name)
                filter_query_dto[field_name] = field_value

        return defaults, filter_query_dto

    def make_join_key(self) -> uuid.UUID:
        network = self._network
        contract = self._contract
        metadata_key = self._big_map_diff.key.get_field_dto().popitem()[1].removeprefix(TEZOS_STORAGE_PREFIX)  # type: ignore[union-attr]

        return uuid.uuid5(
            namespace=uuid.NAMESPACE_OID,
            name=UUID_NAME_DELIMITER.join(
                [
                    network,
                    contract,
                    metadata_key,
                ]
            ),
        )

    async def handle_token_metadata(self, key):
        if key is None:
            return
        metadata = await MetadataBigMapState.get_or_none(
            network=self._network,
            contract=self._contract,
            key=key,
        )
        if metadata is None:
            return
        token_metadata_queryset = await TokenMetadataBigMapState.filter(
            network=self._network,
            contract=self._contract,
            metadata_key=key,
        )
        for token_metadata in token_metadata_queryset:
            await self._ctx.update_token_metadata(
                network=self._network,
                address=self._contract,
                token_id=token_metadata.token_id,
                metadata=metadata.value,
            )
