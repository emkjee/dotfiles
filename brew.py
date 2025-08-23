#!/usr/bin/env python3
"""
🍺 Homebrew Package Manager - Your Mac's Best Friend! 🚀

✨ What does this script do?
   • Automatically detects and installs Homebrew if missing
   • Manages your entire package ecosystem through a simple JSON file
   • Provides real-time installation feedback with beautiful output
   • Handles both command-line tools (formulae) and GUI apps (casks)
   • Keeps your system clean with automatic cleanup routines

🎯 Perfect for:
   • Setting up a fresh Mac in minutes
   • Maintaining consistent environments across machines 
   • Automating your dotfiles setup process
   • Managing packages without memorizing brew commands

💡 Zero external dependencies - uses only macOS stock Python!

📄 Just create a brew.json file and watch the magic happen:
   {
     "formulae": ["git", "node", "python"],
     "casks": ["visual-studio-code", "chrome"]
   }

🚀 Usage: ./brew_manager.py
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def run_command(
    cmd: Union[str, List[str]],
    shell: bool = False,
    check: bool = True,
    show_output: bool = False,
) -> Optional[subprocess.CompletedProcess]:
    """
    🎯 Execute system commands with style and grace!

    ⚡ What it does:
       • Runs shell commands or executable lists
       • Optionally streams live output to terminal
       • Gracefully handles errors without crashing
       • Returns detailed process information

    🔧 Parameters:
       cmd: Command to run (string for shell, list for executable)
       shell: Whether to use shell interpretation
       check: Whether to raise on non-zero exit codes
       show_output: Stream live output (perfect for brew installs!)

    ✨ Returns: CompletedProcess object or None if failed
    """
    try:
        if show_output:
            # Show real-time output for package installations
            if shell:
                result = subprocess.run(cmd, shell=True, text=True, check=check)
            else:
                result = subprocess.run(cmd, text=True, check=check)
        else:
            # Capture output for silent operations
            if shell:
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, check=check
                )
            else:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, check=check
                )
        return result
    except subprocess.CalledProcessError as e:
        print(f"💥 Command execution failed: {e}")
        return None


def is_brew_installed() -> bool:
    """
    🔍 Detective work: Is Homebrew living on this Mac?

    🕵️ Searches the system PATH for the 'brew' command
    ✅ Returns True if found, False if we need to install it
    💡 Uses shutil.which() - the Pythonic way to find executables!
    """
    return shutil.which("brew") is not None


def install_brew() -> bool:
    """
    🚀 Homebrew Installation Mission Control!

    🎯 What happens here:
       • Downloads the official Homebrew installer script
       • Executes it with full system privileges
       • Handles the entire installation process gracefully
       • Reports success/failure with helpful messages

    ⚠️  Requires internet connection and may prompt for password!
    🎉 Returns True if installation succeeded, False otherwise
    """
    print("🚀 Homebrew not found - installing now...")
    install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    result = run_command(install_cmd, shell=True, check=False)

    if result and result.returncode == 0:
        print("🎉 Homebrew installation completed successfully!")
        return True
    else:
        print("💥 Homebrew installation failed - please check your internet connection")
        return False


def setup_brew_environment() -> None:
    """
    🔧 Environment Setup Wizard - Making Homebrew Feel at Home!

    ✨ Magical tasks performed:
       • Adds Homebrew binary paths to current session PATH
       • Disables analytics (keeps your privacy intact!)
       • Sets cask options to skip quarantine dialogs
       • Supports both Intel (/usr/local) and Apple Silicon (/opt/homebrew)

    🎯 Perfect for scripts that need immediate Homebrew access!
    """
    # Add Homebrew to PATH for this session
    homebrew_paths = ["/opt/homebrew/bin", "/usr/local/bin"]
    current_path = os.environ.get("PATH", "")

    for brew_path in homebrew_paths:
        if os.path.exists(brew_path) and brew_path not in current_path:
            os.environ["PATH"] = f"{brew_path}:{current_path}"
            break

    # Set Homebrew environment variables
    os.environ["HOMEBREW_NO_ANALYTICS"] = "1"
    os.environ["HOMEBREW_CASK_OPTS"] = "--no-quarantine"


def update_brew() -> bool:
    """
    🔄 Package Repository Refresh Service!

    📡 Syncs with Homebrew's central repositories to get:
       • Latest package versions and metadata
       • New formula and cask additions
       • Security updates and bug fixes
       • Fresh dependency information

    💡 Like 'apt update' but for macOS - essential before installing!
    ✨ Returns True if successful, False if network/server issues
    """
    print("🔄 Refreshing Homebrew package lists...")
    result = run_command(["brew", "update"], check=False)
    if result and result.returncode == 0:
        print("✨ Package lists updated successfully")
        return True
    else:
        print("⚠️  Package list update failed, but continuing...")
        return False


def upgrade_brew() -> bool:
    """
    ⬆️  Package Upgrade Command Center!

    🎯 Comprehensive upgrade strategy:
       • Upgrades ALL installed formulae to latest versions
       • Upgrades ALL installed casks to latest releases
       • Handles dependencies and conflicts automatically
       • Preserves your configuration and data

    ⚡ Two-phase operation for maximum compatibility
    🎉 Your packages get the VIP treatment they deserve!
    """
    print("⬆️  Upgrading all installed packages...")

    # Upgrade formulae
    print("   📦 Upgrading formulae...")
    result1 = run_command(["brew", "upgrade"], check=False)

    # Upgrade casks
    print("   📱 Upgrading casks...")
    result2 = run_command(["brew", "upgrade", "--cask"], check=False)

    success = (result1 and result1.returncode == 0) and (
        result2 and result2.returncode == 0
    )
    if success:
        print("✨ All packages upgraded successfully")
    else:
        print("⚠️  Some packages may have failed to upgrade")

    return bool(success)


def cleanup_brew() -> bool:
    """
    🧹 The Great Homebrew Cleanup Service!

    🎯 Spring cleaning for your package manager:
       • Removes old/outdated package versions
       • Clears download caches and temp files
       • Frees up precious disk space
       • Keeps only the latest versions you actually use

    💾 Can free hundreds of MB or even GB of space!
    ✨ Your Mac will thank you with faster performance
    """
    print("🧹 Cleaning up old package versions and cache...")
    result = run_command(["brew", "cleanup", "--prune=all"], check=False)
    if result and result.returncode == 0:
        print("✨ Cleanup completed successfully")
        return True
    else:
        print("⚠️  Cleanup completed with some warnings")
        return False


def read_brew_json(file_path: str = "brew.json") -> Optional[Dict[str, Any]]:
    """
    📄 JSON Configuration File Parser Extraordinaire!

    🎯 What this wizard does:
       • Reads your brew.json configuration file
       • Validates JSON syntax and structure
       • Handles missing files gracefully
       • Provides detailed error messages for debugging

    📋 Expected format: {"formulae": [...], "casks": [...]}
    🔍 Returns parsed data dict or None if something went wrong
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"💥 Invalid JSON format in {file_path}: {e}")
        return None
    except Exception as e:
        print(f"💥 Unexpected error reading {file_path}: {e}")
        return None


