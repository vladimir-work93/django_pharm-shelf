CREATE TABLE IF NOT EXISTS "USER_MEDICATIONS" (
	"id" INTEGER NOT NULL UNIQUE,
	"production_date" TEXT,
	"expiry_date" TEXT,
	"is_searchable" INTEGER DEFAULT false,
	"user_id" INTEGER,
	"medication_id" INTEGER,
	PRIMARY KEY("id", "user_id", "medication_id")
);

CREATE TABLE IF NOT EXISTS "USERS" (
	"id" INTEGER NOT NULL UNIQUE,
	"first_name" TEXT,
	"last_name" TEXT,
	"email" TEXT UNIQUE,
	"phone" TEXT UNIQUE,
	"snils" TEXT,
	"password" TEXT UNIQUE,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "USER_MEDICATIONS"("user_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "MEDICATIONS" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"image_url" TEXT,
	"description" TEXT,
	"manufacturer_id" INTEGER,
	PRIMARY KEY("id", "manufacturer_id"),
	FOREIGN KEY ("id") REFERENCES "USER_MEDICATIONS"("medication_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "MANUFACTURERS" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" TEXT,
	"country" TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY ("id") REFERENCES "MEDICATIONS"("manufacturer_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
);
