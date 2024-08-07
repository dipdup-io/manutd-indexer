class ResolveMetadataTaskManager:
    counter: int = 0

    @classmethod
    async def process_resolve_tasks(cls, ctx):
        if cls.can_start():
            await ctx.fire_hook("resolve_task_manager", wait=False)

    @classmethod
    def can_start(cls) -> bool:
        if cls.counter >= 2:
            return False

        cls.counter += 1
        return True

    @classmethod
    def finish(cls):
        if cls.counter >= 1:
            cls.counter -= 1
