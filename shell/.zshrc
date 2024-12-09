## setup aliases 
alias trail='<<<${(F)path}'  ## sanity resumed while displaying path
alias e="hx" ## e to kickoff helix

## ll / dir
alias ls="lsd"
alias dir="lsd -lArt"
alias ll="lsd -lArt"


## setup plugins ###################################################################################
## starship = better prompt https://starship.rs
## zoxide = smarter cd https://github.com/ajeetdsouza/zoxide
## zsh-syntax-highlighting = syntax highlighting  https://github.com/zsh-users/zsh-syntax-highlighting
## zsh-auto-suggestions = auto suggestions https://github.com/zsh-users/zsh-autosuggestions
####################################################################################################
eval "$(starship init zsh)"
eval "$(zoxide init zsh)"
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
