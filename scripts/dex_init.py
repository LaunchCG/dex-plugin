#!/usr/bin/env python3
"""Scaffold a new dex plugin project."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


MINIMAL_TEMPLATE = {
    "package.json": {
        "name": "",
        "version": "0.1.0",
        "description": "",
        "repository": "",
        "skills": [],
    },
    "context/skills/main.md": "# {name}\n\nYour skill content here.\n",
    "README.md": "# {name}\n\nA dex plugin.\n\n## Installation\n\n```bash\ndex add {name}\n```\n",
}

FULL_TEMPLATE = {
    "package.json": {
        "name": "",
        "version": "0.1.0",
        "description": "",
        "repository": "",
        "skills": [],
        "commands": [],
        "instructions": [],
    },
    "context/skills/main.md": "# {name}\n\nYour skill content here.\n",
    "context/commands/example.md": "# Example Command\n\nCommand content here.\n",
    "context/instructions/example.md": "# Example Instruction\n\nInstruction content here.\n",
    "README.md": "# {name}\n\nA dex plugin.\n\n## Installation\n\n```bash\ndex add {name}\n```\n\n## Skills\n\n- main: Primary skill\n\n## Commands\n\n- /example: Example command\n\n## Instructions\n\n- example: Example instruction\n",
}

MCP_TEMPLATE = {
    "package.json": {
        "name": "",
        "version": "0.1.0",
        "description": "",
        "repository": "",
        "skills": [],
        "mcp": {
            "servers": {
                "": {
                    "command": "python",
                    "args": ["scripts/server.py"],
                }
            }
        },
    },
    "context/skills/main.md": "# {name}\n\nYour skill content here.\n\n## MCP Server\n\nThis plugin includes an MCP server that provides additional tools.\n",
    "scripts/server.py": '''#!/usr/bin/env python3
"""MCP server for {name}."""
from __future__ import annotations

import json
import sys


def main():
    """Run the MCP server."""
    # Implement your MCP server here
    # See https://modelcontextprotocol.io for details
    print(json.dumps({{"error": "Not implemented"}}))
    sys.exit(1)


if __name__ == "__main__":
    main()
''',
    "README.md": "# {name}\n\nA dex plugin with MCP server.\n\n## Installation\n\n```bash\ndex add {name}\n```\n\n## MCP Server\n\nThis plugin provides an MCP server with the following tools:\n\n- TODO: Document your tools\n",
}


def get_template(template_name: str, with_mcp: bool) -> dict:
    """Get the template configuration."""
    if with_mcp or template_name == "mcp-server":
        return MCP_TEMPLATE
    elif template_name == "full":
        return FULL_TEMPLATE
    else:
        return MINIMAL_TEMPLATE


def create_plugin(
    name: str,
    template: str,
    with_mcp: bool,
    with_commands: bool,
    output: Path,
) -> None:
    """Create a new plugin from template."""
    template_config = get_template(template, with_mcp)

    # Create output directory
    output.mkdir(parents=True, exist_ok=True)

    for file_path, content in template_config.items():
        full_path = output / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path == "package.json":
            # Handle package.json specially
            content = dict(content)
            content["name"] = name
            content["description"] = f"A dex plugin: {name}"

            # Add skill reference
            content["skills"] = [
                {
                    "name": "main",
                    "context": "context/skills/main.md",
                }
            ]

            # Add commands if requested
            if with_commands or template == "full":
                content["commands"] = [
                    {
                        "name": "example",
                        "context": "context/commands/example.md",
                    }
                ]
                content["instructions"] = [
                    {
                        "name": "example",
                        "context": "context/instructions/example.md",
                    }
                ]

            # Update MCP server name
            if "mcp" in content:
                servers = content["mcp"]["servers"]
                old_key = list(servers.keys())[0]
                servers[name] = servers.pop(old_key)

            full_path.write_text(json.dumps(content, indent=2) + "\n")
        else:
            # Handle text files
            text = content.format(name=name)
            full_path.write_text(text)

    # Create additional directories
    (output / "context" / "_partials").mkdir(parents=True, exist_ok=True)

    # Add command/instruction templates if requested but not in template
    if with_commands and template == "minimal":
        commands_dir = output / "context" / "commands"
        commands_dir.mkdir(parents=True, exist_ok=True)
        (commands_dir / "example.md").write_text("# Example Command\n\nCommand content here.\n")

        instructions_dir = output / "context" / "instructions"
        instructions_dir.mkdir(parents=True, exist_ok=True)
        (instructions_dir / "example.md").write_text("# Example Instruction\n\nInstruction content here.\n")

    print(f"Created dex plugin '{name}' at {output}")
    print("\nNext steps:")
    print(f"  cd {output}")
    print("  # Edit context files in context/")
    print("  # Validate with: python scripts/dex_validate.py")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scaffold a new dex plugin project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-plugin                    Create minimal plugin named 'my-plugin'
  %(prog)s --template full              Create full-featured plugin
  %(prog)s --with-mcp my-server         Create plugin with MCP server
  %(prog)s --output ~/plugins my-plugin Create plugin at custom location
        """,
    )

    parser.add_argument(
        "name",
        nargs="?",
        help="Plugin name (defaults to directory name)",
    )
    parser.add_argument(
        "--template",
        choices=["minimal", "full", "mcp-server"],
        default="minimal",
        help="Template to use (default: minimal)",
    )
    parser.add_argument(
        "--with-mcp",
        action="store_true",
        help="Include MCP server boilerplate",
    )
    parser.add_argument(
        "--with-commands",
        action="store_true",
        help="Include command templates",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Output directory (default: current dir)",
    )

    args = parser.parse_args()

    # Determine plugin name
    name = args.name or args.output.name
    if not name or name == ".":
        name = Path.cwd().name

    # Validate name
    if not name.replace("-", "").replace("_", "").isalnum():
        print(f"Error: Invalid plugin name '{name}'", file=sys.stderr)
        return 1

    # Determine output directory
    output = args.output
    if args.name and output == Path.cwd():
        output = output / args.name

    try:
        create_plugin(
            name=name,
            template=args.template,
            with_mcp=args.with_mcp,
            with_commands=args.with_commands,
            output=output,
        )
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
