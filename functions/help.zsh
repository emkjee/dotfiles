help() {
  if (( $# == 0 )); then
    print -u2 "usage: help [section] <page>"
    return 1
  fi

  local cache="${XDG_CACHE_HOME:-$HOME/.cache}/man-helix"
  mkdir -p "$cache" || return 1

  local tmpdir
  tmpdir=$(mktemp -d "$cache/XXXXXX") || return 1

  local name="${(j:_:)@}"
  name="${name//[\/ ]/_}"

  local raw="$tmpdir/raw"
  local page="$tmpdir/$name.txt"
  local rc=0

  {
    man "$@" > "$raw" || rc=$?

    if (( rc == 0 )); then
      if [[ -s $raw ]]; then
        col -bx < "$raw" > "$page" && hx "$page"
        rc=$?
      else
        print -u2 "help: empty manual for: $*"
        rc=1
      fi
    fi
  } always {
    rm -rf "$tmpdir"
  }

  return $rc
}