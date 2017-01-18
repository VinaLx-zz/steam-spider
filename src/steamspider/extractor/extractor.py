import bs4
from . import review


class GameInfo:
    pass


def extract(page):
    soup = bs4.BeautifulSoup(page, 'lxml')
    review_summary = review.extract(soup)
