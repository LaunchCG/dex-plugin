# Template Variables

Dex context files support Jinja2 templating. The following variables are available:

## Context Variables

### `{{ context.root }}`
Installation directory for the component, relative to the project root. Includes trailing slash.

Example values by component type:
- Skill: `.claude/skills/my-plugin-my-skill/`
- Command: `.claude/commands/`

```markdown
Run the bundled script:
python "{{ context.root }}scripts/setup.py"
```

## Platform Variables

### `{{ platform.os }}`
Operating system: `windows`, `linux`, or `macos`.

### `{{ platform.arch }}`
CPU architecture: `x64`, `arm64`, `arm`, or `x86`.

## Agent Variables

### `{{ agent.name }}`
Current AI agent: `claude-code`, `cursor`, `github-copilot`, etc.

## Environment Variables

### `{{ env.project.root }}`
Absolute path to the user's project root directory.

### `{{ env.project.name }}`
Name of the user's project (directory name).

### `{{ env.home }}`
User's home directory path.

### `{{ env.* }}`
Any environment variable (e.g., `{{ env.PATH }}`).

## Plugin Variables

### `{{ plugin.name }}`
Name of the plugin from package.json.

### `{{ plugin.version }}`
Version of the plugin.

### `{{ plugin.description }}`
Description of the plugin.

## Component Variables

### `{{ component.name }}`
Name of the current component.

### `{{ component.type }}`
Type of component: `skill`, `command`, `sub_agent`, etc.

## Common Patterns

### Referencing bundled scripts
```markdown
python "{{ context.root }}scripts/my_script.py" --option value
```

### Platform-conditional content
```markdown
{% if agent.name == 'claude-code' %}
Use the `/command` slash command to invoke this tool.
{% else %}
This tool is available as an instruction trigger.
{% endif %}
```

### OS-specific instructions
```markdown
{% if platform.os == 'macos' %}
On macOS, you can also use `pbcopy` for clipboard operations.
{% endif %}
```

### Including partials
```markdown
{% include '_partials/common-setup.md' %}
```

## Notes

- All paths should use forward slashes (`/`) for cross-platform compatibility
- Template variables are resolved at install time
- Use quotes around paths that might contain spaces
- Partials in `_partials/` are not installed as standalone files
- `context.root` is relative to project root; combine with `env.project.root` for absolute path
