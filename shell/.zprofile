# initialize homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# default editor => helix
export EDITOR="$(brew --prefix)/bin/hx"

# disable save/restore shell state
SHELL_SESSIONS_DISABLE=1