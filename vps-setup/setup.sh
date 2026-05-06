#!/bin/bash
# Run once on a fresh Hostinger 2 KVM VPS (Ubuntu 20.04/22.04).
# Installs Xvfb + Chromium + NoMachine, creates tvserver user, and
# installs the systemd service for auto-start on reboot.

set -e

echo "=== VPS TradingView Setup ==="

# ── 1. System update ──────────────────────────────────────────────────────────
echo "[1/5] Updating system packages..."
sudo apt-get update -qq && sudo apt-get upgrade -y -qq

# ── 2. Install dependencies ───────────────────────────────────────────────────
echo "[2/5] Installing Xvfb, Chromium, dbus..."
sudo apt-get install -y -qq xvfb x11-utils chromium-browser dbus

echo "Chromium: $(chromium-browser --version 2>/dev/null || chromium --version)"

# ── 3. Create dedicated user ──────────────────────────────────────────────────
echo "[3/5] Creating tvserver user (if not exists)..."
if ! id tvserver &>/dev/null; then
    sudo useradd -m -s /bin/bash tvserver
    echo "User 'tvserver' created."
else
    echo "User 'tvserver' already exists, skipping."
fi

# ── 4. Install scripts ────────────────────────────────────────────────────────
echo "[4/5] Installing start-display.sh..."
sudo cp "$(dirname "$0")/start-display.sh" /home/tvserver/start-display.sh
sudo chmod +x /home/tvserver/start-display.sh
sudo chown tvserver:tvserver /home/tvserver/start-display.sh

# ── 5. Install systemd service ────────────────────────────────────────────────
echo "[5/5] Installing systemd service..."
sudo cp "$(dirname "$0")/tradingview-display.service" /etc/systemd/system/tradingview-display.service
sudo systemctl daemon-reload
sudo systemctl enable tradingview-display.service

echo ""
echo "=== Setup complete ==="
echo "Start now:  sudo systemctl start tradingview-display"
echo "Check logs: sudo journalctl -u tradingview-display -f"
echo ""
echo "NoMachine: run install-nomachine.sh separately (requires manual download step)."
