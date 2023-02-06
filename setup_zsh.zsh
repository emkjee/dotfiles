#!/usr/bin/env zsh

echo "\n<<< Starting ZSH Setup >>>\n"

# Installation unnecessary; it is in the Brewfile.

echo "Enter superuser (sudo) password to edit /etc/shells" 
echo '/usr/local/bin/zsh' | sudo tee -a '/etc/shells'

echo "enter user password to change login shell"
chsh -s '/usr/local/bin/zsh'	
