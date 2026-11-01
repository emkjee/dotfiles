## shell-functions -------------------------------
source $DOTDIR/functions/crun.zsh
source $DOTDIR/functions/seek.zsh
source $DOTDIR/functions/mkcd.zsh
source $DOTDIR/functions/help.zsh
source $DOTDIR/functions/exst.zsh
source $DOTDIR/functions/avir.zsh
source $DOTDIR/functions/dvir.zsh
source $DOTDIR/functions/femp.zsh
source $DOTDIR/functions/demp.zsh
source $DOTDIR/functions/pset.zsh
# ------------------------------------------------


## setup_aliases ---------------------------------
alias rm='rm -I'
alias rz='exec zsh'
alias trail='<<<${(F)path}'

setopt auto_cd
alias -g ...='../..'
alias -g ....='../../..'
alias -g .....='../../../..'

alias e='hx'
alias ek='e ~/.config/kitty'
alias eh='e ~/.config/helix'
alias ez='e ~/.zshrc'
alias es='e ~/.config/starship.toml'

alias ls='lsd --git --group-directories-first'
alias ll='lsd -lArt --git --group-directories-first'
alias lt='lsd --tree --git'

alias cds='fd -g .DS_Store -H -I -t f -E .git -X trash -v'
alias fbl='fd -t l -L'
alias fem='fd . -t d -t e'
alias dem='fd . -t d -t e -X trash -v'

alias brc='brew cleanup --prune=all'
alias brl='brew list'
alias bro='brew outdated'
alias bru='brew update && brew upgrade'
# ------------------------------------------------


## setup plugins ---------------------------------
## starship = better prompt https://starship.rs
## zoxide = smarter cd https://github.com/ajeetdsouza/zoxide
## zsh-syntax-highlighting = syntax highlighting  https://github.com/zsh-users/zsh-syntax-highlighting
## zsh-auto-suggestions = auto suggestions https://github.com/zsh-users/zsh-autosuggestions
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"
source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
# ------------------------------------------------


## refs ------------------------------------------
## for DS_Store - https://gist.github.com/lohenyumnam/2b127b9c3d1435dc12a33613c44e6308
## for aliases - https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/common-aliases/common-aliases.plugin.zsh
## for exists - https://stackoverflow.com/questions/592620/how-can-i-check-if-a-program-exists-from-a-bash-script/677212#677212
# ------------------------------------------------
