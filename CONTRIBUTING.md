# Contributing

Thanks for your interest. This is a small learning project, and contributions are welcome.

1. Open an issue first for anything larger than a small fix.
2. Fork the repo and create a branch.
3. Install dev tools: `pip install -e ".[dev]"`
4. Make sure `ruff check .` and `pytest` pass. Add tests for new behavior.
5. Open a pull request describing what changed and why.

Never commit API keys. Tests must not call the real network.
