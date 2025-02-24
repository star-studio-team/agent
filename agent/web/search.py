from agent.core import config, common
import json


async def search_4get(query: str) -> list:
    data_str = str()
    async with common.client_ssl.stream(
        method='GET',
        url=config.web.api_url,
        params={'s': query},
        timeout=30.0
    ) as executed:
        async for chunk in executed.aiter_bytes():
            data_str += chunk.decode('utf-8', errors='ignore')
    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        return []

    web_data = data.get('web', [])
    simplified_list = []
    for item in web_data:
        simplified_list.append({
            'title': item.get('title', ''),
            'description': item.get('description', ''),
            'url': item.get('url', '')
        })
    return simplified_list


async def google_search(query: str) -> str:
    '''
    search from google.
    example for search python version:
    await google_search(query='latest version of python')
    '''
    common.console.print('[bold orange1]<internet search>', query)
    data = await search_4get(query)
    return str(data)

