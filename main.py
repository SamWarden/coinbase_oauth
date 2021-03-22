from typing import Tuple, Dict
import json

from coinbase.wallet.client import OAuthClient
from coinbase.wallet.model import APIObject


def load_tokens() -> Tuple[str, str]:
    with open('tokens.json') as f:
        data: Dict[str, str] = json.load(f)

    access_token: str = data['access_token']
    refresh_token: str = data.get('refresh_token', '')

    return (access_token, refresh_token)


def update_token(client: OAuthClient) -> None:
    client.refresh()
    with open('tokens.json', 'w') as f:
        json.dump({
            'access_token': client.access_token,
            'refresh_token': client.refresh_token,
        }, f, indent=2)


def print_price(client: OAuthClient, base: str, currency: str) -> None:
    currency_pair = '{}-{}'.format(base, currency)
    print(f'Price for {currency_pair}:')
    print('Buy price:', client.get_buy_price(currency_pair=currency_pair).amount)
    print('Sell price:', client.get_sell_price(currency_pair=currency_pair).amount)
    print('Spot price:', client.get_spot_price(currency_pair=currency_pair).amount)


def print_accounts(client: OAuthClient) -> None:
    print('Accounts:\n', client.get_accounts())


def print_currencies(client: OAuthClient) -> None:
    print('Currencies:\n', client.get_currencies())


def main() -> None:
    tokens = load_tokens()
    client = OAuthClient(*tokens)

    print_price(client, 'BTC', 'USD')
    print_accounts(client)
    print_currencies(client)


if __name__ == '__main__':
    main()
