# Dex Builder

You are an expert in building dex packages and registries using the modern HCL-based format. Dex is a universal package manager for AI coding agents that provides a standardized way to define, distribute, and install capabilities (skills, commands, rules, MCP servers) across multiple AI agent platforms.

## Quick Reference

### Package Format
- **Format**: HCL (HashiCorp Configuration Language)
- **Template Syntax**: Go `text/template`
- **Package File**: `package.hcl` (required)
- **Project File**: `dex.hcl` (optional, for project configuration)

### Core CLI Commands
```bash
dex init --platform <platform>    # Initialize a project
dex install <source>              # Install a plugin
dex install <name>@<version>      # Install specific version
dex uninstall <name>              # Uninstall a plugin
dex list                          # List installed plugins
dex pack                          # Validate package (in plugin dir)
```

### Resource Types by Platform

| Resource Type | Claude Code | Cursor | GitHub Copilot |
|---------------|:-----------:|:------:|:--------------:|
| Skills | `claude_skill` | - | `copilot_skill` |
| Commands | `claude_command` | `cursor_command` | - |
| Prompts | - | - | `copilot_prompt` |
| Agents | `claude_subagent` | - | `copilot_agent` |
| Rules (merged) | `claude_rule` | `cursor_rule` | `copilot_instruction` |
| Rules (standalone) | `claude_rules` | `cursor_rules` | `copilot_instructions` |
| Settings | `claude_settings` | - | - |
| MCP Servers | `claude_mcp_server` | `cursor_mcp_server` | `copilot_mcp_server` |

### HCL Functions
- `file("path")` - Read file content
- `templatefile("path.tmpl", {vars})` - Render template with Go template syntax
- `env("VAR")` or `env("VAR", "default")` - Read environment variable

---

## 1. HCL Package Format

### Package Block

Every plugin must have a `package` block in `package.hcl`:

```hcl
package {
  name        = "my-plugin"
  version     = "1.0.0"
  description = "Plugin description"
  author      = "Your Name"
  license     = "MIT"
  repository  = "https://github.com/owner/repo"
  platforms   = ["claude-code", "cursor", "github-copilot"]
}
```

**Attributes:**

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | yes | Plugin name (lowercase, hyphens allowed) |
| `version` | yes | Semantic version (e.g., "1.0.0") |
| `description` | no | Human-readable description |
| `author` | no | Plugin author |
| `license` | no | License identifier (e.g., "MIT") |
| `repository` | no | Source repository URL |
| `platforms` | no | Supported platforms (empty = all platforms) |

### Variable Block

Variables allow users to customize plugin behavior at installation:

```hcl
variable "python_version" {
  description = "Python version to use"
  default     = "3.11"
  required    = false
  env         = "PYTHON_VERSION"
}
```

**Attributes:**

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | yes | Variable identifier (block label) |
| `description` | no | Variable description |
| `default` | no | Default value if not provided |
| `required` | no | Whether user must provide a value |
| `env` | no | Environment variable to read from |

Variables can be referenced in templates using `{{ .Variables.python_version }}`.

### HCL Functions

**`file(path)`** - Reads a file relative to the plugin directory:

```hcl
claude_skill "example" {
  description = "Example skill"
  content     = file("skills/example.md")
}
```

**`templatefile(path, vars)`** - Renders a template file with Go template syntax:

```hcl
claude_skill "deployment" {
  description = "Deployment guidance"
  content     = templatefile("skills/deployment.md.tmpl", {
    environment = "production"
    region      = "us-east-1"
  })
}
```

**`env(name, default?)`** - Reads an environment variable:

```hcl
claude_mcp_server "database" {
  type = "command"
  source = "uvx:mcp-postgres"

  env = {
    DATABASE_URL = env("DATABASE_URL")
    DEBUG        = env("DEBUG", "false")
  }
}
```

---

## 2. Resource Types Reference

### Claude Code Resources

#### claude_skill

