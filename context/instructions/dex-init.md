# dex-init Instruction

When the user wants to scaffold or create a new dex plugin project, guide them to use the `dex_init.py` script.

## When to Activate

- User mentions creating a new dex plugin
- User wants to scaffold a plugin project
- User is starting dex plugin development
- Working in an empty directory intended for a new plugin

## Script Location

```bash
python ".github/skills/dex-development/scripts/dex_init.py" [OPTIONS] [NAME]
```

## Available Options

| Option | Description |
|--------|-------------|
| `NAME` | Plugin name (defaults to directory name) |
| `--template` | Template: `minimal`, `full`, or `mcp-server` |
| `--with-mcp` | Include MCP server boilerplate |
| `--with-commands` | Include command templates |
| `--output PATH` | Output directory (default: current) |

## Common Usage Patterns

### Basic plugin
```bash
python ".github/skills/dex-development/scripts/dex_init.py" my-plugin
```

### Full-featured plugin
```bash
python ".github/skills/dex-development/scripts/dex_init.py" --template full my-plugin
```

### Plugin with MCP server
```bash
python ".github/skills/dex-development/scripts/dex_init.py" --with-mcp my-mcp-plugin
```

## Template Descriptions

- **minimal**: Basic structure with one skill file
- **full**: Complete structure with skills, commands, and instructions
- **mcp-server**: Includes MCP server boilerplate and configuration

## Next Steps After Init

1. Edit context files in `context/` directory
2. Update `package.json` with description and repository
3. Validate with `dex_validate.py`
4. Test locally with `dex add ./`
