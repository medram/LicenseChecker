import random
import os

import requests


def random_agent():
    agents = (
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15",
        "Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
    )
    return random.choice(agents)


def verify_envato_license_code(code, envato_token):
    url = f'https://api.envato.com/v3/market/author/sale?code={code}'
    data = {}

    headers = {
        'Authorization': f"Bearer {envato_token}",
        'User-Agent': random_agent()
    }

    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        try:
            data = req.json()
            if data.get('license') and data.get('purchase_count') > 0:
                """
                                "amount": "4.37",
                                "sold_at": "2021-12-19T01:43:13+11:00",
                                "license": "Regular License",
                                "support_amount": "1.84",
                                "supported_until": "2022-12-19T07:43:13+11:00",
                                "buyer": "username",
                                "purchase_count": 1
                """
                # TODO: register the client (if he is new).

                return data, True
        except Exception as e:
            print(e)

    return data, False


def generate_api_key():
    return os.urandom(20).hex()
