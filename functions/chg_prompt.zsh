chg_prompt() {
  local preset_dir="$DOTDIR/starship/dot-config/presets"
  local starship_file="$DOTDIR/starship/dot-config/starship.toml"
  local backup_file="$starship_file.bak"

  # --restore mode
  if [[ -n "$1" ]]; then
    if [[ "$1" == "--restore" ]]; then
      if [[ -f "$backup_file" ]]; then
        cp "$backup_file" "$starship_file"
        trash "$backup_file"
        echo "♻️  Restored starship.toml from backup."
        echo "🗑️  Deleted backup file: $backup_file"
      else
        echo "❌ No backup found at: $backup_file"
      fi
      return
    else
      echo "❌ Invalid option: $1"
      echo "👉 Only supported option: --restore"
      return 1
    fi
  fi

  # Ensure preset directory exists
  if [[ ! -d "$preset_dir" ]]; then
    echo "❌ Preset directory not found: $preset_dir"
    return 1
  fi

  # Select a preset with preview
  local selected
  selected=$(fd . "$preset_dir" --type f | fzf \
    --prompt="Select Starship Preset: " \
    --preview="bat --style=plain --color=always {}")

  if [[ -n "$selected" ]]; then
    echo "✅ Selected: $selected"

    # Backup current config
    if [[ -f "$starship_file" ]]; then
      cp "$starship_file" "$backup_file"
      echo "📝 Backed up current starship.toml to: $backup_file"
    fi

    # Replace with selected preset
    if cp "$selected" "$starship_file"; then
      echo "✨ Starship preset changed!"
    else
      echo "❌ Failed to copy $selected to $starship_file"
      return 1
    fi
  else
    echo "⚠️ No preset selected."
  fi
}
