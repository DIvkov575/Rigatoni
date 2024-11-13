from lib.lib import create_driver, authenticate, select_user_agent, set_random_timezone, \
    set_fake_geolocation, get_accounts, select_language, enable_repeat, open_uri, press_play_playlist, \
    try_accept_cookies
from concurrent.futures.thread import ThreadPoolExecutor
from selenium.webdriver.common.by import By
import random
import time


def main():
    print("-" * 8 + "Rigatoni" + "-" * 8)

    driver_path = 'assets/chromedriver'
    accounts_path = 'assets/accounts.txt'
    uri = "https://open.spotify.com/playlist/1uqAtFEvDCUEwHouRP4Ogx?si=TBIQLRqQTv-SN5OGPyOkBw"

    random_user_agent = select_user_agent()
    accounts = get_accounts(accounts_path)
    drivers = []

    def spawn(account):
        username, password = account['username'], account['password']
        random_language = select_language()
        driver = create_driver(random_user_agent, random_language, driver_path)

        # auth
        authenticate(driver, username, password)
        time.sleep(random.uniform(4, 6))

        # page
        open_uri(driver, uri)
        time.sleep(random.uniform(2, 6))

        # cookies
        try_accept_cookies(driver, username)
        time.sleep(random.uniform(5, 10))

        # play
        press_play_playlist(driver)
        time.sleep(random.uniform(2, 6))

        # repeat
        enable_repeat(driver)

        set_random_timezone(driver)
        set_fake_geolocation(driver)
        drivers.append(driver)

        print(f"Username: {username} - Listening process has started.")

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(spawn, accounts))

    while True:
        pass


if __name__ == "__main__":
    main()
