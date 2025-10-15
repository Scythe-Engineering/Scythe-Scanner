# Scythe Scanner

A repository scanner that clones Git repositories and generates hierarchical LLM-based summaries for all files and directories.

## Features

- Clones Git repositories (supports branches and pull requests)
- Generates concise summaries for individual files using LLM
- Creates directory rollup summaries from file summaries
- Respects ignore patterns (exact names and glob patterns)
- Skips binary files automatically
- Stores summaries as markdown files in `scanner_metadata/`
- Only regenerates summaries when they don't already exist
- Uses OpenRouter API with configurable models

## Setup

1. Install dependencies:
```bash
uv pip install -e .
```

2. Configure your API key and model in `config.json`:
```json
{
  "openrouter_api_key": "your-openrouter-api-key-here",
  "model": "x-ai/grok-beta"
}
```

## Usage

To scan a repository:

```python
from scanners.ScanFullRepo import scan_repository

# Scan a repository
scan_repository("https://github.com/user/repo.git")
```

Or run directly:

```bash
uv run python scanners/ScanFullRepo.py
```

Edit the `repository_url` variable in `ScanFullRepo.py` to specify which repository to scan.

## Configuration

### config.json

- `openrouter_api_key`: Your OpenRouter API key
- `model`: The model to use (default: "x-ai/grok-beta")

### ignore.json

Configure which files and directories to ignore:

```json
{
  "names": [
    "file-to-ignore.txt",
    "directory-to-ignore"
  ],
  "regexes": [
    "*.log",
    "temp/*"
  ]
}
```

## Output

Summaries are saved as markdown files in `scanner_metadata/` within the cloned repository:

- File summaries: `scanner_metadata/path/to/file.py.summary.md`
- Directory summaries: `scanner_metadata/path/to/dir/_directory_summary.md`
- Repository summary: `scanner_metadata/_repository_summary.md`

## Dependencies

- `gitpython`: For Git repository operations
- `openai`: For OpenRouter API integration
