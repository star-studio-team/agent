from agent.core import config, common
import agent.llm.writer


async def create(
    image: str = config.podman.default_image,
    writer: agent.llm.writer.Writer = agent.llm.writer.Writer(),
) -> str:
    '''
    create podman container
    '''
    writer.write('creating container')
    resp = await common.client.post(
        url=f'{config.podman.api_url}/containers/create',
        json={
            'command': ['sleep', 'infinity'],
            'image': image,
            'name': config.podman.container_name,
            'replace': True,
        }
    )
    resp_json = resp.json()
    writer.write(str(resp_json))
    if resp.status_code != 500:
        resp.raise_for_status()
    return writer.output