Skills provide specialized knowledge or capabilities. Installed to `.claude/skills/{plugin}-{name}/SKILL.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Block label identifying this skill |
| `description` | string | yes | When and how to use this skill |
| `content` | string | yes | The skill's instructions/knowledge |
| `argument_hint` | string | no | Hint shown during autocomplete (e.g., `"[filename]"`) |
| `disable_model_invocation` | bool | no | Prevent auto-loading; user must invoke manually |
| `user_invocable` | bool | no | Set to `false` to hide from `/` menu (default: true) |
| `allowed_tools` | list(string) | no | Tools Claude can use without asking |
| `model` | string | no | Model: `sonnet`, `haiku`, or `opus` |
| `context` | string | no | Set to `"fork"` to run in isolated subagent |
| `agent` | string | no | Subagent type when `context = "fork"` |
| `metadata` | map(string) | no | Additional frontmatter fields |

**Nested Blocks:**
- `file` - Static files to copy alongside
- `template_file` - Template files to render and copy

**Examples:**

Simple skill:
```hcl
claude_skill "code-review" {
  description = "Performs thorough code reviews"

  content = <<-EOT
    When reviewing code:
    1. Check for bugs and edge cases
    2. Evaluate code style and readability
    3. Look for security vulnerabilities
    4. Suggest improvements with examples
  EOT
}
```

Skill with content from file:
```hcl
claude_skill "testing" {
  description = "Helps write comprehensive tests using pytest"
  content     = file("skills/testing.md")
}
```

Skill with helper files:
```hcl
claude_skill "data-validation" {
  description = "Validates JSON data against schemas"
  content     = file("skills/data-validation.md")

  file {
    src = "schemas/user.schema.json"
  }

  file {
    src   = "scripts/validate.py"
    chmod = "755"
  }
}
```

Skill with templates:
```hcl
claude_skill "deployment" {
  description = "Guides deployment to configured environment"
  content     = templatefile("skills/deployment.md.tmpl", {
    environment = "production"
    region      = "us-east-1"
  })
}
```

Skill with tool restrictions:
```hcl
claude_skill "file-analyzer" {
  description   = "Analyzes files for issues"
  argument_hint = "[filename]"

  content = <<-EOT
    Analyze the specified file for:
    1. Code quality issues
    2. Performance bottlenecks
    3. Security vulnerabilities
  EOT

  allowed_tools = ["Read", "Grep", "Glob"]
  model         = "sonnet"
}
```

#### claude_command

Commands are user-invokable actions via `/{name}`. Installed to `.claude/commands/{plugin}-{name}.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Command name (invoked as `/{name}`) |
| `description` | string | yes | Brief description |
| `content` | string | yes | Command instructions |
| `argument_hint` | string | no | Hint for arguments |
| `allowed_tools` | list(string) | no | Tools this command can use |
| `model` | string | no | Model: `sonnet`, `haiku`, or `opus` |

**Nested Blocks:**
- `file` - Static files
- `template_file` - Template files

**Example:**

```hcl
claude_command "test" {
  description = "Run project tests"

  content = <<-EOT
    Run the project's test suite:
    1. Identify the test framework
    2. Run all tests
    3. Report results and failures
  EOT
}
```

With arguments:
```hcl
claude_command "deploy" {
  description   = "Deploy to environment"
  argument_hint = "[environment]"

  content = <<-EOT
    Deploy the application to the specified environment:
    1. Run tests first
    2. Build the application
    3. Push to container registry
    4. Update deployment
  EOT

  allowed_tools = ["Bash(docker:*)", "Bash(kubectl:*)"]
}
```

#### claude_subagent

