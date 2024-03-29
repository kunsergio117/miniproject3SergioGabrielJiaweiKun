DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


-- Populate user table with example data
INSERT INTO user (username, password) VALUES ('user1', 'password1');
INSERT INTO user (username, password) VALUES ('user2', 'password2');

-- Populate post table with example data
INSERT INTO post (author_id, title, body) VALUES (1, 'Example Post 1', 'This is an example post.');
INSERT INTO post (author_id, title, body) VALUES (2, 'Example Post 2', 'This is another example post.');


