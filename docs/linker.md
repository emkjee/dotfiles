# 🎯 Simple Dotfile Linker

> ✨ A vibrant and intelligent dotfile management tool that organizes your configuration files with style and efficiency! ✨

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/yourusername/dotfile-linker)

## 🚀 Features

- 📦 **Smart Install** - Only creates symlinks when needed, skips already valid ones
- 📊 **Status Checking** - Beautiful table view of all your dotfile links  
- 🧹 **Cleanup** - Automatically removes orphaned symlinks
- 💾 **Safe Backups** - Timestamped backups before any changes
- 🎨 **Colorful Output** - Eye-catching emoji indicators and colored messages
- ⚡ **Lightning Fast** - Efficient operations with minimal overhead
- 🔧 **Flexible Config** - JSON-based configuration system
- 🛡️ **Type Safe** - Full Python type hints for reliability
- 🔍 **Dry Run Mode** - Preview all operations before execution
- 🛡️ **Advanced Safety** - Protected paths and risk validation

## 🛡️ Safety Features

### Core Safety Mechanisms

#### **Protected Paths Prevention**
The linker includes comprehensive protection against accidentally symlinking critical system directories:

```python
# Absolutely protected paths - these are NEVER touched
PROTECTED_PATHS = {
    ".",           # Home directory itself
    "~",           # Home directory reference  
    ".config",     # Entire config directory
    ".local",      # Entire local directory
    ".ssh",        # SSH directory (security risk)
    ".gnupg",      # GPG directory (security risk)
    "Documents",   # User documents folder
    "Desktop",     # Desktop folder
    "Downloads",   # Downloads folder
    # ... and more
}
```

#### **Risk Assessment System**
For potentially risky operations, the tool will:
- 🚨 **Detect risky paths** like `.local`, `.mozilla`, `Library`
- ⚠️ **Show detailed warning** with path analysis
- 🤔 **Require explicit confirmation** (type 'YES' in capitals)
- 🛑 **Allow safe cancellation** at any point

#### **Automatic Backup System**
- 💾 **Every replacement** is automatically backed up
- ⏰ **Timestamped backups** (`filename_YYYYMMDD_HHMMSS`)  
- 📁 **Organized storage** in `backups/removed_entity/`
- 🔄 **Handles all types**: files, directories, broken symlinks
- ✅ **Backup validation** before proceeding with operations

### Path Validation
```
✅ Safe:     .vimrc, .config/nvim, .bashrc
⚠️  Risky:   .local/anything, .mozilla/firefox  
❌ Blocked:  ., .ssh, Documents, Desktop
```

## 🔍 Dry Run Mode

### Why Use Dry Run?
The `--dry-run` flag is your safety net - it shows exactly what would happen without making any changes:

```bash
# Preview before doing anything
./linker.py install --dry-run
```

### What Dry Run Shows You:

#### **📋 Operation Preview**
```
🔍 Dry Run Summary: 5/5 symlinks would be correctly linked
✨ Would skip 2 already valid symlinks (no backup needed)  
🔗 Would create 3 new symlinks
📄 Would backup and replace 1 existing file

💡 Run without --dry-run to actually perform these operations
```

#### **🔍 Detailed Analysis**
```
🔍 Would process: configs/vimrc (file)
  📄 Would backup and replace existing file: /home/user/.vimrc
  🔗 Would create symlink: /home/user/.vimrc -> /home/user/dotfiles/configs/vimrc

🔍 Would process: configs/nvim (directory)  
  ✨ Already correctly linked: /home/user/.config/nvim -> /home/user/dotfiles/configs/nvim
```

#### **🛡️ Safety Validation Preview**
Dry run includes full safety validation:
- ✅ **Path safety checks** without requiring confirmations
- 📝 **Risk assessment** with detailed warnings
- 🚫 **Blocked operations** clearly identified
- ⚠️ **Risky operations** flagged for review

### Best Practices with Dry Run

1. **Always dry run first** on new configurations:
   ```bash
   ./linker.py install --dry-run -c new-config.json
   ```

2. **Review the output carefully**:
   - Check which files will be backed up
   - Verify symlink targets are correct
   - Look for any warning messages

3. **Test with minimal configs** when unsure:
   ```json
   {
     "dotfiles": [
       {
         "source": "test/safe-file",
         "target": "test-symlink", 
         "type": "file"
       }
     ]
   }
   ```

## 📸 Screenshots

