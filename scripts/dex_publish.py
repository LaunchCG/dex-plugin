#!/usr/bin/env python3
"""Publish a dex plugin to various targets."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], dry_run: bool = False, check: bool = True) -> subprocess.CompletedProcess | None:
    """Run a shell command."""
    if dry_run:
        print(f"  [dry-run] Would run: {' '.join(cmd)}")
        return None

    return subprocess.run(cmd, check=check, capture_output=True, text=True)


def publish_to_github(
    source: Path,
    repo: str,
    tag: str,
    draft: bool,
    dry_run: bool,
) -> bool:
    """Publish to GitHub as a release."""
    # Check if gh CLI is available
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: GitHub CLI (gh) not found. Install it from https://cli.github.com/", file=sys.stderr)
        return False

    # Check if authenticated
    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: Not authenticated with GitHub CLI. Run 'gh auth login' first.", file=sys.stderr)
        return False

    # Find or build the package
    dist_dir = source / "dist"
    package_files = list(dist_dir.glob("*.tar.gz")) + list(dist_dir.glob("*.zip"))

    if not package_files:
        print("No package found in dist/. Building first...")
        build_script = source / "scripts" / "dex_build.py"
        if build_script.exists():
            result = run_command(
                [sys.executable, str(build_script), str(source), "--checksum"],
                dry_run=dry_run,
            )
            if result and result.returncode != 0:
                print(f"Error: Build failed", file=sys.stderr)
                return False
            package_files = list(dist_dir.glob("*.tar.gz")) + list(dist_dir.glob("*.zip"))
        else:
            print("Error: No build script found and no packages in dist/", file=sys.stderr)
            return False

    if not package_files and not dry_run:
        print("Error: No package files found after build", file=sys.stderr)
        return False

    package_file = package_files[0] if package_files else Path("dist/package.tar.gz")

    # Load package.json for release notes
    package_data = json.loads((source / "package.json").read_text())
    name = package_data.get("name", source.name)
    description = package_data.get("description", "")

    # Create release
    cmd = [
        "gh", "release", "create", tag,
        "--repo", repo,
        "--title", f"{name} {tag}",
        "--notes", f"## {name}\n\n{description}\n\nInstall with:\n```bash\ndex add {repo}\n```",
    ]

    if draft:
        cmd.append("--draft")

    # Add package files
    for pf in package_files:
        cmd.append(str(pf))

    # Add checksum files
    for pf in package_files:
        checksum_file = pf.with_suffix(pf.suffix + ".sha256")
        if checksum_file.exists():
            cmd.append(str(checksum_file))

    print(f"Publishing {name} {tag} to github.com/{repo}...")
    result = run_command(cmd, dry_run=dry_run)

    if result and result.returncode != 0:
        print(f"Error: Failed to create release: {result.stderr}", file=sys.stderr)
        return False

    if not dry_run:
        print(f"✓ Published to https://github.com/{repo}/releases/tag/{tag}")

    return True


def publish_to_local(
    source: Path,
    registry_path: Path,
    dry_run: bool,
) -> bool:
    """Publish to a local registry directory."""
    # Load package info
    package_data = json.loads((source / "package.json").read_text())
    name = package_data.get("name", source.name)
    version = package_data.get("version", "0.0.0")

    # Create registry structure
    package_dir = registry_path / name / version
    print(f"Publishing {name} {version} to {registry_path}...")

    if dry_run:
        print(f"  [dry-run] Would create: {package_dir}")
        print(f"  [dry-run] Would copy plugin files")
        return True

    package_dir.mkdir(parents=True, exist_ok=True)

    # Copy all plugin files
    for item in source.iterdir():
        if item.name in [".git", "dist", "build", "__pycache__", ".dex"]:
            continue

        dest = package_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Create/update registry index
    index_path = registry_path / "index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text())
    else:
        index = {"packages": {}}

    if name not in index["packages"]:
        index["packages"][name] = {"versions": []}

    if version not in index["packages"][name]["versions"]:
        index["packages"][name]["versions"].append(version)
        index["packages"][name]["versions"].sort(key=lambda v: [int(x) for x in v.split(".")[:3]])
        index["packages"][name]["latest"] = index["packages"][name]["versions"][-1]

    index_path.write_text(json.dumps(index, indent=2) + "\n")

    print(f"✓ Published to {package_dir}")
    return True


def publish_to_registry(
    source: Path,
    registry_url: str,
    tag: str,
    dry_run: bool,
) -> bool:
    """Publish to a dex registry (future feature)."""
    print("Error: Remote registry publishing is not yet implemented.", file=sys.stderr)
    print("For now, use --target github or --target local", file=sys.stderr)
    return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Publish a dex plugin to various targets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --target github --repo owner/repo
  %(prog)s --target github --repo owner/repo --tag v1.0.0 --draft
  %(prog)s --target local --registry ~/.dex/local-registry
  %(prog)s --target github --repo owner/repo --dry-run
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
        "--target",
        choices=["github", "local", "registry"],
        required=True,
        help="Where to publish: github, local, or registry",
    )
    parser.add_argument(
        "--repo",
        help="GitHub repo (owner/repo) for github target",
    )
    parser.add_argument(
        "--tag",
        help="Release tag (default: version from package.json)",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        help="Registry path for local target",
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Create as draft release (github)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without doing it",
    )

    args = parser.parse_args()

    source = args.path.resolve()

    if not source.exists():
        print(f"Error: Source path not found: {source}", file=sys.stderr)
        return 1

    # Load package.json
    package_path = source / "package.json"
    if not package_path.exists():
        print(f"Error: package.json not found in {source}", file=sys.stderr)
        return 1

    try:
        package_data = json.loads(package_path.read_text())
    except json.JSONDecodeError as e:
        print(f"Error: Invalid package.json: {e}", file=sys.stderr)
        return 1

    # Determine tag/version
    version = package_data.get("version", "0.0.0")
    tag = args.tag or f"v{version}"

    if args.dry_run:
        print("[DRY RUN MODE - no changes will be made]\n")

    success = False

    if args.target == "github":
        if not args.repo:
            # Try to get from package.json
            repo = package_data.get("repository", "")
            if repo.startswith("https://github.com/"):
                repo = repo.replace("https://github.com/", "").rstrip("/")
            elif not repo:
                print("Error: --repo is required for github target", file=sys.stderr)
                return 1
            args.repo = repo

        success = publish_to_github(source, args.repo, tag, args.draft, args.dry_run)

    elif args.target == "local":
        registry = args.registry or Path.home() / ".dex" / "local-registry"
        success = publish_to_local(source, registry, args.dry_run)

    elif args.target == "registry":
        registry_url = os.environ.get("DEX_REGISTRY_URL", "https://registry.dex.dev")
        success = publish_to_registry(source, registry_url, tag, args.dry_run)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