def install_formulae(formulae: List[str]) -> bool:
    """
    📦 Command-Line Tools Installation Specialist!

    ⚡ What makes this special:
       • Installs each formula with live progress tracking
       • Shows real-time Homebrew output and download progress
       • Handles dependencies automatically
       • Continues installing even if some packages fail
       • Provides detailed success/failure statistics

    🛠️  Perfect for: git, node, python, docker, curl, vim, etc.
    🎯 Returns True only if ALL installations succeeded
    """
    if not formulae:
        print("📦 No formulae to install")
        return True

    print(f"📦 Installing {len(formulae)} command-line tools...")
    print("-" * 50)
    success_count = 0

    for i, formula in enumerate(formulae, 1):
        print(f"\n⚡ [{i}/{len(formulae)}] Installing {formula}...")
        print("─" * 30)
        result = run_command(
            ["brew", "install", formula], check=False, show_output=True
        )
        if result and result.returncode == 0:
            print(f"✅ {formula} installed successfully\n")
            success_count += 1
        else:
            print(f"❌ {formula} installation failed\n")

    print("=" * 50)
    print(
        f"📦 Formula installation complete: {success_count}/{len(formulae)} successful"
    )
    return success_count == len(formulae)


def install_casks(casks: List[str]) -> bool:
    """
    📱 GUI Applications Installation Maestro!

    🎨 The premium app installer experience:
       • Downloads and installs macOS applications seamlessly
       • Shows real-time progress for large app downloads
       • Handles app signatures and permissions automatically
       • Skips quarantine dialogs for trusted sources
       • Tracks installation success rates like a pro

    🚀 Perfect for: VS Code, Chrome, Slack, Docker Desktop, etc.
    ✨ Returns True only if ALL applications installed successfully
    """
    if not casks:
        print("📱 No applications to install")
        return True

    print(f"📱 Installing {len(casks)} applications...")
    print("-" * 50)
    success_count = 0

    for i, cask in enumerate(casks, 1):
        print(f"\n⚡ [{i}/{len(casks)}] Installing {cask}...")
        print("─" * 30)
        result = run_command(
            ["brew", "install", "--cask", cask], check=False, show_output=True
        )
        if result and result.returncode == 0:
            print(f"✅ {cask} installed successfully\n")
            success_count += 1
        else:
            print(f"❌ {cask} installation failed\n")

    print("=" * 50)
    print(
        f"📱 Application installation complete: {success_count}/{len(casks)} successful"
    )
    return success_count == len(casks)


