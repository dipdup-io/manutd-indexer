from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from tortoise.exceptions import IntegrityError

from manutd_indexer.models import Metadata
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_key import MetadataKey
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_value import MetadataValue


async def on_metadata_update(
    ctx: HandlerContext,
    metadata: TezosBigMapDiff[MetadataKey, MetadataValue],
) -> None:
    if metadata.key is None or metadata.value is None:
        return

    metadata_key = metadata.key.root
    metadat_value = metadata.value.root

    try:
        await Metadata.update_or_create(
            network=ctx.handler_config.parent.datasources[0].name,
            key=metadata_key,
            value=metadat_value,
        )
    except IntegrityError:
        pass
