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

	try:
		# First, get the login page to capture any necessary tokens
		response = session.get(
			"https://online.maccabi4u.co.il/dana/home/starter.cgi?startpageonly=1",
			verify=True
		)
		response.raise_for_status()

		# Extract any hidden fields from the login form
		soup = BeautifulSoup(response.text, 'html.parser')
		login_form = soup.find('form')
		
		if not login_form:
			raise ValueError("Could not find login form on the page")

		# Prepare login data
		login_data = {
			'username': username,
			'password': password,
		}

		# Add any hidden fields from the form
		for hidden_field in login_form.find_all('input', type='hidden'):
			login_data[hidden_field.get('name')] = hidden_field.get('value')

		# Submit the login form
		login_response = session.post(
			response.url,
			data=login_data,
			allow_redirects=True
		)
		login_response.raise_for_status()

		# Check if login was successful
		if "error" in login_response.url.lower() or "login" in login_response.url.lower():
			raise ValueError("Login failed - please check your credentials")

		return session

	except requests.RequestException as e:
		raise ConnectionError(f"Failed to connect to Maccabi website: {str(e)}")

def read_env_file(file_path: str) -> dict:
	secrets = {}
	assert os.path.isfile(file_path), "secrets file not found"
	with open(file_path, "r") as f:
		for line in f:
			if line.startswith("#") or not line.strip():
				continue
			key, value = line.strip().split("=")
			secrets[key] = value

def main():
	secrets = read_env_file(".secrets")
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