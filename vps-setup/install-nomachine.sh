#!/bin/bash
# Downloads and installs NoMachine server on the VPS.
# NoMachine provides remote desktop access from Android/iOS.
#
# Usage: bash install-nomachine.sh [version]
# Default version: 8.14.1

set -e

NX_VERSION="${1:-8.14.1}"
NX_BUILD="1"
NX_PKG="nomachine_${NX_VERSION}_${NX_BUILD}_amd64.deb"
NX_URL="https://download.nomachine.com/download/${NX_VERSION%.*}/Linux/${NX_PKG}"

echo "=== Installing NoMachine ${NX_VERSION} ==="

echo "Downloading ${NX_PKG}..."
wget -q --show-progress -O "/tmp/${NX_PKG}" "${NX_URL}"

echo "Installing..."
sudo dpkg -i "/tmp/${NX_PKG}"
rm "/tmp/${NX_PKG}"

echo "Starting nxserver..."
sudo /usr/NX/bin/nxserver --start

echo ""
echo "=== NoMachine ready ==="
sudo /usr/NX/bin/nxserver --status
echo ""
echo "Connect from your phone:"
echo "  1. Install 'NoMachine' app (Android/iOS)"
echo "  2. Add server: <VPS_IP>  port 4000"
echo "  3. Log in with OS credentials (tvserver user or root)"
