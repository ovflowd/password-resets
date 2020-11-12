CREATE TABLE tokens (
    id int NOT NULL AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    token varchar(32) NOT NULL,
    claimed int NOT NULL,
    expired int NOT NULL,
    date DATETIME NOT NULL,
    PRIMARY KEY (id)
);
