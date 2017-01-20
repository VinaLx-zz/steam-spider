from workerpool import WorkerPool
from worker import Worker
from extractor import extractor
from database import gamedb
import json
import crawler
import sys

class Menu:
    def __init__(self, db_config, work_config, argv):
        self._db_config = db_config
        self._work_config = work_config
        self._argv = argv
        self._command_handler = {
            'fetch': self.fetch_handler,
            'extract': self.extract_handler,
            'save': self.save_handler
        }

    def execute(self):
        if len(self._argv) == 1:
            self.start_all()
        else:
            self.dispatch_command()

    def start_all(self):
        pool = WorkerPool(self._work_config, self._db_config)
        pool.start()


    def dispatch_command(self):
        assert len(self._argv) > 1
        command = self._argv[1]
        self._command_handler.get(command, self.unknown_handler)()

    def fetch_handler(self):
        index = int(self._argv[2])
        text = crawler.get_game(index)
        print(text)

    def extract_handler(self):
        for path in self._argv[2:]:
            self._print_info(path)

    def unknown_handler(self):
        pass

    def _print_info(self, html_path):
        with open(html_path) as f:
            game_info = extractor.extract(f.read())
            print('%s:' % html_path)
            if game_info is None:
                print('null')
                return
            json.dump(game_info.to_json(), sys.stdout, indent=4)
            print()

    def save_handler(self):
        for path in self._argv[2:]:
            self._save_record(path)

    def _save_record(self, html_path):
        with open(html_path) as f:
            game_info = extractor.extract(f.read())
        if game_info is None:
            return
        game_db = gamedb.GameDb(self._db_config)
        game_db.save(game_info)

