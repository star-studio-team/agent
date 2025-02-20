### what is agent?

- this project puts llm into podman container
- llm is allowed to run any bash commands, install any packages, compile and run any code

### what can i ask to agent?

- `write python app, try run it in podman, and lint it with ruff and pyright`

### run code

```shell
systemctl enable --now --user podman.socket
git clone https://github.com/star-studio-team/agent
cd agent
python -m pip install -U uv
env api_key=YOUR_GEMINI_API_KEY uv run agent
```

### license

gnu affero general public license version 3

