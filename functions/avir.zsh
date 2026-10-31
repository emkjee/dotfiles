avir() {
  [[ -f .venv/bin/activate ]] || { echo "❌ No .venv in this directory." >&2; return 1 }
  source .venv/bin/activate
}
