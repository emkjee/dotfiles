## setup-functions -------------------------------
## ensure_folder = check if a folder exists, if not create it
# ------------------------------------------------
source $HOME/repos/dotfiles/functions/ensure_folder.sh


## setup_aliases ---------------------------------
## trail = sanity resumed while displaying path
## e = to kickoff helix
## ls / ll / dir = default to lsd
## rm -i = rm interactive
## cds = to clean all .DS_Store files in current directory / sub directories
# ------------------------------------------------
alias trail='<<<${(F)path}'
alias e="hx"
alias ls="lsd"
alias dir="lsd -lart"
alias ll="lsd -lart"
alias rm="rm -i"
alias cds="fd '.DS_Store' . --hidden --type f -E .git -x trash -v"


## setup plugins ---------------------------------
## starship = better prompt https://starship.rs
## zoxide = smarter cd https://github.com/ajeetdsouza/zoxide
## zsh-syntax-highlighting = syntax highlighting  https://github.com/zsh-users/zsh-syntax-highlighting
## zsh-auto-suggestions = auto suggestions https://github.com/zsh-users/zsh-autosuggestions
# ------------------------------------------------
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"
source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh


## refs
## for DS_Store - https://gist.github.com/lohenyumnam/2b127b9c3d1435dc12a33613c44e6308
## for aliases - https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/common-aliases/common-aliases.plugin.zsh
