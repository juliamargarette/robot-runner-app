#!/usr/bin/env bash

# 🐍 Install Python dependencies
pip install -r requirements.txt

# 🧹 Update packages and install needed tools
apt-get update && apt-get install -y wget unzip curl gnupg

# 🌐 Install Google Chrome
curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable

# 🚘 Install ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
