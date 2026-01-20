# Dex Plugin Development (Claude Code)

You are assisting with dex plugin development in Claude Code. Dex is a package manager for AI coding assistants.

## What is Dex?

Dex plugins enhance AI assistants with:
- **Skills**: Persistent context that shapes assistant behavior
- **Commands**: Slash commands for specific workflows
- **Instructions**: Contextual guidance (for other platforms)
- **MCP Servers**: Tools and resources via Model Context Protocol

## Plugin Structure

```
my-plugin/
├── package.json        # Plugin manifest (required)
├── README.md           # Documentation
├── context/            # Context files
│   ├── _partials/      # Shared snippets (not installed standalone)
│   ├── skills/         # Skill context files
│   ├── commands/       # Command files for Claude Code
│   └── instructions/   # Instruction files (other platforms)
├── scripts/            # Optional bundled tools
└── .dex/               # Local metadata
```

## Available Commands

This plugin provides the following slash commands:

| Command | Purpose |
|---------|---------|
| `/dex-init` | Scaffold a new dex plugin project |
| `/dex-validate` | Validate plugin structure and package.json |
| `/dex-build` | Build a distributable package |
| `/dex-publish` | Publish to GitHub or local registry |
| `/dex-upstream` | Manage upstream dependencies |

## Package.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "repository": "https://github.com/owner/repo",
  "skills": [{ "name": "skill-name", "context": "context/skills/skill.md" }],
  "commands": [{ "name": "cmd-name", "context": "context/commands/cmd.md" }],
  "mcp": {
    "servers": {
      "server-name": { "command": "python", "args": ["scripts/server.py"] }
    }
  }
}
```

## Template Variables

Context files support Jinja2:
- `{{ context.root }}` - Component install directory (relative to project root)
- `{{ env.project.root }}` - User's project path (absolute)
- `{{ plugin.name }}`, `{{ plugin.version }}` - Plugin metadata

## Development Workflow

1. **Create**: Use `/dex-init` to scaffold
2. **Develop**: Edit context files in `context/`
3. **Validate**: Use `/dex-validate` to check
4. **Test**: Install locally with `dex add ./`
5. **Build**: Use `/dex-build` to package
6. **Publish**: Use `/dex-publish` to release

## Bundled Tools

Python scripts in `scripts/` provide CLI tools:

```bash
# Scaffold new plugin
python "{{ context.root }}scripts/dex_init.py" my-plugin --template full

# Validate plugin
python "{{ context.root }}scripts/dex_validate.py" --strict

# Build package
python "{{ context.root }}scripts/dex_build.py" --checksum

# Publish to GitHub
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/repo

# Manage upstreams
python "{{ context.root }}scripts/dex_upstream.py" add owner/base-plugin
```

## Best Practices

1. **Use commands**: Prefer `/dex-*` commands for common operations
2. **Validate early**: Check structure before building
3. **Platform variants**: Use `.claude_code.md` suffix for Claude-specific content
4. **Script paths**: Quote paths with `{{ context.root }}` for spaces
5. **Test locally**: Always test with `dex add ./` before publishing