def get_user_confirmation() -> bool:
    """
    🤔 Interactive Decision Point - Your Choice Matters!

    🎯 User-friendly confirmation system:
       • Presents a clear question about package installation
       • Accepts various positive responses (y, yes, Y, YES)
       • Handles Ctrl+C gracefully without crashes
       • Gives users full control over the installation process

    💡 Prevents accidental installations on shared machines
    ✨ Returns True for 'yes', False for anything else
    """
    try:
        print("\n🤔 Ready to install packages from brew.json")
        answer = input("   Continue with installation? (y/N): ").strip().lower()
        return answer in ["y", "yes"]
    except KeyboardInterrupt:
        print("\n\n🛑 Installation cancelled by user")
        return False


def display_package_summary(formulae: List[str], casks: List[str]) -> None:
    """
    📋 Package Preview Dashboard - Know Before You Install!

    🎨 Beautiful summary display featuring:
       • Total package count across categories
       • Smart truncation for long package lists
       • Clear separation between tools and applications
       • Prevents information overload with "... and X more"

    💡 Helps users make informed decisions before installation
    🎯 Perfect for reviewing large package collections at a glance
    """
    total_packages = len(formulae) + len(casks)
    print(f"\n📋 Package Summary ({total_packages} total)")

    if formulae:
        print(f"   📦 Command-line tools ({len(formulae)}): {', '.join(formulae[:5])}")
        if len(formulae) > 5:
            print(f"      ... and {len(formulae) - 5} more")

    if casks:
        print(f"   📱 Applications ({len(casks)}): {', '.join(casks[:5])}")
        if len(casks) > 5:
            print(f"      ... and {len(casks) - 5} more")


def main() -> None:
    """
    🎭 The Grand Orchestra Conductor - Where All Magic Happens!

    🎯 This is the main event that orchestrates:
       • Homebrew detection and installation workflow
       • Configuration file discovery and validation
       • User interaction and confirmation dialogs
       • Package installation with live progress tracking
       • System cleanup and final status reporting

    ✨ Features beautiful console output with:
       • Progress indicators and status updates
       • Error handling that keeps going when possible
       • Helpful tips when things don't go as planned
       • Celebration messages when everything works!

    🚀 The complete Mac setup experience in one function!
    """
    print("🍺 Homebrew Package Manager")
    print("=" * 40)

    # Check if Homebrew is installed
    print("\n🔍 Checking Homebrew installation...")
    if is_brew_installed():
        print("✅ Homebrew is already installed")
        update_brew()
    else:
        # Install Homebrew
        if not install_brew():
            print("💥 Cannot continue without Homebrew - exiting")
            sys.exit(1)

    # Setup environment
    setup_brew_environment()

    # Check if brew.json exists
    print("\n📄 Looking for brew.json configuration...")
    json_path = Path("brew.json")

    if not json_path.exists():
        print("❌ brew.json not found in current directory")
        print("🔄 Falling back to package upgrades...")
        upgrade_brew()
        cleanup_brew()
        print("\n💡 Tip: Create a brew.json file to manage your packages!")
        sys.exit(1)

    # Read brew.json
    print("✅ Found brew.json - reading configuration...")
    brew_config = read_brew_json()
    if not brew_config:
        print("💥 Could not read brew.json - please check the file format")
        sys.exit(1)

    # Extract packages from JSON
    formulae = brew_config.get("formulae", [])
    casks = brew_config.get("casks", [])

    # Validate package lists
    if not isinstance(formulae, list):
        print("⚠️  'formulae' should be a list - treating as empty")
        formulae = []
    if not isinstance(casks, list):
        print("⚠️  'casks' should be a list - treating as empty")
        casks = []

    if not formulae and not casks:
        print("❌ No packages found in brew.json")
        upgrade_brew()
        cleanup_brew()
        sys.exit(1)

    # Display package summary
    display_package_summary(formulae, casks)

    # Get user confirmation
    if get_user_confirmation():
        print("\n🚀 Starting package installation...")

        # Install packages
        formulae_success = install_formulae(formulae)
        casks_success = install_casks(casks)

        if formulae_success and casks_success:
            print("\n🎉 All packages installed successfully!")
        else:
            print("\n⚠️  Some packages failed to install - check the output above")
    else:
        print("\n⏭️  Skipping package installation")
        print("🔄 Upgrading existing packages instead...")
        upgrade_brew()

    # Cleanup
    print("\n🧹 Final cleanup...")
    cleanup_brew()
    print("\n✨ All done! Your system is ready to go!")


if __name__ == "__main__":
    main()
