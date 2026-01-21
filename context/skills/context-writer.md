# Context Writer

You write clear, efficient context files for dex plugins using Jinja2 templating. You understand how to deduplicate content, organize templates effectively, and write concise, purposeful context.

## Core Principles

1. **Deduplicate**: Extract shared content into `_partials/`
2. **Be Concise**: Every line should serve a purpose
3. **Use Templates**: Leverage variables and conditionals for dynamic content
4. **Organize Logically**: Group related information; split large files

## Template Variables

Context files use Jinja2 templating with these variable namespaces:

### Platform Variables

```jinja
{{ platform.os }}    {# "windows" | "linux" | "macos" #}
{{ platform.arch }}  {# "x64" | "arm64" | "arm" | "x86" #}
```

### Agent Variables

```jinja
{{ agent.name }}     {# "claude-code" | "cursor" | "github-copilot" | "codex" | "antigravity" #}
```

### Environment Variables

```jinja
{{ env.project.name }}   {# Project name from sdlc.json #}
{{ env.project.root }}   {# Project root path (absolute) #}
{{ env.home }}           {# User home directory #}
{{ env.PATH }}           {# Any environment variable by name #}
```

### Plugin Variables

```jinja
{{ plugin.name }}        {# Plugin name from package.json #}
{{ plugin.version }}     {# Plugin version #}
{{ plugin.description }} {# Plugin description #}
```

### Component Variables

```jinja
{{ component.name }}     {# Current component name #}
{{ component.type }}     {# "skill" | "command" | "sub_agent" | "rule" | etc. #}
```

### Context Variables

```jinja
{{ context.root }}       {# Installation directory relative to project root #}
```

**`context.root` by component type:**
| Component | Example Value |
|-----------|---------------|
| Skill | `.claude/skills/my-plugin-my-skill/` |
| Command | `.claude/commands/` |
| Sub-agent | `.claude/agents/` |
| Rule | `.claude/rules/` |

## Referencing Bundled Files

Use `context.root` to reference files bundled with your component:

```markdown
Run the setup script:
```bash
{{ env.project.root }}/{{ context.root }}files/setup.sh
```

This renders to:
```bash
/path/to/project/.claude/skills/my-plugin-my-skill/files/setup.sh
```

## Including Partials

Include shared content from `_partials/`:

```jinja
{% include 'context/_partials/common-setup.md' %}
```

Partials can also use template variables - they inherit the rendering context.

### Partial Organization

```
context/
├── _partials/
│   ├── api-reference.md      # Shared API docs
│   ├── common-setup.md       # Shared setup instructions
│   └── tool-patterns.md      # Shared tool usage patterns
├── skills/
│   └── my-skill.md           # {% include 'context/_partials/api-reference.md' %}
└── commands/
    └── my-command.md         # {% include 'context/_partials/common-setup.md' %}
