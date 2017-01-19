import requests
import json

BASE_URL = 'http://store.steampowered.com/app/'
HEADERS = json.load(open('headers.json'))


def pages(start_idx, end_idx, step):
    for index in range(start_idx, end_idx, step):
        text = get_game(index)
        if not len(text):
            continue
        yield index, text


def get_game(index):
    url = _make_url(index)
    text = _get_page(url)
    return text


def _make_url(index):
    # http://store.steampowered.com/app/XX0
    return BASE_URL + str(index * 10)


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
    STARTING_POINT = 0
    END_POINT = 100
    STEP = 1
    for index, page in pages(STARTING_POINT, END_POINT, STEP):
        print('get', index)
        _save_page(index, page)
