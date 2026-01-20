#!/usr/bin/env python3
"""Validate a dex plugin package."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    """Result of a validation check."""
    level: str  # "error", "warning", "info"
    message: str
    path: str | None = None
    fixable: bool = False


class Validator:
    """Validates a dex plugin package."""

    REQUIRED_FIELDS = ["name", "version"]
    OPTIONAL_FIELDS = ["description", "repository", "author", "license", "skills", "commands", "instructions", "mcp"]
    COMPONENT_FIELDS = ["name", "context"]
    VALID_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9\-_]*$")
    VALID_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$")

    def __init__(self, path: Path, strict: bool = False, check_files: bool = True):
        self.path = path
        self.strict = strict
        self.check_files = check_files
        self.results: list[ValidationResult] = []
        self.package_data: dict = {}

    def error(self, message: str, path: str | None = None, fixable: bool = False) -> None:
        """Record an error."""
        self.results.append(ValidationResult("error", message, path, fixable))

    def warning(self, message: str, path: str | None = None, fixable: bool = False) -> None:
        """Record a warning."""
        self.results.append(ValidationResult("warning", message, path, fixable))

    def info(self, message: str, path: str | None = None) -> None:
        """Record info."""
        self.results.append(ValidationResult("info", message, path))

    def validate(self) -> bool:
        """Run all validation checks."""
        self.validate_package_json()
        self.validate_structure()
        self.validate_context_files()

        return self.is_valid()

    def is_valid(self) -> bool:
        """Check if validation passed."""
        errors = [r for r in self.results if r.level == "error"]
        if self.strict:
            warnings = [r for r in self.results if r.level == "warning"]
            return len(errors) == 0 and len(warnings) == 0
        return len(errors) == 0

    def validate_package_json(self) -> None:
        """Validate package.json file."""
        package_path = self.path / "package.json"

        if not package_path.exists():
            self.error("package.json not found", "package.json")
            return

        try:
            self.package_data = json.loads(package_path.read_text())
        except json.JSONDecodeError as e:
            self.error(f"Invalid JSON in package.json: {e}", "package.json")
            return

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in self.package_data:
                self.error(f"Missing required field: {field}", "package.json", fixable=True)
            elif not self.package_data[field]:
                self.error(f"Empty required field: {field}", "package.json")

        # Validate name format
        name = self.package_data.get("name", "")
        if name and not self.VALID_NAME_PATTERN.match(name):
            self.error(
                f"Invalid plugin name '{name}': must be lowercase alphanumeric with hyphens/underscores",
                "package.json",
            )

        # Validate version format
        version = self.package_data.get("version", "")
        if version and not self.VALID_VERSION_PATTERN.match(version):
            self.error(
                f"Invalid version '{version}': must be semver (e.g., 1.0.0)",
                "package.json",
            )

        # Check for recommended fields
        if "description" not in self.package_data:
            self.warning("Missing recommended field: description", "package.json", fixable=True)

        if "repository" not in self.package_data:
            self.warning("Missing recommended field: repository", "package.json", fixable=True)

        # Validate components
        for component_type in ["skills", "commands", "instructions"]:
            self.validate_components(component_type)

        # Validate MCP config
        if "mcp" in self.package_data:
            self.validate_mcp_config()

    def validate_components(self, component_type: str) -> None:
        """Validate a component array (skills, commands, instructions)."""
        components = self.package_data.get(component_type, [])

        if not isinstance(components, list):
            self.error(f"{component_type} must be an array", "package.json")
            return

        names_seen = set()
        for i, component in enumerate(components):
            if not isinstance(component, dict):
                self.error(f"{component_type}[{i}] must be an object", "package.json")
                continue

            for field in self.COMPONENT_FIELDS:
                if field not in component:
                    self.error(f"{component_type}[{i}] missing required field: {field}", "package.json")

            name = component.get("name", "")
            if name in names_seen:
                self.error(f"Duplicate {component_type} name: {name}", "package.json")
            names_seen.add(name)

            # Check context file exists
            context_path = component.get("context", "")
            if context_path and self.check_files:
                full_path = self.path / context_path
                if not full_path.exists():
                    self.error(f"Context file not found: {context_path}", context_path)

    def validate_mcp_config(self) -> None:
        """Validate MCP server configuration."""
        mcp = self.package_data.get("mcp", {})

        if not isinstance(mcp, dict):
            self.error("mcp must be an object", "package.json")
            return

        servers = mcp.get("servers", {})
        if not isinstance(servers, dict):
            self.error("mcp.servers must be an object", "package.json")
            return

        for server_name, server_config in servers.items():
            if not isinstance(server_config, dict):
                self.error(f"mcp.servers.{server_name} must be an object", "package.json")
                continue

            if "command" not in server_config:
                self.error(f"mcp.servers.{server_name} missing required field: command", "package.json")

    def validate_structure(self) -> None:
        """Validate directory structure."""
        context_dir = self.path / "context"

        if not context_dir.exists():
            self.error("context/ directory not found")
            return

        # Check for at least one context type
        has_content = False
        for subdir in ["skills", "commands", "instructions"]:
            subdir_path = context_dir / subdir
            if subdir_path.exists() and any(subdir_path.glob("*.md")):
                has_content = True
                break

        if not has_content:
            self.warning("No context files found in context/skills/, context/commands/, or context/instructions/")

    def validate_context_files(self) -> None:
        """Validate context markdown files."""
        if not self.check_files:
            return

        context_dir = self.path / "context"
        if not context_dir.exists():
            return

        for md_file in context_dir.rglob("*.md"):
            # Skip partials (they're included in other files)
            if "_partials" in str(md_file):
                continue

            content = md_file.read_text()

            # Check for empty files
            if not content.strip():
                self.warning(f"Empty context file", str(md_file.relative_to(self.path)))

            # Check for placeholder content
            if "TODO" in content or "FIXME" in content:
                self.info(f"Contains TODO/FIXME markers", str(md_file.relative_to(self.path)))

    def fix_issues(self) -> int:
        """Attempt to fix fixable issues."""
        fixed = 0

        for result in self.results:
            if not result.fixable:
                continue

            if result.path == "package.json":
                if "Missing required field: name" in result.message:
                    self.package_data["name"] = self.path.name
                    fixed += 1
                elif "Missing required field: version" in result.message:
                    self.package_data["version"] = "0.1.0"
                    fixed += 1
                elif "Missing recommended field: description" in result.message:
                    self.package_data["description"] = f"A dex plugin: {self.package_data.get('name', self.path.name)}"
                    fixed += 1

        if fixed > 0:
            package_path = self.path / "package.json"
            package_path.write_text(json.dumps(self.package_data, indent=2) + "\n")

        return fixed

    def print_results(self) -> None:
        """Print validation results."""
        for result in self.results:
            icon = {"error": "✗", "warning": "⚠", "info": "ℹ"}[result.level]
            path = f" ({result.path})" if result.path else ""
            fix = " [fixable]" if result.fixable else ""
            print(f"  {icon} {result.message}{path}{fix}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate a dex plugin package.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     Validate plugin in current directory
  %(prog)s ./my-plugin         Validate plugin at path
  %(prog)s --strict            Fail on warnings too
  %(prog)s --fix               Auto-fix simple issues
        """,
    )

    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Path to plugin directory (default: current dir)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings too",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix simple issues (missing fields, formatting)",
    )
    parser.add_argument(
        "--check-files",
        action="store_true",
        default=True,
        help="Verify all referenced context/script files exist (default: True)",
    )
    parser.add_argument(
        "--no-check-files",
        action="store_false",
        dest="check_files",
        help="Skip file existence checks",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="Use custom schema file (not yet implemented)",
    )

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        return 1

    if not args.path.is_dir():
        print(f"Error: Not a directory: {args.path}", file=sys.stderr)
        return 1

    validator = Validator(args.path, strict=args.strict, check_files=args.check_files)

    print(f"Validating plugin at {args.path}...")
    valid = validator.validate()

    if args.fix and not valid:
        fixed = validator.fix_issues()
        if fixed > 0:
            print(f"\nFixed {fixed} issue(s). Re-validating...")
            validator = Validator(args.path, strict=args.strict, check_files=args.check_files)
            valid = validator.validate()

    if validator.results:
        print("\nResults:")
        validator.print_results()

    errors = len([r for r in validator.results if r.level == "error"])
    warnings = len([r for r in validator.results if r.level == "warning"])

    print(f"\n{errors} error(s), {warnings} warning(s)")

    if valid:
        print("✓ Validation passed")
        return 0
    else:
        print("✗ Validation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
