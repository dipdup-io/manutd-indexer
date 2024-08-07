from dipdup.context import HandlerContext
from dipdup.models.tezos import TezosBigMapDiff
from tortoise.exceptions import IntegrityError

from manutd_indexer.manager import ResolveMetadataTaskManager
from manutd_indexer.models import TokenMetadata
from manutd_indexer.types.mu_minter.tezos_big_maps.assets_token_metadata_key import AssetsTokenMetadataKey
from manutd_indexer.types.mu_minter.tezos_big_maps.assets_token_metadata_value import AssetsTokenMetadataValue


async def on_token_metadata_update(
        ctx: HandlerContext,
        token_metadata: TezosBigMapDiff[AssetsTokenMetadataKey, AssetsTokenMetadataValue],
) -> None:
    token_id = token_metadata.value.token_id
    metadata_key = token_metadata.value.token_info.get("")

    try:

        await TokenMetadata.update_or_create(
            network=ctx.handler_config.parent.datasources[0].name,
            contract=ctx.handler_config.contract.address,
            token_id=token_id,
            metadata_key=metadata_key,
        )

    except IntegrityError:
        pass

    await ResolveMetadataTaskManager.process_resolve_tasks(ctx)
