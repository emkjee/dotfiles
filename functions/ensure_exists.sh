ensure_exists() {

  ## `command -v` is similar to `which`
  ## https://stackoverflow.com/a/677212/1341838

  ## more explicitly written as :
  ## command -v $1 1>/dev/null 2>/dev/null

  command -v "$1" >/dev/null 2>&1
}

exists() {
  local cmd="$1"

  if [[ -z "$cmd" ]]; then
    echo "⚠️ Please provide a command name."
    return 2
  fi

  if type -a "$cmd" >/dev/null 2>&1; then
    echo "✅ Command '$cmd' is available."

    type -a "$cmd"
    return 0
  else
    echo "❌ Command '$cmd' is NOT available."
    return 1
  fi
}