CREATE TABLE "User"(
	name VARCHAR(16) NOT NULL PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(128) NOT NULL,
	signup_date TIMESTAMP NOT NULL,
	is_admin BOOLEAN NOT NULL
);

CREATE TABLE "Establishment"(
	id SERIAL NOT NULL,
	name VARCHAR(16) NOT NULL,
	address_street VARCHAR(64) NOT NULL,
	address_number SMALLINT NOT NULL,
	address_postcode INT NOT NULL,
	address_locality VARCHAR(32) NOT NULL,
	gps_longitude NUMERIC(12, 8) NOT NULL,
	gps_latitude NUMERIC(12, 8) NOT NULL,
	phone_number VARCHAR(16) NOT NULL,
	website VARCHAR(255),
	creator_name VARCHAR(16) NOT NULL,
	created_time DATE NOT NULL,
	CONSTRAINT created_time_posterior_creator_signup CHECK(created_time >= (SELECT signup_date FROM User WHERE name=creator_name)),
	CONSTRAINT creator_is_admin CHECK((SELECT is_admin FROM User WHERE name=creator_name) = 1),
	INDEX(creator_name),
	PRIMARY KEY(id),
	FOREIGN KEY (creator_name) REFERENCES User(name) ON DELETE RESTRICT
)

CREATE TABLE "Restaurant"(
	price_range FLOAT(6,2) NOT NULL,
	banquet_capacity INT NOT NULL,
	take_away BOOLEAN NOT NULL,
	delivery BOOLEAN NOT NULL,
	establishment_id INT NOT NULL,
	PRIMARY KEY(establishment_id),
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE
);

CREATE TABLE "RestaurantClosures"(
	day VARCHAR(16) NOT NULL,
	am BOOLEAN NOT NULL,
	pm BOOLEAN NOT NULL,
	establishment_id INT NOT NULL,
	INDEX(establishment_id),
	CONSTRAINT numbers_of_closures_max_7 CHECK((SELECT COUNT(establishment_id)) <= 7),
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE
);

CREATE TABLE "Bar"(
	smoking BOOLEAN NOT NULL,
	snack BOOLEAN NOT NULL,
	establishment_id INT NOT NULL,
	PRIMARY KEY(establishment_id),
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE
);

CREATE TABLE "Hotel"(
	stars TINYINT NOT NULL,
	rooms_number INT NOT NULL,
	price_range FLOAT(6,2) NOT NULL,
	establishment_id INT NOT NULL,
	CONSTRAINT stars_between_0_and_5 CHECK(stars>=0 AND stars<=5),
	PRIMARY KEY(establishment_id),
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE
);

CREATE TABLE "EstablishmentComment"(
	written_date TIMESTAMP NOT NULL,
	score TINYINT NOT NULL,
	comment_text TEXT NOT NULL,
	user_name VARCHAR(16) NOT NULL,
	establishment_id INT NOT NULL,
	INDEX(user_name),
	INDEX(establishment_id),
	CONSTRAINT score_between_0_and_5 CHECK(score>=0 AND score<=5),
	CONSTRAINT one_comment_per_day_by_user_and_establishment CHECK((SELECT COUNT(written_date))
	CONSTRAINT one_comment_per_day_by_user_and_establishment UNIQUE(written_date,user_name,establishment_id),
	CONSTRAINT comment_date_posterior_user_signup_date CHECK(written_date >= (SELECT signup_date FROM User WHERE name=user_name)),
	CONSTRAINT comment_date_posterior_establishment_creation_date CHECK(written_date >= (SELECT created_time FROM Establishment WHERE id=establishment_id)),
	FOREIGN KEY (user_name) REFERENCES User(name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE
);

CREATE TABLE "Tag"(
	name VARCHAR(16) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE "EstablishmentTags"(
	establishment_id INT NOT NULL,
	tag_name VARCHAR(16) NOT NULL,
	user_name VARCHAR(16) NOT NULL,
	INDEX(establishment_id),
	INDEX(tag_name),
	CONSTRAINT one_tag_by_user_by_establishment UNIQUE(establishment_id, tag_name, user_name),
	FOREIGN KEY (user_name) REFERENCES User(name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (tag_name) REFERENCES Tag(name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (establishment_id) REFERENCES Establishment(id) ON DELETE CASCADE
);

