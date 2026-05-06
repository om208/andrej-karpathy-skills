#!/bin/bash
# Starts a headless X display on :99 and launches Chromium in kiosk mode.
# Designed to run as the 'tvserver' user via systemd.

export DISPLAY=:99

# Kill stale Xvfb lock if present (e.g. after unclean shutdown)
rm -f /tmp/.X99-lock

Xvfb :99 -screen 0 1920x1080x24 -ac &
XVFB_PID=$!

# Wait until display is ready
for i in $(seq 1 10); do
    xdpyinfo -display :99 &>/dev/null && break
    sleep 1
done

chromium-browser \
    --display=:99 \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-gpu \
    --window-size=1920,1080 \
    --start-maximized \
    "https://www.tradingview.com" &

wait $XVFB_PID
