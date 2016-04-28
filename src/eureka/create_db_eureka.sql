CREATE DATABASE db_eureka;
USE db_eureka;

CREATE TABLE User(
	name VARCHAR(16) NOT NULL,
	email VARCHAR(32) NOT NULL,
	password VARCHAR(128) NOT NULL,
	signup_date DATE NOT NULL,
	is_admin BOOLEAN NOT NULL,
	PRIMARY KEY(username),
	PRIMARY KEY(email),
	UNIQUE(username),
	UNIQUE(email)
);

CREATE TABLE Establishment(
	id INT UNSIGNED NOT NULL AUTO_INCREMENT,
	name VARCHAR(16) NOT NULL,
	address_street VARCHAR(64) NOT NULL,
	address_number SMALLINT UNSIGNED NOT NULL,
	address_postcode INT UNSIGNED NOT NULL,
	address_locality VARCHAR(32) NOT NULL,
	gps_longitude FLOAT(12, 8) NOT NULL,
	gps_latitude FLOAT(12, 8) NOT NULL,
	phone_number VARCHAR(16) NOT NULL,
	website VARCHAR(255),
	created_by
	PRIMARY KEY(id)
);

CREATE TABLE Restaurant(
	price_range FLOAT(6,2) NOT NULL,
	banquet_capacity INT UNSIGNED NOT NULL,
	take_away BOOLEAN NOT NULL,
	delivery BOOLEAN NOT NULL,
	establishment_id INT UNSIGNED NOT NULL,
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE;
);

CREATE TABLE RestaurantClosures(
	day VARCHAR(16) NOT NULL,
	am BOOLEAN NOT NULL,
	pm BOOLEAN NOT NULL,
	establishment_id INT UNSIGNED NOT NULL,
	PRIMARY KEY(day),
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE;
);

CREATE TABLE Bar(
	smoking BOOLEAN NOT NULL,
	snack BOOLEAN NOT NULL,
	establishment_id INT UNSIGNED NOT NULL,
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE;
);

CREATE TABLE Hotel(
	stars TINYINT UNSIGNED NOT NULL,
	rooms_number INT UNSIGNED NOT NULL,
	price_range FLOAT(6,2) NOT NULL,
	establishment_id INT UNSIGNED NOT NULL,
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE;
);

CREATE TABLE Comment(
	written_date DATETIME NOT NULL,
	score TINYINT UNSIGNED NOT NULL,
	comment_text TEXT NOT NULL,
	username VARCHAR(16) NOT NULL,
	establishment_id INT UNSIGNED NOT NULL,
	FOREIGN KEY (user_name) REFERENCES User(name) ON DELETE CASCADE ON UPDATE CASCADE; 
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE;
);
