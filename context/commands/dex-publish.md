# /dex-publish

Publish a dex plugin to GitHub, local registry, or other targets.

## Usage

Run the `dex_publish.py` script:

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `PATH` | Path to plugin directory (default: current directory) |
| `--target` | Where to publish: `github`, `local`, or `registry` (required) |
| `--repo` | GitHub repo (`owner/repo`) for github target |
| `--tag` | Release tag (default: `v{version}` from package.json) |
| `--registry PATH` | Registry path for local target |
| `--draft` | Create as draft release (github) |
| `--dry-run` | Show what would happen without doing it |

## Examples

### Publish to GitHub
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin
```

### Publish specific version
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin --tag v1.0.0
```

### Create draft release
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin --draft
```

### Publish to local registry
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" --target local
```

### Publish to specific local path
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" --target local --registry ~/.dex/my-registry
```

### Dry run
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_publish.py" --target github --repo owner/my-plugin --dry-run
```

## GitHub Publishing

### Prerequisites
1. Install GitHub CLI: https://cli.github.com/
2. Authenticate: `gh auth login`

### What Happens
1. Builds package if not already built
2. Creates GitHub release with tag
3. Uploads package archive and checksum
4. Generates release notes from package.json

### Repository Setup
The `--repo` can be inferred from `repository` field in package.json:
```json
{
  "repository": "https://github.com/owner/repo"
}
```

## Local Publishing

### Default Location
`~/.dex/local-registry/`

### Structure
```
~/.dex/local-registry/
├── index.json
└── my-plugin/
    └── 1.0.0/
        ├── package.json
        ├── context/
        └── ...
```

### Using Local Plugins
```bash
dex add ~/.dex/local-registry/my-plugin
```

## Before Publishing

1. Update version in package.json
2. Run `/dex-validate --strict`
3. Run `/dex-build --checksum`
4. Test locally with `dex add ./`
5. Use `--dry-run` to preview

## Release Notes

GitHub releases include:
- Plugin name and version
- Description from package.json
- Installation command
