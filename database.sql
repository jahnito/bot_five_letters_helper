CREATE TABLE "dictionary" (
	"id"	INTEGER,
	"word"	TEXT,
	"code"	INTEGER,
	"code_parent"	INTEGER,
	"gender"	TEXT,
	"wcase"	INTEGER,
	"soul"	INTEGER,
	"description"	TEXT,
	"added"	TEXT,
	"changed"	TEXT,
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


CREATE TABLE "filtered_dicts" (
	"id"	INTEGER,
	"tg_id"	INTEGER,
	"word"	TEXT,
	"session_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
