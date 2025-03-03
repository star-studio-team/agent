from agent.core import config, common
import pydantic_ai, pydantic_core
import rich.markdown
import rich.live
import asyncio
from httpx import ReadTimeout


async def run_stream() -> str:
    message: str = ''
    async with common.agent.run_stream(
        model_settings=config.llm.model_settings(timeout=30),
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
        except ReadTimeout:
            common.console.print('[red]<error>[/red] Timeout while creating or using run_stream')
            continue
        except pydantic_core._pydantic_core.ValidationError:
            common.console.print('[red]<error>[/red] Validation error')
            continue
        except pydantic_ai.exceptions.UnexpectedModelBehavior as e:
            if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e):
                common.console.print('[red]<error>[/red] 429, sleeping for 30 seconds\n')
                await asyncio.sleep(30)
                continue
        else:
            config.llm.user_prompt = 'continue'
            if '##DONE##' in result_text:
                config.llm.user_prompt = common.console.input('[green]<message (type "quit" or press "enter" to exit)>[/green] ')
                if config.llm.user_prompt.strip().lower() == 'quit' or config.llm.user_prompt.strip().lower() == '':
                    break
            if config.app.sleep:
                common.console.print(f'[slate_blue3]<llm stopped dialog, sleeping {config.app.sleep} seconds and continuig...>\n')
                await asyncio.sleep(config.app.sleep)
            else:
                common.console.print('[slate_blue3]<llm stopped dialog, continuig...>\n')

