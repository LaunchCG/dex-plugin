# Dex Overview

Dex is a package manager for AI coding assistants. It enables developers to create, share, and install plugins that enhance AI assistants with custom skills, commands, and instructions.

## Plugin Structure

A dex plugin is a directory containing:

```
my-plugin/
├── package.json        # Plugin manifest (required)
├── README.md           # Documentation
├── context/            # Context files directory
│   ├── _partials/      # Shared content snippets
│   ├── skills/         # Skill context files
│   ├── commands/       # Command context files (Claude Code)
│   └── instructions/   # Instruction context files (Copilot)
├── scripts/            # Optional scripts/tools
└── .dex/               # Local dex metadata
```

## Component Types

### Skills
Skills provide persistent context that shapes how the AI assistant behaves. They're always available during conversations.

- Defined in `context/skills/`
- Referenced in `package.json` under `skills`
- Can have platform-specific variants (e.g., `skill.claude_code.md`)

### Commands (Claude Code)
Commands are slash commands that trigger specific behaviors or workflows.

- Defined in `context/commands/`
- Referenced in `package.json` under `commands`
- Invoked with `/command-name`

### Instructions (GitHub Copilot)
Instructions are contextual guidance for GitHub Copilot based on file patterns or triggers.

- Defined in `context/instructions/`
- Referenced in `package.json` under `instructions`
- Activated based on file context

### MCP Servers
Plugins can include Model Context Protocol servers that provide tools and resources.

- Configured in `package.json` under `mcp.servers`
- Scripts typically in `scripts/`

## Package.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What this plugin does",
  "repository": "https://github.com/owner/repo",
  "author": "Your Name",
  "license": "MIT",
  "skills": [
    {
      "name": "skill-name",
      "context": "context/skills/skill-name.md"
    }
  ],
  "commands": [
    {
      "name": "command-name",
      "context": "context/commands/command-name.md"
    }
  ],
  "instructions": [
    {
      "name": "instruction-name",
      "context": "context/instructions/instruction-name.md"
    }
  ],
  "mcp": {
    "servers": {
      "server-name": {
        "command": "python",
        "args": ["scripts/server.py"]
      }
    }
  }
}
```

## Platform-Specific Variants

Context files can have platform-specific variants using the naming convention:

- `file.md` - Default (fallback)
- `file.claude_code.md` - Claude Code specific
- `file.github_copilot.md` - GitHub Copilot specific
- `file.cursor.md` - Cursor specific

The most specific variant is used when available.
