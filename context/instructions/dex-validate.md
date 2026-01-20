# dex-validate Instruction

When the user wants to validate a dex plugin or check for errors, guide them to use the `dex_validate.py` script.

## When to Activate

- User asks to validate a dex plugin
- User wants to check plugin structure
- User encounters errors during plugin installation
- Before publishing or building a plugin
- Working on package.json in a dex plugin

## Script Location

```bash
python ".github/skills/dex-development/scripts/dex_validate.py" [OPTIONS] [PATH]
```

## Available Options

| Option | Description |
|--------|-------------|
| `PATH` | Plugin directory (default: current) |
| `--strict` | Fail on warnings too |
| `--fix` | Auto-fix simple issues |
| `--check-files` | Verify referenced files exist |
| `--no-check-files` | Skip file checks |

## Common Usage Patterns

### Basic validation
```bash
python ".github/skills/dex-development/scripts/dex_validate.py"
```

### Strict mode
```bash
python ".github/skills/dex-development/scripts/dex_validate.py" --strict
```

### With auto-fix
```bash
python ".github/skills/dex-development/scripts/dex_validate.py" --fix
```

### Validate specific directory
```bash
python ".github/skills/dex-development/scripts/dex_validate.py" ./my-plugin
```

## What Gets Validated

### Package.json
- Required fields: `name`, `version`
- Name format (lowercase alphanumeric)
- Version format (semver)
- Component arrays structure
- MCP configuration

### Directory Structure
- `context/` directory exists
- Context files exist and are not empty

### File References
- All paths in package.json point to existing files

## Auto-fixable Issues

With `--fix`:
- Missing `name` → uses directory name
- Missing `version` → sets `0.1.0`
- Missing `description` → generates from name

## Exit Codes

- `0`: Validation passed
- `1`: Validation failed

## Interpreting Results

- ✗ Error: Must be fixed
- ⚠ Warning: Should be addressed
- ℹ Info: For your awareness
