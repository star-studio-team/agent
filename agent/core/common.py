import pydantic_ai.models
import pydantic_ai
import rich.markdown
import rich.console
import rich.live
import httpx

client: httpx.AsyncClient
console: rich.console.Console = rich.console.Console(no_color=True, force_terminal=False)
output: str = ''
live: rich.live.Live
model: pydantic_ai.models.Model
agent: pydantic_ai.Agent
transport: httpx.AsyncHTTPTransport

