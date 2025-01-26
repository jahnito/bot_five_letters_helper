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

CREATE TABLE "sessions" (
	"id"	INTEGER,
	"tg_id"	INTEGER,
	"started"	TEXT,
	"ended"	TEXT,
	"active"	INTEGER,
	"word_len"	INTEGER,
	"result"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "attempts" (
	"id"	INTEGER,
	"session_id"	INTEGER,
	"message_id"	INTEGER,
	"chars_excluded"	TEXT,
	"chars_included"	TEXT,
	"chars_non_in_pos"	TEXT,
	"chars_in_pos"	TEXT,
	"attempt_number"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);