Specialized agents for specific tasks. Installed to `.claude/agents/{plugin}-{name}.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Agent identifier |
| `description` | string | yes | When to use this agent |
| `content` | string | yes | Agent instructions |
| `model` | string | no | Model: `inherit`, `sonnet`, `haiku`, or `opus` |
| `color` | string | no | Display color: `blue`, `green`, `yellow`, `red`, `purple` |
| `tools` | list(string) | no | Allowed tools |

**Example:**

```hcl
claude_subagent "test-runner" {
  description = "Runs tests and reports results"

  content = <<-EOT
    You are a test runner agent. Your job is to:
    1. Identify relevant test files
    2. Run tests using the framework
    3. Report results clearly
    4. Suggest fixes for failures
  EOT

  model = "haiku"
  color = "green"
  tools = ["Bash", "Read", "Glob", "Grep"]
}
```

#### claude_rule

Rules merged into `CLAUDE.md`. Multiple plugins can contribute rules.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Rule identifier |
| `description` | string | yes | Rule description |
| `content` | string | yes | Rule content |
| `paths` | list(string) | no | File patterns for scoping |

**Example:**

```hcl
claude_rule "no-console-log" {
  description = "Avoid console.log in production"

  content = <<-EOT
    Do not use console.log() in production code.
    Use the project's logging framework instead.
  EOT
}
```

With path scoping:
```hcl
claude_rule "typescript-strict" {
  description = "TypeScript strict mode requirements"

  content = <<-EOT
    When writing TypeScript:
    - Always use explicit types, avoid `any`
    - Use strict null checks
    - Prefer interfaces over type aliases
  EOT

  paths = ["src/**/*.ts", "src/**/*.tsx"]
}
```

#### claude_rules

Standalone rules file. Installed to `.claude/rules/{plugin}-{name}.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Rules file identifier |
| `description` | string | yes | Rules description |
| `content` | string | yes | Rules content |
| `paths` | list(string) | no | File patterns for scoping |

**Example:**

```hcl
claude_rules "security" {
  description = "Security best practices"
  content     = file("rules/security.md")
  paths       = ["**/*.ts", "**/*.js"]
}
```

#### claude_settings

Settings merged into `.claude/settings.json`. Multiple plugins contribute.

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `allow` | list(string) | Tool patterns to auto-allow |
| `ask` | list(string) | Tool patterns requiring confirmation |
| `deny` | list(string) | Tool patterns to block |
| `env` | map(string) | Environment variables |

Project-level only:
- `enable_all_project_mcp_servers`
- `enabled_mcp_servers`
- `disabled_mcp_servers`
- `respect_gitignore`
- `include_co_authored_by`
- `model`
- `output_style`
- `always_thinking_enabled`
- `plans_directory`

**Example:**

```hcl
claude_settings "node-tools" {
  allow = [
    "Bash(npm:*)",
    "Bash(npx:*)",
    "Bash(node:*)",
  ]

  env = {
    NODE_ENV = "development"
  }
}
```

#### claude_mcp_server

MCP server configurations merged into `.mcp.json`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Server identifier |
| `description` | string | no | Server description |
| `type` | string | yes | Server type: `command` or `http` |
| `command` | string | conditional | Command to run (for `type = "command"`) |
| `args` | list(string) | no | Command-line arguments |
| `env` | map(string) | no | Environment variables |
| `source` | string | conditional | Package manager shortcut: `npm:`, `uvx:`, `pip:` |
| `url` | string | conditional | HTTP endpoint (for `type = "http"`) |

**Examples:**

Command-based:
```hcl
claude_mcp_server "filesystem" {
  type    = "command"
  command = "npx"
  args    = ["-y", "@anthropic/mcp-filesystem"]

  env = {
    HOME = env("HOME")
  }
}
```

Using source shortcut:
```hcl
claude_mcp_server "postgres" {
  type   = "command"
  source = "uvx:mcp-postgres"

  env = {
    DATABASE_URL = env("DATABASE_URL")
  }
}
```

HTTP-based:
```hcl
claude_mcp_server "remote-api" {
  description = "Remote API integration"
  type        = "http"
  url         = "https://mcp.example.com/api"
}
```

### Cursor Resources

#### cursor_rule

Rules merged into `AGENTS.md`.

```hcl
cursor_rule "coding-standards" {
  description = "Project coding standards"

  content = <<-EOT
    Always follow these coding standards:
    - Use TypeScript strict mode
    - Prefer async/await over callbacks
    - Document all public APIs
  EOT
}
```

#### cursor_rules

Standalone rules in `.cursor/rules/{plugin}-{name}.mdc`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Rules file identifier |
| `description` | string | yes | Rules description |
| `content` | string | yes | Rules content |
| `globs` | list(string) | no | File patterns |
| `always_apply` | bool | no | Always apply rule |

