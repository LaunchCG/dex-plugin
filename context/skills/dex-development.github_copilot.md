# Dex Plugin Development (GitHub Copilot)

You are assisting with dex plugin development in GitHub Copilot. Dex is a package manager for AI coding assistants.

## What is Dex?

Dex plugins enhance AI assistants with:
- **Skills**: Persistent context that shapes assistant behavior
- **Instructions**: Contextual guidance triggered by file patterns
- **Commands**: Slash commands (for other platforms like Claude Code)
- **MCP Servers**: Tools and resources via Model Context Protocol

## Plugin Structure

```
my-plugin/
├── package.json        # Plugin manifest (required)
├── README.md           # Documentation
├── context/            # Context files
│   ├── _partials/      # Shared snippets (not installed standalone)
│   ├── skills/         # Skill context files
│   ├── commands/       # Command files (other platforms)
│   └── instructions/   # Instruction files for Copilot
├── scripts/            # Optional bundled tools
└── .dex/               # Local metadata
```

## Available Instructions

This plugin provides instructions for dex plugin development tasks:

| Instruction | Purpose |
|-------------|---------|
| `dex-init` | Scaffold a new dex plugin project |
| `dex-validate` | Validate plugin structure and package.json |
| `dex-build` | Build a distributable package |
| `dex-publish` | Publish to GitHub or local registry |
| `dex-upstream` | Manage upstream dependencies |

## Package.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "repository": "https://github.com/owner/repo",
  "skills": [{ "name": "skill-name", "context": "context/skills/skill.md" }],
  "instructions": [{ "name": "instr-name", "context": "context/instructions/instr.md" }],
  "mcp": {
    "servers": {
      "server-name": { "command": "python", "args": ["scripts/server.py"] }
    }
  }
}
```

## Template Variables

Context files support Jinja2:
{% raw %}- `{{ context.root }}` - Component install directory (relative to project root)
- `{{ env.project.root }}` - User's project path (absolute)
- `{{ plugin.name }}`, `{{ plugin.version }}` - Plugin metadata{% endraw %}

## Development Workflow

1. **Create**: Use `dex-init` instruction to scaffold
2. **Develop**: Edit context files in `context/`
3. **Validate**: Use `dex-validate` instruction to check
4. **Test**: Install locally with `dex add ./`
5. **Build**: Use `dex-build` instruction to package
6. **Publish**: Use `dex-publish` instruction to release

## Bundled Tools

Python scripts in `scripts/` provide CLI tools. Run these via terminal:

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

1. **Use instructions**: Reference dex instructions for common operations
2. **Validate early**: Check structure before building
3. **Platform variants**: Use `.github_copilot.md` suffix for Copilot-specific content
4. **Test locally**: Always test with `dex add ./` before publishing
5. **Document triggers**: Be clear about when instructions should activate
