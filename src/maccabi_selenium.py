import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver() -> webdriver.Chrome:
	"""Initialize Chrome WebDriver with appropriate options."""
	options = webdriver.ChromeOptions()
	
	# Add options for better stability and performance
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument('--disable-gpu')
	options.add_argument('--window-size=600,400')
	
	# Fix for DevToolsActivePort error
	options.add_argument('--remote-debugging-port=9222')
	options.add_argument('--disable-setuid-sandbox')
	
	# Disable logging that might interfere with browser initialization
	options.add_argument('--log-level=3')
	options.add_argument('--silent')
	
	# Disable features that might cause issues
	options.add_argument('--disable-extensions')
	options.add_argument('--disable-infobars')
	options.add_argument('--disable-notifications')
	
	# Add user agent to avoid detection
	options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
	
	# Enable headless mode with specific arguments to avoid DevTools error
	options.add_argument('--headless=new')
	options.add_argument('--disable-software-rasterizer')
	
	try:
		# Create a temporary directory for Chrome if it doesn't exist
		chrome_tmp_dir = "/tmp/chrome-data"
		if not os.path.exists(chrome_tmp_dir):
			os.makedirs(chrome_tmp_dir)
		options.add_argument(f'--user-data-dir={chrome_tmp_dir}')
		
		# Install ChromeDriver
		driver_path = ChromeDriverManager().install()
		print(f"ChromeDriver path: {driver_path}")
		
		service = Service(driver_path)
		service.log_path = os.path.join(os.getcwd(), "selenium.log")
		
		print("Initializing Chrome WebDriver...")
		driver = webdriver.Chrome(
			options=options,
			service=service
		)
		
		# Set reasonable page load timeout
		driver.set_page_load_timeout(30)
		driver.implicitly_wait(10)
		
		# Verify driver is working
		print("Testing WebDriver...")
		driver.get("about:blank")
		print("WebDriver initialized successfully")
		
		return driver
		
	except WebDriverException as e:
		print("\nChrome WebDriver initialization failed:")
		print(f"Error type: {type(e).__name__}")
		print(f"Error message: {str(e)}")
		
		# Check Chrome installation
		chrome_path = None
		if sys.platform.startswith('linux'):
			chrome_paths = [
				'/usr/bin/google-chrome',
				'/usr/bin/chrome',
				'/usr/bin/chromium',
				'/usr/bin/chromium-browser'
			]
			for path in chrome_paths:
				if os.path.exists(path):
					chrome_path = path
					break
		print(f"\nChrome installation found at: {chrome_path if chrome_path else 'Not found'}")
		
		print("\nPlease check:")
		print("1. Chrome browser is installed and up-to-date")
		print("2. You have necessary permissions")
		print("3. Check selenium.log for detailed error information")
		print("\nTry running these commands:")
		print("google-chrome --version")
		print("chromedriver --version")
		print("chmod +x " + driver_path if 'driver_path' in locals() else "chmod +x /path/to/chromedriver")
		raise

def login_with_selenium(driver: webdriver.Chrome, url: str, user_id: str, password: str) -> None:
	"""Perform login using Selenium WebDriver."""
	try:
		print(f"Navigating to {url}")
		driver.get(url)
		
		wait = WebDriverWait(driver, 20)
		
		# identify with password
		field = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#IdentifyWithPassword"]'))
		)
		field.click()
			
		print("Waiting for username field...")
		username_field = wait.until(
			EC.presence_of_element_located((By.ID, "identifyWithPasswordCitizenId"))
		)
		username_field.clear()  # Clear field before sending keys
		username_field.send_keys(user_id)
		
		print("Locating password field...")
		password_field = wait.until(
			EC.presence_of_element_located((By.ID, "password"))
		)
		password_field.clear()  # Clear field before sending keys
		password_field.send_keys(password)
		
		print("Clicking login button...")
		button = wait.until(
		EC.element_to_be_clickable((By.CLASS_NAME, "validatePassword"))
		)
		button.click()
		
	except TimeoutException as e:
		print(f"Timeout error: {str(e)}")
		print("Current URL:", driver.current_url)
		print("Page source:", driver.page_source)
		raise Exception("Timeout waiting for page elements")
	except Exception as e:
		print(f"Login error: {str(e)}")
		print("Current URL:", driver.current_url)
		if driver.get_screenshot_as_file("error_screenshot.png"):
			print("Error screenshot saved as 'error_screenshot.png'")
		raise Exception(f"Login failed: {str(e)}")

def read_env_file(file_path: str) -> dict:
	"""Read environment variables from file."""
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
	original_url = "https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/"
	# original_url = "https://online.maccabi4u.co.il/dana/home/starter.cgi?startpageonly=1"
	secrets = read_env_file("src/.secrets")
	
	try:
		username = secrets["id"]
		password = secrets["password"]
	except KeyError:
		print("Error: Missing required credentials in .secrets file")
		sys.exit(1)
	
	driver = None
	try:
		driver = initialize_driver()
		login_with_selenium(driver, original_url, username, password)
		print("Successfully authenticated to Maccabi website")

		print("Waiting for successful login...")
		
		wait = WebDriverWait(driver, 20)
		new_content = wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "src-components-Header-Header__logo___NSUR"))
		)
		print("New content loaded!")
		return new_content
		
		# Wait for protected content to load (adjust timeout and selector as needed)
		wait = WebDriverWait(driver, 20)
		wait.until(
			EC.presence_of_element_located((By.CLASS_NAME, "protected-content"))
		)
		
		# You can add additional actions here, such as:
		# - Extracting data from the protected page
		# - Navigating to other pages
		# - Taking screenshots
		
	except Exception as e:
		print(f"Error: {str(e)}")
		sys.exit(1)
	finally:
		if driver:
			driver.quit()

if __name__ == "__main__":
	main() 