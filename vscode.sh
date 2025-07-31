#!/usr/bin/env zsh

if [[ -f ~/Library/Application\ Support/Code/User/settings.json ]]; then
  
    if [[ ! -d "$HOME/backup/Code/User" ]]; then
       mkdir -p "$HOME/backup/Code/User"
    fi

    echo "\n➡️ taking backup of settings.json"
    cp -L ~/Library/Application\ Support/Code/User/settings.json ~/backup/Code/User/settings.json.bkup-$(date +%F)
    echo "📦 settings.json backed up in ~/backup/Code/User/settings.json.bkup-$(date +%F)"
fi

if [[ -f ~/Library/Application\ Support/Code/User/keybindings.json ]]; then

    if [[ ! -d "$HOME/backup/Code/User" ]]; then
       mkdir -p "$HOME/backup/Code/User"
    fi

    echo "\n➡️ taking backup of keybindings.json"
    cp -L ~/Library/Application\ Support/Code/User/keybindings.json ~/backup/Code/User/keybindings.json.bkup-$(date +%F)
    echo "📦 keybindings.json backed up in ~/backup/Code/User/keybindings.json.bkup-$(date +%F)"
fi

echo "\n➡️ creating vscode setting & keybindings symlinks"
ln -sf ~/repos/dotfiles/vscode/settings.json ~/Library/Application\ Support/Code/User/settings.json
ln -sf ~/repos/dotfiles/vscode/keybindings.json ~/Library/Application\ Support/Code/User/keybindings.json

if [[ -L "$HOME/Library/Application Support/Code/User/settings.json" ]] && \
   [[ -L "$HOME/Library/Application Support/Code/User/keybindings.json" ]]; then
    echo "✅ vscode settings and keybindings symlinks are created"
fi

echo "\n➡️ start installing vscode extentions!"

code --install-extension albert.tabout --force
code --install-extension charliermarsh.ruff --force
code --install-extension docker.docker --force
code --install-extension eamodio.gitlens --force
code --install-extension esbenp.prettier-vscode --force
code --install-extension johnpapa.winteriscoming --force
code --install-extension ms-azuretools.vscode-containers --force
code --install-extension ms-azuretools.vscode-docker --force
code --install-extension ms-python.debugpy --force
code --install-extension ms-python.python --force
code --install-extension ms-python.vscode-pylance --force
code --install-extension ms-python.vscode-python-envs --force
code --install-extension ms-toolsai.jupyter --force
code --install-extension ms-toolsai.jupyter-keymap --force
code --install-extension ms-toolsai.jupyter-renderers --force
code --install-extension ms-toolsai.vscode-jupyter-cell-tags --force
code --install-extension ms-toolsai.vscode-jupyter-slideshow --force
code --install-extension pkief.material-icon-theme --force
code --install-extension rust-lang.rust-analyzer --force
code --install-extension sainnhe.everforest --force
code --install-extension sainnhe.gruvbox-material --force
code --install-extension tamasfe.even-better-toml --force

echo "\n✅ finished installing vscode extentions!"
