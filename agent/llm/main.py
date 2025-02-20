from agent.core import config, common
import agent.llm.result
import agent.llm.init
import agent.podman
import httpx


async def main():
    agent.llm.init.init()
    async with httpx.AsyncClient(
        transport=common.transport,
        timeout=config.podman.timeout,
    ) as client:
        common.client = client
        while True:
            user_prompt = input('message> ')
            print('waiting for response, it can be very log...')
            if config.llm.stream:
                await agent.llm.result.stream(user_prompt)
            else:
                await agent.llm.result.no_stream(user_prompt)
            await agent.podman.stop()
            await agent.podman.delete()

