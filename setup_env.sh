curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync
source .venv/bin/activate

uv pip install --editable .
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=sharedcontrolpaper
uv run --with jupyter jupyter lab