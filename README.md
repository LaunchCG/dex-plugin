# dex-builder

Build dex packages and registries using HCL-based dex format.

## Installation

Install using dex from a git repository:

```bash
dex install --source git+https://github.com/LaunchCG/dex-plugin.git
```

Or install from a local clone:

```bash
dex install --source file:///path/to/dex-plugin
```

## What This Plugin Provides

Once installed, Claude has complete knowledge of modern dex package development. Ask Claude to:

- "Create a new dex package for code review"
- "Build a dex registry for my team"
- "Show me how to use Go templates in dex"
- "Create a multi-platform dex package"

## Skills Included

### dex-builder

Comprehensive knowledge of:

- **HCL Package Format**: Using `package.hcl` with package blocks, variable blocks, and resource blocks
- **Go Template Syntax**: Using Go's `text/template` with `templatefile()`
- **Resource Types**: Complete reference for all resource types across platforms:
  - Claude Code: `claude_skill`, `claude_command`, `claude_subagent`, `claude_rule`, `claude_rules`, `claude_settings`, `claude_mcp_server`
  - Cursor: `cursor_rule`, `cursor_rules`, `cursor_command`, `cursor_mcp_server`
  - GitHub Copilot: `copilot_skill`, `copilot_prompt`, `copilot_agent`, `copilot_instruction`, `copilot_instructions`, `copilot_mcp_server`
- **Template Variables**: Using `{{ .ComponentDir }}`, `{{ .PluginName }}`, `{{ .PluginVersion }}`, `{{ .ProjectRoot }}`, `{{ .Platform }}`
- **HCL Functions**: `file()`, `templatefile()`, `env()`
- **Registry Management**: Creating and publishing to registries
- **Multi-Platform Development**: Sharing content across platforms
- **Best Practices**: Security, performance, organization, and testing

## Examples

This plugin includes working examples in the `examples/` directory:

### Minimal Example

Simple single-skill package demonstrating basic structure:

```bash
cd examples/minimal
dex pack  # Validate the package
```

### Multi-Resource Example

Complex package with multiple resource types (skill, command, rule, settings):

```bash
cd examples/multi-resource
dex pack
```

### Multi-Platform Example

Cross-platform package demonstrating content sharing and platform-specific variations:

```bash
cd examples/multi-platform
dex pack
```

## Quick Start

After installing this plugin, try creating a new dex package:

```bash
# Create a new directory
mkdir my-plugin
cd my-plugin

# Ask Claude to create a dex package
# Claude now knows the complete dex format and can guide you
```

Example prompts:

- "Create a package.hcl for a Python testing plugin"
- "Add a claude_command that runs tests"
- "Show me how to use templatefile() for multi-platform support"
- "Create a skill with helper files"

## Format Reference

### Package File

```hcl
package {
  name        = "my-plugin"
  version     = "1.0.0"
  description = "My awesome plugin"
  license     = "MIT"
  platforms   = ["claude-code", "cursor", "github-copilot"]
}
```

### Resource Example

```hcl
claude_skill "example" {
  description = "Example skill"
  content     = file("skills/example.md")

  file {
    src   = "scripts/helper.sh"
    chmod = "755"
  }
}
```

### Template Example

```hcl
claude_command "deploy" {
  description = "Deploy the application"
  content     = templatefile("commands/deploy.md.tmpl", {
    environment = "production"
  })
}
```

## Source Material

This plugin is based on the latest dex documentation:

- [Dex Repository](https://github.com/launchcg/dex)
- [Resource Reference](https://github.com/launchcg/dex/blob/main/docs/RESOURCES.md)
- [Plugin Development Guide](https://github.com/launchcg/dex/blob/main/docs/plugins.md)

## License

MIT
