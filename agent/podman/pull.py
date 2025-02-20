from agent.core import config, common
import agent.llm.writer
import json


async def pull(
    image: str = config.podman.default_image,
    writer: agent.llm.writer.Writer = agent.llm.writer.Writer(),
) -> str:
    '''
    pull podman image
    '''
    writer.write(f'pulling {image}')
    async with common.client.stream(
        method='POST',
        url=f'{config.podman.api_url}/images/pull',
        params={
            'reference': image,
            'compatMode': True,
        }
    ) as resp:
        async for chunk in resp.aiter_bytes():
            data = json.loads(chunk)
            data_str = chunk.decode(errors='ignore')
            if 'progress' in data:
                writer.write(data['progress'])
            else:
                writer.write(data_str)
    return writer.output

