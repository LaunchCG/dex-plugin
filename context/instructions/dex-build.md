# dex-build Instruction

When the user wants to build or package a dex plugin for distribution, guide them to use the `dex_build.py` script.

## When to Activate

- User wants to build a dex plugin package
- User wants to create a distributable archive
- Before publishing a plugin
- User mentions packaging or distribution

## Script Location

```bash
python ".github/skills/dex-development/scripts/dex_build.py" [OPTIONS] [PATH]
```

## Available Options

| Option | Description |
|--------|-------------|
| `PATH` | Plugin directory (default: current) |
| `--output PATH` | Output directory (default: `./dist`) |
| `--format` | Archive format: `tar.gz` or `zip` |
| `--include-dev` | Include test/dev files |
| `--checksum` | Generate SHA256 checksum |
| `--clean` | Clean output directory first |

## Common Usage Patterns

### Basic build
```bash
python ".github/skills/dex-development/scripts/dex_build.py"
```

### Build with checksum
```bash
python ".github/skills/dex-development/scripts/dex_build.py" --checksum
```

### Build as zip
```bash
python ".github/skills/dex-development/scripts/dex_build.py" --format zip
```

### Clean build
```bash
python ".github/skills/dex-development/scripts/dex_build.py" --clean --checksum
```

### Custom output location
```bash
python ".github/skills/dex-development/scripts/dex_build.py" --output ./releases
```

## Output Files

Creates in `./dist/`:
- `{name}-{version}.tar.gz` (or `.zip`)
- `{name}-{version}.tar.gz.sha256` (with `--checksum`)

## Excluded by Default

- `.git`, `.github`
- `__pycache__`, `*.pyc`
- `node_modules`, virtual environments
- `.env`, `.DS_Store`
- `dist`, `build`, `.dex`

## Build Workflow

1. Run `dex_validate.py` first
2. Build with `--checksum`
3. Verify archive contents if needed
4. Test with `dex add ./dist/archive.tar.gz`
5. Publish with `dex_publish.py`

## Verify Archive

```bash
tar -tzf dist/my-plugin-1.0.0.tar.gz
```
