from agent.core import common

async def fetch_text_content(url: str) -> str:
    data_str = str()
    async with common.client_ssl.stream(
        method='GET',
        url=url,
        timeout=30.0
    ) as executed:
        async for chunk in executed.aiter_bytes():
            data_str += chunk.decode('utf-8', errors='ignore')

    markdown_content = common.converter.handle(data_str)
    return markdown_content

async def open_url(url: str) -> str:
    """
    fetch information from url.
    example for fetch information from python.org website:
    await open_url(url='https://www.python.org')
    """

    common.console.print('[bold orange1]<fetch url>', url)
    text = await fetch_text_content(url)
    return text

