from pathlib import Path
import pydantic_ai.models.gemini
import os


class podman:
    default_image: str = 'registry.fedoraproject.org/fedora-toolbox:latest'
    container_name: str = 'agent'
    socket: str = '/run/user/1000/podman/podman.sock'
    api_url: str = 'http://localhost/v5.0.0/libpod'
    timeout: int = 600


class llm:
    model_class = pydantic_ai.models.gemini.GeminiModel
    model_name: str = 'gemini-2.0-flash'
    api_key: str = os.getenv('api_key') or ''
    retries: int = 10
    stream: bool = True
    delta: bool = False
    user_prompt: str = os.getenv('user_prompt') or ''
    user_prompt_file: Path = Path.cwd() / 'prompt.txt'
    system_prompt = f'''
- you are able to run any commands in podman container
- default image is {podman.default_image}
- you should prefer :latest tag if possible
- you can read files with cat command, create files with tee command
- you should solve tasks with little steps, write small code parts and test each part
- you have two almost similar tools `run`, and `bash`
- `bash` tool should be prefferred if possible, `run` tool should be avoided if possible
- do not try do everything at once, one tool should be run once per request
- use `nohup` for projects and scripts that run continuously in a loop and can only be stopped with Ctrl + C. You can view the logs for these commands in `nohup.out`
- you don't need to create a Dockerfile or a Compose file; just use the current container environment.
- IMPORTANT: DO NOT RETURN RESPONSE TO USER UNTIL APP IS FULLY TESTED WITH PODMAN EXEC TOOL AND CONFIRMED WORKING
- When you believe you've completed everything, include '##DONE##' in your final message.
'''

class app:
    log_file: Path

