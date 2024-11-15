# mkdir then cd into it
function mkcd () {
  mkdir -p "$@" && cd "$_";
}

# check if a command exists
function exists() {

  # `command -v` is similar to `which`
  # https://stackoverflow.com/a/677212/1341838

  #more explicitly written as :
  # command -v $1 1>/dev/null 2>/dev/null

  command -v $1 >/dev/null 2>&1
}