CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* To 'auth_user'@'localhost';

USE auth;

CREATE TABLE user(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(55) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO USER(email,password) VALUES ('amanatanayak@gmail.com','2004')