### Dry Run Output
```
🔍═══════════════════════════════════════════════════════════════════════════🔍
🎯 DRY RUN - PREVIEW MODE 🎯
📂 Repository directory: /home/user/dotfiles
⚙️ Config file: /home/user/dotfiles/dot-config.json
🏠 Home directory: /home/user
🔍═══════════════════════════════════════════════════════════════════════════🔍

🛡️ Running safety validation on configuration...
✅ Safety validation completed - all entries look safe

🔍 Would process: configs/vimrc (file)
  📄 Would backup and replace existing file: /home/user/.vimrc
  🔗 Would create symlink: /home/user/.vimrc -> /home/user/dotfiles/configs/vimrc

🔍 Dry Run Summary: 1/1 symlinks would be correctly linked
🔗 Would create 1 new symlinks
🎉 All dotfiles would be correctly linked! Run without --dry-run to proceed! 🎉
```

### Safety Warning Example
```
🚨 RISKY OPERATION DETECTED 🚨
Target: .local/share/applications
Source: configs/applications  
Risky components: .local

⚠️  This operation could affect important system/application directories!
⚠️  Make sure this is exactly what you want to do.

💡 Consider using a more specific path instead.

🤔 Are you absolutely sure you want to proceed? (type 'YES' in capitals): 
```

### Install Command
```
🚀═══════════════════════════════════════════════════════════════════════════🚀
⚡ INSTALLING DOTFILES ⚡
📂 Repository directory: /home/user/dotfiles
⚙️ Config file: /home/user/dotfiles/dot-config.json
🏠 Home directory: /home/user
💾 Backup directory: /home/user/dotfiles/backups/removed_entity
🚀═══════════════════════════════════════════════════════════════════════════🚀

🛡️ Running safety validation on configuration...
✅ Safety validation completed - all entries look safe

⚡ Processing: configs/vimrc (file)
  ✨ Already correctly linked: /home/user/.vimrc -> /home/user/dotfiles/configs/vimrc

⚡ Processing: configs/nvim (directory)
  📁 Found existing directory: /home/user/.config/nvim
  💾 Created backup: /home/user/dotfiles/backups/removed_entity/nvim_20241201_150000
  ✅ Created symlink: /home/user/.config/nvim -> /home/user/dotfiles/configs/nvim

📊 Summary: 2/2 symlinks are correctly linked
✨ Skipped 1 already valid symlinks (no backup needed)
🔗 Created 1 new symlinks
🎉 All dotfiles linked successfully! Your setup is ready to rock! 🎉
```

### Status Command
```
📊 Name                    🏷️ Type      📦 Source 🎯 Target 🔗 Linked ✅ Correct
───────────────────────────────────────────────────────────────────────────
configs/vimrc              file        ✅       ✅       ✅        ✅      
configs/nvim               directory   ✅       ✅       ✅        ✅      
configs/bashrc             file        ✅       ✅       ✅        ✅      

🎉 All dotfiles are correctly linked! You're all set! 🎉
```

## 🔥 Quick Start

### 1. Clone and Setup
```bash
cd ~
git clone https://github.com/emkjee/dotfiles.git your_dotfiles
cd your_dotfiles
chmod +x linker.py
```

### 2. Create Configuration
Create a `dot-config.json` file:
```json
{
  "dotfiles": [
    {
      "source": "configs/bash/.zshrc",
      "target": ".zshrc",
      "type": "file"
    },
    {
      "source": "configs/helix",
      "target": ".config/helix",
      "type": "directory"
    },
    {
      "source": "configs/git/.gitconfig",
      "target": ".gitconfig",
      "type": "file"
    }
  ]
}
```

### 3. Preview Your Setup (Recommended!)
```bash
./linker.py install --dry-run
```

### 4. Install Your Dotfiles
```bash
./linker.py install
```

### 5. Check Status
```bash
./linker.py status
```

## 🎮 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `install` | 📦 Create symlinks for all configured dotfiles | `./linker.py install` |
| `install --dry-run` | 🔍 Preview what install would do (no changes) | `./linker.py install --dry-run` |
| `status` | 📊 Check current status of all dotfile links | `./linker.py status` |
| `clean` | 🧹 Remove orphaned symlinks not in config | `./linker.py clean` |

### Command Options

All commands support:
- `-c, --config`: Use alternate configuration file
- `--dry-run`: Preview mode (install command only)
  ```bash
  ./linker.py install --config work-dotfiles.json --dry-run
  ./linker.py status -c ~/.config/dotfiles/personal.json
  ```

## ⚙️ Configuration

### Schema
```json
{
  "dotfiles": [
    {
      "source": "path/relative/to/repo",
      "target": "path/relative/to/home", 
      "type": "file|directory"
    }
  ]
}
```

