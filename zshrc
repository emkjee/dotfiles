#PROMPT
PROMPT="
%1~ %L %# "

RPROMPT="%*"


#Alias
alias ll="ls -lAFh"
alias ls="ls -lAFh"


# Add locations to $PATH Variable
# Add Visual Studio Code (code)
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"


#Functions

function mkcd () {
  mkdir -p "$@" && cd "$_";
}
