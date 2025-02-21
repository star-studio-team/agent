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
        env_user_prompt = config.llm.user_prompt
        file_user_prompt = config.llm.user_prompt_file
        while True:
            if env_user_prompt:
                user_prompt = env_user_prompt
            elif file_user_prompt.is_file():
                print('use prompt.txt')
                user_prompt = file_user_prompt.read_text(encoding='utf-8')
            else:
                user_prompt = input('message> ')
            print('waiting for response, it can be very long...')
            if config.llm.stream:
                await agent.llm.result.stream(user_prompt)
            else:
                await agent.llm.result.no_stream(user_prompt)
            await agent.podman.stop()
            await agent.podman.delete()
            if env_user_prompt or file_user_prompt:
                break

