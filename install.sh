#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  █░█ █░█ ▀▀▀█░█▀▄ ▄▀▄ ▄▀▀                              ║"
echo "║  ▀▄▀ ▄▀▄ ░▄▀░░█░█ █░█ ░▀▄                              ║"
echo "║  ░▀░ ▀░▀ ▀▀▀▀░▀▀░ ░▀░ ▀▀░                              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "${YELLOW}          Izumi DDoS Tool - Ultimate Installer${NC}"
echo -e "${BLUE}========================================================${NC}\n"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[!] Please run as root: sudo bash install.sh${NC}"
    exit 1
fi

# Update and install dependencies
echo -e "${GREEN}[+] Updating system...${NC}"
apt update -y > /dev/null 2>&1

echo -e "${GREEN}[+] Installing Python3 and pip...${NC}"
apt install python3 python3-pip -y > /dev/null 2>&1

echo -e "${GREEN}[+] Installing required Python packages...${NC}"
pip3 install requests urllib3 colorama --break-system-packages > /dev/null 2>&1 || pip3 install requests urllib3 colorama

echo -e "${GREEN}[+] Setting permissions...${NC}"
chmod +x Izumi.py

echo -e "${GREEN}[+] Creating shortcut...${NC}"
ln -sf $(pwd)/Izumi.py /usr/local/bin/izumi 2>/dev/null

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ${GREEN}INSTALLATION COMPLETE, KONTOL!${BLUE}                           ║"
echo "║                                                          ║"
echo "║  ${YELLOW}Run: python3 Izumi.py${BLUE}                                    ║"
echo "║  ${YELLOW}Or:   izumi${BLUE} (if shortcut created)                       ║"
echo "║                                                          ║"
echo "║  ${RED}Developed by: Izumi Kece | XYNOOZ MECY 07${BLUE}                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"