import bs4
import json

if __name__ != '__main__':
    from . import review
    from . import detail
else:
    import review
    import detail


class GameInfo:
    def __init__(self, review=None, detail=None):
        self._review_summary = review
        self._details = detail

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
            'details': self.details.to_json()
        }

    def __str__(self):
        return json.dumps(self.to_json())


def extract(page):
    soup = bs4.BeautifulSoup(page, 'lxml')
    game_info = GameInfo()
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
