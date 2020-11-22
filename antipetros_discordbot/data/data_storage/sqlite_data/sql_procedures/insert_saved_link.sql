INSERT INTO "saved_links_tbl" (
        "link_name",
        "link",
        "post_time",
        "delete_time",
        "author_id"
    )
VALUES (
        ?,
        ?,
        ?,
        ?,
(
            SELECT "id"
            FROM "author_tbl"
            WHERE "name" = ?
        )
    )