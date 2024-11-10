from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
import keyboard
from pystyle import Center, Colors, Colorate
import time

from lib.lib import create_driver, authenticate, select_user_agent, set_random_timezone, \
    set_fake_geolocation, get_accounts, select_language, press_play, enable_repeat, get_song


def main():
    print("-" * 8 + "Rigatoni" + "-" * 8)

    driver_path = '../../programming/bot/selenium/chromedriver'
    accounts_path = '../../programming/bot/selenium/accounts.txt'
    spotify_song = "https://open.spotify.com/track/5bGWa3ltaNGKkGpASo3Uvt?si=0024aedd312646e0"
    proxies = []

    random_user_agent = select_user_agent()
    accounts = get_accounts(accounts_path)
    drivers = []

    for account in accounts:
        username = account['username']
        password = account['password']

        random_language = select_language()
        driver = create_driver(random_user_agent, random_language, driver_path)

        authenticate(driver, username, password)
        time.sleep(random.uniform(4, 6))

        get_song(driver, spotify_song)
        time.sleep(random.uniform(2,6))

        try:
            driver.find_element(By.XPATH, "//button[text()='Accept Cookies']").click()
            print(f"{username} Accepted Cookies")
        except Exception as e:
            print(f"{username} didn't accept cookies; got this error: \n{e}")

        time.sleep(random.uniform(5,10))
        press_play(driver)
        time.sleep(random.uniform(2,6))
        enable_repeat(driver)

        set_random_timezone(driver)
        set_fake_geolocation(driver)

        drivers.append(driver)

        print(f"Username: {username} - Listening process has started.")

    while True:
        pass


if __name__ == "__main__":
    main()
