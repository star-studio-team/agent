from agent.core import config, common
from pathlib import Path
import pydantic_ai
import agent.podman
import agent.web
import tempfile
import datetime


async def init():
    temp: Path = Path(tempfile.gettempdir())
    temp_agent = temp / 'agent'
    temp_agent.mkdir(
        parents=True,
        exist_ok=True,
    )
    now: str = datetime.datetime.now().strftime("%d.%m.%Y_%H-%M-%S")
    config.app.log_file = temp_agent / f'{now}.log'
    common.console.print('[blue]<prompt>[/blue] ', end='')
    if await agent.podman.is_exists():
        if await agent.podman.get_image() != config.podman.image:
            await agent.podman.stop()
            await agent.podman.delete()
    common.model = config.llm.model_class(
        model_name=config.llm.model_name,
        api_key=config.llm.api_key,
    )
    common.agent = pydantic_ai.Agent(
        common.model,
        system_prompt=config.llm.system_prompt,
        retries=config.llm.retries,
        tools=[
            pydantic_ai.Tool(agent.podman.run),
            pydantic_ai.Tool(agent.podman.bash),
            pydantic_ai.Tool(agent.web.google_search),
            pydantic_ai.Tool(agent.web.open_url)
        ]
    )
    if config.llm.user_prompt:
        common.console.print(config.llm.user_prompt)
    elif config.llm.user_prompt_file.is_file():
        config.llm.user_prompt = config.llm.user_prompt_file.read_text(encoding='utf-8')
        common.console.print(config.llm.user_prompt)
    else:
        config.llm.user_prompt = input()
    common.console.print()

