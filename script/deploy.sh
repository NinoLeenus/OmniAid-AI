#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/NinoLeenus/OmniAid-AI.git"
BRANCH="wip"
BASE_DIR="$HOME/OmniAid-AI"
SERVICE_NAME="omni-aid"
VENV_DIR="$BASE_DIR/venv"

echo "===== OmniAid Deployment Started ====="

########################################
# Expand disk if volume increased
########################################

echo "Checking disk resize..."

sudo apt update -y
sudo apt install -y cloud-guest-utils

sudo growpart /dev/nvme0n1 1 || true
sudo resize2fs /dev/nvme0n1p1 || true

df -h

########################################
# Install system dependencies
########################################

echo "Installing system dependencies..."

sudo apt install -y \
    python3.12-venv \
    python3-pip \
    git \
    ufw

########################################
# Firewall setup
########################################

echo "Configuring firewall..."

sudo ufw allow 22/tcp
sudo ufw allow 8501/tcp
sudo ufw --force enable

########################################
# Clone or update repository
########################################

echo "Fetching application code..."

if [[ ! -d "$BASE_DIR" ]]; then
    git clone "$REPO_URL" "$BASE_DIR"
fi

cd "$BASE_DIR"

git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

########################################
# Create venv only if missing
########################################

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

########################################
# Install Python dependencies
########################################

echo "Installing Python dependencies..."

pip install --upgrade pip

pip install torch --index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt

########################################
# Clean pip cache (saves ~500MB)
########################################

echo "Cleaning pip cache..."
rm -rf ~/.cache/pip

########################################
# Setup systemd service
########################################

echo "Setting up system service..."

sudo cp script/omni-aid.service /etc/systemd/system/$SERVICE_NAME.service

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

########################################
# Final status
########################################

echo "===== Deployment Complete ====="

PUBLIC_IP=$(curl -s ifconfig.me)

echo ""
echo "Application running at:"
echo "http://$PUBLIC_IP:8501"
echo ""