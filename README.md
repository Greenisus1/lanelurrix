# Lanelurrix

Offline terminal moving-lane crossing game. Version 1.0.0. Original terminal artwork; no account, desktop or telemetry. No assets or names taken from other games.

## Install and run

    bash app-store.sh install
    bash app-store.sh run

Python3 with curses (normally included on Linux). No downloaded dependencies.

Arrows/WASD move, P pause, R restart, Q quit. Reach the top HOME row without touching traffic. Safe resting rows are 0,4,8,11. Traffic ticks every 0.35 seconds; original fixed-width lanes repeat every 7 columns. No endless scrolling, coins, score saving or levels.

Interactive curses terminal at least 46x19. Too-small windows show a resize notice and retain/pause the game. Terminal default, no GUI and no desktop requirement. R with --seed restarts the same seeded sequence, otherwise a fresh random board. For a non-interactive snapshot, use:

    python3 lanelurrix.py --seed 42 --demo

For tests:

    python3 -m unittest -v

7 core tests plus actual Linux PTY visual/input smoke. Linux tested; physical Raspberry Pi and non-Linux untested. Without curses the interactive game is unavailable. No paid features. games category marker line3; older stores still list/launch it. MIT license; see LICENSE.txt.
