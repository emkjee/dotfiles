## setup aliases 
alias trail='<<<${(F)path}'  ## sanity resumed while displaying path
alias e="hx" ## e to kickoff helix
alias ls="lsd" ## default to lsd
alias dir="lsd -lart"
alias ll="lsd -lart"
alias clean_dss="fd '.DS_Store' . --hidden --type f --exact-depth 1 -E .git -x rm -v"
alias clean_dss_all="fd '.DS_Store' . --hidden --type f -E .git -x rm -v"


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