from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
	username, password = read_secrets()

	driver = webdriver.Chrome()  # Launch Chrome VISIBLY (not headless)
	try:
		# 1) Go to a page that redirects to the login
		driver.get("https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/")

		wait = WebDriverWait(driver, 20)

		# 2) Click the "כניסה עם סיסמה" tab
		login_tab = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#IdentifyWithPassword"]'))
		)
		login_tab.click()

		# 3) Fill in user ID
		username_field = wait.until(
			EC.presence_of_element_located((By.ID, "identifyWithPasswordCitizenId"))
		)
		username_field.clear()
		username_field.send_keys(username)

		# 4) Fill in password
		password_field = driver.find_element(By.ID, "password")
		password_field.clear()
		password_field.send_keys(password)

		# 5) Click "כניסה לאזור האישי."
		submit_button = driver.find_element(By.CLASS_NAME, "validatePassword")
		submit_button.click()

		# 6) Wait for post-login React content inside #app-wrap
		#    If the React app loads a child <div> only after login,
		#    wait until that child exists:
		wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "#app-wrap > *"))
		)

		# 7) Dump the post-login HTML to a file
		post_login_html = driver.page_source
		with open("post_login.html", "w", encoding="utf-8") as f:
			f.write(post_login_html)

		print("Post-login HTML saved to post_login.html")

	except Exception as e:
		print(f"Error during login: {e}")
	finally:
		input("Press Enter to close the browser...")  # So you can visually inspect
		driver.quit()

if __name__ == "__main__":
	main()
