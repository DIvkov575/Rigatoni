from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chromium.webdriver import ChromiumDriver

import random
import pytz
import keyboard
from pystyle import Center, Colors, Colorate
import time


def select_language():
    supported_languages = [
        "en-US", "en-GB", "en-CA", "en-AU", "en-NZ", "fr-FR", "fr-CA", "fr-BE", "fr-CH", "fr-LU",
        "de-DE", "de-AT", "de-CH", "de-LU", "es-ES", "es-MX", "es-AR", "es-CL", "es-CO", "es-PE",
        "it-IT", "it-CH", "ja-JP", "ko-KR", "pt-BR", "pt-PT", "ru-RU", "tr-TR", "nl-NL", "nl-BE",
        "sv-SE", "da-DK", "no-NO"
    ]
    return random.choice(supported_languages)


def select_user_agent():
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
    return random.choice(user_agents)


def set_random_timezone(driver):
    supported_timezones = pytz.all_timezones
    random_timezone = random.choice(supported_timezones)
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": random_timezone})


def set_fake_geolocation(driver: ChromiumDriver):
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    }
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", params)


def authenticate(driver: ChromiumDriver, uname: str, passwrd: str):
    driver.get("https://www.spotify.com/us/login/")
    username_input = driver.find_element(By.CSS_SELECTOR, "input#login-username")
    password_input = driver.find_element(By.CSS_SELECTOR, "input#login-password")
    username_input.send_keys(uname)
    password_input.send_keys(passwrd)
    driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button']").click()


def create_driver(random_user_agent, random_language, driver_path):
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
    return driver


def get_accounts(path: str):
    accounts = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            username, password = line.strip().split(":")
            accounts.append({'username': username, 'password': password})
    return accounts

def press_play(driver:ChromiumDriver):
    driver.find_element(By.CSS_SELECTOR, "#main > div > div.ZQftYELq0aOsg6tPbVbV > div.jEMA2gVoLgPQqAFrPhFw > div.main-view-container > div.main-view-container__scroll-node.main-view-container__scroll-node--offset-topbar > div:nth-child(2) > div > main > section > div:nth-child(3) > div:nth-child(2) > div > div > div > button").click()

def enable_repeat(driver: ChromiumDriver):
    repeat_song = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[2]/div/div[1]/div[2]/button[2]')
    repeat_song_state = repeat_song.get_attribute("aria-label")
    if repeat_song_state == 'Disable repeat':
        repeat_song.click()
        time.sleep(random.uniform(0, 1))
        repeat_song.click()
    elif repeat_song_state == 'Enable repeat':
        repeat_song.click()
    elif repeat_song_state == 'Enable repeat one':
        pass
    else:
        print(Colors.red, "unknown repeat-button state")
    repeat_song = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[2]/div/div[1]/div[2]/button[2]')
    print(repeat_song)

def get_song(driver: ChromiumDriver, spotify_song_uri: str):
    driver.get(spotify_song_uri)
    keyboard.press_and_release('esc')