```hcl
cursor_rules "typescript" {
  description = "TypeScript best practices"
  globs       = ["**/*.ts", "**/*.tsx"]

  content = <<-EOT
    When writing TypeScript:
    - Always use explicit types
    - Use strict null checks
  EOT
}
```

#### cursor_command

Commands in `.cursor/commands/{plugin}-{name}.md`.

```hcl
cursor_command "test" {
  description = "Run project tests"

  content = <<-EOT
    Run the test suite and report results.
  EOT
}
```

#### cursor_mcp_server

MCP servers in `.cursor/mcp.json`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Server identifier |
| `type` | string | yes | Type: `stdio`, `http`, or `sse` |
| `command` | string | conditional | Command (for `stdio`) |
| `url` | string | conditional | URL (for `http`/`sse`) |
| `args` | list(string) | no | Arguments |
| `env` | map(string) | no | Environment variables |
| `env_file` | string | no | Env file path |
| `headers` | map(string) | no | HTTP headers |

### GitHub Copilot Resources

#### copilot_instruction

Instructions merged into `.github/copilot-instructions.md`.

```hcl
copilot_instruction "coding-standards" {
  description = "Project coding standards"

  content = <<-EOT
    Always follow these standards:
    - Use TypeScript strict mode
    - Document all public APIs
  EOT
}
```

#### copilot_instructions

Standalone instructions in `.github/instructions/{plugin}-{name}.instructions.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Instructions identifier |
| `description` | string | yes | Description |
| `content` | string | yes | Instructions content |
| `apply_to` | string | no | Glob pattern |

```hcl
copilot_instructions "typescript" {
  description = "TypeScript best practices"
  apply_to    = "**/*.ts"

  content = <<-EOT
    When writing TypeScript:
    - Use explicit types
    - Use strict null checks
  EOT
}
```

#### copilot_prompt

Prompts in `.github/prompts/{plugin}-{name}.prompt.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Prompt name |
| `description` | string | yes | Description |
| `content` | string | yes | Prompt instructions |
| `argument_hint` | string | no | Argument hint |
| `agent` | string | no | Agent mode: `ask`, `edit`, `agent`, or custom |
| `model` | string | no | Model selection |
| `tools` | list(string) | no | Tools to enable |

```hcl
copilot_prompt "review" {
  description = "Review code for issues"
  agent       = "ask"

  content = <<-EOT
    Review this code for:
    1. Bugs and edge cases
    2. Security vulnerabilities
    3. Performance issues
  EOT
}
```

#### copilot_agent

Agents in `.github/agents/{plugin}-{name}.agent.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Agent identifier |
| `description` | string | yes | When to use |
| `content` | string | yes | Agent instructions |
| `model` | string | no | Model selection |
| `tools` | list(string) | no | Available tools |
| `handoffs` | list(string) | no | Sequential workflow transitions |
| `infer` | bool | no | Enable subagent usage |
| `target` | string | no | Target: `vscode` or `github-copilot` |

```hcl
copilot_agent "test-runner" {
  description = "Runs tests and reports results"

  content = <<-EOT
    You run tests and report results clearly.
  EOT

  tools  = ["fetch", "search"]
  target = "vscode"
}
```

#### copilot_skill

Skills in `.github/skills/{plugin}-{name}/SKILL.md`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Skill name (max 64 chars) |
| `description` | string | yes | When to use (max 1024 chars) |
| `content` | string | yes | Skill instructions |

```hcl
copilot_skill "testing" {
  description = "Best practices for tests"

  content = <<-EOT
    When writing tests:
    1. Test happy paths and edge cases
    2. Use descriptive test names
    3. Follow Arrange-Act-Assert
  EOT
}
```

#### copilot_mcp_server

MCP servers in `.vscode/mcp.json`.

**Attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Server identifier |
| `type` | string | yes | Type: `stdio`, `http`, or `sse` |
| `command` | string | conditional | Command (for `stdio`) |
| `url` | string | conditional | URL (for `http`/`sse`) |
| `args` | list(string) | no | Arguments |
| `env` | map(string) | no | Environment variables |
| `env_file` | string | no | Env file path |
| `headers` | map(string) | no | HTTP headers |

---

## 3. Go Template Syntax

Dex uses Go's `text/template` package for templates.

### Template Variables

Available in `templatefile()` and `template_file` blocks:

| Variable | Description |
|----------|-------------|
| `{{ .ComponentDir }}` | Absolute path to installed component directory |
| `{{ .PluginName }}` | Name of the plugin |
| `{{ .PluginVersion }}` | Version of the plugin |
| `{{ .ProjectRoot }}` | Absolute path to project root |
| `{{ .Platform }}` | Target platform (e.g., `claude-code`) |

Custom variables passed to `templatefile()` are available as `{{ .VarName }}`.

### Control Structures

**Conditionals:**

```
{{ if eq .Platform "claude-code" }}
Claude Code specific content
{{ end }}

