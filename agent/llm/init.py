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



