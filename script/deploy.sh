# #!/usr/bin/env bash
# set -euo pipefail

# # This script bootstraps an EC2 instance with the OmniAid-AI application.
# # It is intended to be run as the ``ubuntu`` user on a fresh Ubuntu image.

# REPO_URL="https://github.com/NinoLeenus/OmniAid-AI.git"
# BRANCH="wip"
# BASE_DIR="$HOME/OmniAid-AI"
# SERVICE_NAME="omni-aid"

# # basic safety check
# if [[ $(id -u) -eq 0 ]]; then
#   echo "It is recommended to run this script as a non-root user (ubuntu)."
# fi

# # update system packages and install prerequisites
# sudo apt update
# sudo apt install -y python3.12-venv git ufw

# # firewall configuration
# sudo ufw allow 22/tcp
# sudo ufw allow 8501/tcp
# sudo ufw --force enable

# # clone or update repository
# if [[ ! -d "$BASE_DIR" ]]; then
#   git clone "$REPO_URL" "$BASE_DIR"
# fi
# cd "$BASE_DIR"

# git fetch origin "$BRANCH"
# git checkout "$BRANCH"
# git pull origin "$BRANCH"

# # create virtual environment and install python dependencies
# python3 -m venv venv
# # shellcheck disable=SC1091
# source venv/bin/activate
# pip install --upgrade pip
# pip install torch --index-url https://download.pytorch.org/whl/cpu
# pip install -r requirements.txt

# copy systemd unit and enable the service
sudo cp "script/omni-aid.service" "/etc/systemd/system/$SERVICE_NAME.service"
#sudo cp "./omni-aid.service" "/etc/systemd/system/$SERVICE_NAME.service"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "Deployment complete. Visit http://$(curl -s ifconfig.me):8501 to see the app."
