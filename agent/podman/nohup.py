from agent.podman.is_exists import is_exists
from agent.podman.pull import pull
from agent.podman.create_container import create_container
from agent.podman.start import start
from agent.podman.exec import exec
from agent.core import common
import rich.syntax


async def nohup(
    command: str,
    log_file: str = '/tmp/log_file.log'
) -> str:
    '''
    run command in background in podman container
    example for loop telegram bot:
    await nohup(command='python tg_bot.py', log_file='/tmp/tg_bot.log')
    '''
    if not await is_exists():
        await pull()
        await create_container()
    await start()
    command_syntax = rich.syntax.Syntax(
        code=command,
        lexer='sh',
    )
    common.console.print(f'[bold orange1]<executing command in nohup>[/bold orange1] [blue](log_file={log_file})[/blue]', command_syntax)
    return await exec(
        command=['sh', '-c', f'nohup sh -c "{command} > {log_file} 2>&1" & echo "PID: $!"'],
        timeout_seconds=60,
    )

