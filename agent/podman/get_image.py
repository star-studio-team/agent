from agent.core import config, common


async def get_image() -> str:
    '''
    create podman container
    '''
    resp = await common.client.get(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/json'
    )
    resp.raise_for_status()
    return resp.json()['Config']['Image']

