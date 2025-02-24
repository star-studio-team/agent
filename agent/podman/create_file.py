from agent.podman.is_exists import is_exists
from agent.podman.pull import pull
from agent.podman.create_container import create_container
from agent.podman.start import start
from agent.core import config, common
import rich.syntax


async def exec(
    command: list[str],
):
    exec_create = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/exec',
        json={
            'cmd': command,
            'attachstdout': True,
            'attachstderr': True,
        },
    )
    exec_create.raise_for_status()
    exec_id = exec_create.json()['Id']
    exec_start = await common.client.post(
        url=f'{config.podman.api_url}/exec/{exec_id}/start',
        json={},
    )
    exec_start.raise_for_status()


async def create_file(
    content: str,
    path: str,
) -> None:
    '''
    creating a file in podman container

    path can be full or relative
    '''
    if not await is_exists():
        await pull()
        await create_container()
    await start()


    lexer = rich.syntax.Syntax.guess_lexer(
        path=path,
        code=content,
    )
    syntax = rich.syntax.Syntax(
        code=content,
        lexer=lexer,
    )
    common.console.print(f'[bold orange1]<creating file>[/] {path}', syntax)
    writer = f'''
cat <<EOF > {path}
{content}
EOF
'''
    await exec(['bash', '-c', writer])

