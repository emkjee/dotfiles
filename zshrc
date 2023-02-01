echo "hello from .zshrc"

#Set Variables
#Syntax Highlighting man pages using bat
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export HOMEBREW_CASK_OPTS="--no-quarantine"


#PROMPT
PROMPT="
%1~ %L %# "

RPROMPT="%*"


#Alias
alias ls="exa -laFh --git"
alias ll="exa -laFh --git"
alias exa="exa -laFh --git"
alias refresh="source ~/.zshrc"
alias bbd="brew bundle dump --force --describe"


# Add locations to $PATH Variable
# Add Visual Studio Code (code)
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"


#Functions

function mkcd () {
  mkdir -p "$@" && cd "$_";
}


#homebrew no analytics
export HOMEBREW_NO_ANALYTICS=1
