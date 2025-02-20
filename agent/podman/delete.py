from agent.core import config, common
import agent.llm.writer


async def delete(
    writer: agent.llm.writer.Writer = agent.llm.writer.Writer(),
) -> str:
    '''
    delete podman container
    '''
    writer.write('deleting container')
    resp = await common.client.delete(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}',
    )
    if resp.status_code == 404:
        writer.write('container does not exists')
    else:
        resp.raise_for_status()
        writer.write('container deleted')
    return writer.output

