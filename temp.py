from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the YouTube website
driver.get("https://www.youtube.com")

# Find the search box and enter your search query
search_box = driver.find_element(By.NAME, "search_query")
search_box.send_keys("your search query")

# Submit the search form
search_box.submit()

# Wait for the search results to load
wait = WebDriverWait(driver, 10)
results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a#video-title")))

# Click on the first search result
if results:
    first_result = results[0]
    first_result.click()

# Wait for the video to load and play
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))

# Keep the browser window open until you close it manually
input("Press any key to exit...")
driver.quit()