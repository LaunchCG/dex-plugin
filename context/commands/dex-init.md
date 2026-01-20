# /dex-init

Scaffold a new dex plugin project with the proper structure.

## Usage

Run the `dex_init.py` script with appropriate options:

```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_init.py" [OPTIONS] [NAME]
```

## Options

| Option | Description |
|--------|-------------|
| `NAME` | Plugin name (defaults to directory name if not provided) |
| `--template` | Template to use: `minimal`, `full`, or `mcp-server` |
| `--with-mcp` | Include MCP server boilerplate |
| `--with-commands` | Include command templates |
| `--output PATH` | Output directory (default: current directory) |

## Examples

### Create minimal plugin
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_init.py" my-plugin
```

### Create full-featured plugin
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_init.py" --template full my-plugin
```

### Create plugin with MCP server
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_init.py" --with-mcp my-mcp-plugin
```

### Create at specific location
```bash
python ".claude/skills/dex-plugin-dex-development/scripts/dex_init.py" --output ~/plugins my-plugin
```

## Templates

### minimal
- Basic package.json
- Single skill file
- README.md

### full
- Complete package.json with all component types
- Skill, command, and instruction templates
- README.md with documentation structure

### mcp-server
- Package.json with MCP configuration
- Skill file referencing MCP tools
- Boilerplate MCP server script
- README.md with MCP documentation

## After Scaffolding

1. Edit `context/skills/*.md` to define your skill content
2. Add commands in `context/commands/` if needed
3. Run `/dex-validate` to check the structure
4. Test locally with `dex add ./`
