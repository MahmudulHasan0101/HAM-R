from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

youtube = build('youtube', 'v3', developerKey = YOUTUBE_API_KEY)


def APIsearch(query, results = 3):
    request = youtube.search().list(
        part='id,snippet',
        q=query,
        maxResults = results,
        type='video'
    )

    response = request.execute()
    search_results = []

    #print(response)

    for video in response['items']:
        item = {
            'name': video["snippet"]["title"],
            'url': f'https://www.youtube.com/watch?v={video["id"]["videoId"]}',
        }

        search_results.append(item)

    return search_results

def search_and_open(query, headless = False):
    chrome_options = Options()

    if headless: 
        chrome_options.add_argument("--headless") 

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.youtube.com")

    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(query)

    search_box.submit()

    wait = WebDriverWait(driver, 10)
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a#video-title")))

    if results:
        first_result = results[0]
        first_result.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
    return driver

def open(url, headless = False):
    chrome_options = Options()
    if headless: 
        chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(320)  # Wait for up to 10 seconds for elements to appear
    driver.set_page_load_timeout(320)  # Wait for up to 15 seconds for the page to load
    driver.set_script_timeout(320) # Using set_script_timeout (waits for JavaScript execution)

    driver.get(url)
    play_button = driver.find_element(By.CSS_SELECTOR, ".ytp-play-button")
    play_button.click()

    return driver


if __name__ == "__main__":
    # video = APIsearch("white tee")[0]
    # driver = open(video['url'], True)

    driver = search_and_open("white tee", True)

    input("Press any key to exit...")
    driver.quit()
