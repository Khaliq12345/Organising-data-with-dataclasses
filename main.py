from dataclasses import dataclass, asdict
from requests_html import HTMLSession
from typing import Optional
import pandas as pd

@dataclass
class Item:
    name: str
    price: float
    sku: str
    attributes: Optional[list[str]] = None

def get_data(url):
    session = HTMLSession()
    resp = session.get(url)
    return resp

def parse_data(response):
    product = Item(
        name = response.html.find('h1', first=True).text,
        price = response.html.find('.prod-price', first=True).text.replace('£', ''),
        sku = response.html.find('h2.prod-title', first=True).text, 
        attributes= [item.text for item in response.html.find('div.medium-6.cell li')],
    )

    return product

def main(url):
    html = get_data(url)
    pedal = parse_data(html)
    print(asdict(pedal))
    item_list.append(asdict(pedal))

if __name__ == '__main__':
    item_list = []
    urls = [
        'https://www.fxpedalplanet.co.uk/product/magrabo-stripe-sc-entry-biege-5-cm-dark-brown-terminals-aged-brass-buckle-230-111m',
        'https://www.fxpedalplanet.co.uk/product/magrabo-stripe-sc-entry-black-5-cm-black-terminals-silver-buckle-230-010m',
        'https://www.fxpedalplanet.co.uk/product/magrabo-stripe-sc-entry-black-5-cm-dark-brown-terminals-aged-brass-buckle-230-011m',
        'https://www.fxpedalplanet.co.uk/product/magrabo-stripe-sc-entry-brown-5-cm-dark-brown-terminals-aged-brass-buckle-230-211m',
    ]
    for url in urls:
        main(url)
    df = pd.DataFrame(item_list).to_csv('demo.csv', index=False)