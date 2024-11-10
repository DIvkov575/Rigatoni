from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import requests
import webbrowser
import random
import pytz
import time
import os
import keyboard
from colorama import Fore
from pystyle import Center, Colors, Colorate
import time


supported_timezones = pytz.all_timezones

def set_random_timezone(driver):
    random_timezone = random.choice(supported_timezones)
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": random_timezone})

def set_fake_geolocation(driver, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    }
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)

def main():
    print("-"*5 + "Rigatoni" + "-"*5)

    user_agents = [
    # Chrome (Windows)
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",

    # Chrome (Mac)
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.116 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.116 Safari/537.36",

    # # Firefox (Windows)
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    # "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    #
    # # Firefox (Mac)
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.4; rv:93.0) Gecko/20100101 Firefox/93.0",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:93.0) Gecko/20100101 Firefox/93.0",
    #
    # # Safari (Mac)
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    #
    # # Opera (Windows)
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 OPR/80.0.4170.61",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 OPR/80.0.4170.61",
    # "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 OPR/80.0.4170.61"
    ]
    
    #FAKE Language
    supported_languages = [
    "en-US", "en-GB", "en-CA", "en-AU", "en-NZ", "fr-FR", "fr-CA", "fr-BE", "fr-CH", "fr-LU",
    "de-DE", "de-AT", "de-CH", "de-LU", "es-ES", "es-MX", "es-AR", "es-CL", "es-CO", "es-PE",
    "it-IT", "it-CH", "ja-JP", "ko-KR", "pt-BR", "pt-PT", "ru-RU", "tr-TR", "nl-NL", "nl-BE",
    "sv-SE", "da-DK", "no-NO"
    ]

    chrome_path = './GoogleChrome'
    driver_path = './chromedriver'

    random_user_agent = random.choice(user_agents)

    with open('accounts.txt', 'r') as file:
        accounts = file.readlines()

    proxies = []
    spotify_song = "https://open.spotify.com/track/5bGWa3ltaNGKkGpASo3Uvt?si=0024aedd312646e0"
    drivers = []


    for account in accounts:
        random_language = random.choice(supported_languages)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ["enable-automation", 'enable-logging'])
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--window-size=1366,768")
        chrome_options.add_argument("--lang=en-US,en;q=0.9")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(f"--user-agent={random_user_agent}")
        chrome_options.add_argument(f"--lang={random_language}")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.notifications': 2
        })

        driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

        username, password = account.strip().split(':')

        driver.get("https://www.spotify.com/us/login/")
        username_input = driver.find_element(By.CSS_SELECTOR, "input#login-username")
        password_input = driver.find_element(By.CSS_SELECTOR, "input#login-password")
        username_input.send_keys(username)
        password_input.send_keys(password)

        driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button']").click()
        time.sleep(random.uniform(2, 6))

        driver.get(spotify_song)
        driver.maximize_window()
        keyboard.press_and_release('esc')
        time.sleep(10)

        try:
            cookie = driver.find_element(By.XPATH, "//button[text()='Accept Cookies']")
            cookie.click()
        except NoSuchElementException:
            try:
                button = driver.find_element(By.XPATH, "//button[contains(@class,'onetrust-close-btn-handler onetrust-close-btn-ui')]")
                button.click()
            except NoSuchElementException:
                time.sleep(random.uniform(5, 14))



        playmusic = driver.find_element(By.CSS_SELECTOR, "#main > div > div.ZQftYELq0aOsg6tPbVbV > div.jEMA2gVoLgPQqAFrPhFw > div.main-view-container > div.main-view-container__scroll-node.main-view-container__scroll-node--offset-topbar > div:nth-child(2) > div > main > section > div:nth-child(3) > div:nth-child(2) > div > div > div > button")
        playmusic.click()

#            time.sleep(random.uniform(0,1))
        repeate_song = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[2]/div/div[1]/div[2]/button[2]')
#            repeate_song.click()
#            time.sleep(random.uniform(0,1))
#            repeate_song.click()

        state = driver.find_element(
        print("state 2")

        print(Colors.green, f"Username: {username} - Listening process has started.")


        set_random_timezone(driver)
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        set_fake_geolocation(driver, latitude, longitude)

        drivers.append(driver)


        print("drviers", drivers)

    while True:
        pass

if __name__ == "__main__":
    main()
