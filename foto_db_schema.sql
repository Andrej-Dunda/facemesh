DROP TABLE IF EXISTS fotos;

CREATE TABLE fotos (
    foto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    elo_general INTEGER DEFAULT 1400,
    elo_male INTEGER DEFAULT 1400,
    elo_female INTEGER DEFAULT 1400,
    general_encounters_count INTEGER DEFAULT 0,
    male_encounters_count INTEGER DEFAULT 0,
    female_encounters_count INTEGER DEFAULT 0,
    general_reached_2400 INTEGER DEFAULT 0,
    male_reached_2400 INTEGER DEFAULT 0,
    female_reached_2400 INTEGER DEFAULT 0
);