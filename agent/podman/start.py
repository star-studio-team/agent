from agent.core import config, common
import agent.llm.writer


async def start(
    writer: agent.llm.writer.Writer = agent.llm.writer.Writer(),
) -> str:
    '''
    start podman container
    '''
    writer.write('starting container')
    resp = await common.client.post(
        url=f'{config.podman.api_url}/containers/{config.podman.container_name}/start'
    )
    try:
        resp_json = resp.json()
    except Exception:
        pass
    else:
        writer.write(str(resp_json))
    if resp.status_code == 304:
        writer.write('container already started\n')
    if resp.status_code not in [204, 304]:
        resp.raise_for_status()
    return writer.output

