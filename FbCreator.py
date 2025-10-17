import os
os.system('pkg install espeak -y > /dev/null 2>&1')
import threading
from queue import Queue
import requests
import random
import string
import json
import hashlib
import time
import urllib3
from faker import Faker
import warnings

# SSL warnings disable karein
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

os.system('clear')
os.system('espeak -s 300 "AUTOCREATE TOOL BY JAN" > /dev/null 2>&1')

print("""\033[1;94m
WELLCOME TO AUTO CREATE TOOL BY JAN x JAN
╔═╗╔═╗────────────
║║╚╝║║────────────
║╔╗╔╗╠══╦═╦╦══╦══╗
║║║║║║╔╗║╔╬╣╔╗║╔╗║
║║║║║║╔╗║║║║║║║╔╗║
╚╝╚╝╚╩╝╚╩╝╚╩╝╚╩╝╚╝
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓           
> › Github :- MARINA KHAN
> › By      :- MARINA KHAN
> › AUTO ACCCOUNTS CREATER TOOOL BY JAN x JAN
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛                """)
print('\x1b[38;5;94m⇼'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;22m•'*60)
print('\x1b[38;5;94m⇼'*60)

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def get_mail_domains(proxy=None):
    url = "https://api.mail.tm/domains"
    try:
        if proxy and proxy != "no_proxy":
            response = requests.get(url, proxies=proxy, timeout=10, verify=False)
        else:
            response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            return response.json().get('hydra:member', [])
        else:
            print(f'[×] E-mail Error : {response.status_code}')
            return None
    except Exception as e:
        print(f'[×] API Error : {str(e)[:100]}')
        return None

def create_mail_tm_account(proxy=None):
    fake = Faker()
    mail_domains = get_mail_domains(proxy)
    if mail_domains:
        domain = random.choice(mail_domains).get('domain', '')
        if not domain:
            return None, None, None, None, None
            
        username = generate_random_string(10)
        password = fake.password()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=45)
        first_name = fake.first_name()
        last_name = fake.last_name()
        url = "https://api.mail.tm/accounts"
        headers = {"Content-Type": "application/json"}
        data = {"address": f"{username}@{domain}", "password": password}       
        try:
            if proxy and proxy != "no_proxy":
                response = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=10, verify=False)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=10, verify=False)
                
            if response.status_code == 201:
                print(f'[✓] Email Created: {username}@{domain}')
                return f"{username}@{domain}", password, first_name, last_name, birthday
            else:
                print(f'[×] Email Creation Failed : {response.status_code}')
                return None, None, None, None, None
        except Exception as e:
            print(f'[×] Email Creation Error : {str(e)[:100]}')
            return None, None, None, None, None
    else:
        print('[×] No mail domains available')
    return None, None, None, None, None

