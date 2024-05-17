from scraper import Scraper


def main() -> None:
    scraper: Scraper = Scraper()
    scraper.get_data()


if __name__ == '__main__':
    main()
