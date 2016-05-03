CREATE TABLE "User"(
	name VARCHAR(16) NOT NULL PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(128) NOT NULL,
	signup_date TIMESTAMP NOT NULL,
	is_admin BOOLEAN NOT NULL
);

CREATE TABLE "Establishment"(
	id SERIAL NOT NULL CHECK (id>=0),
	name VARCHAR(64) NOT NULL,
	address_street VARCHAR(64) NOT NULL,
	address_number SMALLINT NOT NULL,
	address_postcode INT NOT NULL,
	address_locality VARCHAR(32) NOT NULL,
	gps_longitude NUMERIC(12, 8) NOT NULL,
	gps_latitude NUMERIC(12, 8) NOT NULL,
	phone_number VARCHAR(16) NOT NULL,
	website VARCHAR(255),
	creator_name VARCHAR(32) NOT NULL,
	created_time DATE NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (creator_name) REFERENCES "User"(name) ON DELETE RESTRICT
);

CREATE INDEX "creator_name" ON "Establishment"(creator_name);

CREATE TABLE "Restaurant"(
	price_range NUMERIC(6,2) NOT NULL CHECK (price_range>=0),
	banquet_capacity INT NOT NULL CHECK (banquet_capacity>=0),
	take_away BOOLEAN NOT NULL,
	delivery BOOLEAN NOT NULL,
	establishment_id INT NOT NULL,
	PRIMARY KEY(establishment_id),
	FOREIGN KEY (establishment_id) REFERENCES "Establishment"(id) ON DELETE CASCADE
);

CREATE TABLE "RestaurantClosures"(
	day VARCHAR(16) NOT NULL,
	am BOOLEAN NOT NULL,
	pm BOOLEAN NOT NULL,
	establishment_id INT NOT NULL,
	FOREIGN KEY (establishment_id) REFERENCES "Establishment"(id) ON DELETE CASCADE
);

CREATE INDEX "establishment_id_closures" ON "RestaurantClosures"(establishment_id);

CREATE TABLE "Bar"(
	smoking BOOLEAN NOT NULL,
	snack BOOLEAN NOT NULL,
	establishment_id INT NOT NULL CHECK (establishment_id>=0),
	PRIMARY KEY(establishment_id),
	FOREIGN KEY (establishment_id) REFERENCES "Establishment"(id) ON DELETE CASCADE
);

CREATE TABLE "Hotel"(
	stars SMALLINT NOT NULL CHECK (stars>=0 and stars <=5),
	rooms_number INT NOT NULL CHECK (rooms_number>=0),
	price_range NUMERIC(6,2) NOT NULL CHECK (price_range>=0),
	establishment_id INT NOT NULL CHECK (establishment_id>=0),
	PRIMARY KEY(establishment_id),
	FOREIGN KEY (establishment_id) REFERENCES "Establishment"(id) ON DELETE CASCADE
);

CREATE TABLE "EstablishmentComment"(
	written_date TIMESTAMP NOT NULL,
	score SMALLINT NOT NULL CHECK (score>=0 and score<=5),
	comment_text TEXT NOT NULL,
	user_name VARCHAR(16) NOT NULL,
	establishment_id INT NOT NULL CHECK (establishment_id>=0),
	CONSTRAINT one_comment_per_day_by_user_and_establishment UNIQUE(written_date,user_name,establishment_id),
	FOREIGN KEY (user_name) REFERENCES "User"(name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (establishment_id) REFERENCES "Establishment"(id) ON DELETE CASCADE
);

CREATE INDEX "establishment_id_comment" ON "EstablishmentComment"(establishment_id);
CREATE INDEX "user_name" ON "EstablishmentComment"(user_name);



CREATE TABLE "Tag"(
	name VARCHAR(32) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE "EstablishmentTags"(
	establishment_id INT NOT NULL CHECK (establishment_id>=0),
	tag_name VARCHAR(32) NOT NULL,
	user_name VARCHAR(16) NOT NULL,
	CONSTRAINT one_tag_by_user_by_establishment UNIQUE(establishment_id, tag_name, user_name),
	FOREIGN KEY (user_name) REFERENCES "User"(name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (tag_name) REFERENCES "Tag"(name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (establishment_id) REFERENCES "Establishment"(id) ON DELETE CASCADE
);

CREATE INDEX "establishment_id_tags" ON "EstablishmentTags"(establishment_id);
CREATE INDEX "tag_name" ON "EstablishmentTags"(tag_name);
