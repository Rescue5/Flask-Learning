CREATE TABLE IF NOT EXISTS users(
    user_id_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS songs(
    songs_id_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT NOT NULL,
    duration TEXT NOT NULL
);

INSERT OR IGNORE INTO users (login, password) VALUES ('admin', 'admin');

INSERT INTO songs (name, artist, album, duration) VALUES
                      ('Saw', 'Orbit Culture', 'Redfog', '5:40'),
                      ('TokSik', 'STARSET', 'EP TokSik', '3:51'),
                      ('Let Me Go', 'Sullivan King', 'Thrones of Blood', '3:42');
