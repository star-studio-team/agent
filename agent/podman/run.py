from agent.podman.is_exists import is_exists
from agent.podman.pull import pull
from agent.podman.create import create
from agent.podman.start import start
from agent.podman.exec import exec
from agent.core import common


async def run(
    command: list[str] = [],
    timeout_seconds: int = 60,
) -> str:
    '''
    run command in podman container
    you should avoid using this tool, and use bash tool if possible
    use this tool only if bash not working
    example:
    await run(command=['echo', 'hello world'], timeout_seconds=int(60))
    '''
    if not await is_exists():
        await pull()
        await create()
    await start()
    common.console.print(f'[bold orange1]<executing>[/bold orange1] [blue][{timeout_seconds}][/blue]', command)
    return await exec(
        command=command,
        timeout_seconds=timeout_seconds,
    )

