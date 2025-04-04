import pydantic_ai.models
import pydantic_ai.settings
import pydantic_ai
import rich.markdown
import rich.console
import rich.live
import httpx
import html2text
import ssl
import certifi

ctx = ssl.create_default_context(cafile=certifi.where())

client_timeout = httpx.Timeout(30.0)
client: httpx.AsyncClient
client_agent = httpx.AsyncClient(timeout=client_timeout)
client_ssl = httpx.AsyncClient(verify=ctx)

console: rich.console.Console = rich.console.Console(
    log_path=False,
    record=True,
)
model: pydantic_ai.models.Model
agent: pydantic_ai.Agent
message_history: list = []
converter = html2text.HTML2Text()

