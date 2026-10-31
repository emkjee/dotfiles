pset() {
  local preset_dir="$DOTDIR/starship"
  local starship_file="${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml"

  if [[ ! -d $preset_dir ]]; then
    echo "Error: starship directory not found: $preset_dir" >&2
    return 1
  fi

  if [[ -e $starship_file && ! -L $starship_file ]]; then
    echo "Error: $starship_file exists but is not a symlink." >&2
    return 1
  fi

  local selected
  selected=$(fd -e toml -d 1 --type f . "$preset_dir" | fzf \
    --prompt="Select Starship Preset: " \
    --preview="bat --style=plain --color=always {}")

  if [[ -n $selected ]]; then
    ln -sfn "${selected:A}" "$starship_file"
    echo "starship.toml now linked to $(basename "$selected")"
  else
    echo "No preset selected."
  fi
}