{{ if .UseDocker }}
Use Docker
{{ else }}
Use local environment
{{ end }}
```

**Loops:**

```
{{ range .Files }}
- {{ . }}
{{ end }}
```

**Comparisons:**

```
{{ if eq .Platform "claude-code" }}...{{ end }}
{{ if ne .Environment "production" }}...{{ end }}
{{ if and .Debug .Verbose }}...{{ end }}
{{ if or .UseDocker .UseK8s }}...{{ end }}
```

### Functions

```
{{ upper .Text }}        - Uppercase
{{ lower .Text }}        - Lowercase
{{ title .Text }}        - Title case
{{ trim .Text }}         - Trim whitespace
{{ replace .Text "a" "b" 1 }}  - Replace
```

### Example Template

**skills/setup.md.tmpl:**

```markdown
# Setup for {{ .PluginName }}

Version: {{ .PluginVersion }}

{{ if eq .Platform "claude-code" }}
## Claude Code Setup

Install dependencies:

```bash
cd {{ .ComponentDir }}
pip install -r requirements.txt
```
{{ else if eq .Platform "cursor" }}
## Cursor Setup

Configure your environment:

```bash
cd {{ .ComponentDir }}
npm install
```
{{ end }}

{{ if .EnableDebug }}
Debug mode is enabled.
{{ end }}
```

**Using in package.hcl:**

```hcl
claude_skill "setup" {
  description = "Project setup instructions"
  content     = templatefile("skills/setup.md.tmpl", {
    EnableDebug = "true"
  })
}
```


---

## 4. File and Template File Blocks

Resources can include additional files alongside the main content.

### file Block

Copies static files to the component directory.

**Attributes:**

| Attribute | Required | Description |
|-----------|----------|-------------|
| `src` | yes | Source path relative to plugin root |
| `dest` | no | Destination filename (defaults to basename) |
| `chmod` | no | File permissions (e.g., `"755"`) |

**Example:**

```hcl
claude_skill "data-validation" {
  description = "Validates JSON data"
  content     = file("skills/data-validation.md")

  file {
    src = "schemas/user.schema.json"
  }

  file {
    src   = "scripts/validate.py"
    dest  = "validate.py"
    chmod = "755"
  }

  file {
    src = "scripts/requirements.txt"
  }
}
```

This installs files to:
- `.claude/skills/plugin-data-validation/SKILL.md`
- `.claude/skills/plugin-data-validation/user.schema.json`
- `.claude/skills/plugin-data-validation/validate.py` (executable)
- `.claude/skills/plugin-data-validation/requirements.txt`

### template_file Block

Renders templates and copies them to the component directory.

**Attributes:**

| Attribute | Required | Description |
|-----------|----------|-------------|
| `src` | yes | Source template path |
| `dest` | no | Destination filename (defaults to basename without `.tmpl`) |
| `chmod` | no | File permissions |
| `vars` | no | Additional template variables |

**Example:**

```hcl
claude_command "setup" {
  description = "Project setup"
  content     = file("commands/setup.md")

  template_file {
    src   = "scripts/config.py.tmpl"
    dest  = "config.py"
    vars = {
      api_endpoint = "https://api.example.com"
      timeout      = "30"
    }
  }

  template_file {
    src   = "scripts/run.sh.tmpl"
    chmod = "755"
  }
}
```

**scripts/config.py.tmpl:**

```python
# Generated for {{ .PluginName }} v{{ .PluginVersion }}

