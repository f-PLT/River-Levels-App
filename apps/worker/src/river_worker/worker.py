from arq.connections import RedisSettings


class WorkerSettings:
    functions = []
    redis_settings = RedisSettings(host="redis", port=6379)

    async def on_startup(self, ctx, **kwargs):
        print("Worker started")

    async def on_shutdown(self, ctx, **kwargs):
        print("Worker shutdown")
