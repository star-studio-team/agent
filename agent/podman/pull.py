from agent.core import config, common
import json


async def pull() -> None:
    '''
    pull podman image
    '''
    common.console.print(f'pulling {config.podman.image}')
    async with common.client.stream(
        method='POST',
        url=f'{config.podman.api_url}/images/pull',
        params={
            'reference': config.podman.image,
            'compatMode': True,
        }
    ) as resp:
        async for chunk in resp.aiter_bytes():
            data = json.loads(chunk)
            data_str = chunk.decode(errors='ignore')
            if 'progress' in data:
                common.console.print(data['progress'])
            else:
                common.console.print(data_str)