API_ENDPOINT = "{{ .api_endpoint }}"
TIMEOUT = {{ .timeout }}
PROJECT_ROOT = "{{ .ProjectRoot }}"
```

---

## 5. Installation Paths by Platform

### Claude Code

| Resource | Installation Path |
|----------|-------------------|
| `claude_skill` | `.claude/skills/{plugin}-{name}/SKILL.md` |
| `claude_command` | `.claude/commands/{plugin}-{name}.md` |
| `claude_subagent` | `.claude/agents/{plugin}-{name}.md` |
| `claude_rule` | `CLAUDE.md` (merged with markers) |
| `claude_rules` | `.claude/rules/{plugin}-{name}.md` |
| `claude_settings` | `.claude/settings.json` (merged) |
| `claude_mcp_server` | `.mcp.json` (merged) |

### Cursor

| Resource | Installation Path |
|----------|-------------------|
| `cursor_rule` | `AGENTS.md` (merged with markers) |
| `cursor_rules` | `.cursor/rules/{plugin}-{name}.mdc` |
| `cursor_command` | `.cursor/commands/{plugin}-{name}.md` |
| `cursor_mcp_server` | `.cursor/mcp.json` (merged) |

### GitHub Copilot

| Resource | Installation Path |
|----------|-------------------|
| `copilot_skill` | `.github/skills/{plugin}-{name}/SKILL.md` |
| `copilot_prompt` | `.github/prompts/{plugin}-{name}.prompt.md` |
| `copilot_agent` | `.github/agents/{plugin}-{name}.agent.md` |
| `copilot_instruction` | `.github/copilot-instructions.md` (merged) |
| `copilot_instructions` | `.github/instructions/{plugin}-{name}.instructions.md` |
| `copilot_mcp_server` | `.vscode/mcp.json` (merged) |

---

## 6. Common Workflows

### Creating a New Plugin

```bash
# Create plugin directory
mkdir my-plugin
cd my-plugin

# Create package.hcl
cat > package.hcl << 'EOF'
package {
  name        = "my-plugin"
  version     = "1.0.0"
  description = "My awesome plugin"
  license     = "MIT"
}

claude_skill "example" {
  description = "Example skill"
  content     = file("skills/example.md")
}
EOF

# Create content
mkdir skills
cat > skills/example.md << 'EOF'
# Example Skill

You are an expert in example tasks.
EOF

# Validate the package
dex pack
```

### Installing Plugins

```bash
# Install from Git repository
dex install git+https://github.com/owner/plugin.git

# Install specific version
dex install git+https://github.com/owner/plugin.git@v1.0.0

# Install from local directory (for development)
dex install file:///path/to/plugin

# Install using relative path
dex install --source file://./examples/minimal
```

### Managing Installed Plugins

```bash
# List installed plugins
dex list

# Uninstall a plugin
dex uninstall plugin-name

# Uninstall specific version
dex uninstall plugin-name@1.0.0
```

### Using dex.hcl for Project Configuration

Create `dex.hcl` in your project root:

```hcl
project {
  name             = "my-webapp"
  agentic_platform = "claude-code"
}

plugin "python-tools" {
  source = "git+https://github.com/owner/python-tools.git"
  version = "^1.0.0"

  config = {
    python_version = "3.12"
    test_framework = "pytest"
  }
}

plugin "local-tools" {
  source = "file:///path/to/local-tools"
}
```

Then run:

```bash
dex sync  # Install all plugins from dex.hcl
```

---

## 7. Multi-Platform Plugins

Create plugins that work across multiple AI platforms.

### Sharing Content

Use `file()` to share the same content across platforms:

```hcl
package {
  name      = "code-review-tools"
  version   = "1.0.0"
  platforms = ["claude-code", "github-copilot"]
}

