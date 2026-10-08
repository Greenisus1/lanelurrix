#!/bin/bash
# pi-app-store: 1
# pi-app-store-category: games
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-}" in
  install) python3 -m py_compile lanelurrix.py terminal_ui.py ;;
  run) exec python3 lanelurrix.py ;;
  *) echo 'Use: bash app-store.sh install OR bash app-store.sh run'; exit 1 ;;
esac
