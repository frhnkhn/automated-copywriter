import asyncio

from .generator import generate_copy


MAX_CONCURRENT_REQUESTS = 3


semaphore = asyncio.Semaphore(
    MAX_CONCURRENT_REQUESTS
)


async def generate_one(
    prompt,
    temperature,
    top_p
):

    async with semaphore:

        loop = asyncio.get_running_loop()

        result = await loop.run_in_executor(
            None,
            generate_copy,
            prompt,
            temperature,
            top_p
        )

        return result


async def generate_multiple(requests):

    tasks = []

    for request in requests:

        tasks.append(
            generate_one(
                request["prompt"],
                request["temperature"],
                request["top_p"]
            )
        )

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True
    )

    return results