CREATE TABLE IF NOT EXISTS mood(
    mid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    mood_time INTEGER DEFAULT CURRENT_TIMESTAMP NOT NULL,
    type TEXT NOT NULL,
    score INTEGER NOT NULL
);

CREATE TRIGGER IF NOT EXISTS update_food
    AFTER INSERT ON mood
    BEGIN
        UPDATE food SET mid = NEW.mid WHERE mid ISNULL;
    END;