# Lanelurrix1.1.0

Original offline fullscreen terminal lane-crossing game. No branded assets, accounts, desktop, network or telemetry. Same listing, upgraded from1.0.1.

Choose Levels or Infinity at launch. Levels has10 crossings, gradually faster/denser traffic, safe resting rows and a HOME finish. Enter advances after each win; R retries the current level. Infinity generates deterministic new lanes as you move forward, scrolls the view, keeps a session row record and gradually speeds traffic up. No end in Infinity, no saved scores.

The original20-cell lane logic now expands cells/row height across your terminal. Colored road/grass/traffic, wheel details and a small original player sprite at roomy sizes; compact @ at small sizes. Arrows/WASD move, P/Space pause, R retry, M mode menu, Esc/Q exit. Minimum46x19. Shrinking pauses and preserves state; enlarging resumes with resized drawing. Status and controls stay on screen. Physics is the same20-column grid regardless of screen size, not more columns on wider screens.

    bash app-store.sh install
    bash app-store.sh run
    python3 lanelurrix.py --seed 42 --demo
    python3 lanelurrix.py --version
    python3 -m unittest -v

Python3+curses, no downloaded dependencies. Install only compiles source, no sudo. Noninteractive terminals get a clear error; --demo keeps the old fixed snapshot feature. Seeded retries preserve the current level seed. Infinity caches only nearby lanes, not an ever-growing map. Session progress disappears on exit.

15 core/regression tests, actual Linux PTY level/infinity input, resize and terminal-restoration checked. Fullscreen visual previews inspected. Physical Raspberry Pi and non-Linux untested. Original terminal artwork, not Crossy Road or a commercial-game port. Games marker line3; older stores still list and launch it. MIT license; existing LICENSE.txt unchanged.
