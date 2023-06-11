DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_age INTEGER,
    user_gender TEXT,
    user_timestamp TEXT
);