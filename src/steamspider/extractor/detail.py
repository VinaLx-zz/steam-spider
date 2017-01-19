import json


class Detail:

    def __init__(self, title=None, genre=None,
                 developer=None, publisher=None, release_date=None):
        self._title = title
        self._genre = genre
        self._developer = developer
        self._publisher = publisher
        self._release_date = release_date

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, t):
        self._title = t

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, g):
        self._genre = g

    @property
    def developer(self):
        return self._developer

    @developer.setter
    def developer(self, dev):
        self._developer = dev

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, pub):
        self._publisher = pub

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, date):
        self._release_date = date

    def to_json(self):
        return {
            'title': self.title,
            'release_date': self.release_date,
            'publisher': self.publisher,
            'developer': self.developer,
            'genre': self.genre
        }

    def __str__(self):
        return json.dumps(self.to_json())


def _is_details_block(tag):
    return tag.name == 'div' and \
            tag.get('class') == ['details_block'] and \
            tag.find('b')


def extract(soup):
    details_block = soup.find(_is_details_block)
    detail = Detail()
    detail.title = _extract_title(details_block)
    detail.genre = _extract_genre(details_block)
    detail.developer = _extract_developer(details_block)
    detail.publisher = _extract_publisher(details_block)
    detail.release_date = _extract_release_date(details_block)
    return detail


def _extract_title(details_block):
    return _get_next_string(details_block.b)


def _extract_genre(details_block):
    genre_start = details_block.find(_string_is('Genre:'))
    if not genre_start:
        return []
    genres = _get_contents(genre_start)
    return genres


def _extract_developer(details_block):
    return _get_next_string(details_block.find(_string_is('Developer:')))


def _extract_publisher(details_block):
    return _get_next_string(details_block.find(_string_is('Publisher:')))


def _extract_release_date(details_block):
    date = _get_next_string(details_block.find(_string_is('Release Date:')))
    if date is None:
        return ''
    return date


def _string_is(string):
    def f(tag):
        return tag.name == 'b' and \
                tag.string == string

    return f


def _get_next_string(tag):
    if tag is None:
        return ''
    for string in tag.next_siblings:
        string = string.string
        if string is None:
            return ''
        string = string.strip()
        if len(string):
            return string


def _get_contents(start):
    result = []
    for tag in start.next_siblings:
        if tag.name == 'br' or tag.name == 'b':
            break
        if tag.name == 'a':
            result.append(tag.string)
    return result


if __name__ == '__main__':
    import os
    from os.path import join
    from bs4 import BeautifulSoup as BS
    sample_dir = '../samples/'
    for sample in os.listdir(sample_dir):
        sample_path = join(sample_dir, sample)
        soup = BS(open(sample_path), 'lxml')
        print(extract(soup))
