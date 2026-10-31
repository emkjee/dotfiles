dvir() {
  [[ -n $VIRTUAL_ENV ]] && deactivate || echo "No venv active." >&2
}
