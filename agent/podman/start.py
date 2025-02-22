from agent.core import config, common


async def start() -> None:
    '''
    start podman container
    '''
    resp = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/start'
    )
    if resp.status_code not in [204, 304]:
        resp.raise_for_status()

