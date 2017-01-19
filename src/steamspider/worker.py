if __name__ == 'steamspider.worker':
    from . import crawler
    from .extractor import extractor
    from .database import gamedb
else:
    import crawler
    from extractor import extractor
    from database import gamedb


class Worker:
    def __init__(self, work_range, db_config):
        self._game_db = gamedb.GameDb(db_config)
        self._start = work_range[0]
        self._end = work_range[1]

    def work(self):
        for index in range(self._start, self._end):
            self._work_one(index)

    def _work_one(self, index):
        page = crawler.get_game(index)
        if not len(page):
            return
        game_info = extractor.extract(index, page)
        self._game_db.insert_game(game_info)

if __name__ == '__main__':
    import json
    with open('database/db.json') as f:
        db_config = json.load(f)

    w = Worker((1, 11), db_config)
    w.work()
