import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = 'your_username'
password = 'your_password'
max_tweets = 100

def scroll_down(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

with webdriver.Firefox(options=options) as browser:
    url = 'https://twitter.com/'
    browser.get(url)

    wait = WebDriverWait(browser, 10)

    login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="/login"]')))
    login_button.click()

    username_input = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@name="text"]')))
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)

    time.sleep(3)

    password_input = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@name="password"]')))
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@enterkeyhint="search"]')))

    search_input = browser.find_element(By.XPATH, '//input[@enterkeyhint="search"]')
    search_input.send_keys('python')
    search_input.send_keys(Keys.RETURN)

    current_tweets = 0
    user_data = []
    text_data = []

    while current_tweets < max_tweets:

        for _ in range(5):
            scroll_down(browser)

        tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]')))
        
        for tweet in tweets:
            try:
                user = tweet.find_element(By.XPATH, './/span[contains(text(), "@")]').text
                text = tweet.find_element(By.XPATH, ".//div[@lang]").text
                tweets_data = [user, text]
            except Exception as e:
                print(f"Error extracting tweet: {e}")
                tweets_data = ['user', 'text']

            user_data.append(tweets_data[0])
            text_data.append(" ".join(tweets_data[1].split()))

            current_tweets += 1

        print(f"Scraped {current_tweets} tweets")

        if current_tweets >= max_tweets:
            break

    df = pd.DataFrame({'user': user_data, 'text': text_data})
    df.to_csv('tweets.csv', index=False)
    print(f"Total {current_tweets} tweets scraped")
