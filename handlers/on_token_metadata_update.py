from manutd_indexer.handlers.big_map_controller import BigMapController

from manutd_indexer.types.mu_minter.tezos_big_maps.assets_token_metadata_key import AssetsTokenMetadataKey
from manutd_indexer.types.mu_minter.tezos_big_maps.assets_token_metadata_value import AssetsTokenMetadataValue
from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff

TokenMetadataBigMapDiff = TezosBigMapDiff[AssetsTokenMetadataKey, AssetsTokenMetadataValue]


async def on_token_metadata_update(
    ctx: HandlerContext,
    assets_token_metadata: TokenMetadataBigMapDiff,
) -> None:
    big_map_controller: BigMapController[TokenMetadataBigMapDiff] = BigMapController(ctx, assets_token_metadata)
    await big_map_controller.handle_action()
