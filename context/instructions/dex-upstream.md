# dex-upstream Instruction

When the user wants to manage dependencies or upstream sources for a dex plugin, guide them to use the `dex_upstream.py` script.

## When to Activate

- User wants to add dependencies to a dex plugin
- User mentions upstream plugins or sources
- User wants to extend or build on another plugin
- User asks about plugin dependencies

## Script Location

```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" [OPTIONS] COMMAND
```

## Commands

| Command | Description |
|---------|-------------|
| `add URL` | Add upstream dependency |
| `list` | List current upstreams |
| `remove NAME` | Remove an upstream |
| `update [NAME]` | Update upstreams |
| `sync` | Sync all upstreams |

## Common Usage Patterns

### Add from GitHub
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" add owner/repo
```

### Add specific version
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" add owner/repo@v1.0.0
```

### Add local path
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" add ~/local/plugin --name my-local
```

### List upstreams
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" list
```

### Update all
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" update --all
```

### Sync changes
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" sync
```

### Remove upstream
```bash
python ".github/skills/dex-development/scripts/dex_upstream.py" remove base-plugin --clean
```

## URL Formats

### GitHub
- `owner/repo` - Default branch
- `owner/repo@v1.0.0` - Specific tag
- `owner/repo@main` - Specific branch
- `github.com/owner/repo` - Full URL

### Local
- `~/path/to/plugin` - Home-relative
- `./sibling-plugin` - Relative
- `/absolute/path` - Absolute

### Git
- `git@github.com:owner/repo.git`
- `https://git.example.com/repo.git`

## Storage

- Config: `.dex/upstreams.json`
- Cache: `.dex/upstream/{name}/`

## Use Cases

### Extend base plugin
Add upstream, then reference its content in your context files.

### Track updates
Use `sync` to pull latest changes from upstreams.

### Local development
Add local path upstream for live-reloading during development.
