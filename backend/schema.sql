CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);


-- INSERT INTO users (username, email, password) VALUES ('ozzy', 'kaungpyae@gmail.com', '123@#$*@#DSLFJS');