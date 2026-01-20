#!/usr/bin/env python3
"""Manage upstream dependencies for dex plugins."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


UPSTREAMS_FILE = ".dex/upstreams.json"


def load_upstreams(plugin_path: Path) -> dict:
    """Load upstreams configuration."""
    upstreams_path = plugin_path / UPSTREAMS_FILE
    if upstreams_path.exists():
        return json.loads(upstreams_path.read_text())
    return {"upstreams": {}}


def save_upstreams(plugin_path: Path, data: dict) -> None:
    """Save upstreams configuration."""
    upstreams_path = plugin_path / UPSTREAMS_FILE
    upstreams_path.parent.mkdir(parents=True, exist_ok=True)
    upstreams_path.write_text(json.dumps(data, indent=2) + "\n")


def parse_upstream_url(url: str) -> tuple[str, str, str | None]:
    """Parse an upstream URL and return (type, location, ref)."""
    # GitHub URL
    github_match = re.match(r"(?:https?://)?github\.com/([^/]+/[^/@#]+)(?:@([^#]+))?(?:#(.+))?", url)
    if github_match:
        repo = github_match.group(1)
        ref = github_match.group(2) or "main"
        path = github_match.group(3)
        return ("github", repo, ref)

    # Local path
    if url.startswith("/") or url.startswith("./") or url.startswith("~"):
        path = Path(url).expanduser().resolve()
        return ("local", str(path), None)

    # Git URL
    if url.endswith(".git") or url.startswith("git@"):
        return ("git", url, "main")

    # Assume it's a GitHub shorthand (owner/repo)
    if "/" in url and not url.startswith("http"):
        parts = url.split("@")
        repo = parts[0]
        ref = parts[1] if len(parts) > 1 else "main"
        return ("github", repo, ref)

    return ("unknown", url, None)


def cmd_add(args: argparse.Namespace) -> int:
    """Add an upstream dependency."""
    plugin_path = args.path.resolve()
    url = args.url

    upstream_type, location, ref = parse_upstream_url(url)

    if upstream_type == "unknown":
        print(f"Error: Could not parse upstream URL: {url}", file=sys.stderr)
        return 1

    # Determine name
    name = args.name
    if not name:
        if upstream_type == "github":
            name = location.split("/")[-1]
        elif upstream_type == "local":
            name = Path(location).name
        else:
            name = location.split("/")[-1].replace(".git", "")

    upstreams = load_upstreams(plugin_path)

    if name in upstreams["upstreams"] and not args.force:
        print(f"Error: Upstream '{name}' already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    upstreams["upstreams"][name] = {
        "type": upstream_type,
        "location": location,
        "ref": ref,
        "url": url,
    }

    save_upstreams(plugin_path, upstreams)
    print(f"✓ Added upstream '{name}' ({upstream_type}: {location})")

    if not args.no_sync:
        print(f"\nSyncing '{name}'...")
        return sync_upstream(plugin_path, name, upstreams["upstreams"][name], args.force)

    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List current upstreams."""
    plugin_path = args.path.resolve()
    upstreams = load_upstreams(plugin_path)

    if not upstreams["upstreams"]:
        print("No upstreams configured.")
        return 0

    print("Configured upstreams:\n")
    for name, config in upstreams["upstreams"].items():
        upstream_type = config.get("type", "unknown")
        location = config.get("location", "")
        ref = config.get("ref", "")
        ref_str = f"@{ref}" if ref else ""

        print(f"  {name}")
        print(f"    Type: {upstream_type}")
        print(f"    Location: {location}{ref_str}")
        print()

    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    """Remove an upstream dependency."""
    plugin_path = args.path.resolve()
    name = args.name

    upstreams = load_upstreams(plugin_path)

    if name not in upstreams["upstreams"]:
        print(f"Error: Upstream '{name}' not found.", file=sys.stderr)
        return 1

    del upstreams["upstreams"][name]
    save_upstreams(plugin_path, upstreams)

    # Optionally remove synced files
    upstream_dir = plugin_path / ".dex" / "upstream" / name
    if upstream_dir.exists() and args.clean:
        shutil.rmtree(upstream_dir)
        print(f"✓ Removed upstream '{name}' and cached files")
    else:
        print(f"✓ Removed upstream '{name}'")

    return 0


def sync_upstream(plugin_path: Path, name: str, config: dict, force: bool = False) -> int:
    """Sync a single upstream."""
    upstream_type = config.get("type")
    location = config.get("location")
    ref = config.get("ref", "main")

    cache_dir = plugin_path / ".dex" / "upstream" / name

    if upstream_type == "github":
        return sync_github(location, ref, cache_dir, force)
    elif upstream_type == "local":
        return sync_local(Path(location), cache_dir, force)
    elif upstream_type == "git":
        return sync_git(location, ref, cache_dir, force)
    else:
        print(f"Error: Unknown upstream type: {upstream_type}", file=sys.stderr)
        return 1


