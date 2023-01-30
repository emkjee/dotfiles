#PROMPT
PROMPT="
%1~ %L %# "

RPROMPT="%*"


#Alias
alias ll="ls -lAFh"
alias ls="ls -lAFh"

#Functions

function mkcd () {
  mkdir -p "$@" && cd "$_";
}
