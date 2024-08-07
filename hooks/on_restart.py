from dipdup.context import HookContext

from manutd_indexer.manager import ResolveMetadataTaskManager


async def on_restart(
        ctx: HookContext,
) -> None:
    await ResolveMetadataTaskManager.process_resolve_tasks(ctx)
    await ctx.execute_sql('on_restart')
