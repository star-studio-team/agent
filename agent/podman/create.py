from agent.core import config, common


async def create() -> None:
    '''
    create podman container
    '''
    common.console.print('creating container')
    resp = await common.client.post(
        url=f'{config.podman.api_url}/containers/create',
        json={
            'command': ['sleep', 'infinity'],
            'image': config.podman.image,
            'name': config.podman.container_name,
            'replace': True,
        }
    )
    common.console.print(resp.json())
    resp.raise_for_status()

