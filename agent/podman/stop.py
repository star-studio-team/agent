from agent.core import config, common
import agent.llm.writer


async def stop(
    writer: agent.llm.writer.Writer = agent.llm.writer.Writer(),
) -> str:
    '''
    stop podman container
    '''
    resp = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/stop',
    )
    match resp.status_code:
        case 404:
            writer.write('container does not exists')
        case 304:
            writer.write('container already stopped')
        case _:
            resp.raise_for_status()
            writer.write('container stopped')
    return writer.output

