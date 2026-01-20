# Using the Dex Plugin Development Tools

This plugin includes Python scripts for common dex plugin development tasks. All scripts are located in the `scripts/` directory.

## Available Tools

### dex_init.py - Scaffold New Plugin
Create a new dex plugin project with the proper structure.

```bash
# Create minimal plugin in current directory
python "{{ context.root }}scripts/dex_init.py" my-plugin

# Create full-featured plugin
python "{{ context.root }}scripts/dex_init.py" --template full my-plugin

# Create plugin with MCP server
python "{{ context.root }}scripts/dex_init.py" --with-mcp my-mcp-plugin

# Create plugin at specific location
python "{{ context.root }}scripts/dex_init.py" --output ~/plugins my-plugin
```

### dex_validate.py - Validate Plugin
Check a plugin for errors and warnings.

```bash
# Validate current directory
python "{{ context.root }}scripts/dex_validate.py"

# Validate specific path
python "{{ context.root }}scripts/dex_validate.py" ./my-plugin

# Strict mode (fail on warnings)
python "{{ context.root }}scripts/dex_validate.py" --strict

# Auto-fix simple issues
python "{{ context.root }}scripts/dex_validate.py" --fix
```

### dex_build.py - Build Package
Create a distributable package.

```bash
# Build to ./dist
python "{{ context.root }}scripts/dex_build.py"

# Build to custom location
python "{{ context.root }}scripts/dex_build.py" --output ./releases

# Build as zip instead of tar.gz
python "{{ context.root }}scripts/dex_build.py" --format zip

# Include checksum file
python "{{ context.root }}scripts/dex_build.py" --checksum

# Include dev/test files
python "{{ context.root }}scripts/dex_build.py" --include-dev
```

### dex_publish.py - Publish Plugin
Publish to GitHub, local registry, or other targets.

```bash
# Publish to GitHub
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/repo

# Publish specific version
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/repo --tag v1.0.0

# Create draft release
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/repo --draft

# Publish to local registry
python "{{ context.root }}scripts/dex_publish.py" --target local --registry ~/.dex/local-registry

# Dry run (see what would happen)
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/repo --dry-run
```

### dex_upstream.py - Manage Dependencies
Manage upstream plugin dependencies.

```bash
# Add upstream from GitHub
python "{{ context.root }}scripts/dex_upstream.py" add owner/repo

# Add specific version
python "{{ context.root }}scripts/dex_upstream.py" add owner/repo@v1.0.0

# Add local upstream
python "{{ context.root }}scripts/dex_upstream.py" add ~/local/plugin --name my-local

# List upstreams
python "{{ context.root }}scripts/dex_upstream.py" list

# Update all upstreams
python "{{ context.root }}scripts/dex_upstream.py" update --all

# Sync with upstream changes
python "{{ context.root }}scripts/dex_upstream.py" sync
```

## Common Workflows

### Creating a New Plugin
```bash
# 1. Scaffold the plugin
python "{{ context.root }}scripts/dex_init.py" --template full my-plugin
cd my-plugin

# 2. Edit context files
# ... edit context/skills/*.md, etc.

# 3. Validate
python "{{ context.root }}scripts/dex_validate.py" --strict

# 4. Build
python "{{ context.root }}scripts/dex_build.py" --checksum

# 5. Publish
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/my-plugin
```

### Updating a Plugin
```bash
# 1. Make changes
# ... edit files

# 2. Update version in package.json

# 3. Validate
python "{{ context.root }}scripts/dex_validate.py"

# 4. Build and publish
python "{{ context.root }}scripts/dex_build.py" --checksum
python "{{ context.root }}scripts/dex_publish.py" --target github --repo owner/repo
```

### Working with Upstreams
```bash
# Add a base plugin as upstream
python "{{ context.root }}scripts/dex_upstream.py" add owner/base-plugin

# Keep synced with upstream changes
python "{{ context.root }}scripts/dex_upstream.py" sync
```
