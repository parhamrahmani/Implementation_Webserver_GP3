#!/usr/bin/env bash
# script for setting up database
mysql -u "$1" --password="$2" -e """CREATE DATABASE mydb;
USE mydb;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
CREATE TABLE credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
INSERT INTO credentials (user, password) VALUES ('testuser', 'testpassword');

GRANT ALL PRIVILEGES ON mydb.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;"""

printf "\nDEBUG: List of tables in database mydb:\n"
mysql -u "$1" --password="$2" -e "USE mydb; SHOW FULL TABLES;"

printf "\nDEBUG: Schema of table credentials:\n"
mysql -u "$1" --password="$2" -e "USE mydb; SHOW COLUMNS FROM credentials;"