# Same content for both platforms
claude_skill "code-review" {
  description = "Code review capability"
  content     = file("content/code-review.md")
}

copilot_skill "code-review" {
  description = "Code review capability"
  content     = file("content/code-review.md")  # Same file!
}
```

### Platform-Specific Variations

Use `templatefile()` for platform-specific variations:

```hcl
# Claude Code command
claude_command "review" {
  description = "Run code review"
  content     = templatefile("commands/review.md.tmpl", {
    tool_name = "Read"
    platform  = "claude-code"
  })
}

# GitHub Copilot prompt
copilot_prompt "review" {
  description = "Run code review"
  content     = templatefile("commands/review.md.tmpl", {
    tool_name = "fetch"
    platform  = "github-copilot"
  })
}
```

**commands/review.md.tmpl:**

```markdown
# Code Review

{{ if eq .Platform "claude-code" }}
Use the Read tool to examine files.
{{ else if eq .Platform "github-copilot" }}
Use the fetch tool to examine files.
{{ end }}

Review for:
1. Bugs and edge cases
2. Security vulnerabilities
3. Performance issues
```

### Platform Detection in Templates

```markdown
# Setup

{{ if eq .Platform "claude-code" }}
This is Claude Code. Use Bash tool for commands.
{{ else if eq .Platform "cursor" }}
This is Cursor. Use shell commands.
{{ else if eq .Platform "github-copilot" }}
This is GitHub Copilot. Use VS Code terminal.
{{ end }}
```

---

## 8. Registry Management

Registries provide centralized plugin distribution.

### Registry Types

- **Local**: `file:///path/to/registry`
- **Git**: `git+https://github.com/owner/registry.git`
- **HTTPS**: `https://registry.example.com`
- **S3**: `s3://bucket-name/registry`
- **Azure**: `azure://container/registry`

### Registry Structure

A registry is a directory with:

```
registry/
├── registry.json     # Registry metadata
└── plugins/
    ├── plugin1.tar.gz
    ├── plugin2.tar.gz
    └── ...
```

**registry.json:**

```json
{
  "name": "my-registry",
  "description": "My plugin registry",
  "plugins": {
    "plugin-name": {
      "versions": {
        "1.0.0": {
          "description": "Plugin description",
          "tarball": "plugins/plugin-name-1.0.0.tar.gz",
          "sha256": "abc123..."
        }
      }
    }
  }
}
```

### Creating a Registry

```bash
# Create registry structure
mkdir -p my-registry/plugins

# Create registry.json
cat > my-registry/registry.json << 'EOF'
{
  "name": "my-registry",
  "description": "My plugin registry",
  "plugins": {}
}
EOF
```

### Publishing to Registry

```bash
# Package your plugin
cd my-plugin
dex pack
tar -czf ../my-registry/plugins/my-plugin-1.0.0.tar.gz .

# Update registry.json manually or with a script
# Add entry for your plugin version
```

### Using Registries

In `dex.hcl`:

```hcl
registry "company" {
  url = "https://plugins.company.com"
}

registry "local" {
  path = "/path/to/local-registry"
}

plugin "company-tools" {
  registry = "company"
  version  = "^1.0.0"
}
```

---

## 9. Best Practices

### Package Design

1. **Use semantic versioning**: Follow semver (major.minor.patch)
2. **Descriptive names**: Use clear, meaningful names for resources
3. **Document thoroughly**: Provide comprehensive instructions in content
4. **Test on all platforms**: Verify on each target platform

### Content Organization

1. **Share content**: Use `file()` to share content across platforms
2. **Use templates wisely**: Use `templatefile()` only when needed for variations
3. **Keep files organized**: Use subdirectories (skills/, commands/, rules/, scripts/)
4. **Version assets**: Tag releases in Git with version numbers

### Resource Recommendations

1. **Skills**: Provide specialized knowledge with clear use cases
2. **Commands**: Make commands focused and single-purpose
3. **Rules**: Keep rules concise and actionable
4. **MCP Servers**: Document required environment variables

### Security

