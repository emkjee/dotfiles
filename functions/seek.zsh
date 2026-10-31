seek() {
  local -a files
  files=("${(@f)$(fzf -m --query="$1" --select-1 --exit-0 --preview 'bat --color=always --style=numbers {} 2>/dev/null || cat {}')}")
  (( ${#files} )) && [[ -n $files[1] ]] && hx "${files[@]}"
}
