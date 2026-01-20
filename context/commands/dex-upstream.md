# /dex-upstream

Manage upstream dependencies for dex plugins.

## Usage

Run the `dex_upstream.py` script:

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" [OPTIONS] COMMAND
```

## Commands

| Command | Description |
|---------|-------------|
| `add URL` | Add an upstream dependency |
| `list` | List current upstreams |
| `remove NAME` | Remove an upstream |
| `update [NAME]` | Update one or all upstreams |
| `sync` | Sync local with upstream changes |

## Global Options

| Option | Description |
|--------|-------------|
| `--path PATH` | Path to plugin directory (default: current directory) |

## Add Command

Add a new upstream dependency.

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add URL [OPTIONS]
```

Options:
- `--name NAME` - Custom name for the upstream
- `--force` - Overwrite existing upstream
- `--no-sync` - Don't sync after adding

### Examples
```bash
# Add from GitHub
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add owner/repo

# Add specific version
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add owner/repo@v1.0.0

# Add from full URL
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add github.com/owner/repo

# Add local path
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add ~/local/plugin --name my-local
```

## List Command

Show all configured upstreams.

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" list
```

Output:
```
Configured upstreams:

  base-plugin
    Type: github
    Location: owner/base-plugin@main

  my-local
    Type: local
    Location: /Users/me/local/plugin
```

## Remove Command

Remove an upstream dependency.

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" remove NAME [OPTIONS]
```

Options:
- `--clean` - Also remove cached files

### Example
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" remove base-plugin --clean
```

## Update Command

Update one or all upstreams to latest.

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" update [NAME] [OPTIONS]
```

Options:
- `--all` - Update all upstreams
- `--force` - Force overwrite local changes

### Examples
```bash
# Update specific upstream
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" update base-plugin

# Update all
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" update --all
```

## Sync Command

Sync all upstreams with their sources.

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" sync [OPTIONS]
```

Options:
- `--force` - Force overwrite local changes

## Upstream Sources

### GitHub
```bash
owner/repo              # Latest from default branch
owner/repo@v1.0.0       # Specific tag
owner/repo@main         # Specific branch
github.com/owner/repo   # Full URL
```

### Local Path
```bash
~/local/plugin          # Home-relative
./sibling-plugin        # Relative
/absolute/path          # Absolute
```

### Git URL
```bash
git@github.com:owner/repo.git
https://git.example.com/repo.git
```

## Storage

Upstreams are stored in `.dex/upstreams.json`:
```json
{
  "upstreams": {
    "base-plugin": {
      "type": "github",
      "location": "owner/base-plugin",
      "ref": "main",
      "url": "owner/base-plugin"
    }
  }
}
```

Cached content is in `.dex/upstream/{name}/`.

## Use Cases

### Extend a base plugin
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add owner/base-plugin
# Reference upstream content in your context files
```

### Track updates
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" sync
# Review changes in .dex/upstream/
```

### Local development
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_upstream.py" add ~/dev/shared-contexts --name shared
# Local symlink for live updates
```