### Field Details

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | string | ✅ | Path to source file/directory (relative to repo root) |
| `target` | string | ✅ | Target path in home directory (relative to ~) |
| `type` | string | ✅ | Either `"file"` or `"directory"` |

### Safe Configuration Examples
```json
{
  "dotfiles": [
    {
      "source": "shell/bashrc",
      "target": ".bashrc",
      "type": "file"
    },
    {
      "source": "shell/zshrc", 
      "target": ".zshrc",
      "type": "file"
    },
    {
      "source": "editors/nvim",
      "target": ".config/nvim",
      "type": "directory"
    },
    {
      "source": "git/gitconfig",
      "target": ".gitconfig", 
      "type": "file"
    },
    {
      "source": "terminal/tmux.conf",
      "target": ".tmux.conf",
      "type": "file"
    },
    {
      "source": "scripts/bin",
      "target": ".local/bin/my-tools",
      "type": "directory"
    }
  ]
}
```

### ⚠️ Risky Configuration Examples
These require confirmation:
```json
{
  "dotfiles": [
    {
      "source": "firefox/profile",
      "target": ".mozilla/firefox/default",
      "type": "directory"
    },
    {
      "source": "app-configs", 
      "target": ".local/share/applications",
      "type": "directory"
    }
  ]
}
```

## 🎯 Smart Install Feature

The install command is intelligent and efficient:

### ✅ **Skips Valid Symlinks**
- Checks existing symlinks before making changes
- Only creates backups when necessary
- Avoids cluttering backup directory

### 📄 **Handles Different Scenarios**
- **Valid symlink** → Skip (no backup needed)
- **Wrong symlink** → Backup and replace
- **Broken symlink** → Backup and replace  
- **Regular file/directory** → Backup and replace
- **Missing target** → Create new symlink

### 📊 **Clear Reporting**
```
📊 Summary: 5/5 symlinks are correctly linked
✨ Skipped 3 already valid symlinks (no backup needed)
🔗 Created 2 new symlinks
```

## 💾 Backup System

### Automatic Backups
- **Location**: `<repo>/backups/removed_entity/`
- **Format**: `<filename>_YYYYMMDD_HHMMSS`
- **Types**: Files, directories, and broken symlinks
- **Safety**: Backup creation is verified before proceeding

### Backup Structure
```
backups/
├── removed_entity/           # Files replaced during install
│   ├── .vimrc_20241201_143022
│   ├── nvim_20241201_143045/
│   └── .bashrc_20241201_143101
└── removed_symlinks/         # Orphaned symlinks from clean
    └── old-config_20241201_144000
```

### Backup Recovery
```bash
# List available backups
ls -la backups/removed_entity/

# Restore a backup (example)
cp backups/removed_entity/.vimrc_20241201_143022 ~/.vimrc

# Or restore a directory
cp -r backups/removed_entity/nvim_20241201_143045/ ~/.config/nvim
```

## 🔧 Advanced Usage

### Safe Development Workflow
```bash
# 1. Start with dry run
./linker.py install --dry-run -c new-config.json

# 2. Review the output carefully
# 3. Check for any warnings or risky operations

# 4. Test with a subset first (create minimal config)
./linker.py install -c minimal-test.json

# 5. Verify everything works
./linker.py status -c minimal-test.json

# 6. Apply full configuration
./linker.py install -c new-config.json
```

### Multiple Configuration Files
```bash
# Work setup (safe paths only)
./linker.py install -c configs/work.json --dry-run
./linker.py install -c configs/work.json

# Personal setup (might include risky paths)
./linker.py install -c configs/personal.json --dry-run
# Review warnings carefully!
./linker.py install -c configs/personal.json

# Development setup
./linker.py install -c configs/dev.json --dry-run
./linker.py install -c configs/dev.json
```

### Repository Structure Example
```
dotfiles/
├── linker.py                 # The main script
├── dot-config.json          # Default configuration
├── configs/
│   ├── work.json           # Work-specific config (safe paths)
│   ├── personal.json       # Personal config (some risky paths)
│   └── minimal.json        # Testing config
├── shell/
│   ├── bashrc
│   ├── zshrc
│   └── aliases
├── editors/
│   ├── nvim/
│   └── vim/
├── git/
│   └── gitconfig
└── backups/                # Auto-generated backups
    ├── removed_entity/
    └── removed_symlinks/
```

### Integration with Git
```bash
# Track your dotfiles and configs
git add configs/ shell/ editors/ git/
git add dot-config.json linker.py

# Don't track backups or temporary files
echo "backups/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".DS_Store" >> .gitignore

# Always test new configs
git checkout -b test-new-config
# Edit configs, test with --dry-run
./linker.py install --dry-run
# If safe, apply and commit
./linker.py install
git add . && git commit -m "Add new dotfile configurations"
```

