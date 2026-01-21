# dex-plugin

Skills for dex plugin development.

## Installation

```bash
dex install --source git+https://github.com/LaunchCG/dex-plugin.git
```

## Skills

### dex-package-manager

Manages dex plugin packages and package.json. Understands:
- Package structure and schema
- Component definitions (skills, commands, instructions, rules)
- Platform-specific variants
- References the [dex repo](https://github.com/launchcg/dex) for source of truth

### context-writer

Writes clear, efficient context files. Specializes in:
- Deduplicating content using partials
- Jinja2 templating and variables
- Organizing context logically
- Concise, purposeful writing

## License

MIT
