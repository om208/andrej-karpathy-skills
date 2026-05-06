# VPS TradingView Backtesting Setup

Offloads TradingView Strategy Tester to Hostinger 2 KVM VPS, accessible via NoMachine from Android.

## Prerequisites

- Hostinger 2 KVM VPS (Ubuntu 20.04/22.04, 2 vCPU, 2 GB RAM)
- SSH access to VPS
- NoMachine app installed on Android phone

---

## First-Time Setup (run once)

```bash
# 1. SSH into VPS
ssh root@<VPS_IP>

# 2. Clone or copy vps-setup/ to VPS
scp -r vps-setup/ root@<VPS_IP>:~/

# 3. Run main setup (installs packages, creates tvserver user, registers systemd service)
bash ~/vps-setup/setup.sh

# 4. Install NoMachine remote desktop server
bash ~/vps-setup/install-nomachine.sh

# 5. Start the display service
sudo systemctl start tradingview-display
```

---

## Daily Use (each session)

```bash
# Check service is running
sudo systemctl status tradingview-display

# If stopped, start it
sudo systemctl start tradingview-display

# Connect from phone
# NoMachine app → <VPS_IP>:4000 → log in → Chromium opens to TradingView
```

---

## Verify Everything Works

```bash
# Xvfb running?
ps aux | grep Xvfb

# Chromium running?
ps aux | grep chromium

# NoMachine running?
sudo /usr/NX/bin/nxserver --status

# Service logs
sudo journalctl -u tradingview-display -f
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `X99-lock` error on start | `rm -f /tmp/.X99-lock` then restart service |
| Chromium crashes (OOM) | Add `--memory-pressure-off` flag to `start-display.sh` |
| NoMachine shows black screen | Stop service, start Xvfb manually, reconnect |
| Cannot reach VPS port 4000 | Check Hostinger firewall — open TCP 4000 |
| TradingView loads slowly | Normal first load; subsequent loads are faster |

---

## Auto-start on Reboot

The systemd service is enabled automatically by `setup.sh`:

```bash
# Confirm it's enabled
sudo systemctl is-enabled tradingview-display   # should print "enabled"
```

After a VPS reboot, the display starts automatically — just reconnect via NoMachine.

---

## Architecture

```
Android phone (NoMachine client)
        │  port 4000
        ▼
Hostinger VPS
├── NoMachine server (remote desktop)
├── Xvfb :99  (headless X11 display)
└── Chromium  (TradingView Strategy Tester)
```

---

## Next Steps

- **Automated backtesting**: Use Playwright/Puppeteer to drive Chromium headlessly, scrape Strategy Tester results into CSV
- **Delta Exchange integration**: Feed backtest results into live order pipeline
- **Scheduled runs**: `cron` to trigger weekly backtests and email reports