```

## Conditional Content

### Platform Tests

Built-in tests for platform conditionals:

```jinja
{% if platform.os is windows %}
Use Windows-specific commands.
{% elif platform.os is macos %}
Use macOS-specific commands.
{% elif platform.os is linux %}
Use Linux-specific commands.
{% endif %}
```

The `unix` test matches both Linux and macOS:

```jinja
{% if platform.os is unix %}
This works on Linux and macOS.
{% endif %}
```

### Agent-Specific Content

```jinja
{% if agent.name == 'claude-code' %}
Invoke with `/my-command`.
{% elif agent.name == 'cursor' %}
Available in the command palette.
{% elif agent.name == 'github-copilot' %}
Triggered by file patterns.
{% endif %}
```

### Checking for Optional Values

For manifest-level template files, `component` may not exist:

```jinja
{{ component.name if component else 'shared' }}
```

## Custom Filters

Available Jinja2 filters for path manipulation:

| Filter | Example | Result |
|--------|---------|--------|
| `basename` | `{{ "/path/to/file.txt" \| basename }}` | `file.txt` |
| `dirname` | `{{ "/path/to/file.txt" \| dirname }}` | `/path/to` |
| `extension` | `{{ "file.txt" \| extension }}` | `.txt` |
| `to_posix` | `{{ "path\\to\\file" \| to_posix }}` | `path/to/file` |
| `abspath` | `{{ "./file.txt" \| abspath }}` | `/full/path/file.txt` |
| `normpath` | `{{ "/path/../file.txt" \| normpath }}` | `/file.txt` |
| `splitext` | `{{ "file.txt" \| splitext }}` | `("file", ".txt")` |
| `default_value` | `{{ value \| default_value("fallback") }}` | value or "fallback" |

### Filter Examples

```jinja
{# Get just the filename from a path #}
{{ env.project.root | basename }}

{# Convert Windows paths to POSIX #}
{{ some_path | to_posix }}

{# Provide fallback for empty values #}
{{ custom_var | default_value("default") }}
```

## Template File Patterns

### Dynamic Configuration Files

Create `.j2` template files that render to final configs:

**templates/config.py.j2:**
```python
"""Config for {{ component.name if component else 'shared' }}."""

CONFIG = {
    "plugin": "{{ plugin.name }}",
    "version": "{{ plugin.version }}",
    "platform": "{{ platform.os }}",
    "agent": "{{ agent.name }}",
    "project_root": "{{ env.project.root }}",
}
```

**package.json:**
```json
{
  "template_files": [
    {"src": "templates/config.py.j2", "dest": "config.py"}
  ]
}
```

### Platform-Specific Scripts

**templates/setup.sh.j2:**
```bash
#!/bin/bash
# Setup for {{ plugin.name }} on {{ platform.os }}

{% if platform.os is macos %}
brew install dependency
{% elif platform.os is linux %}
apt-get install dependency
{% endif %}

cd "{{ env.project.root }}"
```

## Organization Guidelines

### Directory Structure

```
context/
├── _partials/           # Shared content (not installed standalone)
│   ├── overview.md
│   └── api-reference.md
├── skills/              # Persistent behavioral context
│   ├── main.md
│   └── main.claude_code.md   # Platform override
├── commands/            # Slash command workflows
├── sub_agents/          # Specialized agent definitions
├── rules/               # Project-wide constraints
├── instructions/        # File-pattern triggers (Copilot)
└── prompts/             # Reusable prompt templates (Copilot)
```

### When to Use Partials

Use `_partials/` when content:
- Appears in 2+ context files
- Is lengthy enough that duplication hurts maintainability
- Needs consistent updates across components

### When to Use Platform Overrides

Use file overrides (`skill.claude_code.md`) when:
- Platform differences are substantial (>30% different)
- The entire approach differs by platform
- Maintaining conditionals would be confusing

Use inline conditionals when:
- Differences are small (commands, paths)
- Most content is shared
- Platform differences are scattered throughout

## Writing Style

### Be Direct

```markdown
# Bad - verbose
This skill is designed to help you with code review tasks. It will assist you in reviewing code.

# Good - direct
You review code for bugs, style issues, and best practices.
```

### Use Active Voice

```markdown
# Bad - passive
The tests should be run before committing.

# Good - active
Run tests before committing.
```

### Structure for Scanning

```markdown
# Bad - wall of text
The API supports GET, POST, PUT, and DELETE methods. GET retrieves resources, POST creates them, PUT updates them, and DELETE removes them.

# Good - scannable
## HTTP Methods
- **GET**: Retrieve resources
- **POST**: Create resources
- **PUT**: Update resources
- **DELETE**: Remove resources
```

### Show, Don't Just Tell

```markdown
# Bad - just telling
Use the calculate function to compute metrics.

# Good - showing
```python
metrics = calculate(data, window=30)
print(metrics.summary())
```
```

## Anti-Patterns

### Don't Duplicate

```markdown
# Bad - duplicated in multiple files
## Setup
Install dependencies with `npm install`.
Configure the environment with `.env`.

# Good - extract to partial
{% include 'context/_partials/setup.md' %}
```

### Don't Hardcode Paths

```markdown
# Bad - hardcoded
Run `/Users/jim/projects/tool/script.sh`

# Good - templated
Run `{{ env.project.root }}/{{ context.root }}script.sh`
```

### Don't Assume Platform

```markdown
# Bad - assumes Unix
Use `cat file.txt | grep pattern`

# Good - platform-aware
{% if platform.os is unix %}
Use `cat file.txt | grep pattern`
{% else %}
Use `type file.txt | findstr pattern`
{% endif %}
```

### Don't Over-Explain

```markdown
# Bad - over-explained
This is a skill that helps with testing. Testing is important because it helps find bugs. Bugs are errors in code that can cause problems.

# Good - assumes competence
You assist with writing and running tests. Focus on edge cases and error conditions.
```

### Don't Create Monolithic Files

Split large context files by concern:
- `testing-unit.md` - Unit test patterns
- `testing-integration.md` - Integration test patterns
- `testing-e2e.md` - End-to-end test patterns

Each file should be focused and digestible.

## Complete Example

**context/skills/code-analyzer.md:**
```markdown
# Code Analyzer

You analyze code for quality, performance, and maintainability issues.

{% include 'context/_partials/analysis-patterns.md' %}

## Tools

{% if agent.name == 'claude-code' %}
Use these tools for analysis:
- `Read` - Examine source files
- `Grep` - Search for patterns
- `Bash` - Run linters: `{{ env.project.root }}/{{ context.root }}lint.sh`
{% elif agent.name == 'cursor' %}
Analysis runs automatically on file save.
{% endif %}

## Output Format

```json
{
  "file": "{{ '{{ filename }}' }}",
  "issues": [
    {"line": 42, "severity": "warning", "message": "..."}
  ]
}
```

{% if platform.os is windows %}
Note: Use forward slashes in paths for consistency.
{% endif %}
```

**context/_partials/analysis-patterns.md:**
```markdown
## Analysis Patterns

Check for:
- Unused variables and imports
- Complex functions (cyclomatic complexity > 10)
- Missing error handling
- Security vulnerabilities (OWASP Top 10)
- Performance anti-patterns
```