def register_facebook_account(email, password, first_name, last_name, birthday, proxy=None):
    try:
        api_key = '882a8490361da98702bf97a021ddc14d'
        secret = '62f8ce9f74b12f84c123cc23437a4a32'
        gender = random.choice(['M', 'F'])
        req = {
            'api_key': api_key,
            'attempt_login': True,
            'birthday': birthday.strftime('%Y-%m-%d'),
            'client_country_code': 'EN',
            'fb_api_caller_class': 'com.facebook.registration.protocol.RegisterAccountMethod',
            'fb_api_req_friendly_name': 'registerAccount',
            'firstname': first_name,
            'format': 'json',
            'gender': gender,
            'lastname': last_name,
            'email': email,
            'locale': 'en_US',
            'method': 'user.register',
            'password': password,
            'reg_instance': generate_random_string(32),
            'return_multiple_errors': True
        }
        
        sorted_req = sorted(req.items(), key=lambda x: x[0])
        sig = ''.join(f'{k}={v}' for k, v in sorted_req)
        ensig = hashlib.md5((sig + secret).encode()).hexdigest()
        req['sig'] = ensig
        
        api_url = 'https://b-api.facebook.com/method/user.register'
        reg = _call(api_url, req, proxy)
        
        if 'new_user_id' in reg and 'session_info' in reg:
            user_id = reg['new_user_id']
            token = reg['session_info']['access_token']
            print(f'''\033[1;92m
-----------GENERATED-----------
EMAIL : {email}
ID : {user_id}
PASSWORD : {password}
NAME : {first_name} {last_name}
BIRTHDAY : {birthday} 
GENDER : {gender}
Token : {token}
-----------GENERATED-----------''')
            
            # Save to file
            with open('username.txt', 'a') as f:
                f.write(f"{email}:{password}:{first_name} {last_name}:{user_id}\n")
            return True
        else:
            error_msg = reg.get('error_msg', 'Unknown error')
            print(f"\033[1;91m[×] Facebook Registration Failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"\033[1;91m[×] Facebook Registration Error: {str(e)[:100]}")
        return False

def _call(url, params, proxy=None, post=True):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        if post:
            if proxy and proxy != "no_proxy":
                response = requests.post(url, data=params, headers=headers, proxies=proxy, timeout=15, verify=False)
            else:
                response = requests.post(url, data=params, headers=headers, timeout=15, verify=False)
        else:
            if proxy and proxy != "no_proxy":
                response = requests.get(url, params=params, headers=headers, proxies=proxy, timeout=15, verify=False)
            else:
                response = requests.get(url, params=params, headers=headers, timeout=15, verify=False)
                
        return response.json()
    except Exception as e:
        print(f"\033[1;91m[×] API Call Error: {str(e)[:100]}")
        return {}

def clean_proxy_file():
    """Proxies file clean karta hai aur valid proxies nikalta hai"""
    try:
        if not os.path.exists('proxies.txt'):
            print("[!] proxies.txt file not found. Running without proxies...")
            return []
            
        with open('proxies.txt', 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        
        # Filter valid proxy formats only
        valid_proxies = []
        for line in lines:
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            # Check if line looks like IP:PORT
            if ':' in line and len(line.split(':')) == 2:
                ip_part, port_part = line.split(':')
                # Basic validation
                if port_part.isdigit() and 1 <= int(port_part) <= 65535:
                    valid_proxies.append(line)
        
        if valid_proxies:
            print(f"[+] Found {len(valid_proxies)} valid proxies in file")
        else:
            print("[!] No valid proxies found in proxies.txt")
        return valid_proxies
        
    except Exception as e:
        print(f"[×] Error cleaning proxy file: {e}")
        return []

def test_proxy_helper(proxy_str):
    """Single proxy test karta hai"""
    proxy_dict = {'http': f'http://{proxy_str}', 'https': f'http://{proxy_str}'}
    try:
        response = requests.get('https://api.mail.tm/domains', proxies=proxy_dict, timeout=8, verify=False)
        if response.status_code == 200:
            print(f'[✓] Proxy Working: {proxy_str}')
            return proxy_dict
        else:
            print(f'[×] Proxy Failed (Status {response.status_code}): {proxy_str}')
            return None
    except Exception as e:
        print(f'[×] Proxy Failed: {proxy_str}')
        return None

def get_working_proxies():
    """Working proxies find karta hai"""
    raw_proxies = clean_proxy_file()
    
    if not raw_proxies:
        print("[!] Running without proxies...")
        return ["no_proxy"]
    
    print(f"[+] Testing {len(raw_proxies)} proxies...")
    working_proxies = []
    
    # Test proxies with threading
    def test_proxy(proxy_str):
        result = test_proxy_helper(proxy_str)
        if result:
            working_proxies.append(result)
    
    threads = []
    for proxy_str in raw_proxies:
        thread = threading.Thread(target=test_proxy, args=(proxy_str,))
        thread.start()
        threads.append(thread)
        
        # Limit concurrent threads
        if len(threads) >= 3:  # Reduced to avoid overload
            for t in threads:
                t.join()
            threads = []
    
    # Wait for remaining threads
    for thread in threads:
        thread.join()
    
    if working_proxies:
        print(f"[✓] Found {len(working_proxies)} working proxies")
        return working_proxies
    else:
        print("[×] No working proxies found")
        print("[!] Running without proxies...")
        return ["no_proxy"]

# Alternative method agar API fail ho
def create_temp_email_alternative():
    """Alternative email creation method"""
    try:
        # Use temporary email service as backup
        domains = ['mailto.plus', 'tmpmail.org', 'temp-mail.org']
        domain = random.choice(domains)
        username = generate_random_string(12)
        email = f"{username}@{domain}"
        password = Faker().password()
        first_name = Faker().first_name()
        last_name = Faker().last_name()
        birthday = Faker().date_of_birth(minimum_age=18, maximum_age=45)
        
        print(f'[!] Using alternative email: {email}')
        return email, password, first_name, last_name, birthday
    except:
        return None, None, None, None, None

# Main execution
if __name__ == "__main__":
    try:
        working_proxies = get_working_proxies()
        
        try:
            count = int(input('[+] How Many Accounts You Want: '))
        except:
            count = 1
            
        print(f'\n[+] Creating {count} accounts...\n')
        
        successful_accounts = 0
        for i in range(count):
            print(f'\n[+] Creating Account {i+1}/{count}')
            proxy = random.choice(working_proxies) if working_proxies else "no_proxy"
            
            # Pehle primary method try karein
            email, password, first_name, last_name, birthday = create_mail_tm_account(proxy)
            
            # Agar fail ho to alternative method use karein
            if not email:
                print('[!] Trying alternative method...')
                email, password, first_name, last_name, birthday = create_temp_email_alternative()
            
            if email and password and first_name and last_name and birthday:
                if register_facebook_account(email, password, first_name, last_name, birthday, proxy):
                    successful_accounts += 1
                else:
                    print(f"[×] Facebook registration failed for account {i+1}")
            else:
                print(f"[×] Failed to create email for account {i+1}")
            
            # Delay between account creation
            if i < count - 1:
                delay = random.randint(10, 25)
                print(f"[!] Waiting {delay} seconds...")
                time.sleep(delay)
        
        print(f'\n[✓] Successfully created {successful_accounts}/{count} accounts')
        if successful_accounts > 0:
            print('[✓] Accounts saved to username.txt')
        else:
            print('[×] No accounts were created. Check your internet connection.')
        
    except KeyboardInterrupt:
        print('\n[!] Process interrupted by user')
    except Exception as e:
        print(f'[×] Unexpected error: {e}')

print('\x1b[38;5;94m⇼'*60)
