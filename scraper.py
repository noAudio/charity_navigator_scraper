import json
from random import randint, random
from typing import List, Dict
from time import sleep

import requests
from bs4 import BeautifulSoup as bs4

from charity import Charity


class Scraper:
    # https://www.charitynavigator.org/api/search?states=AZ&page=1&pageSize=10
    baseLink: str = 'https://www.charitynavigator.org/api/search?states=AZ'
    headers: Dict[str, str] = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    totalPages: int = 1000
    results: List[Charity] = []

    def __init__(self) -> None:
        pass

    def get_data(self, start: int, end: int) -> None:
        for page_no in range(start, end + 1):
            if page_no == 0:
                continue
            if (page_no - 1) % 10 == 0:
                timer: int = randint(960, 2700)
                print(f'Waiting {timer} seconds')
                sleep(timer)
            print(f'Scraping page {page_no}')
            link: str = f'{self.baseLink}&page={page_no}&pageSize=10'
            response: requests.Response = requests.get(
                link, headers=self.headers)
            json_response = json.loads(response.content)
            page_items: List[Dict[str, str | bool]
                             ] = json_response['data']['searchFaceted']['results']
            for item in page_items:
                print(f'({page_no}) Item {
                      page_items.index(item) + 1}/{len(page_items)}.')
                name: str = item['name']
                profile_link: str = f'https://www.charitynavigator.org{
                    item["url"]}'
                ein: str = item['ein']

                other_data: List[Dict[str, str]
                                 ] = self.get_details(profile_link)

                phone: str = ''
                website: str = ''
                address: str = ''

                if len(other_data) > 0:
                    for data in other_data:
                        if 'phone' in data.keys():
                            phone = data['phone']
                        elif 'website' in data.keys():
                            website = data['website']
                        elif 'address' in data.keys():
                            address = data['address']

                self.results.append(
                    Charity(
                        name=name,
                        profile_link=profile_link,
                        address=address,
                        website=website,
                        ein=ein,
                        phone=phone,
                    )
                )
                duration: int = randint(6, 45)
                print(f'Waiting {duration} seconds')
                sleep(duration)

    def get_details(self, profile_link) -> List[Dict[str, str]]:
        details = []
        response = requests.get(profile_link, headers=self.headers)
        soup = bs4(response.content, 'html.parser')
        anchors = soup.select('a.cn-link-profile')
        for anchor in anchors:
            href = anchor.get('href').lower()
            if 'tel' in href:
                details.append({'phone': anchor.text})
            if 'www' in href or 'http' in href:
                details.append({'website': href})
        address_elem = soup.select_one('.tw-grid.tw-text-gray-600')
        if address_elem:
            details.append({'address': address_elem.text})
        return details
