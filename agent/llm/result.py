from agent.core import config, common
import pydantic_ai
import rich.markdown
import rich.live


async def stream_delta(
    result: pydantic_ai.agent.result.StreamedRunResult,
    live: rich.live.Live,
):
    async for chunk in result.stream_text(delta=True):
        common.output += chunk
        live.update(rich.markdown.Markdown(common.output))


async def stream_no_delta(
    result: pydantic_ai.agent.result.StreamedRunResult,
    live: rich.live.Live,
):
    async for message in result.stream_text(delta=False):
        live.update(rich.markdown.Markdown(message))

message_history = []
async def stream(user_prompt: str):
    while True:
        async with common.agent.run_stream(
            user_prompt=user_prompt,
            message_history=message_history
        ) as result:
            with rich.live.Live(
                renderable='',
                console=common.console,
                vertical_overflow='crop',
            ) as live:
                common.live = live
                if config.llm.delta:
                    await stream_delta(result, live)
                else:
                    await stream_no_delta(result, live)
            text = await result.get_data()
            if "##DONE##" in text:
                break
            message_history.extend(result.new_messages())
        user_prompt = ''
    common.console.print(message_history)


async def no_stream(user_prompt: str):
    result = await common.agent.run(
        user_prompt=user_prompt,
    )
    common.console.print(result.data)
    common.console.print(result.all_messages())

