#!/usr/bin/env python3
"""
🎯 Simple Dotfiles Linker - Creates symlinks based on available dot-config.json 🎯

✨ A vibrant and user-friendly dotfile management tool that helps you organize
   your configuration files with style! ✨

🚀 Features:
   • 📦 Install dotfiles with automatic symlink creation
   • 📊 Check status of all your dotfile links
   • 🧹 Clean up orphaned symlinks automatically
   • 💾 Automatic backup creation for safety
   • 🎨 Beautiful, colorful output with emoji indicators
   • ⚡ Fast and reliable symlink management

💡 Usage:
   /usr/bin/python3 linker.py [install|status|clean]
   you can pass on alternate config file with option -c | --config

🎉 Made with ❤️ for developers who love organized configs! 🎉
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Set, TypedDict

# 🛡️ SAFETY CONFIGURATION 🛡️
# Critical paths that should never be symlinked to prevent catastrophic damage
PROTECTED_PATHS = {
    ".",  # Home directory itself
    "",  # Empty path (also home dir)
    "~",  # Home directory reference
    ".config",  # Entire config directory
    ".local",  # Entire local directory
    ".ssh",  # SSH directory (security risk)
    ".gnupg",  # GPG directory (security risk)
    "Documents",  # User documents folder
    "Desktop",  # Desktop folder
    "Downloads",  # Downloads folder
    "Pictures",  # Pictures folder
    "Music",  # Music folder
    "Videos",  # Videos folder
    "Library",  # macOS Library folder
    "AppData",  # Windows AppData folder
}

# Paths that should trigger additional confirmation
RISKY_PATHS = {
    ".local",
    ".cache",
    ".mozilla",
    ".chrome",
    ".firefox",
    "Library",
    "AppData",
}


class DotfileEntry(TypedDict):
    """Configuration entry for a dotfile/directory"""

    source: str  # Path relative to repo root
    target: str  # Path relative to home directory
    type: str  # "file" or "directory"


class Config(TypedDict):
    """Configuration structure"""

    dotfiles: List[DotfileEntry]


def is_safe_target(target_path: str) -> tuple[bool, str]:
    """
    Check if target path is safe to symlink

    Returns:
        tuple[bool, str]: (is_safe, reason_if_unsafe)
    """
    if not target_path:
        return False, "Empty target path detected"

    # Normalize the path for comparison
    normalized_path = Path(target_path).as_posix().strip("/")

    # Check against absolutely protected paths
    if normalized_path in PROTECTED_PATHS:
        return (
            False,
            f"Protected system path: '{target_path}' - This could damage your system!",
        )

    # Check for parent directory references that could escape home
    if ".." in Path(target_path).parts:
        return False, "Parent directory references (..) are not allowed for security"

    # Check for absolute paths (should be relative to home)
    if Path(target_path).is_absolute():
        return (
            False,
            "Absolute paths are not allowed - use paths relative to home directory",
        )

    return True, ""


def confirm_risky_operation(target_path: str, source_path: str) -> bool:
    """
    Ask user to confirm potentially risky operations

    Args:
        target_path: The target path to check
        source_path: The source path for context

    Returns:
        bool: True if user confirms, False otherwise
    """
    # Check if any part of the path is in risky paths
    path_parts = Path(target_path).parts
    risky_found = []

    for part in path_parts:
        if part in RISKY_PATHS:
            risky_found.append(part)

    if risky_found:
        print("\n🚨 RISKY OPERATION DETECTED 🚨")
        print(f"Target: {target_path}")
        print(f"Source: {source_path}")
        print(f"Risky components: {', '.join(risky_found)}")
        print(
            "\n⚠️  This operation could affect important system/application directories!"
        )
        print("⚠️  Make sure this is exactly what you want to do.")
        print("\n💡 Consider using a more specific path instead.")

        while True:
            response = input(
                "\n🤔 Are you absolutely sure you want to proceed? (type 'YES' in capitals): "
            ).strip()
            if response == "YES":
                print("✅ Proceeding with risky operation...")
                return True
            elif response.lower() in ["no", "n", "quit", "exit", ""]:
                print("🛑 Operation cancelled for safety")
                return False
            else:
                print("❌ Please type 'YES' in capitals to confirm, or 'no' to cancel")

    return True


def validate_config_safety(
    config: Config, script_dir: Path, home_dir: Path, dry_run: bool = False
) -> bool:
    """
    Validate all entries in config for safety before processing

    Args:
        config: The loaded configuration
        script_dir: Repository directory
        home_dir: Home directory
        dry_run: If True, only validate without asking for confirmations

    Returns:
        bool: True if all entries are safe or approved, False otherwise
    """
    print("🛡️ Running safety validation on configuration...")

    unsafe_entries = []
    risky_entries = []

    for i, entry in enumerate(config["dotfiles"]):
        target_path = entry["target"]
        source_path = entry["source"]

        # Check if target is safe
        is_safe, reason = is_safe_target(target_path)

        if not is_safe:
            unsafe_entries.append((i, entry, reason))
            continue

        # Check if source exists and is accessible
        full_source_path = script_dir / source_path
        if not full_source_path.exists():
            print(f"⚠️  Warning: Source doesn't exist: {source_path}")
            continue

        # Check for risky operations
        if any(risky in target_path for risky in RISKY_PATHS):
            risky_entries.append((i, entry))

    # Handle unsafe entries (these are blocked completely)
    if unsafe_entries:
        print("\n❌ UNSAFE CONFIGURATION DETECTED ❌")
        print("The following entries are blocked for your safety:\n")

        for i, entry, reason in unsafe_entries:
            print(f"  Entry #{i + 1}:")
            print(f"    Source: {entry['source']}")
            print(f"    Target: {entry['target']}")
            print(f"    Reason: {reason}")
            print()

        print(
            "🚫 Please fix these entries in your configuration file before proceeding."
        )
        return False

    # Handle risky entries (these need confirmation)
    if risky_entries and not dry_run:
        print("\n⚠️  RISKY OPERATIONS DETECTED ⚠️")
        print("The following entries require your confirmation:\n")

        for i, entry in risky_entries:
            print(f"  Entry #{i + 1}: {entry['source']} -> {entry['target']}")

        print()

        for i, entry in risky_entries:
            print(f"🔍 Reviewing entry #{i + 1}:")
            if not confirm_risky_operation(entry["target"], entry["source"]):
                return False

    if risky_entries:
        print(
            f"✅ Safety validation completed - {len(risky_entries)} risky operations approved"
        )
    else:
        print("✅ Safety validation completed - all entries look safe")

    return True


def create_backup(file_path: Path, backup_dir: Path) -> bool:
    """Create a timestamped backup of a file or directory"""

    try:
        # Create backup directory if it doesn't exist
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Generate timestamped backup name
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name: str = f"{file_path.name}_{timestamp}"
        backup_path: Path = backup_dir / backup_name

        if file_path.is_file() or file_path.is_symlink():
            shutil.copy2(file_path, backup_path, follow_symlinks=False)
        elif file_path.is_dir():
            shutil.copytree(file_path, backup_path, symlinks=True)
        else:
            print(f"  ⚠️  Warning: Cannot backup unknown file type: {file_path}")
            return False

        print(f"  💾 Created backup: {backup_path}")
        return True

    except OSError as e:
        print(f"  ❌ Error creating backup for {file_path}: {e}")
        return False


def create_symlink(source_path: Path, target_path: Path, backup_dir: Path) -> bool:
    """Create a symlink from source to target, backing up existing files"""
    try:
        # Create parent directories if they don't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Backup existing file/link if it exists
        if target_path.exists() or target_path.is_symlink():
            if target_path.is_symlink():
                print(f"  🔗 Found existing symlink: {target_path}")
            elif target_path.is_dir():
                print(f"  📁 Found existing dir: {target_path}")
            else:
                print(f"  📄 Found existing file: {target_path}")

            # Create backup before removing
            if not create_backup(target_path, backup_dir):
                print(
                    f"  🚫 Error: Could not create backup for {target_path}, skipping symlink creation"
                )
                return False

            # Remove after successful backup
            target_path.unlink() if (
                target_path.is_file() or target_path.is_symlink()
            ) else shutil.rmtree(target_path)

        # Create the symlink
        target_path.symlink_to(source_path)
        print(f"  ✅ Created symlink: {target_path} -> {source_path}")
        return True

    except OSError as e:
        print(f"  ❌ Error creating symlink {target_path} -> {source_path}: {e}")
        return False


def load_config(config_path: Path) -> Config:
    """Load configuration from JSON file"""
    try:
        with config_path.open("r", encoding="utf-8") as f:
            config_data: Config = json.load(f)

        # Validate structure
        if "dotfiles" not in config_data:
            raise KeyError("'dotfiles' key missing from config")

        if not isinstance(config_data["dotfiles"], list):
            raise TypeError(
                "values for 'dotfiles' key must be a list [{source, target, type}]"
            )

        # Validate each dotfile entry
        for i, entry in enumerate(config_data["dotfiles"]):
            if not isinstance(entry, dict):
                raise TypeError(f"dotfiles[{i}] must be a dictionary")

            required_keys: list[str] = ["source", "target", "type"]
            for key in required_keys:
                if key not in entry:
                    raise KeyError(f"dotfiles[{i}] missing required key: '{key}'")
                if not isinstance(entry[key], str):  # type: ignore[literal-required]
                    raise TypeError(f"dotfiles[{i}]['{key}'] must be a string")

            if entry["type"] not in ["file", "directory"]:
                raise ValueError(
                    f"dotfiles[{i}]['type'] must be 'file' or 'directory', got: {entry['type']}"
                )

        return config_data

    except FileNotFoundError:
        print(f"❌ Error: Config file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    except (KeyError, TypeError, ValueError) as e:
        print(f"❌ Error: Invalid config structure: {e}")
        sys.exit(1)


def discover_managed_symlinks(script_dir: Path, home_dir: Path) -> Set[Path]:
    """Discover all symlinks in home directory that point to files in script_dir"""
    managed_links: Set[Path] = set()

    def check_symlink(path: Path) -> None:
        """Check if a symlink points to our managed directory"""
        if path.is_symlink():
            try:
                target: Path = path.resolve()
                # Check if the target is within our script directory
                if script_dir in target.parents or target == script_dir:
                    managed_links.add(path)
            except OSError:
                # Broken symlink, ignore
                pass

    # Check common locations for dotfiles
    locations_to_check: List[Path] = [
        home_dir,  # Root level dotfiles
        home_dir / ".config",  # Config directory
        home_dir / "temp",  # temp directory
        home_dir / ".local" / "share",  # Local share
        home_dir / ".local" / "bin",  # Local binaries
    ]

    for location in locations_to_check:
        if not location.exists():
            continue

        # Check direct children for symlinks
        try:
            for item in location.iterdir():
                if item.is_symlink():
                    check_symlink(item)
        except PermissionError:
            # Skip directories we can't read
            continue

    return managed_links


def clean_orphaned_symlinks(config_path: Path, script_dir: Path, home_dir: Path) -> int:
    """Remove symlinks that are no longer in the config file"""
    print()
    print("🧹" + "=" * 73 + "🧹")
    print("🎯 \033[32mCLEANING ORPHANED SYMLINKS\033[0m 🎯")
    print(f"📂 \033[32mRepository directory: {script_dir}\033[0m")
    print(f"⚙️  \033[32mConfig file: {config_path}\033[0m")
    print(f"🏠 \033[32mHome directory: {home_dir}\033[0m")
    print("🧹" + "=" * 73 + "🧹")
    print()

    # Load current configuration
    config: Config = load_config(config_path)

    # Get currently configured targets
    configured_targets: Set[Path] = set()
    for entry in config["dotfiles"]:
        target_path: Path = home_dir / entry["target"]
        configured_targets.add(target_path)

    # Discover all managed symlinks
    print("🔍 Discovering managed symlinks...")
    managed_links: Set[Path] = discover_managed_symlinks(script_dir, home_dir)

    if not managed_links:
        print("✨ No managed symlinks found.")
        return 0

    print(f"📊 Found {len(managed_links)} managed symlinks")
    print()

    # Find orphaned symlinks (managed but not in config)
    orphaned_links: Set[Path] = managed_links - configured_targets

    if not orphaned_links:
        print(
            "🎉 No orphaned symlinks found. All managed symlinks are in the configuration!"
        )
        return 0

    print(f"🗑️  Found {len(orphaned_links)} orphaned symlinks:")
    for link in sorted(orphaned_links):
        try:
            target = link.resolve()
            relative_target = target.relative_to(script_dir)
            print(f"  🔗 {link} -> {relative_target}")
        except (OSError, ValueError):
            print(f"  💀 {link} -> <broken link>")

    print()

    # Setup backup directory
    backup_dir: Path = script_dir / "backups" / "removed_symlinks"

    # Remove orphaned symlinks
    removed_count: int = 0
    for link_path in sorted(orphaned_links):
        print(f"🗑️  Removing orphaned symlink: {link_path}")

        # Create backup first
        if create_backup(link_path, backup_dir):
            try:
                link_path.unlink()
                print(f"  ✅ Removed: {link_path}")
                removed_count += 1
            except OSError as e:
                print(f"  ❌ Error removing {link_path}: {e}")
        else:
            print(f"  ⏭️  Skipped removal due to backup failure: {link_path}")

        print()

    print(
        f"📊 Summary: Removed {removed_count}/{len(orphaned_links)} orphaned symlinks"
    )

    if removed_count == len(orphaned_links):
        print("🎉 All orphaned symlinks removed successfully!")
        return 0
    else:
        print("⚠️  Some orphaned symlinks could not be removed.")
        return 1


def check_status(config_path: Path, script_dir: Path, home_dir: Path) -> int:
    """Check status of all dotfile links"""
    print()
    print("📊" + "=" * 73 + "📊")
    print("🎯 \033[32mDOTFILE STATUS CHECK\033[0m 🎯")
    print(f"📂 \033[32mRepository directory: {script_dir}\033[0m")
    print(f"⚙️  \033[32mConfig file: {config_path}\033[0m")
    print(f"🏠 \033[32mHome directory: {home_dir}\033[0m")
    print("📊" + "=" * 73 + "📊")
    print()

    # Load configuration
    config: Config = load_config(config_path)

    print(
        f"{'📄 Name':<25} {'🏷️  Type':<10} {'📦 Source':<8} {'🎯 Target':<8} {'🔗 Linked':<8} {'✅ Correct':<8}"
    )
    print("─" * 75)

    all_correct: bool = True

    for entry in config["dotfiles"]:
        source_path: Path = script_dir / entry["source"]
        target_path: Path = home_dir / entry["target"]

        # Check source exists
        source_exists: bool = source_path.exists()

        # Check target exists
        target_exists: bool = target_path.exists()

        # Check if target is a symlink
        is_symlink: bool = target_path.is_symlink()

        # Check if symlink points to correct location
        is_correct: bool = False
        if is_symlink:
            try:
                is_correct = target_path.resolve() == source_path.resolve()
            except OSError:
                is_correct = False

        # Determine overall status
        if not source_exists:
            all_correct = False
        elif not target_exists:
            all_correct = False
        elif not is_symlink:
            all_correct = False
        elif not is_correct:
            all_correct = False

        # Display status with colorful indicators
        print(
            f"{entry['source']:<25} {entry['type']:<10} "
            f"{'✅' if source_exists else '❌':<8} "
            f"{'✅' if target_exists else '❌':<8} "
            f"{'✅' if is_symlink else '❌':<8} "
            f"{'✅' if is_correct else '❌':<8}"
        )

    print()
    if all_correct:
        print("🎉 All dotfiles are correctly linked! You're all set! 🎉")
        return 0
    else:
        print("⚠️  Some dotfiles are not correctly linked. Run 'install' to fix them!")
        return 1


def install_dotfiles(
    config_path: Path,
    script_dir: Path,
    home_dir: Path,
    backup_dir: Path,
    dry_run: bool = False,
) -> int:
    """install dotfiles"""
    print()
    if dry_run:
        print("🔍" + "=" * 71 + "🔍")
        print("🎯 \033[32mDRY RUN - PREVIEW MODE\033[0m 🎯")
    else:
        print("🚀" + "=" * 73 + "🚀")
        print("⚡ \033[32mINSTALLING DOTFILES\033[0m ⚡")
    print(f"📂 \033[32mRepository directory: {script_dir}\033[0m")
    print(f"⚙️  \033[32mConfig file: {config_path}\033[0m")
    print(f"🏠 \033[32mHome directory: {home_dir}\033[0m")
    if not dry_run:
        print(f"💾 \033[32mBackup directory: {backup_dir}\033[0m")
    if dry_run:
        print("🔍" + "=" * 71 + "🔍")
    else:
        print("🚀" + "=" * 73 + "🚀")
    print()

    # Load configuration
    config: Config = load_config(config_path)

    # 🛡️ SAFETY VALIDATION - This is critical!
    if not validate_config_safety(config, script_dir, home_dir, dry_run):
        print("🚫 Installation cancelled due to safety concerns!")
        return 1

    print()

    # Process each dotfile entry
    success_count: int = 0
    skipped_count: int = 0
    total_count: int = len(config["dotfiles"])

    for entry in config["dotfiles"]:
        source_path: Path = script_dir / entry["source"]
        target_path: Path = home_dir / entry["target"]

        if dry_run:
            print(f"🔍 Would process: {entry['source']} ({entry['type']})")
        else:
            print(f"⚡ Processing: {entry['source']} ({entry['type']})")

        # Check if source exists
        if not source_path.exists():
            print(f"  ⚠️  Warning: Source does not exist: {source_path}")
            continue

        # Validate type matches reality
        if entry["type"] == "file" and not source_path.is_file():
            print(f"  ⚠️  Warning: Expected file but found directory: {source_path}")
            continue
        elif entry["type"] == "directory" and not source_path.is_dir():
            print(f"  ⚠️  Warning: Expected directory but found file: {source_path}")
            continue

        # Check if target already exists and is a valid symlink
        if target_path.exists() or target_path.is_symlink():
            if target_path.is_symlink():
                try:
                    # Check if symlink points to the correct location
                    if target_path.resolve() == source_path.resolve():
                        if dry_run:
                            print(
                                f"  ✨ Already correctly linked: {target_path} -> {source_path}"
                            )
                        else:
                            print(
                                f"  ✨ Already correctly linked: {target_path} -> {source_path}"
                            )
                        success_count += 1
                        skipped_count += 1
                        print()
                        continue
                    else:
                        if dry_run:
                            print(
                                f"  🔄 Would fix symlink pointing to wrong location: {target_path}"
                            )
                        else:
                            print(
                                f"  🔄 Found symlink pointing to wrong location: {target_path}"
                            )
                except OSError:
                    if dry_run:
                        print(f"  💀 Would fix broken symlink: {target_path}")
                    else:
                        print(f"  💀 Found broken symlink: {target_path}")
            else:
                if dry_run:
                    print(
                        f"  📁 Would backup and replace existing {'directory' if target_path.is_dir() else 'file'}: {target_path}"
                    )
                else:
                    print(
                        f"  📁 Found existing {'directory' if target_path.is_dir() else 'file'}: {target_path}"
                    )

        # Create symlink (this will handle backup if needed)
        if dry_run:
            print(f"  🔍 Would create symlink: {target_path} -> {source_path}")
            success_count += 1
        else:
            if create_symlink(source_path, target_path, backup_dir):
                success_count += 1

        print()

    # Summary
    created_count = success_count - skipped_count
    if dry_run:
        print(
            f"🔍 Dry Run Summary: {success_count}/{total_count} symlinks would be correctly linked"
        )
        if skipped_count > 0:
            print(
                f"✨ Would skip {skipped_count} already valid symlinks (no backup needed)"
            )
        if created_count > 0:
            print(f"🔗 Would create {created_count} new symlinks")
        print("\n💡 Run without --dry-run to actually perform these operations")
    else:
        print(
            f"📊 Summary: {success_count}/{total_count} symlinks are correctly linked"
        )
        if skipped_count > 0:
            print(
                f"✨ Skipped {skipped_count} already valid symlinks (no backup needed)"
            )
        if created_count > 0:
            print(f"🔗 Created {created_count} new symlinks")

    if success_count == total_count:
        if dry_run:
            print(
                "🎉 All dotfiles would be correctly linked! Run without --dry-run to proceed! 🎉"
            )
        else:
            print(
                "🎉 All dotfiles linked successfully! Your setup is ready to rock! 🎉"
            )
        return 0
    else:
        if dry_run:
            print("⚠️  Some dotfiles would have issues. Check the messages above.")
        else:
            print("⚠️  Some dotfiles failed to link. Check the errors above.")
        return 1


def main() -> int:
    """Main function with command line argument parsing"""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="🎯 Simple dotfiles linker - creates symlinks based on dot-config.json 🎯",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
✨ Examples:
  python linker.py install                            # 🚀 Create symlinks for all dotfiles
  python linker.py install --dry-run                  # 🔍 Preview what would happen
  python linker.py install -c alternate_config.json   # ⚙️  Use alternate config file
  python linker.py status                             # 📊 Check status of all dotfiles
  python linker.py clean                              # 🧹 Remove orphaned symlinks

🛡️ Safety Features:
  • Protected paths validation (prevents symlinking critical directories)
  • Risky operation confirmations (extra safety for important paths)
  • Dry-run mode for safe preview
  • Automatic backups before any changes

🎉 Happy dotfile management! 🎉
        """,
    )

    parser.add_argument(
        "command", choices=["install", "status", "clean"], help="Command to execute"
    )
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        help="Path to configuration file",
        default="dot-config.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview operations without making changes (install command only)",
    )

    args: argparse.Namespace = parser.parse_args()

    # Validate dry-run flag usage
    if args.dry_run and args.command != "install":
        print("❌ --dry-run flag can only be used with the 'install' command")
        return 1

    # Get paths
    script_dir: Path = Path(__file__).parent.resolve()
    backup_dir: Path = script_dir / "backups" / "removed_entity"
    config_path: Path = script_dir / args.config
    home_dir: Path = Path.home()

    # Execute command
    if args.command == "install":
        return install_dotfiles(
            config_path, script_dir, home_dir, backup_dir, args.dry_run
        )
    elif args.command == "status":
        return check_status(config_path, script_dir, home_dir)
    elif args.command == "clean":
        return clean_orphaned_symlinks(config_path, script_dir, home_dir)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
