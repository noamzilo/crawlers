from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

def read_secrets():
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

	return username, password

def main():
	# Read credentials from .secrets file
	username, password = read_secrets()

	# 1) Launch Chrome in non-headless mode so we can *see* what's happening.
	driver = webdriver.Chrome()  # Make sure chromedriver is installed

	try:
		# 2) Navigate to a URL that forces Maccabi to redirect you to the login page.
		driver.get("https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/")
		
		# 3) Click the "כניסה עם סיסמה" tab.
		wait = WebDriverWait(driver, 20)
		login_tab = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#IdentifyWithPassword"]'))
		)
		login_tab.click()

		# 4) Fill in user ID.
		username_field = wait.until(
			EC.presence_of_element_located((By.ID, "identifyWithPasswordCitizenId"))
		)
		username_field.clear()
		username_field.send_keys(username)  # Using username from .secrets

		# Fill in password.
		password_field = driver.find_element(By.ID, "password")
		password_field.clear()
		password_field.send_keys(password)  # Using password from .secrets

		# 5) Click "כניסה לאזור האישי."
		submit_button = driver.find_element(By.CLASS_NAME, "validatePassword")
		submit_button.click()

		# 6) Wait a few seconds for the post-login content to appear.
		time.sleep(10)

		# 7) Dump the post-login HTML to a file.
		post_login_html = driver.page_source
		with open("post_login.html", "w", encoding="utf-8") as f:
			f.write(post_login_html)

		print("Post-login HTML saved to post_login.html")
	
	except Exception as e:
		print(f"Error during login: {e}")
	finally:
		# Keep the browser open a bit (optional). 
		# Remove this or set a smaller sleep if you want it to close quickly
		time.sleep(5)
		driver.quit()

if __name__ == "__main__":
	main()