## 🛡️ Advanced Safety Features

### Configuration Validation
The tool validates your configuration before any operations:

```bash
# These would be rejected:
{
  "dotfiles": [
    {
      "source": "dangerous",
      "target": ".",           # ❌ Blocked: Home directory
      "type": "directory"
    },
    {
      "source": "ssh-config",
      "target": ".ssh",        # ❌ Blocked: Security risk
      "type": "directory" 
    },
    {
      "source": "../escape",   # ❌ Blocked: Parent directory
      "target": "safe-target",
      "type": "file"
    }
  ]
}
```

### Error Recovery
If something goes wrong:

1. **Check backup directory**: `ls -la backups/removed_entity/`
2. **Restore from backup**: Copy files back manually
3. **Clean up**: `./linker.py clean` to remove broken symlinks
4. **Verify status**: `./linker.py status` to check current state
5. **Start over**: Fix config and try `--dry-run` again

### Security Best Practices
- ✅ **Never run as root** - dotfiles should be user-specific
- ✅ **Always use --dry-run** for new configurations
- ✅ **Review risky operations** carefully before confirming
- ✅ **Keep backups** - don't delete the backups directory
- ✅ **Use version control** for your dotfiles repository
- ✅ **Test on non-production** machines first

## 📋 Requirements

- **Python**: 3.6 or higher
- **OS**: Unix-like system (Linux, macOS, WSL)
- **Permissions**: Write access to home directory
- **Storage**: Some space for backups

## 🚀 Installation

### Option 1: Direct Download
```bash
curl -O https://raw.githubusercontent.com/emkjee/dotfiles/main/linker.py
chmod +x linker.py
```

### Option 2: Clone Repository
```bash
git clone https://github.com/emkjee/dotfiles.git
cd dotfile-linker
chmod +x linker.py
```

### Option 3: As Git Submodule
```bash
# In your existing dotfiles repo
git submodule add https://github.com/yourusername/dotfile-linker.git tools/linker
```

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes and add tests
4. **Commit** your changes: `git commit -m 'Add amazing feature'`
5. **Push** to the branch: `git push origin feature/amazing-feature`  
6. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/dotfile-linker.git
cd dotfile-linker

# Create test config
cp examples/dot-config.json .

# Test the script safely
python3 linker.py status
python3 linker.py install --dry-run
```

### Code Guidelines
- Use type hints for all functions
- Add docstrings for public functions
- Follow Ruff formatting and linting rules
- Keep functions focused and testable
- Always include safety considerations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❓ FAQ

### **Q: What happens if I run install multiple times?**
A: The script is smart! It will skip already-valid symlinks and only make changes where needed. No unnecessary backups.

### **Q: How do I know if an operation is safe?**  
A: Always use `--dry-run` first! The tool will show you exactly what would happen and warn about risky operations.

### **Q: What if I get a "risky operation" warning?**
A: Read the warning carefully. If you're sure it's safe, type 'YES' in capitals. If unsure, cancel and use a more specific path.

### **Q: Can I use different config files?**  
A: Yes! Use the `-c` flag: `./linker.py install -c my-config.json`

### **Q: What if I accidentally delete a file?**
A: Check the `backups/` directory - all replaced files are automatically backed up with timestamps.

### **Q: How do I restore from a backup?**
A: Simply copy files from `backups/removed_entity/` back to their original locations.

### **Q: Can I test configurations safely?**
A: Absolutely! Use `--dry-run` to preview all operations without making any changes.

### **Q: What happens if the backup fails?**
A: The operation is cancelled. No changes are made unless the backup succeeds first.

### **Q: Can I manage dotfiles across multiple machines?**
A: Yes! Use different config files for different setups and sync them via Git.

## 🙏 Acknowledgments

- Inspired by the amazing dotfile management tools in the community
- Built with ❤️ for developers who love organized configurations  
- Thanks to all contributors who help improve this tool!

## 📞 Support

Having issues? I can try to help!

1. 📖 Check the documentation above
2. 🔍 Search [existing issues](https://github.com/yourusername/dotfile-linker/issues)
3. 🆕 [Create a new issue](https://github.com/yourusername/dotfile-linker/issues/new) with:
   - Your configuration file (remove sensitive info)
   - Complete error messages
   - Operating system details
   - Whether you used --dry-run first

---

<div align="center">

**Made with ❤️ and lots of ☕ by developers, for developers**

⭐ **If this tool helps you organize your dotfiles, please give it a star!** ⭐

[⬆️ Back to Top](#-simple-dotfile-linker)

</div>