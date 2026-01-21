# Dex Package Manager

You manage dex plugin packages. You understand the complete package.json schema, component types, platform mappings, and how to structure plugins correctly.

**Source of truth**: https://github.com/launchcg/dex

## Plugin Structure

```
my-plugin/
├── package.json          # Plugin manifest (required)
├── context/              # Context files (Markdown + Jinja2)
│   ├── _partials/        # Shared content (not installed standalone)
│   ├── skills/
│   ├── commands/
│   ├── sub_agents/
│   ├── rules/
│   ├── instructions/
│   └── prompts/
├── files/                # Static files to bundle
├── templates/            # Jinja2 template files (.j2)
└── servers/              # MCP server scripts
```

## package.json Schema

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "repository": "https://github.com/owner/repo",
  "author": "Name",
  "license": "MIT",
  "skills": [],
  "commands": [],
  "sub_agents": [],
  "rules": [],
  "instructions": [],
  "prompts": [],
  "mcp_servers": [],
  "files": [],
  "template_files": [],
  "dependencies": {}
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Lowercase, alphanumeric, hyphens/underscores only. Must start with letter/number. |
| `version` | Semver string (e.g., `"1.0.0"`, `"2.0.0-beta.1"`) |
| `description` | Human-readable description |

## Component Types

### Skills

Persistent context that shapes AI behavior. Always available during conversations.

```json
{
  "skills": [
    {
      "name": "code-review",
      "description": "Automated code review assistance",
      "context": "./context/skills/code-review.md",
      "files": ["./tools/review-helper.py"],
      "template_files": [{"src": "./templates/config.py.j2", "dest": "config.py"}],
      "metadata": {}
    }
  ]
}
```

**Platform support:**
| Platform | Location | Format |
|----------|----------|--------|
| Claude Code | `.claude/skills/{plugin}-{skill}/SKILL.md` | YAML frontmatter |
| GitHub Copilot | `.github/skills/{skill}/SKILL.md` | YAML frontmatter |
| Codex | `.codex/skills/{skill}/SKILL.md` | YAML frontmatter |
| Antigravity | `.agent/skills/{skill}/SKILL.md` | YAML frontmatter |
| Cursor | Not supported | - |

### Commands

Slash commands that trigger specific workflows.

```json
{
  "commands": [
    {
      "name": "deploy",
      "description": "Deploy to production",
      "context": "./context/commands/deploy.md",
      "metadata": {
        "argument_hint": "[environment] [--dry-run]",
        "allowed_tools": "Bash(deploy:*), Read",
        "model": "sonnet"
      }
    }
  ]
}
```

**Platform support:**
| Platform | Location | Format |
|----------|----------|--------|
| Claude Code | `.claude/commands/{plugin}-{command}.md` | YAML frontmatter |
| Cursor | `.cursor/commands/{plugin}-{command}.md` | Plain markdown |
| GitHub Copilot | `.github/instructions/{command}.instructions.md` or `.github/prompts/{command}.prompt.md` | YAML frontmatter |
| Codex | Not supported (use AGENTS.md) | - |
| Antigravity | Not supported | - |

### Sub-agents

Specialized agents with specific capabilities.

```json
{
  "sub_agents": [
    {
      "name": "reviewer",
      "description": "Code review specialist",
      "context": "./context/sub_agents/reviewer.md",
      "metadata": {
        "model": "inherit",
        "color": "green",
        "tools": ["Read", "Grep", "Glob"]
      }
    }
  ]
}
```

**Platform support:**
| Platform | Location | Format |
|----------|----------|--------|
| Claude Code | `.claude/agents/{plugin}-{agent}.md` | YAML frontmatter |
| GitHub Copilot | `.github/agents/{agent}.agent.md` | YAML frontmatter |

### Rules

Project-wide guidelines and constraints.

```json
{
  "rules": [
    {
      "name": "code-style",
      "description": "Code style guidelines",
      "context": "./context/rules/code-style.md",
      "paths": ["src/**/*.ts", "lib/**/*.ts"],
      "glob": "**/*.ts",
      "always": false
    }
  ]
}
```

**Platform-specific fields:**
- `paths` (Claude Code): File patterns for scoping rules
- `glob` (Cursor): File patterns for MDC frontmatter
- `always` (Cursor): If true, applies to every chat session

**Platform support:**
| Platform | Location | Format |
|----------|----------|--------|
| Claude Code | `.claude/rules/{plugin}-{rule}.md` | YAML frontmatter (if paths) |
| Cursor | `.cursor/rules/{plugin}-{rule}.mdc` | MDC frontmatter |
| GitHub Copilot | `.github/copilot-instructions.md` | Plain markdown (appended) |
| Codex | `.codex/rules/{rule}.md` | Plain markdown |
| Antigravity | `.agent/rules/{rule}.md` | Plain markdown |

### Instructions (GitHub Copilot only)

File-scoped guidance for specific file patterns.

```json
{
  "instructions": [
    {
      "name": "python-lint",
      "description": "Python linting guidance",
      "context": "./context/instructions/python-lint.md",
      "metadata": {
        "applyTo": "**/*.py",
        "excludeAgent": "code-review"
      }
    }
  ]
}
```

### Prompts (GitHub Copilot only)

Reusable prompt templates.

