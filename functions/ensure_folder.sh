ensure_folder() {
  local folder="$1"

  if [[ ! -d "$folder" ]]; then
    mkdir -p "$folder"
  fi
}