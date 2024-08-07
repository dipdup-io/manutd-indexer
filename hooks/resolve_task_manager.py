from asyncio import gather

from dipdup.context import HookContext
from tortoise.utils import chunk

from manutd_indexer.manager import ResolveMetadataTaskManager
from manutd_indexer.models import TokenMetadata, Metadata
from manutd_indexer.const import ResolveTokenMetadataConst as Const


async def resolve_task_manager(
    ctx: HookContext,
) -> None:
    logger = ctx.logger

    while tasks_list := await TokenMetadata.get_unresolved_chunk():
        logger.info(f"Processing {len(tasks_list)} unresolved tokens")

        for task_chunk in chunk(tasks_list, Const.resolve_chunk_size):
            tasks = [
                task_resolver(
                    ctx,
                    task,
                    logger,
                )
                for task in task_chunk
            ]
            await gather(*tasks)

    ResolveMetadataTaskManager.finish()
    logger.info("Waiting for unresolved tokens...")


async def task_resolver(ctx, task, logger):
    logger.info(f"Resolving metadata for token {task}")
    metadata = await Metadata.get_or_none(
        network=task.network,
        key=task.metadata_key,
    )

    if metadata is None:
        return

    await ctx.update_token_metadata(
        network=task.network,
        address=task.contract,
        token_id=task.token_id,
        metadata=hex_to_string(metadata.value),
    )
    await task.set_resolved()

def hex_to_string(hex_str):
    try:
        bytes_obj = bytes.fromhex(hex_str)
        return bytes_obj.decode('utf-8')
    except ValueError:
        return "Invalid hex string"