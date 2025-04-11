from pathlib import Path
import pydantic_ai.models.openai
import os


class podman:
    image: str = os.getenv('image') or 'registry.fedoraproject.org/fedora-toolbox:latest'
    image_pkg: str = os.getenv('image_pkg') or 'dnf'
    container_name: str = 'agent'
    socket: str = '/run/user/1000/podman/podman.sock'
    api_url: str = 'http://localhost/v5.0.0/libpod'
    timeout: int = 600

class web:
    api_host: str = os.getenv('web_host') or '4get.ch'
    api_url: str = f'https://{api_host}/api/v1/web'

class llm:
    model_class = pydantic_ai.models.openai.OpenAIModel
    model_name: str = 'openrouter/quasar-alpha'
    api_key: str = os.getenv('api_key') or ''
    retries: int = 10
    user_prompt: str = os.getenv('user_prompt') or ''
    user_prompt_file: Path = Path.cwd() / 'prompt.txt'
    system_prompt = f'''
- you can use tools to run bash commands in {podman.image} podman container, your package manager is {podman.image_pkg}
- you can read files with cat command, create files with `create_file` tool
- you should solve tasks with little steps, write small code parts and test each part
- you have three almost similar tools `run`, `nohup`, and `bash`
- `bash` tool should be prefferred if possible, `run` tool should be avoided if possible
- use `timeout` (in seconds) in `bash` and `run` tools to either shorten or extend the execution time for commands
- for commands that have no end (running in a loop), use a timeout of 15 seconds or less
- there is also a `nohup` tool for looping commands
- use `nohup` tool if you want to send a command to the background and do something in parallel
- the `nohup` tool gives the PID of the process, memorize it and kill the command when it is not needed
- you can also use the `google_search` and `open_url` tools to look up information on the internet
- for searching the internet, you have two tools
- if possible, you should give preference to `google_search` to get the correct url, then use `open_url` to retrieve information from the site
- do not try do everything at once, one tool should be run once per request
- you should not write containerfiles, just use bash tool, container already created
- IMPORTANT: DO NOT RETURN RESPONSE TO USER UNTIL APP IS FULLY TESTED WITH PODMAN EXEC TOOL AND CONFIRMED WORKING
- when you believe you've completed everything, include '##DONE##' in your final message
'''

class app:
    sleep: int = int(os.getenv('sleep') or 0 )
    log_file: Path
