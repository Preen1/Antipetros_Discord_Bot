CREATE TABLE author_tbl (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT UNIQUE NOT NULL,
    discord_id INTEGER UNIQUE NOT NULL,
    is_member BOOLEAN NOT NULL
);
CREATE TABLE category_tbl (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL,
    emoji TEXT UNIQUE
);
INSERT INTO category_tbl (
        id,
        name,
        emoji
    )
VALUES (
        1,
        'General',
        '🇴'
    );
INSERT INTO category_tbl (
        id,
        name,
        emoji
    )
VALUES (
        2,
        'Bug',
        '🇧'
    );
INSERT INTO category_tbl (
        id,
        name,
        emoji
    )
VALUES (
        3,
        'Change request',
        '🇨'
    );
INSERT INTO category_tbl (
        id,
        name,
        emoji
    )
VALUES (
        4,
        'Feature request',
        '🇫'
    );
INSERT INTO category_tbl (
        id,
        name,
        emoji
    )
VALUES (
        5,
        'Game Balance',
        '🇬'
    );
INSERT INTO category_tbl (
        id,
        name,
        emoji
    )
VALUES (
        6,
        'Minor Task',
        '🚸'
    );
CREATE TABLE extra_data_tbl (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    location TEXT UNIQUE NOT NULL
);
CREATE TABLE suggestion_tbl (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name TEXT,
    author_id INTEGER REFERENCES author_tbl (id) NOT NULL,
    added_by_author_id INTEGER REFERENCES author_tbl (id) NOT NULL,
    message_discord_id INTEGER UNIQUE NOT NULL,
    link_to_message TEXT UNIQUE,
    utc_posted_time DATETIME NOT NULL,
    utc_saved_time DATETIME NOT NULL,
    upvotes INTEGER DEFAULT (0),
    downvotes INTEGER DEFAULT (0),
    content BLOB UNIQUE NOT NULL,
    extra_data_id INTEGER REFERENCES extra_data_tbl (id),
    discussed BOOLEAN DEFAULT (0),
    category_id INTEGER REFERENCES category_tbl (id) DEFAULT (1)
);
CREATE TABLE emoji_tbl(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name TEXT NOT NULL UNIQUE,
    alias TEXT NOT NULL UNIQUE,
    as_unicode TEXT NOT NULL UNIQUE
)