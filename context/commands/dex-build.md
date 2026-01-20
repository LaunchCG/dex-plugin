# /dex-build

Build a distributable dex plugin package.

## Usage

Run the `dex_build.py` script:

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_build.py" [OPTIONS] [PATH]
```

## Options

| Option | Description |
|--------|-------------|
| `PATH` | Path to plugin directory (default: current directory) |
| `--output PATH` | Output directory (default: `./dist`) |
| `--format` | Archive format: `tar.gz` or `zip` (default: `tar.gz`) |
| `--include-dev` | Include dev files (tests, etc.) |
| `--checksum` | Generate SHA256 checksum file |
| `--clean` | Clean output directory before building |

## Examples

### Basic build
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_build.py"
```

### Build with checksum
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_build.py" --checksum
```

### Build to custom directory
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_build.py" --output ./releases
```

### Build as zip
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_build.py" --format zip
```

### Full build with clean
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_build.py" --clean --checksum
```

## Output

The script creates:
- `dist/{name}-{version}.tar.gz` (or `.zip`)
- `dist/{name}-{version}.tar.gz.sha256` (with `--checksum`)

## Excluded Files

By default, these are excluded:
- `.git`, `.github`
- `__pycache__`, `*.pyc`
- `node_modules`, `.venv`, `venv`
- `.env`, `.envrc`
- `.DS_Store`, `Thumbs.db`
- `dist`, `build`
- `.dex`

With `--include-dev`, these are also included:
- `tests/`
- `test_*.py`, `*_test.py`
- `conftest.py`, `pytest.ini`
- `pyproject.toml`, `setup.py`

## Package Structure

The archive contains:
```
{name}-{version}/
├── package.json
├── README.md
├── context/
│   ├── skills/
│   ├── commands/
│   └── instructions/
└── scripts/
```

## After Building

1. Verify the package contents if needed:
   ```bash
   tar -tzf dist/my-plugin-1.0.0.tar.gz
   ```

2. Test installation:
   ```bash
   dex add ./dist/my-plugin-1.0.0.tar.gz
   ```

3. Publish with `/dex-publish`
