import sys
from agent.core import config, common
import agent.llm.result
import agent.llm.init
import agent.podman
import httpx

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)

    def flush(self):
        for f in self.files:
            f.flush()

async def main():
    agent.llm.init.init()
    async with httpx.AsyncClient(
        transport=common.transport,
        timeout=config.podman.timeout,
    ) as client:
        common.client = client
        with config.app.log_file.open(mode="a", encoding="utf-8") as f:
            original_stdout = sys.stdout
            sys.stdout = Tee(sys.stdout, f)
            print('waiting for response, it can be very long...')
            if config.llm.stream:
                await agent.llm.result.stream(config.llm.user_prompt)
            else:
                await agent.llm.result.no_stream(config.llm.user_prompt)
            sys.stdout = original_stdout
        await agent.podman.stop()
        if config.podman.del_container: 
            print('delete container')
            await agent.podman.delete()

