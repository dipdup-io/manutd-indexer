from dipdup.context import HookContext
from tortoise.exceptions import OperationalError


async def on_reindex(
    ctx: HookContext,
) -> None:
    try:
        await ctx.execute_sql('on_reindex')
    except OperationalError as e:
        ctx.logger.error(e)
