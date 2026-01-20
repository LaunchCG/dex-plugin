# dex-publish Instruction

When the user wants to publish or release a dex plugin, guide them to use the `dex_publish.py` script.

## When to Activate

- User wants to publish a dex plugin
- User wants to create a GitHub release
- User mentions releasing or distributing a plugin
- User asks about sharing their plugin

## Script Location

```bash
python ".github/skills/dex-development/scripts/dex_publish.py" [OPTIONS]
```

## Available Options

| Option | Description |
|--------|-------------|
| `PATH` | Plugin directory (default: current) |
| `--target` | Publish target: `github`, `local`, `registry` (required) |
| `--repo` | GitHub repo `owner/repo` |
| `--tag` | Release tag (default: `v{version}`) |
| `--registry PATH` | Local registry path |
| `--draft` | Create draft release |
| `--dry-run` | Preview without changes |

## Common Usage Patterns

### Publish to GitHub
```bash
python ".github/skills/dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin
```

### Publish with specific tag
```bash
python ".github/skills/dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin --tag v1.0.0
```

### Create draft release
```bash
python ".github/skills/dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin --draft
```

### Publish to local registry
```bash
python ".github/skills/dex-development/scripts/dex_publish.py" --target local
```

### Dry run first
```bash
python ".github/skills/dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin --dry-run
```

## GitHub Publishing Prerequisites

1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: `gh auth login`

## Publish Workflow

1. Update version in `package.json`
2. Run `dex_validate.py --strict`
3. Run `dex_build.py --checksum`
4. Run `dex_publish.py --dry-run` to preview
5. Run `dex_publish.py` to publish

## Local Registry

Default location: `~/.dex/local-registry/`

Users can install with:
```bash
dex add ~/.dex/local-registry/my-plugin
```

## Repository Field

If `--repo` not provided, uses `repository` from package.json:
```json
{
  "repository": "https://github.com/owner/repo"
}
```
