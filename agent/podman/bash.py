from agent.podman.is_exists import is_exists
from agent.podman.pull import pull
from agent.podman.create_container import create_container
from agent.podman.start import start
from agent.podman.exec import exec
from agent.core import common
import rich.syntax


async def bash(
    command: str,
    timeout_seconds: int = 60,
) -> str:
    '''
    run bash command in podman container
    '''
    if not await is_exists():
        await pull()
        await create_container()
    await start()
    command_syntax = rich.syntax.Syntax(
        code=command,
        lexer='bash',
    )
    common.console.print(f'[bold orange1]<executing bash command with timeout={timeout_seconds}>[/]', command_syntax)
    return await exec(
        command=['bash', '-c', command],
        timeout_seconds=timeout_seconds,
    )

