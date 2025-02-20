from agent.core import config, common


async def is_exists() -> bool:
    '''
    check if podman container exists
    '''
    resp = await common.client.get(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/exists'
    )
    if resp.status_code == 204:
        return True
    else:
        return False

