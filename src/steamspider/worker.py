import crawler
from extractor import extractor
from database import gamedb


class Worker:
    def __init__(self, work_range, db_config):
        self._game_db = gamedb.GameDb(db_config)
        self._range = work_range

    def work(self):
        for index in self._range:
            try:
                self._work_one(index)
            except Exception as e:
                import os
                import sys
                print("EXCEPTION index: %d, title: %s"
                        % (index, e), file=sys.stderr)

    def _work_one(self, index):
        page = crawler.get_game(index)
        if not len(page):
            return
        game_info = extractor.extract(index, page)
        self._game_db.save(game_info)

if __name__ == '__main__':
    import json
    with open('config-files/db.json') as f:
        db_config = json.load(f)

    w = Worker((1, 11), db_config)
    w.work()
