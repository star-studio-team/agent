from agent.core import config, common
import agent.llm.writer


async def exec(
    command: list[str],
    writer: agent.llm.writer.Writer = agent.llm.writer.Writer(),
) -> str:
    created = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/exec',
        json={
            'cmd': command,
            'attachstdout': True,
            'attachstderr': True,
        }
    )
    if created.status_code == 404:
        writer.write(str(created.json()))
        return writer.output
    created.raise_for_status()
    exec_id = created.json()['Id']
    async with common.client.stream(
        method='POST',
        url=f'{config.podman.api_url}/exec/{exec_id}/start',
        json={
            'Detach': False,
            'Tty': False
        }
    ) as executed:
        async for chunk in executed.aiter_bytes():
            data = chunk.decode('utf-8', errors='ignore')
            writer.write(data, end='')
    writer.write('')
    return writer.output