```json
{
  "prompts": [
    {
      "name": "explain-code",
      "description": "Explain selected code",
      "context": "./context/prompts/explain.md"
    }
  ]
}
```

### Agent File Content

Content injected into the main agent file (CLAUDE.md or AGENTS.md).

```json
{
  "agent_file": {
    "context": "./context/agent-file.md"
  }
}
```

| Platform | Location |
|----------|----------|
| Claude Code | `CLAUDE.md` |
| Codex | `AGENTS.md` |

## Files and Template Files

Bundle additional resources with components.

### Static Files

Copied directly without processing.

```json
{
  "files": [
    "calculator.py",
    {"src": "schemas/input.json", "dest": "schema.json"},
    {"src": "../../shared/utils.py"}
  ]
}
```

### Template Files

Rendered through Jinja2 with access to all template variables.

```json
{
  "template_files": [
    "config.py.j2",
    {"src": "settings.yaml.j2", "dest": "settings.yaml"}
  ]
}
```

### File Format

| Field | Required | Description |
|-------|----------|-------------|
| `src` | Yes | Path relative to plugin root |
| `dest` | No | Destination filename (defaults to basename) |

### Manifest-Level Files

Files at the manifest level install to `.claude/files/{plugin}/`.

```json
{
  "files": ["shared/utils.py"],
  "template_files": [{"src": "templates/shared-config.py.j2", "dest": "config.py"}]
}
```

## Platform-Specific File Overrides

Any file can have platform-specific variants using naming conventions.

### Convention

- `{filename}.{ext}` - default
- `{filename}.{platform}.{ext}` - platform override
- `{filename}.{platform1,platform2}.{ext}` - multi-platform override

### Platform Identifiers

Use underscores in filenames:
- `claude_code`
- `cursor`
- `codex`
- `github_copilot`
- `antigravity`

### Example

```
context/
├── skill.md                          # Default
├── skill.claude_code.md              # Claude Code override
├── skill.cursor.md                   # Cursor override
└── skill.{codex,antigravity}.md      # Shared override
```

Reference the default in package.json - dex resolves the correct variant:

```json
{
  "context": "./context/skill.md"
}
```

## MCP Servers

### Bundled (local script)

```json
{
  "mcp_servers": [
    {
      "name": "my-server",
      "type": "bundled",
      "path": "./servers/server.js",
      "config": {
        "args": ["--port", "8080"],
        "env": {"API_KEY": "${API_KEY}"}
      }
    }
  ]
}
```

### Remote (npm package)

```json
{
  "mcp_servers": [
    {
      "name": "external-server",
      "type": "remote",
      "source": "npm:@example/mcp-server",
      "version": "1.0.0"
    }
  ]
}
```

**Platform support:**
| Platform | Location |
|----------|----------|
| Claude Code | `.mcp.json` |
| Cursor | `.cursor/mcp.json` |
| GitHub Copilot | `.vscode/mcp.json` |
| Codex | `~/.codex/config.toml` (global) |
| Antigravity | UI-only configuration |

## Platform-Specific Metadata

### Claude Code Commands

```json
{
  "metadata": {
    "argument_hint": "[file] [options]",
    "allowed_tools": "Bash(build:*), Read, Write",
    "model": "sonnet"
  }
}
```

### Claude Code Sub-agents

```json
{
  "metadata": {
    "model": "inherit",
    "color": "blue",
    "tools": ["Read", "Grep", "Glob"]
  }
}
```

### Cursor Rules

```json
{
  "glob": "**/*.ts",
  "always": true
}
```

### GitHub Copilot

```json
{
  "metadata": {
    "applyTo": "**/*.py",
    "excludeAgent": "code-review"
  }
}
```

For prompts instead of instructions, add:
```json
{
  "copilot_mode": "prompt"
}
```

### Codex Skills

```json
{
  "metadata": {
    "short-description": "Brief UI description"
  }
}
```

## Dependencies

```json
{
  "dependencies": {
    "other-plugin": "^1.0.0",
    "another-plugin": "~2.0.0"
  }
}
```

### Version Specifiers

| Specifier | Meaning |
|-----------|---------|
| `1.0.0` | Exact version |
| `^1.0.0` | Compatible (>=1.0.0 <2.0.0) |
| `~1.0.0` | Patch-level (~1.0.x) |
| `>=1.0.0` | Greater than or equal |
| `<2.0.0` | Less than |
| `latest` | Latest available |

## Cross-Platform Example

```json
{
  "name": "universal-plugin",
  "version": "1.0.0",
  "description": "Works on all platforms",
  "skills": [
    {
      "name": "code-review",
      "description": "Automated code review",
      "context": "./context/skills/review.md",
      "files": ["./tools/helper.py"],
      "metadata": {
        "short-description": "Review code"
      }
    }
  ],
  "commands": [
    {
      "name": "lint",
      "description": "Run linting",
      "context": "./context/commands/lint.md",
      "metadata": {
        "applyTo": "**/*.py",
        "argument_hint": "[files...]",
        "allowed_tools": "Bash(lint:*)"
      }
    }
  ],
  "rules": [
    {
      "name": "typescript-style",
      "description": "TypeScript guidelines",
      "context": "./context/rules/typescript.md",
      "glob": "**/*.ts",
      "paths": ["src/**/*.ts"],
      "always": false
    }
  ]
}
```

Each platform uses the metadata keys it recognizes; unknown keys are ignored.
