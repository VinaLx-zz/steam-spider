import re
import json


class ReviewSummary:
    def __init__(self, recent=None, overall=None):
        self._recent = recent
        self._overall = overall

    @property
    def recent(self):
        return self._recent

    @property
    def overall(self):
        return self._overall

    def to_json(self):
        return {
            'recent': self.recent.to_json() if self.recent else None,
            'overall': self.overall.to_json() if self.overall else None
        }

    def __str__(self):
        return json.dumps(self.to_json())


class ReviewInfo:
    def __init__(self, opinion, total_rev, like_percent):
        self._opinion = opinion
        self._total_rev = total_rev
        self._like_percent = like_percent

    @property
    def opinion(self):
        return self._opinion

    @property
    def total_review(self):
        return self._total_rev

    @property
    def like_percent(self):
        return self._like_percent

    def to_json(self):
        return {
            'opinion': self.opinion,
            'total': self.total_review,
            'like': self.like_percent
        }

    def __str__(self):
        return json.dumps(self.to_json())


def extract(soup):
    review_infos = soup.find_all('div', 'user_reviews_summary_row')
    if not review_infos:
        return None
    overall_info = _extract_info(review_infos[len(review_infos)-1])
    if (len(review_infos) > 1):
        recent_info = _extract_info(review_infos[0])
    else:
        recent_info = None

    return ReviewSummary(recent_info, overall_info)


def _extract_info(review_summary_row):
    like_percent, total_review = _extract_data(review_summary_row)
    if like_percent is None and total_review is None:
        return None
    opinion = review_summary_row.find('span', 'game_review_summary').string
    return ReviewInfo(opinion, total_review, like_percent)


def _extract_data(review_summary_row):
    tooltip = review_summary_row['data-store-tooltip']
    if tooltip == 'No user reviews':
        return None, None
    regex = re.compile(r'^(\d+)% of the ([\d,]+?) ')
    match_result = re.match(regex, tooltip).groups()
    return int(match_result[0]) / 100, \
        int(match_result[1].replace(',', ''))


if __name__ == '__main__':
    from bs4 import BeautifulSoup
    from os.path import join
    import os

    sample_dir = '../samples/'
    samples = os.listdir(sample_dir)
    for sample in samples:
        sample_path = join(sample_dir, sample)
        soup = BeautifulSoup(open(sample_path), 'lxml')
        print(extract(soup))
