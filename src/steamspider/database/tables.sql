DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS ReviewSummary;
DROP TABLE IF EXISTS GameInfo;

CREATE TABLE GameInfo (
    game_title VARCHAR(255),
    num int NOT NULL,
    developer VARCHAR(255),
    publisher VARCHAR(255),
    release_date VARCHAR(127),
    PRIMARY KEY (game_title)
);

CREATE TABLE Genre (
    game_title VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    FOREIGN KEY(game_title) REFERENCES GameInfo(game_title)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ReviewSummary (
    game_title VARCHAR(255) NOT NULL,
    opinion VARCHAR(255) NOT NULL,
    like_rate float NOT NULL,
    reviews_num INT NOT NULL,
    type VARCHAR(255) NOT NULL,

    FOREIGN KEY(game_title) REFERENCES GameInfo(game_title)
        ON DELETE CASCADE ON UPDATE CASCADE,

    CHECK (type in ("Recent", "Overall")),
    CHECK (like_rate <= 1 AND like_rate >= 0)
);
