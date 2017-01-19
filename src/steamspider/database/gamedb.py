import pymysql


class GameDb:

    def __init__(self, db_config):
        self._connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['username'],
            password=db_config['password'],
            db=db_config['database'])

    INSERT_GENRE_SQL = \
        'INSERT INTO Genre (game_title, genre) VALUES (%s, %s);'

    INSERT_DETAIL_SQL = \
        """
        INSERT INTO GameInfo
        (game_title, num, developer, publisher, release_date)
        VALUES (%s, %s, %s, %s, %s);
        """

    INSERT_REVIEW_SQL = \
        """
        INSERT INTO ReviewSummary
        (game_title, opinion, like_rate, reviews_num, type)
        VALUES (%s, %s, %s, %s, %s);
        """

    DELETE_BY_TITLE_SQL = \
        """
        DELETE FROM GameInfo WHERE game_title = %s;
        """

    def save(self, game_info):
        with self._connection.cursor() as self._cursor:
            title = game_info.details.title
            self._delete_by_title(title)
            self._insert_game_details(game_info.index, game_info.details)
            self._insert_review(title, game_info.review_summary)

        self._connection.commit()
        import os
        print('pid: %d, %d: %s' %
              (os.getpid(), game_info.index, game_info.details.title))

    def _insert_game_details(self, index, detail):
        self._cursor.execute(self.INSERT_DETAIL_SQL, (
            detail.title, index, detail.developer,
            detail.publisher, detail.release_date))

        self._insert_genres(detail.title, detail.genre)

    def _insert_genres(self, title, genres):
        for genre in genres:
            self._cursor.execute(self.INSERT_GENRE_SQL, (title, genre))

    def _insert_review(self, title, review):
        self._insert_review_info(title, review.overall, "Overall")
        if review.recent is not None:
            self._insert_review_info(title, review.recent, "Recent")

    def _insert_review_info(self, title, review, t):
        self._cursor.execute(
            self.INSERT_REVIEW_SQL, (
                title, review.opinion, review.like_percent,
                review.total_review, t))

    def _delete_by_title(self, title):
        self._cursor.execute(self.DELETE_BY_TITLE_SQL, (title,))

if __name__ == '__main__':
    import sys
    import os
    import json
    sys.path.append('..')
    from extractor import extractor
    sample_dir = '../samples'
    samples = os.listdir(sample_dir)
    with open('../config-files/db.json') as config_file:
        db_config = json.load(config_file)

    game_db = GameDb(db_config)

    for sample in samples:
        sample_path = os.path.join(sample_dir, sample)
        with open(sample_path) as f:
            game_info = extractor.extract(0, f.read())
            game_db.save(game_info)
