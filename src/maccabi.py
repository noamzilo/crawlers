import os
import sys
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

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

	user_id = secrets.get("id")
	password = secrets.get("password")
	if not user_id or not password:
		print("Error: Missing ID/password in .secrets")
		sys.exit(1)

	return user_id, password

import glob

def get_newest_file(directory, extension="*"):
    """
    Get the newest file in the specified directory with the given extension.
    """
    files = glob.glob(os.path.join(directory, f"*.{extension}"))
    if not files:
        raise FileNotFoundError(f"No files found in directory: {directory}")
    return max(files, key=os.path.getctime)

def count_files_in_dir(directory, extension="pdf"):
	"""Count number of files with given extension in directory"""
	return len([f for f in os.listdir(directory) if f.endswith(f".{extension}")])

def wait_for_new_file(directory, initial_count, timeout=30, extension="pdf"):
	"""Wait for a new file to appear in the directory and return its path"""
	start_time = time.time()
	while time.time() - start_time < timeout:
		current_files = set(f for f in os.listdir(directory) if f.endswith(f".{extension}"))
		initial_files = set(f for f in os.listdir(directory) if f.endswith(f".{extension}"))
		new_files = current_files - initial_files
		
		if new_files:
			# Give a small delay to ensure file is fully written
			time.sleep(0.5)
			return os.path.join(directory, new_files.pop())
		time.sleep(0.5)
	raise TimeoutError(f"File download timed out after {timeout} seconds")

def scroll_to_element(driver, element):
	"""Scroll element into view using JavaScript"""
	driver.execute_script("arguments[0].scrollIntoView(true);", element)
	# Add small delay after scroll
	time.sleep(0.5)

def load_all_items(driver, wait):
	"""Scroll until all items are loaded and return the complete list"""
	last_item_count = 0
	
	while True:
		# Get current items
		items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
			'div.TimeLineItem-module__item___D5ZMV')))
		
		# If no new items were loaded after scrolling, we're done
		if len(items) == last_item_count:
			return items
		
		# Update count and scroll to last item
		last_item_count = len(items)
		scroll_to_element(driver, items[-1])
		time.sleep(1)  # Wait for potential new items to load

def download_pdf_from_list_view(driver, wait, item, download_dir, download_name):
	"""Handle items with direct PDF button in list view"""
	# Get initial files
	initial_files = set(f for f in os.listdir(download_dir) if f.endswith(".pdf"))
	
	# Find the button within the specific item and click it using JavaScript
	button = item.find_element(By.ID, "ButtonDocument")
	driver.execute_script("arguments[0].click();", button)
	
	# Switch to new window for PDF
	wait.until(lambda d: len(d.window_handles) > 1)
	driver.switch_to.window(driver.window_handles[-1])
	
	# Wait for new file to appear and get its path
	downloaded_file = wait_for_new_file(download_dir, len(initial_files))
	target_path = os.path.join(download_dir, download_name)
	
	# Rename the file
	os.rename(downloaded_file, target_path)
	
	# Close PDF tab/window and switch back
	driver.close()
	driver.switch_to.window(driver.window_handles[0])
	
	return target_path

def download_pdf_from_lab_result(driver, wait, item, download_dir, download_name):
	"""Handle items that require clicking into lab result view"""
	# Get initial files
	initial_files = set(f for f in os.listdir(download_dir) if f.endswith(".pdf"))
	
	# Click the item to open the detailed view using JavaScript
	detailed_button = item.find_element(By.CSS_SELECTOR, 
		"div.MainBody-module__wrap___ZGWaQ.MainBody-module__layout-spread___eCdRv.MainBody-module__quickAction___zkoXs > div > div > div > div > div:nth-child(3) > div:nth-child(2) > div"
	)
	driver.execute_script("arguments[0].click();", detailed_button)
	
	# Wait and click the save button (שמירה) using JavaScript
	save_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
		"div.MainHeadline-module__wrap___LPzAO.LabResult__headerT___B1pfk.d-flex > ul > li:nth-child(1) > button"
	)))
	driver.execute_script("arguments[0].click();", save_button)
	
	# Wait for new file to appear and get its path
	downloaded_file = wait_for_new_file(download_dir, len(initial_files))
	target_path = os.path.join(download_dir, download_name)
	
	# Rename the file
	os.rename(downloaded_file, target_path)
	
	# Click back button (חזרה לכל הבדיקות) using JavaScript
	back_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
		"div.LabResult__headerTitle___qNlv9 > div > button"
	)))
	driver.execute_script("arguments[0].click();", back_button)
	
	return target_path

