CREATE TABLE "author_tbl" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" STRING UNIQUE NOT NULL
);
CREATE TABLE "saved_links_tbl" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "link_name" STRING UNIQUE NOT NULL,
    "link" STRING NOT NULL,
    "post_time" DATETIME NOT NULL,
    "delete_time" DATETIME NOT NULL,
    "author_id" INTEGER NOT NULL REFERENCES author_tbl ("id")
);