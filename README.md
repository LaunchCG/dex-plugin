# dex-plugin

A development toolkit for building, packaging, and publishing dex plugins.

## Installation

From GitHub:

```bash
uvx --from git+https://github.com/launchcg/dex dex install --source git+https://github.com/launchcg/dex-plugin.git
```

Or from local path during development:

```bash
uvx --from git+https://github.com/launchcg/dex dex install --source /path/to/dex-plugin
```

To add to your project's `dex.yaml` and persist the dependency:

```bash
uvx --from git+https://github.com/launchcg/dex dex install --source git+https://github.com/launchcg/dex-plugin.git --save
```

## What's Included

### Skills

- **dex-development** - Context for dex plugin development assistance

### Commands (Claude Code)

| Command | Description |
|---------|-------------|
| `/dex-init` | Scaffold a new dex plugin project |
| `/dex-validate` | Validate plugin structure and package.json |
| `/dex-build` | Build a distributable package |
| `/dex-publish` | Publish to GitHub or local registry |
| `/dex-upstream` | Manage upstream dependencies |

### Instructions (GitHub Copilot)

Same operations as commands, triggered contextually when working on dex plugin files.

### Python Scripts

Located in `scripts/`:

| Script | Purpose |
|--------|---------|
| `dex_init.py` | Scaffold new plugin projects |
| `dex_validate.py` | Validate plugin structure |
| `dex_build.py` | Build distributable packages |
| `dex_publish.py` | Publish to targets |
| `dex_upstream.py` | Manage dependencies |

## Quick Start

### Create a New Plugin

```bash
# Using the command
/dex-init my-plugin

# Or directly
python scripts/dex_init.py my-plugin --template full
```

### Validate

```bash
python scripts/dex_validate.py --strict
```

### Build

```bash
python scripts/dex_build.py --checksum
```

### Publish

```bash
python scripts/dex_publish.py --target github --repo owner/my-plugin
```

## Script Usage

### dex_init.py

```bash
python scripts/dex_init.py [OPTIONS] [NAME]

Options:
  --template TEXT    Template: minimal, full, mcp-server
  --with-mcp         Include MCP server boilerplate
  --with-commands    Include command templates
  --output PATH      Output directory
```

### dex_validate.py

```bash
python scripts/dex_validate.py [OPTIONS] [PATH]

Options:
  --strict           Fail on warnings
  --fix              Auto-fix simple issues
  --check-files      Verify referenced files exist
```

### dex_build.py

```bash
python scripts/dex_build.py [OPTIONS]

Options:
  --output PATH      Output directory (default: ./dist)
  --format TEXT      Archive format: tar.gz, zip
  --include-dev      Include test/dev files
  --checksum         Generate SHA256 checksum
  --clean            Clean output directory first
```

### dex_publish.py

```bash
python scripts/dex_publish.py [OPTIONS]

Options:
  --target TEXT      Where to publish: github, local, registry (required)
  --repo TEXT        GitHub repo (owner/repo)
  --tag TEXT         Release tag
  --registry PATH    Local registry path
  --draft            Create draft release
  --dry-run          Preview without changes
```

### dex_upstream.py

```bash
python scripts/dex_upstream.py COMMAND [OPTIONS]

Commands:
  add URL            Add upstream dependency
  list               List current upstreams
  remove NAME        Remove an upstream
  update [NAME]      Update upstreams
  sync               Sync with upstream changes
```

## Development Workflow

1. **Create**: `python scripts/dex_init.py --template full my-plugin`
2. **Develop**: Edit context files in `context/`
3. **Validate**: `python scripts/dex_validate.py --strict`
4. **Test**: `dex add ./` to install locally
5. **Build**: `python scripts/dex_build.py --checksum`
6. **Publish**: `python scripts/dex_publish.py --target github --repo owner/repo`

## Plugin Structure

```
my-plugin/
├── package.json        # Plugin manifest
├── README.md           # Documentation
├── context/
│   ├── _partials/      # Shared content
│   ├── skills/         # Skill files
│   ├── commands/       # Command files (Claude Code)
│   └── instructions/   # Instruction files (Copilot)
└── scripts/            # Optional tools
```

## Template Variables

Context files support Jinja2 templating:

- `{{ context.root }}` - Component install directory (relative to project root)
- `{{ env.project.root }}` - User's project path (absolute)
- `{{ agent.name }}` - Current AI agent
- `{{ plugin.name }}`, `{{ plugin.version }}` - Plugin metadata

## License

MIT
