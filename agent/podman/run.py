from agent.podman.is_exists import is_exists
from agent.podman.get_image import get_image
from agent.podman.stop import stop
from agent.podman.delete import delete
from agent.podman.pull import pull
from agent.podman.create import create
from agent.podman.start import start
from agent.podman.exec import exec
from agent.core import config
import agent.llm.writer


async def run(
    command: list[str] = [],
    image: str = config.podman.default_image,
) -> str:
    '''
    run command in podman container
    you should not provide 'image' arg unless you explicitly need some custom image
    returns command and output
    example:
    await podman.run(command=['echo', 'hello world'])
    '''
    writer = agent.llm.writer.Writer()
    writer.write(f'> {command}')
    if await is_exists() and await get_image() != image:
        await stop()
        await delete()
    if not await is_exists():
        await pull()
        await create()
    await start()
    return await exec(
        command=command,
        writer=writer,
    )

