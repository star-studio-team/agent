from pathlib import Path
import pydantic_ai.models.gemini
import os


class podman:
    image: str = 'registry.fedoraproject.org/fedora-toolbox:latest'
    container_name: str = 'agent'
    socket: str = '/run/user/1000/podman/podman.sock'
    api_url: str = 'http://localhost/v5.0.0/libpod'
    timeout: int = 600


class llm:
    model_class = pydantic_ai.models.gemini.GeminiModel
    model_name: str = 'gemini-2.0-flash'
    api_key: str = os.getenv('api_key') or ''
    retries: int = 10
    user_prompt: str = os.getenv('user_prompt') or ''
    user_prompt_file: Path = Path.cwd() / 'prompt.txt'
    system_prompt = f'''
- you can use tools to run bash commands in {podman.image} podman container, your package manager is dnf
- you can read files with cat command, create files with tee command
- you should solve tasks with little steps, write small code parts and test each part
- you have two almost similar tools `run`, and `bash`
- `bash` tool should be prefferred if possible, `run` tool should be avoided if possible
- do not try do everything at once, one tool should be run once per request
- you should not write containerfiles, just use bash tool, container already created
- IMPORTANT: DO NOT RETURN RESPONSE TO USER UNTIL APP IS FULLY TESTED WITH PODMAN EXEC TOOL AND CONFIRMED WORKING
- when you believe you've completed everything, include '##DONE##' in your final message
'''

class app:
    sleep: int = int(os.getenv('sleep') or 0 )
    log_file: Path

