# ruff: noqa: F401

from pathlib import Path
import asyncio
import sys
sys.path.append(str(Path(__file__).parent.parent.resolve()))
import agent.podman.pull
import agent.llm.main


async def async_main():
    await agent.llm.main.main()


def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print('\033[0;31mReceived Ctrl+C - exiting.\033[0m')


if __name__ == '__main__':
    main()

