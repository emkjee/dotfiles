exst() {
  local cmd="$1"

  if [[ -z "$cmd" ]]; then
    echo "Please provide a command name." >&2
    return 2
  fi

  local found
  if found=$(type -a "$cmd" 2>/dev/null); then
    echo "Command '$cmd' is available."
    echo "$found"
    return 0
  else
    echo "Command '$cmd' is NOT available."
    return 1
  fi
}
