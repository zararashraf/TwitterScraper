import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to create a SQLite database and table
def create_database():
    conn = sqlite3.connect('matches.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            home_team TEXT,
            score TEXT,
            away_team TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(date, home_team, score, away_team):
    conn = sqlite3.connect('matches.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO matches (date, home_team, score, away_team)
        VALUES (?, ?, ?, ?)
    ''', (date, home_team, score, away_team))
    conn.commit()
    conn.close()

# Start the web scraping process
url = 'https://www.adamchoi.co.uk/overs/detailed'
driver = webdriver.Firefox()
driver.get(url)

wait = WebDriverWait(driver, 10)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

# Initialize the SQLite database
create_database()

while True:
    date = []
    home_team = []
    score = []
    away_team = []

    matches = driver.find_elements(By.XPATH, '//tr[starts-with(@data-ng-repeat, "match in")]')

    for match in matches:
        date.append(match.find_element(By.XPATH, './td[1]').text)
        home_team.append(match.find_element(By.XPATH, './td[2]').text)
        score.append(match.find_element(By.XPATH, './td[3]').text)
        away_team.append(match.find_element(By.XPATH, './td[4]').text)

        # Insert data into the database
        insert_data(date[-1], home_team[-1], score[-1], away_team[-1])

    # Check for the presence of a "Next" button for pagination
    next_button = driver.find_element(By.XPATH, '//button[text()="Next"]')
    if next_button.get_attribute("disabled") == "true":
        break
    else:
        next_button.click()

driver.quit()