1. **Avoid hardcoded secrets**: Use `env()` to read from environment
2. **Validate permissions**: Use `allowed_tools` to restrict capabilities
3. **Document requirements**: Specify required environment variables
4. **Review dependencies**: Audit MCP servers and helper scripts

### Performance

1. **Minimize file size**: Keep content concise
2. **Use appropriate models**: Use `haiku` for simple tasks
3. **Scope rules**: Use `paths` to limit rule application
4. **Lazy loading**: Use `disable_model_invocation` for specialized skills

### Maintenance

1. **Keep dependencies updated**: Update MCP server versions
2. **Test after changes**: Run `dex pack` after modifications
3. **Document changes**: Maintain a CHANGELOG
4. **Use Git tags**: Tag stable releases

---

## 10. Examples

### Minimal Plugin

**package.hcl:**

```hcl
package {
  name        = "hello-world"
  version     = "1.0.0"
  description = "Simple greeting skill"
  license     = "MIT"
}

claude_skill "greeter" {
  description = "Greets users warmly"
  content     = file("skills/greeter.md")
}
```

**skills/greeter.md:**

```markdown
# Greeter

You greet users warmly and professionally.

When a user starts a conversation, begin with a friendly greeting.
```

### Multi-Resource Plugin

**package.hcl:**

```hcl
package {
  name        = "dev-workflow"
  version     = "1.0.0"
  description = "Development workflow tools"
  author      = "DevTeam"
  license     = "MIT"
  platforms   = ["claude-code"]
}

claude_skill "dev-workflow" {
  description = "Development workflow best practices"
  content     = file("skills/dev-workflow.md")
}

claude_command "test" {
  description = "Run project tests"
  content     = file("commands/test.md")
}

claude_rule "code-style" {
  description = "Code style guidelines"
  content     = file("rules/code-style.md")
}

claude_settings "dev" {
  allow = [
    "Bash(npm:*)",
    "Bash(pytest:*)",
    "Bash(go test:*)",
  ]
}
```

### Multi-Platform Plugin

**package.hcl:**

```hcl
package {
  name        = "code-reviewer"
  version     = "1.0.0"
  description = "Code review across platforms"
  platforms   = ["claude-code", "github-copilot", "cursor"]
}

# Shared content
claude_skill "review" {
  description = "Perform code reviews"
  content     = file("content/shared-skill.md")
}

copilot_skill "review" {
  description = "Perform code reviews"
  content     = file("content/shared-skill.md")
}

# Platform-specific commands
claude_command "review" {
  description = "Review code"
  content     = templatefile("commands/review.md.tmpl", {
    tool = "Read"
  })
}

copilot_prompt "review" {
  description = "Review code"
  content     = templatefile("commands/review.md.tmpl", {
    tool = "fetch"
  })
}

cursor_command "review" {
  description = "Review code"
  content     = templatefile("commands/review.md.tmpl", {
    tool = "read_file"
  })
}
```

**commands/review.md.tmpl:**

```markdown
# Code Review

Use the {{ .tool }} tool to examine the code.

Check for:
1. Bugs and edge cases
2. Security vulnerabilities
3. Performance issues
4. Code style

{{ if eq .Platform "claude-code" }}
Use the Read and Grep tools to analyze files.
{{ else if eq .Platform "github-copilot" }}
Use fetch and search tools to analyze files.
{{ else if eq .Platform "cursor" }}
Use read_file to analyze files.
{{ end }}
```

---

## Reference Links

- Dex Repository: https://github.com/launchcg/dex
- HCL Documentation: https://github.com/hashicorp/hcl
- Go Templates: https://pkg.go.dev/text/template

---

## Summary

When building dex packages:

1. Use **HCL format** in `package.hcl`
2. Use **Go templates** with `templatefile()`
3. Define resources for target platforms (`claude_skill`, `copilot_skill`, etc.)
4. Share content with `file()` across platforms
5. Use templates for platform-specific variations
6. Test with `dex pack` before publishing
7. Document environment variables and requirements
8. Follow semantic versioning
9. Organize files in logical subdirectories

Always validate your package with `dex pack` before distributing.