def identify_item_type(item):
	"""Identify if the item has a direct PDF button or is a clickable lab result"""
	button_document = item.find_elements(By.ID, "ButtonDocument")
	return "pdf_visible_in_list_view" if button_document else "lab_result_clickable"

def download_all_pdfs(driver, wait, items, download_dir):
	"""Download PDFs for all items in the list"""
	downloaded = []
	
	for idx, item in enumerate(items):
		try:
			# Create download name
			download_name = f"{idx}.pdf"
			
			# Identify item type and handle accordingly
			item_type = identify_item_type(item)
			try:
				if item_type == "pdf_visible_in_list_view":
					full_path = download_pdf_from_list_view(driver, wait, item, download_dir, download_name)
				else:  # lab_result_clickable
					full_path = download_pdf_from_lab_result(driver, wait, item, download_dir, download_name)
			except TimeoutError as ex:
				print(f"Failed on item #{idx} due to timeout: {ex}")
				downloaded.append({
					"name_of_item": download_name,
					"full_path_to_item": None,
				})	
				continue
			
			downloaded.append({
				"name_of_item": os.path.basename(full_path),
				"full_path_to_item": full_path
			})
			
		except Exception as e:
			print(f"Failed on item #{idx}: {e}")
			continue
	
	return downloaded

def main():
	# PHASE 1: Setup and Authentication
	user_id, password = read_secrets()

	# Setup download directory
	download_dir = os.path.expanduser(f"~/crawler_downloads/{user_id}")
	os.makedirs(download_dir, exist_ok=True)

	# Configure Chrome for automatic PDF downloads
	options = webdriver.ChromeOptions()
	prefs = {
		"download.default_directory": download_dir,
		"download.prompt_for_download": False,
		"plugins.always_open_pdf_externally": True
	}
	options.add_experimental_option("prefs", prefs)
	driver = webdriver.Chrome(options=options)

	wait = WebDriverWait(driver, 30)
	try:
		# PHASE 2: Login and Navigation
		driver.get("https://online.maccabi4u.co.il/sonline/homepage/NotificationAndUpdates/")
		
		# Login sequence
		login_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#IdentifyWithPassword"]')))
		login_tab.click()
		username_field = wait.until(EC.presence_of_element_located((By.ID, "identifyWithPasswordCitizenId")))
		username_field.clear()
		username_field.send_keys(user_id)
		password_field = driver.find_element(By.ID, "password")
		password_field.clear()
		password_field.send_keys(password)
		submit_button = driver.find_element(By.CLASS_NAME, "validatePassword")
		submit_button.click()
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#app-wrap > *")))

		# Navigate to medical records
		hamburger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
			'div.src-components-Header-Header__hamburger___WA5WU.d-xl-none.d-flex > button')))
		hamburger.click()

		medical_record_button = wait.until(
			EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "תיק רפואי")]'))
		)
		medical_record_button.click()

		# Navigate to test results
		link_to_click = wait.until(
		EC.element_to_be_clickable((By.CSS_SELECTOR,
			'#app-wrap > div.src-containers-App-App__wrap___T6unK > div.src-containers-App-App__header___f0tCR.hideForMobileModal > div.src-components-Header-Header__hamburger___WA5WU.d-xl-none.d-flex.src-components-Header-Header__hamburgerOpen___izDuJ > nav > div > div.src-components-Header-Header__navbar___yF8R3 > div > div.node_modules-\\@maccabi-m-ui-src-components-InputAutoComplete-InputAutoComplete-module__itemWrapperClass___Haf94.src-components-Navigation-Navigation__autocompleteitemsWrapper___bW0PT > div > div:nth-child(4) > div.node_modules-\\@maccabi-m-ui-src-components-Expandable-Expandable-module__wrap___dNT7S.collapse.show > li:nth-child(1) > a'
		))
		)
		link_to_click.click()

		# PHASE 3: Load All Available Items
		print("Loading all items...")
		all_items = load_all_items(driver, wait)
		print(f"Found {len(all_items)} items")

		# PHASE 4: Download All PDFs
		print("Starting downloads...")
		downloaded = download_all_pdfs(driver, wait, all_items, download_dir)
		print(f"Successfully downloaded {len(downloaded)} files")

		# PHASE 5: Save Results
		json_path = os.path.join(download_dir, "downloaded_files.json")
		with open(json_path, "w", encoding="utf-8") as f:
			json.dump(downloaded, f, ensure_ascii=False, indent=2)

		input("All done. Press Enter to close the browser...")

	except Exception as e:
		print(f"Error: {e}")
	finally:
		# PHASE 6: Cleanup
		driver.quit()

if __name__ == "__main__":
	main()
