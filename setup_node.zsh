#!/usr/bin/env zsh

echo "\n<<< Starting Node Setup >>>\n"

#node versions are managed with `n`, installation of `n` will be handled in Brewfile.

if exists node; then
echo "node $(node --version) & NPM (npm --version) already installed"
else
echo "installing node & npm through n..."
n latest
fi