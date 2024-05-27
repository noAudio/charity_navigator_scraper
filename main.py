import concurrent.futures.process
import csv

from scraper import Scraper


def main(start: int, end: int) -> None:
    scraper: Scraper = Scraper()
    scraper.get_data(start=start, end=end + 1)
    with open(f'charities{start}_{end}.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['EIN', 'Name', 'Phone', 'Website', 'Address', 'Profile Link'])
        for charity in scraper.results:
            writer.writerow([charity.ein, charity.name, charity.phone, charity.website, charity.address, charity.profileLink])
        f.close()


if __name__ == '__main__':
    ranges = [(0, 100), (100, 200), (200, 300), (300, 400), (400, 500), (500, 600), (600, 700), (700, 800), (800, 900), (900, 1000)]
    with concurrent.futures.process.ProcessPoolExecutor(max_workers=len(ranges)) as executor:
        results = list(executor.map(main, *zip(*ranges)))

