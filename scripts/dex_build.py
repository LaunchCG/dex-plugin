#!/usr/bin/env python3
"""Build a distributable dex plugin package."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Iterator


# Files/directories to exclude by default
DEFAULT_EXCLUDES = [
    ".git",
    ".gitignore",
    ".github",
    "__pycache__",
    "*.pyc",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    ".env",
    ".envrc",
    ".DS_Store",
    "Thumbs.db",
    "dist",
    "build",
    "*.egg-info",
    ".dex",
]

# Additional dev files to exclude unless --include-dev
DEV_FILES = [
    "tests",
    "test_*.py",
    "*_test.py",
    "conftest.py",
    "pytest.ini",
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    "Makefile",
    ".pre-commit-config.yaml",
    "tox.ini",
    ".coverage",
    "htmlcov",
]


def matches_pattern(path: Path, patterns: list[str]) -> bool:
    """Check if path matches any of the patterns."""
    name = path.name
    for pattern in patterns:
        if pattern.startswith("*."):
            if name.endswith(pattern[1:]):
                return True
        elif pattern.endswith("*"):
            if name.startswith(pattern[:-1]):
                return True
        elif "*" in pattern:
            # Simple glob matching
            import fnmatch
            if fnmatch.fnmatch(name, pattern):
                return True
        else:
            if name == pattern:
                return True
    return False


def get_files_to_include(
    source: Path,
    include_dev: bool = False,
) -> Iterator[Path]:
    """Get list of files to include in the package."""
    excludes = DEFAULT_EXCLUDES.copy()
    if not include_dev:
        excludes.extend(DEV_FILES)

    for path in source.rglob("*"):
        if path.is_dir():
            continue

        # Check if any parent directory should be excluded
        skip = False
        for parent in path.relative_to(source).parents:
            if matches_pattern(source / parent, excludes):
                skip = True
                break

        if skip:
            continue

        # Check if file itself should be excluded
        if matches_pattern(path, excludes):
            continue

        yield path


def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def build_tarball(
    source: Path,
    output_path: Path,
    include_dev: bool = False,
) -> None:
    """Build a .tar.gz package."""
    package_name = source.name

    with tarfile.open(output_path, "w:gz") as tar:
        for file_path in get_files_to_include(source, include_dev):
            rel_path = file_path.relative_to(source)
            arcname = f"{package_name}/{rel_path}"
            tar.add(file_path, arcname=arcname)

    print(f"Created: {output_path}")


def build_zipfile(
    source: Path,
    output_path: Path,
    include_dev: bool = False,
) -> None:
    """Build a .zip package."""
    package_name = source.name

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in get_files_to_include(source, include_dev):
            rel_path = file_path.relative_to(source)
            arcname = f"{package_name}/{rel_path}"
            zf.write(file_path, arcname=arcname)

    print(f"Created: {output_path}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build a distributable dex plugin package.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Build package in ./dist
  %(prog)s --output ./releases      Build to custom directory
  %(prog)s --format zip             Build as zip file
  %(prog)s --checksum               Generate SHA256 checksum file
  %(prog)s --include-dev            Include test files
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
        "--output",
        type=Path,
        default=Path("./dist"),
        help="Output directory (default: ./dist)",
    )
    parser.add_argument(
        "--format",
        choices=["tar.gz", "zip"],
        default="tar.gz",
        help="Archive format (default: tar.gz)",
    )
    parser.add_argument(
        "--include-dev",
        action="store_true",
        help="Include dev files (tests, etc.)",
    )
    parser.add_argument(
        "--checksum",
        action="store_true",
        help="Generate SHA256 checksum file",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean output directory before building",
    )

    args = parser.parse_args()

    source = args.path.resolve()

    if not source.exists():
        print(f"Error: Source path not found: {source}", file=sys.stderr)
        return 1

    # Load package.json to get name and version
    package_path = source / "package.json"
    if not package_path.exists():
        print(f"Error: package.json not found in {source}", file=sys.stderr)
        return 1

    try:
        package_data = json.loads(package_path.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: Invalid package.json: {e}", file=sys.stderr)
        return 1

    name = package_data.get("name", source.name)
    version = package_data.get("version", "0.0.0")

    # Create output directory
    output_dir = args.output
    if not output_dir.is_absolute():
        output_dir = source / output_dir

    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Build archive
    extension = "tar.gz" if args.format == "tar.gz" else "zip"
    output_path = output_dir / f"{name}-{version}.{extension}"

    print(f"Building {name} v{version}...")

    if args.format == "tar.gz":
        build_tarball(source, output_path, args.include_dev)
    else:
        build_zipfile(source, output_path, args.include_dev)

    # Generate checksum
    if args.checksum:
        checksum = calculate_checksum(output_path)
        checksum_path = output_path.with_suffix(output_path.suffix + ".sha256")
        checksum_path.write_text(f"{checksum}  {output_path.name}\n")
        print(f"Created: {checksum_path}")
        print(f"SHA256: {checksum}")

    # Print file info
    size = output_path.stat().st_size
    if size < 1024:
        size_str = f"{size} B"
    elif size < 1024 * 1024:
        size_str = f"{size / 1024:.1f} KB"
    else:
        size_str = f"{size / (1024 * 1024):.1f} MB"

    print(f"\nPackage size: {size_str}")

    # List included files
    file_count = sum(1 for _ in get_files_to_include(source, args.include_dev))
    print(f"Files included: {file_count}")

    print(f"\n✓ Build complete: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
