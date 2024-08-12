from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff

from manutd_indexer.handlers.big_map_controller import BigMapController
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_key import MetadataKey
from manutd_indexer.types.mu_minter.tezos_big_maps.metadata_value import MetadataValue

MetadataBigMapDiff = TezosBigMapDiff[MetadataKey, MetadataValue]


async def on_metadata_update(
    ctx: HandlerContext,
    metadata: MetadataBigMapDiff,
) -> None:
    big_map_controller: BigMapController[MetadataBigMapDiff] = BigMapController(ctx, metadata)
    await big_map_controller.handle_action()
