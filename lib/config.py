import json


def parse_config(config_path):
    with open(config_path, "r") as file:
        data = json.load(file)
        a = data["Proxies"]
        b = data["Accounts"]


if __name__ == '__main__':
    parse_config("./assets/config.json")