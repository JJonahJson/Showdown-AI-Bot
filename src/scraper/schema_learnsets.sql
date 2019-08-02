USE showdown_db;

CREATE TABLE Learnsets (
    id VARCHAR(30) NOT NULL,
    move VARCHAR(30) NOT NULL,
    PRIMARY KEY (id, move)
);
