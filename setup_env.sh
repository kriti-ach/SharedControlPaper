pip install uv

uv sync
source .venv/bin/activate

uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=sharedcontrolpaper
uv run --with jupyter jupyter lab