#!/usr/bin/env zsh


## << please note that this is deprecated in favor of brew.py, please use brew.py for better package installations >>

echo "\n➡️ checking if brew installed, if not it will be installed"
if command -v brew &>/dev/null; then
echo "✅ brew exists, skipping installation..."
brew update
else
echo "❌ brew doesn't exist, continuing with the install"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo "✅ finished installing brew"
fi

# setup brew for this session, eventually this information will sit in .zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
export HOMEBREW_NO_ANALYTICS=1
export HOMEBREW_CASK_OPTS="--no-quarantine"

# check if Brewfile exists
echo "\n➡️ checking if Brewfile exists in current directory"
if [[ ! -f Brewfile ]]; then
  echo "❌ Brewfile not found in the current directory."
  echo "➡️ upgrading existing packages if any" 
  brew upgrade
  brew upgrade --cask
  echo "\n🧹 running cleanup..."
  brew cleanup --prune=all
  exit 1
fi

echo "\n➡️ do you want to install packages from Brewfile? (y/N): "
read answer
answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

if [[ "$answer" == "y" || "$answer" == "yes" ]]; then
  brew bundle --verbose
  echo "\n✅ installed packages from Brewfile"
else
  echo "\n➡️ skipping installation, upgrading existing packages if any"
  brew upgrade
  brew upgrade --cask
fi

# run cleanup
echo "\n🧹 running cleanup..."
brew cleanup --prune=all
