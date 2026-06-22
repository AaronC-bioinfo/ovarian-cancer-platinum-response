# Contributing

Contributions, bug reports, and feature suggestions are welcome.

## Reporting bugs

Open an issue at https://github.com/AaronC-bioinfo/ovarian-cancer-platinum-response/issues
with the following:
- Operating system and Python version (`python --version`)
- Exact command that produced the error
- Full traceback
- Relevant section of your `config/config.yaml` (replace your data path with a placeholder)

## Suggesting features

Open an issue labelled `enhancement`. Describe the use case and why it would
benefit the research community.

## Submitting a pull request

1. Fork the repository and create a branch: `git checkout -b feature/your-feature`
2. Install in development mode: `pip install -e ".[dev]"`
3. Copy the config template: `cp config/config.template.yaml config/config.yaml`
4. Fill in your local data path in `config/config.yaml`
5. Write tests for any new functionality in `tests/` — all tests must use
   synthetic data so they pass without the TCGA dataset on disk
6. Ensure all tests pass: `pytest tests/ -v`
7. Open a pull request describing what changed and why

## Running the test suite

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=src
```

All 52 tests must pass. No TCGA data download is required.

## Code of conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/).
Be respectful and constructive in all interactions.
