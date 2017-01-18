import requests
import json

BASE_URL = 'http://store.steampowered.com/app/'

STARTING_POINT = 0
END_POINT = 100
STEP = 10

HEADERS = json.load(open('headers.json'))


def pages():
    for index in range(STARTING_POINT, END_POINT, STEP):
        url = _make_url(index)
        text = _get_page(url)
        if not len(text):
            continue
        yield index, text


def _make_url(index):
    # http://store.steampowered.com/app/XX
    return BASE_URL + str(index)


def _get_page(url):
    print('getting', url)
    response = requests.get(url, headers=HEADERS, allow_redirects=False)
    if response.status_code != 200:
        return ""
    return response.text


def _save_page(index, page):
    with open('samples/{0}.html'.format(index), 'w') as f:
        f.write(page)

if __name__ == '__main__':
    for index, page in pages():
        print('get', index)
        _save_page(index, page)
