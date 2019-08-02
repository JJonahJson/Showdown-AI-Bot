CREATE TABLE Abilities (
    id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    weather VARCHAR(30),
    modify_stat VARCHAR(4),
    multiplier int(3),
    stat VARCHAR(4),
    value int(3),
    target VARCHAR(10),
    type VARCHAR(20)
);
