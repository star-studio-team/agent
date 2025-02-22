import pydantic_ai.models
import pydantic_ai
import rich.markdown
import rich.console
import rich.live
import httpx


client: httpx.AsyncClient
console: rich.console.Console = rich.console.Console(log_path=False)
model: pydantic_ai.models.Model
agent: pydantic_ai.Agent
message_history: list = []

