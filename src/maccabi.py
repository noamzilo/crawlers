import os
import requests
from bs4 import BeautifulSoup
import sys
from requests.auth import HTTPBasicAuth


def login(url: str, user_id: str, password: str):
	# For Basic Authentication
	# response = requests.get(url, auth=HTTPBasicAuth(username, password))

	payload = {
		"type": "password",
		"id": f"0-{user_id}",  
		"password": f"{password}" 
	}

	# Define the headers (as seen in the Network tab)
	headers = {
		"Content-Type": "application/json",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
		"Accept": "application/json; charset=utf-8",
		"Origin": "https://mac.maccabi4u.co.il",
		"Referer": "https://mac.maccabi4u.co.il/login"
	}
	# Create a session object to maintain cookies and connection
	session = requests.Session()
	response = session.post(url, json=payload, headers=headers)
	# Set the initial cookies and headers
	# Check if login was successful
	if response.status_code == 200:
		print("Login successful!")
		print("Cookies set:", session.cookies.get_dict())  # Print cookies for debugging
	else:
		print("Login failed:", response.status_code, response.text)

	return session


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

	url = 'https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/'

	try:
		# login_url = "https://online.maccabi4u.co.il/dana/home/starter.cgi?startpageonly=1"
		login_url = "https://mac.maccabi4u.co.il/infosec/auth"
		post_login_url = 'https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/'
		session = login(login_url, username, password)
		print("Successfully logged in to Maccabi website")
		# You can now use the session object to make authenticated requests
	except (ConnectionError, ValueError) as e:
		print(f"Error: {str(e)}")
		sys.exit(1)
		# Use session instead of one-off request

	protected_url = 'https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/',
	response = session.get(protected_url)
	print(response.text)
	soup = BeautifulSoup(response.text, 'html.parser')
	with open("output1.html", "w") as f:
		f.write(str(soup))

if __name__ == "__main__":
	main()