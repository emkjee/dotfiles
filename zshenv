echo "hello from .zshenv"

#functions!
function exists() {
  # `command -v` is similar to `which`
  # https://stackoverflow.com/a/677212/1341838
  
  command -v $1 >/dev/null 2>&1

  #more explicitly written as :
  # command -v $1 1>/dev/null 2>/dev/null
}