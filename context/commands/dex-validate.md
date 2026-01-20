# /dex-validate

Validate a dex plugin package structure and configuration.

## Usage

Run the `dex_validate.py` script:

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_validate.py" [OPTIONS] [PATH]
```

## Options

| Option | Description |
|--------|-------------|
| `PATH` | Path to plugin directory (default: current directory) |
| `--strict` | Fail on warnings too (not just errors) |
| `--fix` | Auto-fix simple issues (missing fields, formatting) |
| `--check-files` | Verify all referenced context/script files exist (default: true) |
| `--no-check-files` | Skip file existence checks |
| `--schema PATH` | Use custom schema file (not yet implemented) |

## Examples

### Validate current directory
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_validate.py"
```

### Validate specific plugin
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_validate.py" ./my-plugin
```

### Strict mode
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_validate.py" --strict
```

### Auto-fix issues
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_validate.py" --fix
```

## What Gets Validated

### Package.json
- Required fields: `name`, `version`
- Name format (lowercase, alphanumeric, hyphens/underscores)
- Version format (semver)
- Component arrays (skills, commands, instructions)
- MCP configuration

### Structure
- `context/` directory exists
- At least one context file exists
- Referenced files exist (with `--check-files`)

### Context Files
- Files are not empty
- Warns about TODO/FIXME markers

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Validation failed (errors found, or warnings with --strict) |

## Auto-fixable Issues

The `--fix` flag can automatically fix:
- Missing `name` field (uses directory name)
- Missing `version` field (sets to `0.1.0`)
- Missing `description` field (generates from name)

## Common Issues

### "Missing required field: name"
Add a `name` field to package.json or use `--fix`.

### "Context file not found"
Ensure the path in package.json matches the actual file location.

### "Invalid plugin name"
Name must be lowercase alphanumeric with hyphens or underscores only.

### "Invalid version"
Version must be semver format: `MAJOR.MINOR.PATCH` (e.g., `1.0.0`).
