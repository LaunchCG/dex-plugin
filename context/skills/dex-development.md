# Dex Plugin Development

You are assisting with dex plugin development. Dex is a package manager for AI coding assistants that enables creating, sharing, and installing plugins.

## What is Dex?

Dex plugins enhance AI assistants with:
- **Skills**: Persistent context that shapes assistant behavior
- **Commands**: Slash commands for specific workflows (Claude Code)
- **Instructions**: Contextual guidance (GitHub Copilot)
- **MCP Servers**: Tools and resources via Model Context Protocol

## Plugin Structure

```
my-plugin/
├── package.json        # Plugin manifest (required)
├── README.md           # Documentation
├── context/            # Context files
│   ├── _partials/      # Shared snippets (not installed standalone)
│   ├── skills/         # Skill context files
│   ├── commands/       # Command files (Claude Code)
│   └── instructions/   # Instruction files (Copilot)
├── scripts/            # Optional bundled tools
└── .dex/               # Local metadata
```

## Package.json Schema

Required fields:
- `name`: Plugin identifier (lowercase, alphanumeric, hyphens)
- `version`: Semver version string

Optional fields:
- `description`: What the plugin does
- `repository`: Source repository URL
- `author`, `license`: Metadata
- `skills`, `commands`, `instructions`: Component arrays
- `mcp`: MCP server configuration

## Component Definitions

Each component needs:
- `name`: Unique identifier within its type
- `context`: Path to the context file

## Platform-Specific Variants

Files can have platform variants:
- `file.md` - Default
- `file.claude_code.md` - Claude Code
- `file.github_copilot.md` - GitHub Copilot

## Template Variables

Context files support Jinja2 templating:
{% raw %}- `{{ context.root }}` - Component install directory (relative to project root)
- `{{ env.project.root }}` - User's project path (absolute)
- `{{ agent.name }}` - Current AI agent (e.g., `claude-code`)
- `{{ plugin.name }}`, `{{ plugin.version }}` - Plugin metadata{% endraw %}

## Development Tools

This plugin includes development tools in `scripts/`:
- `dex_init.py` - Scaffold new plugins
- `dex_validate.py` - Validate plugin structure
- `dex_build.py` - Build distributable packages
- `dex_publish.py` - Publish to GitHub/registry
- `dex_upstream.py` - Manage dependencies

## Best Practices

1. **Keep context focused**: Each file should have a clear purpose
2. **Use partials**: Share common content via `_partials/`
3. **Validate often**: Run validation during development
4. **Test locally**: Install locally before publishing
5. **Version properly**: Follow semver conventions
6. **Document well**: Include README and inline comments
