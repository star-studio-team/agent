import agent.core.common
import agent.core.config
import rich.markdown


class Writer:
    def __init__(self) -> None:
        self.output: str = ''

    def write(
        self,
        data: str,
        end: str = '\n',
    ):
        data += end
        self.output += data
        if agent.core.config.llm.stream and agent.core.config.llm.delta:
            agent.core.common.output += data
            agent.core.common.live.update(
                rich.markdown.Markdown(agent.core.common.output)
            )