def sync_github(repo: str, ref: str, cache_dir: Path, force: bool) -> int:
    """Sync from GitHub."""
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: GitHub CLI (gh) not found. Install from https://cli.github.com/", file=sys.stderr)
        return 1

    cache_dir.mkdir(parents=True, exist_ok=True)

    # Clone or update repo
    if (cache_dir / ".git").exists():
        print(f"  Updating {repo}@{ref}...")
        subprocess.run(["git", "-C", str(cache_dir), "fetch", "origin"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(cache_dir), "checkout", ref], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(cache_dir), "pull", "origin", ref], check=False, capture_output=True)
    else:
        print(f"  Cloning {repo}@{ref}...")
        subprocess.run(
            ["gh", "repo", "clone", repo, str(cache_dir), "--", "--branch", ref],
            check=True,
            capture_output=True,
        )

    print(f"  ✓ Synced to {cache_dir}")
    return 0


def sync_local(source: Path, cache_dir: Path, force: bool) -> int:
    """Sync from local path."""
    if not source.exists():
        print(f"Error: Local path not found: {source}", file=sys.stderr)
        return 1

    cache_dir.mkdir(parents=True, exist_ok=True)

    # Create symlink or copy
    if cache_dir.exists():
        if cache_dir.is_symlink():
            cache_dir.unlink()
        else:
            shutil.rmtree(cache_dir)

    # Use symlink for local upstreams
    cache_dir.symlink_to(source)
    print(f"  ✓ Linked to {source}")

    return 0


def sync_git(url: str, ref: str, cache_dir: Path, force: bool) -> int:
    """Sync from git URL."""
    cache_dir.mkdir(parents=True, exist_ok=True)

    if (cache_dir / ".git").exists():
        print(f"  Updating {url}@{ref}...")
        subprocess.run(["git", "-C", str(cache_dir), "fetch", "origin"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(cache_dir), "checkout", ref], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(cache_dir), "pull", "origin", ref], check=False, capture_output=True)
    else:
        print(f"  Cloning {url}@{ref}...")
        subprocess.run(
            ["git", "clone", "--branch", ref, url, str(cache_dir)],
            check=True,
            capture_output=True,
        )

    print(f"  ✓ Synced to {cache_dir}")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Update one or all upstreams."""
    plugin_path = args.path.resolve()
    upstreams = load_upstreams(plugin_path)

    if not upstreams["upstreams"]:
        print("No upstreams configured.")
        return 0

    names = list(upstreams["upstreams"].keys()) if args.all or not args.name else [args.name]

    errors = 0
    for name in names:
        if name not in upstreams["upstreams"]:
            print(f"Error: Upstream '{name}' not found.", file=sys.stderr)
            errors += 1
            continue

        print(f"\nUpdating '{name}'...")
        result = sync_upstream(plugin_path, name, upstreams["upstreams"][name], args.force)
        if result != 0:
            errors += 1

    return 1 if errors > 0 else 0


def cmd_sync(args: argparse.Namespace) -> int:
    """Sync local plugin with upstream changes."""
    plugin_path = args.path.resolve()
    upstreams = load_upstreams(plugin_path)

    if not upstreams["upstreams"]:
        print("No upstreams configured.")
        return 0

    print("Syncing all upstreams...")

    errors = 0
    for name, config in upstreams["upstreams"].items():
        print(f"\nSyncing '{name}'...")
        result = sync_upstream(plugin_path, name, config, args.force)
        if result != 0:
            errors += 1

    if errors == 0:
        print("\n✓ All upstreams synced")
    else:
        print(f"\n⚠ {errors} upstream(s) failed to sync")

    return 1 if errors > 0 else 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage upstream dependencies for dex plugins.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  add URL              Add upstream dependency
  list                 List current upstreams
  remove NAME          Remove an upstream
  update [NAME]        Update one or all upstreams
  sync                 Sync local with upstream changes

Examples:
  %(prog)s add github.com/owner/repo
  %(prog)s add owner/repo@v1.0.0
  %(prog)s add ~/local/plugin --name my-local
  %(prog)s list
  %(prog)s update --all
  %(prog)s sync
        """,
    )

    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Path to plugin directory (default: current dir)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add upstream dependency")
    add_parser.add_argument("url", help="Upstream URL (GitHub repo, git URL, or local path)")
    add_parser.add_argument("--name", help="Name for the upstream (default: derived from URL)")
    add_parser.add_argument("--force", action="store_true", help="Overwrite existing upstream")
    add_parser.add_argument("--no-sync", action="store_true", help="Don't sync after adding")

    # List command
    list_parser = subparsers.add_parser("list", help="List current upstreams")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an upstream")
    remove_parser.add_argument("name", help="Name of upstream to remove")
    remove_parser.add_argument("--clean", action="store_true", help="Also remove cached files")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update one or all upstreams")
    update_parser.add_argument("name", nargs="?", help="Name of upstream to update")
    update_parser.add_argument("--all", action="store_true", help="Update all upstreams")
    update_parser.add_argument("--force", action="store_true", help="Force overwrite local changes")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync local with upstream changes")
    sync_parser.add_argument("--force", action="store_true", help="Force overwrite local changes")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "add":
        return cmd_add(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "remove":
        return cmd_remove(args)
    elif args.command == "update":
        return cmd_update(args)
    elif args.command == "sync":
        return cmd_sync(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
