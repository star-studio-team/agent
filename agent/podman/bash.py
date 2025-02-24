from agent.podman.is_exists import is_exists
from agent.podman.pull import pull
from agent.podman.create import create
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
    example for creating a file:
    await bash(command="""cat > /tmp/file.txt << EOF
    file content
    EOF
    """, timeout_seconds=int(60))
    '''
    if not await is_exists():
        await pull()
        await create()
    await start()
    command_syntax = rich.syntax.Syntax(
        code=command,
        lexer='bash',
    )
    common.console.print(f'[bold orange1]<executing bash command>[/bold orange1] [blue](timeout={timeout_seconds})[/blue]', command_syntax)
    return await exec(
        command=['bash', '-c', command],
        timeout_seconds=timeout_seconds,
    )

