CREATE TABLE "dictionary" (
	"id"	INTEGER,
	"word"	TEXT,
	"part_of_speech"	INTEGER,
	"description"	TEXT,
	"added"	DATETIME,
	"changed"	DATETIME,
	PRIMARY KEY("id")
);

CREATE TABLE "users" (
	"id"	INTEGER,
	"tg_id"	INTEGER,
	"status"	INTEGER,
	"registered"	DATETIME,
	"activity"	DATETIME,
	PRIMARY KEY("id" AUTOINCREMENT)
);