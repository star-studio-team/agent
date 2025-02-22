from agent.core import config, common
import pydantic_ai
import rich.markdown
import rich.live
import asyncio


async def run_stream() -> str:
    message: str = ''
    async with common.agent.run_stream(
        user_prompt=config.llm.user_prompt,
        message_history=common.message_history,
    ) as result:
        common.console.print('[light_green]<response>')
        with config.app.log_file.open('a') as log:
            log.write(common.console.export_text())
        with rich.live.Live(
            renderable='',
            vertical_overflow='crop',
        ) as live:
            async for message in result.stream_text():
                live.update(rich.markdown.Markdown(message))
        with config.app.log_file.open('a') as log:
            log.write(message)
    common.console.print()
    result_data = await result.get_data()
    common.message_history.extend(result.new_messages())
    return result_data


async def stream_cycle():
    while True:
        try:
            result_text = await run_stream()
        except pydantic_ai.exceptions.UnexpectedModelBehavior as e:
            if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                common.console.print('[red]<error>[/red] 429, sleeping for 30 seconds\n')
                await asyncio.sleep(30)
                continue
        else:
            if '##DONE##' in result_text:
                break
            config.llm.user_prompt = 'continue'
            if config.app.sleep:
                common.console.print(f'[slate_blue3]<llm stopped dialog, sleeping {config.app.sleep} and continuig...>\n')
                await asyncio.sleep(config.app.sleep)
            else:
                common.console.print('[slate_blue3]<llm stopped dialog, continuig...>\n')

