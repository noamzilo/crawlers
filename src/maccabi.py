import os
import requests
from bs4 import BeautifulSoup
import sys

def login_to_maccabi(username: str, password: str) -> requests.Session:
	"""
	Attempts to login to Maccabi healthcare website
	Returns the session object if successful
	"""
	session = requests.Session()
	
	# Set up headers to mimic a browser
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Connection': 'keep-alive',
	}
	
	session.headers.update(headers)

	post_login_curl = """
		curl 'https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/' \
		-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
		-H 'Accept-Language: en-US,en;q=0.9' \
		-H 'Cache-Control: no-cache' \
		-H 'Connection: keep-alive' \
		-H 'Cookie: _cls_v=f80f52ff-471b-4557-8b4a-f66718fd36ef; _cls_s=a6a9955f-75e8-4c3f-b384-65ae82beb194:0; rto=c0; LastMRH_Session=ff6b6733; MRHSession=2aeb171df728ac09bec72fbbff6b6733; TS01e632ca=0184b3c362645582055d3c1a30da8305fd923c982bad6aa2f7f2cb5ed849ac9b5ff7d4b5e0680ff9e8068d092ef01809562c517a6b; TS1a59e30d027=089a239b29ab200020ded068116e321121d4e9c8359b6339c0c1910934be681dd2f1f091b9b18e3508024cbe3611300087f16c470001fb959d58310d5c5134e10d67c073ad6963de909c08e4330ed44d8e737da048e1550224373f89775325a3' \
		-H 'Pragma: no-cache' \
		-H 'Referer: https://online.maccabi4u.co.il/my.policy' \
		-H 'Sec-Fetch-Dest: document' \
		-H 'Sec-Fetch-Mode: navigate' \
		-H 'Sec-Fetch-Site: same-origin' \
		-H 'Upgrade-Insecure-Requests: 1' \
		-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
		-H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
		-H 'sec-ch-ua-mobile: ?0' \
		-H 'sec-ch-ua-platform: "Windows"'

	"""

	cookies = {
		'_cls_v': 'f80f52ff-471b-4557-8b4a-f66718fd36ef',
		'_cls_s': 'a6a9955f-75e8-4c3f-b384-65ae82beb194:0',
		'rto': 'c0',
		'LastMRH_Session': 'ff6b6733',
		'MRHSession': '2aeb171df728ac09bec72fbbff6b6733',
		'TS01e632ca': '0184b3c362645582055d3c1a30da8305fd923c982bad6aa2f7f2cb5ed849ac9b5ff7d4b5e0680ff9e8068d092ef01809562c517a6b',
		'TS1a59e30d027': '089a239b29ab200020ded068116e321121d4e9c8359b6339c0c1910934be681dd2f1f091b9b18e3508024cbe3611300087f16c470001fb959d58310d5c5134e10d67c073ad6963de909c08e4330ed44d8e737da048e1550224373f89775325a3',
	}

	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Language': 'en-US,en;q=0.9',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		# 'Cookie': '_cls_v=f80f52ff-471b-4557-8b4a-f66718fd36ef; _cls_s=a6a9955f-75e8-4c3f-b384-65ae82beb194:0; rto=c0; LastMRH_Session=ff6b6733; MRHSession=2aeb171df728ac09bec72fbbff6b6733; TS01e632ca=0184b3c362645582055d3c1a30da8305fd923c982bad6aa2f7f2cb5ed849ac9b5ff7d4b5e0680ff9e8068d092ef01809562c517a6b; TS1a59e30d027=089a239b29ab200020ded068116e321121d4e9c8359b6339c0c1910934be681dd2f1f091b9b18e3508024cbe3611300087f16c470001fb959d58310d5c5134e10d67c073ad6963de909c08e4330ed44d8e737da048e1550224373f89775325a3',
		'Pragma': 'no-cache',
		'Referer': 'https://online.maccabi4u.co.il/my.policy',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'same-origin',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
		'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
	}

	response = requests.get(
		'https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/',
		cookies=cookies,
		headers=headers,
	)
	if response.status_code != 200:
		raise ConnectionError(f"Failed to connect to Maccabi website: {response.status_code}")
	
	soup = BeautifulSoup(response.text, 'html.parser')

	hi=5

def read_env_file(file_path: str) -> dict:
	env_vars = {}
	assert os.path.isfile(file_path), "secrets file not found"
	with open(file_path, "r") as f:
		for line in f:
			if line.startswith("#") or not line.strip():
				continue
			key, value = line.strip().split("=")
			env_vars[key] = value
	return env_vars

def main():
	secrets = read_env_file("src/.secrets")
	try:
		username = secrets["id"]
		password = secrets["password"]
	except KeyError:
		print("Error: Missing required credentials in .env file")
		sys.exit(1)

	try:
		session = login_to_maccabi(username, password)
		print("Successfully logged in to Maccabi website")
		# You can now use the session object to make authenticated requests
		
	except (ConnectionError, ValueError) as e:
		print(f"Error: {str(e)}")
		sys.exit(1)

if __name__ == "__main__":
	main()