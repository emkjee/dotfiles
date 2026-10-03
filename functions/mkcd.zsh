## mkdir then cd into it
function mkcd () {
  mkdir -p "$@" && cd "$_";
}
