from sqlite3 import IntegrityError

from manutd_indexer.models import ContinuousHelper
from manutd_indexer.models import TokenMetadataBigMapHistory
from manutd_indexer.types.mu_minter.tezos_big_maps.assets_token_metadata_key import AssetsTokenMetadataKey
from manutd_indexer.types.mu_minter.tezos_big_maps.assets_token_metadata_value import AssetsTokenMetadataValue
from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff


async def on_token_metadata_update(
    ctx: HandlerContext,
    assets_token_metadata: TezosBigMapDiff[AssetsTokenMetadataKey, AssetsTokenMetadataValue],
) -> None:
    if assets_token_metadata.key is None or assets_token_metadata.value is None:
        return

    token_id = assets_token_metadata.value.token_id
    metadata_key = assets_token_metadata.value.get_metadata_key()
    network = ctx.handler_config.parent.datasources[0].name

    await TokenMetadataBigMapHistory.update_or_create(
        timestamp=assets_token_metadata.data.timestamp,
        network=network,
        level=assets_token_metadata.data.level,
        contract=ctx.handler_config.contract.address,
        token_id=token_id,
        metadata_key=metadata_key,
        join_key=ContinuousHelper.make_join_key(network, metadata_key),
    )
