from agent.core import config, common


async def delete() -> None:
    '''
    delete podman container
    '''
    resp = await common.client.delete(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}',
    )
    if resp.status_code == 404:
        common.console.print('[red]<can\'t delete container: container does not exists>')
    else:
        common.console.print('[bold orange1]<container deleted>')

