import bs4
import json

if __name__ != '__main__':
    from . import review
    from . import detail
else:
    import review
    import detail


class GameInfo:
    def __init__(self, index, review=None, detail=None):
        self._review_summary = review
        self._details = detail
        self._index = index

    @property
    def index(self):
        return self._index

    @property
    def review_summary(self):
        return self._review_summary

    @review_summary.setter
    def review_summary(self, rev):
        self._review_summary = rev

    @property
    def details(self):
        return self._details

    @details.setter
    def details(self, d):
        self._details = d

    def to_json(self):
        return {
            'review_summary': self.review_summary.to_json(),
            'details': self.details.to_json(),
            'index': self.index
        }

    def __str__(self):
        return json.dumps(self.to_json())

def _check_page(soup):
    review_infos = soup.find_all('div', 'user_reviews_summary_row')
    if not review_infos:
        return False
    return True


def extract(page, index=0):
    soup = bs4.BeautifulSoup(page, 'lxml')
    if not _check_page(soup):
        return None
    game_info = GameInfo(index)
    game_info.review_summary = review.extract(soup)
    game_info.details = detail.extract(soup)
    return game_info


if __name__ == '__main__':
    from os.path import join
    import os
    from sys import stdout

    sample_dir = '../samples/'
    samples = os.listdir(sample_dir)
    for sample in samples:
        sample_path = join(sample_dir, sample)
        with open(sample_path) as f:
            content = f.read()
            json.dump(extract(content).to_json(), stdout, indent=4)
