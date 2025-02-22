from agent.core import config, common


async def stop() -> None:
    '''
    stop podman container
    '''
    resp = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/stop',
    )
    match resp.status_code:
        case 404:
            common.console.print('[red]<can\'t stop container: container does not exists>')
        case 304:
            common.console.print('[red]<can\'t stop container: container already stopped')
        case _:
            resp.raise_for_status()
            common.console.print('[bold orange1]<container stopped>')

