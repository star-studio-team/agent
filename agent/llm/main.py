from agent.core import config, common
import agent.llm.result
import agent.llm.init
import agent.podman
import httpx


async def main():
    transport = httpx.AsyncHTTPTransport(
        uds=config.podman.socket
    )
    async with httpx.AsyncClient(
        transport=transport,
        timeout=config.podman.timeout,
    ) as client:
        common.client = client
        await agent.llm.init.init()
        await agent.llm.result.stream_cycle()
        await agent.podman.stop()

