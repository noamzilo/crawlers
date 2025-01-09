import os
import sys
import requests
from bs4 import BeautifulSoup

def login_maccabi(username: str, password: str) -> requests.Session:
	"""
	1) Create a requests.Session so cookies persist automatically.
	2) Attempt to reach the final target URL (which should redirect to the SAML login).
	3) Parse the resulting login form for hidden SAML fields (SAMLRequest, RelayState, etc.).
	4) Submit user+pass to the actual login form endpoint (sometimes 'infosec/auth').
	5) Let requests handle any 302 redirects, capturing new cookies or tokens.
	6) Return the session, now hopefully authenticated for subsequent calls.
	"""

	# STEP 1: Start a session
	session = requests.Session()
	session.max_redirects = 10

	# The final page you want:
	target_url = "https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/"

	# STEP 2: Hit the target page (which typically redirects you to the SAML login).
	resp1 = session.get(target_url, allow_redirects=True)

	# If the server hasn’t redirected yet, or the form is already present:
	soup = BeautifulSoup(resp1.text, 'html.parser')
	saml_request_input = soup.find('input', {'name': 'SAMLRequest'})

	if not saml_request_input:
		print("[DEBUG] Could not find 'SAMLRequest' in the HTML. Maybe they changed flow or you’re on a different path.")
		# We’ll still proceed if there's no SAML form. Possibly the site already gave you a login form.
		pass

	# STEP 3: We often find a <form> with SAMLRequest, RelayState, etc.
	# Example:
	#   <form action="https://mac.maccabi4u.co.il/login" method="POST">
	#       <input type="hidden" name="SAMLRequest" value="fZBb..."/>
	#       <input type="hidden" name="RelayState" value="..."/>
	#   </form>
	form_tag = soup.find('form')
	if not form_tag:
		print("[DEBUG] No <form> found. Possibly the request already included a redirect. Continue carefully.")
		# In real usage, handle that scenario gracefully.

	form_action = form_tag.get('action') if form_tag else None
	if not form_action:
		print("[DEBUG] No form action found. We'll guess the final login endpoint below.")
		# If you already know the endpoint is 'https://mac.maccabi4u.co.il/infosec/auth', proceed with that

	# Construct the form data. We always have user & pass (like you had in `payload`).
	# We might also include any hidden fields (SAMLRequest, RelayState) if found.
	form_data = {
		"type": "password",
		"id": f"0-{username}",  
		"password": password
	}

	# If you find hidden fields, add them:
	if saml_request_input:
		form_data["SAMLRequest"] = saml_request_input.get('value')
	relay_input = soup.find('input', {'name': 'RelayState'})
	if relay_input:
		form_data["RelayState"] = relay_input.get('value')

	# STEP 4: Submit the credentials to the correct URL.
	# Sometimes the form action is something like https://mac.maccabi4u.co.il/infosec/auth
	# If form_action is None, fallback to your known login endpoint:
	login_url = form_action if form_action else "https://mac.maccabi4u.co.il/infosec/auth"

	login_response = session.post(login_url, data=form_data, allow_redirects=True)
	if login_response.status_code != 200:
		raise ConnectionError(f"Login step failed with status {login_response.status_code}")

	# Possibly the server returns JSON with a new JWT. Possibly not.
	# If you DO get a JSON with 'jwt', store it in the session headers:
	try:
		js = login_response.json()
		jwt_token = js.get("jwt")
		if jwt_token:
			session.headers.update({'Authorization': f'Bearer {jwt_token}'})
	except:
		pass  # Not all flows return JSON here.

	# After this, session might get auto-redirected to more pages (SAML handshake, etc.).
	# We'll do another quick request to confirm all cookies are properly set.
	test_auth = session.get(target_url)
	if test_auth.status_code == 200:
		print("[DEBUG] Possibly logged in, got 200 from target_url.")
	else:
		print(f"[DEBUG] Possibly not logged in. Status was {test_auth.status_code}")

	# Return the session, now presumably authenticated
	return session


def main():
	# Read credentials
	secrets_path = "src/.secrets"
	if not os.path.isfile(secrets_path):
		print("Error: secrets file missing")
		sys.exit(1)

	secrets = {}
	with open(secrets_path, "r") as f:
		for line in f:
			if line.startswith("#") or not line.strip():
				continue
			key, val = line.strip().split("=")
			secrets[key] = val

	username = secrets.get("id")
	password = secrets.get("password")
	if not username or not password:
		print("Error: Missing ID/password in .secrets")
		sys.exit(1)

	# Use the new login approach
	session = login_maccabi(username, password)

	# Now test the final protected page
	test_url = "https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/"
	resp = session.get(test_url)
	if resp.status_code == 200:
		print("Successfully authenticated!")
		with open("output1.html", "w", encoding="utf-8") as f:
			f.write(resp.text)
	else:
		print(f"Failed to authenticate. Status: {resp.status_code}")

if __name__ == "__main__":
	main()
