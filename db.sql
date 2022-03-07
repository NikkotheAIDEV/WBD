CREATE DATABASE WBD;
USE WBD;

CREATE TABLE Categories (
	id BIGINT UNIQUE PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(177) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
);

CREATE TABLE Museums (
	id BIGINT UNIQUE PRIMARY KEY AUTO_INCREMENT,
    museum_name VARCHAR(177) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    country VARCHAR(37) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    address VARCHAR(177) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    avg_rating DOUBLE,
    category_id BIGINT,
    longitude Double,
    latitude Double,
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);

CREATE TABLE Person (
	id BIGINT UNIQUE PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(77) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    surname VARCHAR(77) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    visited_museums_id BIGINT,
    FOREIGN KEY (visited_museums_id) REFERENCES Museums(id),
    most_liked_category_id BIGINT
);

CREATE TABLE Visited (
	id BIGINT UNIQUE PRIMARY KEY AUTO_INCREMENT,
    person_id BIGINT,
    FOREIGN KEY (person_id) REFERENCES Person(id),
    museum_id BIGINT,
    FOREIGN KEY (museum_id) REFERENCES Museums(id)
);

INSERT INTO Categories (category_name)
VALUES 
("Art Museums"),
("Arboretums, Botanical Gardens, & Nature Centers"),
("Children's Museums"),
("Uncategorized or General Museums"),
("Historical Societies, Historic Preservation"),
("History Museums"),
("Natural History & Natural Science Museums"),
("Science & Technology Museums & Planetariums"),
("Zoos, Aquariums, & Wildlife Conservation");