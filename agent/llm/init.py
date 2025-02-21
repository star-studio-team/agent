from agent.core import config, common
from pathlib import Path
import pydantic_ai
import agent.podman
import tempfile
import datetime
import httpx


def init():
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
        ]
    )
    common.transport = httpx.AsyncHTTPTransport(
        uds=config.podman.socket
    )
    temp: Path = Path(tempfile.gettempdir())
    now: str = datetime.datetime.now().strftime("%d.%m.%Y_%H:%M:%S")
    config.app.log_file = temp / f'agent_{now}.log'
    if config.llm.user_prompt:
        common.console.log(f'[blue]message>[/blue] {config.llm.user_prompt}')
    elif config.llm.user_prompt_file.is_file():
        config.llm.user_prompt = config.llm.user_prompt_file.read_text(encoding='utf-8')
        common.console.log(f'[blue]message>[/blue] {config.llm.user_prompt}')
    else:
        config.llm.user_prompt = input('user message> ')

