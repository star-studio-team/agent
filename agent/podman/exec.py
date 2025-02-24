from agent.podman.stop import stop
from agent.core import config, common
import rich.errors
import rich.syntax
import rich.live
import asyncio


async def exec_create(command: list[str]) -> str:
    created = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/exec',
        json={
            'cmd': command,
            'attachstdout': True,
            'attachstderr': True,
        }
    )
    if created.status_code == 404:
        json = created.json()
        common.console.print(json)
        return str(json)
    created.raise_for_status()
    return created.json()['Id']


async def exec_stream(
    exec_id: str,
    podman_output: list[str],
):
    podman_output_str: str = ''
    with config.app.log_file.open('a') as log:
        log.write(common.console.export_text())
    async with common.client.stream(
        method='POST',
        url=f'{config.podman.api_url}/exec/{exec_id}/start',
        json={
            'detach': False,
            'tty': False
        }
    ) as executed:
        with rich.live.Live(
            renderable='',
            vertical_overflow='crop',
        ) as live:
            async for chunk in executed.aiter_bytes():
                chunk_decoded = chunk.decode('utf-8', errors='ignore')
                podman_output.append(chunk_decoded)
                podman_output_str = ''.join(podman_output).strip()
                lexer = rich.syntax.Syntax.guess_lexer(
                    path='',
                    code=podman_output_str,
                )
                output_syntax = rich.syntax.Syntax(
                    code=podman_output_str,
                    lexer=lexer,
                )
                live.update(output_syntax)
    remove_chars = ''.join(chr(i) for i in range(32))
    to_log = podman_output_str.lstrip(remove_chars) + '\n'
    with config.app.log_file.open('a') as log:
        log.write(to_log)


async def exec(
    command: list[str],
    timeout_seconds: int,
) -> str:
    exec_id = await exec_create(command)
    podman_output: list = []
    timeout_seconds = min(timeout_seconds, 180)
    coroutine = exec_stream(
        exec_id=exec_id,
        podman_output=podman_output,
    )
    common.console.print('[bold orange1]<output>')
    try:
        await asyncio.wait_for(
            fut=coroutine,
            timeout=timeout_seconds,
        )
    except asyncio.TimeoutError:
        await stop()
        podman_output.append('podman command timed out')
        common.console.print(f'[bold orange1]<podman command timed out>[/bold orange1] [blue](timeout={timeout_seconds})[/blue]\n')
    except rich.errors.LiveError:
        common.console.print('[bold orange1]<you can\'t run multiple commands at once>\n')
        podman_output.append('you can\'t run multiple commands at once')
    else:
        common.console.print()
    return ''.join(podman_output)

