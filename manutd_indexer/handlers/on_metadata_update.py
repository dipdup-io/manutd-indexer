from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from orjson import orjson
from tortoise.exceptions import BaseORMException

from manutd_indexer.models import ContinuousHelper
from manutd_indexer.models import MetadataBigMapHistory
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_key import MetadataKey
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_value import MetadataValue


async def on_metadata_update(
    ctx: HandlerContext,
    metadata: TezosBigMapDiff[MetadataKey, MetadataValue],
) -> None:
    if metadata.key is None or metadata.value is None or metadata.key.root == '':
        return

    network = ctx.handler_config.parent.datasources[0].name
    key = metadata.key.root
    try:
        await MetadataBigMapHistory.update_or_create(
            timestamp=metadata.data.timestamp,
            network=network,
            level=metadata.data.level,
            key=key,
            value=metadata.value.as_dict(),
            join_key=ContinuousHelper.make_join_key(network, key),
        )
    except BaseORMException:
        breakpoint()
