pip install uv
uv venv

source .venv/bin/activate

uv sync

uv pip install --editable .
uv pip install jupyter ipykernel
uv add --dev ipykernel
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=sharedcontrolpaper
uv run --with jupyter jupyter lab
