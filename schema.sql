BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Admin_Notifications";
CREATE TABLE IF NOT EXISTS "Admin_Notifications" (
	"Note_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"User_ID"	INTEGER NOT NULL,
	"Item_ID"	INTEGER NOT NULL DEFAULT -1,
	"Notification_Type"	INTEGER NOT NULL,
	"Has_Been_Read"	INTEGER NOT NULL DEFAULT 0
);
DROP TABLE IF EXISTS "Character";
CREATE TABLE IF NOT EXISTS "Character" (
	"Character_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"User_ID"	INTEGER NOT NULL,
	"Character_Is_Open"	INTEGER NOT NULL DEFAULT 0,
	"Character_Name"	TEXT NOT NULL,
	"Character_Class"	INTEGER NOT NULL DEFAULT -1,
	"Character_Race"	INTEGER NOT NULL DEFAULT -1,
	"Character_Level"	INTEGER NOT NULL DEFAULT 0,
	"Character_Currency"	INTEGER NOT NULL DEFAULT 0,
	"Character_Base_Carrying_Cap"	INTEGER NOT NULL DEFAULT 0,
	"Character_Max_Carry_Weight"	INTEGER NOT NULL DEFAULT 0,
	"Character_Strength"	INTEGER NOT NULL DEFAULT 0,
	"Character_Dexterity"	INTEGER NOT NULL DEFAULT 0,
	"Character_Constitution"	INTEGER NOT NULL DEFAULT 0,
	"Character_Intelligence"	INTEGER NOT NULL DEFAULT 0,
	"Character_Wisdom"	INTEGER NOT NULL DEFAULT 0,
	"Character_Charisma"	INTEGER NOT NULL DEFAULT 0,
	"Character_Head"	INTEGER NOT NULL DEFAULT -1,
	"Character_Torso"	INTEGER NOT NULL DEFAULT -1,
	"Character_Shoulder"	INTEGER NOT NULL DEFAULT -1,
	"Character_Hand"	INTEGER NOT NULL DEFAULT -1,
	"Character_Leg"	INTEGER NOT NULL DEFAULT -1,
	"Character_Foot"	INTEGER NOT NULL DEFAULT -1,
	"Character_Weapon1"	INTEGER NOT NULL DEFAULT -1,
	"Character_Weapon2"	INTEGER NOT NULL DEFAULT -1,
	"Character_Weapon3"	INTEGER NOT NULL DEFAULT -1,
	"Character_Weapon4"	INTEGER NOT NULL DEFAULT -1,
	"Character_Ring1"	INTEGER NOT NULL DEFAULT -1,
	"Character_Ring2"	INTEGER NOT NULL DEFAULT -1,
	"Character_Trinket1"	INTEGER NOT NULL DEFAULT -1,
	"Character_Trinket2"	INTEGER NOT NULL DEFAULT -1,
	"Character_Item1"	INTEGER NOT NULL DEFAULT -1,
	"Character_Item2"	INTEGER NOT NULL DEFAULT -1,
	"Character_Attack_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Character_Initiative"	INTEGER NOT NULL DEFAULT 0,
	"Character_AC"	INTEGER NOT NULL DEFAULT 0,
	"Character_HP"	INTEGER NOT NULL DEFAULT 0,
	"Character_Max_HP"	INTEGER NOT NULL DEFAULT 0,
	"Character_Alignment"	INTEGER NOT NULL DEFAULT -1,
	"Character_Image"	TEXT NOT NULL DEFAULT 'no_image.png',
	"Character_Resource"	INTEGER NOT NULL DEFAULT 0
);
DROP TABLE IF EXISTS "Inventory";
CREATE TABLE IF NOT EXISTS "Inventory" (
	"Character_ID"	INTEGER NOT NULL,
	"Item_ID"	INTEGER NOT NULL,
	"Amount"	INTEGER NOT NULL DEFAULT 0
);
DROP TABLE IF EXISTS "Slots";
CREATE TABLE IF NOT EXISTS "Slots" (
	"Slots_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Slots_Name"	TEXT NOT NULL UNIQUE,
	"Slots_Equipable"	INTEGER NOT NULL DEFAULT 0
);
DROP TABLE IF EXISTS "Items";
CREATE TABLE IF NOT EXISTS "Items" (
	"Item_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Item_Picture"	TEXT NOT NULL DEFAULT 'no_image.png',
	"Item_Name"	TEXT NOT NULL UNIQUE,
	"Item_Description"	TEXT,
	"Rarity_ID"	INTEGER NOT NULL,
	"Item_Slot"	INTEGER NOT NULL,
	"Item_Weight"	INTEGER NOT NULL DEFAULT 0,
	"Item_Str_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Dex_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Con_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Int_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Wis_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Cha_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Effect1"	INTEGER NOT NULL DEFAULT -1,
	"Item_Effect2"	INTEGER NOT NULL DEFAULT -1,
	"Stackable"	INTEGER NOT NULL DEFAULT 0,
	"Item_Attack_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Initiative_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Health_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_AC_Bonus"	INTEGER NOT NULL DEFAULT 0,
	"Item_Damage_Num_Of_Dices"	INTEGER NOT NULL DEFAULT 0,
	"Item_Damage_Num_Of_Dice_Sides"	INTEGER NOT NULL DEFAULT 0,
	"Wield_Str" INTEGER NOT NULL DEFAULT 0,
	"Wield_Dex" INTEGER NOT NULL DEFAULT 0,
	"Wield_Wis" INTEGER NOT NULL DEFAULT 0,
	"Wield_Int" INTEGER NOT NULL DEFAULT 0,
	"Approved"	INTEGER NOT NULL DEFAULT 0,
	"Item_Magic_Resistance"	INTEGER NOT NULL DEFAULT 0
);
DROP TABLE IF EXISTS "Races";
CREATE TABLE IF NOT EXISTS "Races" (
	"Race_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Race_Name"	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS "Class";
CREATE TABLE IF NOT EXISTS "Class" (
	"Class_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Class_Name"	TEXT NOT NULL UNIQUE
);
DROP TABLE IF EXISTS "Skills";
CREATE TABLE IF NOT EXISTS "Skills" (
	"Skill_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Character_ID"	INTEGER NOT NULL,
	"Skill_Name"	TEXT NOT NULL,
	"Skill_Description"	TEXT NOT NULL
);
DROP TABLE IF EXISTS "Alignments";
CREATE TABLE IF NOT EXISTS "Alignments" (
	"Alignment_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Alignment_Name"	TEXT NOT NULL
);
DROP TABLE IF EXISTS "Item_Skills";
CREATE TABLE IF NOT EXISTS "Item_Skills" (
	"Item_ID"	INTEGER NOT NULL,
	"Skill_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Item_ID")
);
DROP TABLE IF EXISTS "Abilities";
CREATE TABLE IF NOT EXISTS "Abilities" (
	"Ability_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Character_ID"	INTEGER NOT NULL,
	"Ability_Type"	TEXT NOT NULL,
	"Ability_Name"	TEXT NOT NULL,
	"Ability_Description"	TEXT NOT NULL,
	"Ability_Damage"	TEXT DEFAULT ''
);
DROP TABLE IF EXISTS "Notification_Types";
CREATE TABLE IF NOT EXISTS "Notification_Types" (
	"Notification_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Type"	TEXT NOT NULL
);
DROP TABLE IF EXISTS "Users";
CREATE TABLE IF NOT EXISTS "Users" (
	"User_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Username"	TEXT NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL,
	"Is_Admin"	INTEGER NOT NULL DEFAULT 0,
	"Is_Verified"	INTEGER NOT NULL DEFAULT 0,
	"Has_Agreed_TOS"	INTEGER NOT NULL DEFAULT 0
);
DROP TABLE IF EXISTS "Login_Attempts";
CREATE TABLE IF NOT EXISTS "Login_Attempts" (
	"User_ID"	INTEGER NOT NULL UNIQUE,
	"Number_Attempts"	INTEGER NOT NULL DEFAULT 0,
	"Attempt_Year"	INTEGER NOT NULL DEFAULT 0,
	"Attempt_Month"	INTEGER NOT NULL DEFAULT 0,
	"Attempt_Day"	INTEGER NOT NULL DEFAULT 0,
	"Attempt_Hour"	INTEGER NOT NULL DEFAULT 0,
	"Attempt_Minute"	INTEGER NOT NULL DEFAULT 0,
	"Attempt_Second"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("User_ID")
);
DROP TABLE IF EXISTS "Rarities";
CREATE TABLE IF NOT EXISTS "Rarities" (
	"Rarities_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Rarities_Name"	TEXT NOT NULL UNIQUE,
	"Rarities_Color"	TEXT NOT NULL DEFAULT '#000000'
);
DROP TABLE IF EXISTS "Effects";
CREATE TABLE IF NOT EXISTS "Effects" (
	"Effect_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Effect_Name"	TEXT NOT NULL,
	"Effect_Description"	TEXT
);
DROP TABLE IF EXISTS "Site_Notifications";
CREATE TABLE IF NOT EXISTS "Site_Notifications"(
	"Notification_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Note"	TEXT NOT NULL DEFAULT 'NULL'	
);
DROP TABLE IF EXISTS "Users_Security_Questions";
CREATE TABLE IF NOT EXISTS "Users_Security_Questions"(
	"ID"			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"User_ID"		INTEGER NOT NULL,
	"Question_ID"	INTEGER NOT NULL,
	"Answer"		TEXT NOT NULL DEFAULT 'NULL'
	
);
DROP TABLE IF EXISTS "Security_Questions";
CREATE TABLE IF NOT EXISTS "Security_Questions"(
	"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Question"	TEXT NOT NULL DEFAULT 'NULL'
);
INSERT INTO "Slots" VALUES (1,'Head',1);
INSERT INTO "Slots" VALUES (2,'Shoulder',1);
INSERT INTO "Slots" VALUES (3,'Torso',1);
INSERT INTO "Slots" VALUES (4,'Hand',1);
INSERT INTO "Slots" VALUES (5,'Leg',1);
INSERT INTO "Slots" VALUES (6,'Foot',1);
INSERT INTO "Slots" VALUES (7,'Trinket',1);
INSERT INTO "Slots" VALUES (8,'Ring',1);
INSERT INTO "Slots" VALUES (9,'Item',1);
INSERT INTO "Slots" VALUES (10,'Weapon',1);
INSERT INTO "Slots" VALUES (11,'Misc.',0);
INSERT INTO "Alignments" VALUES (1,'Lawful Good');
INSERT INTO "Alignments" VALUES (2,'Lawful Neutral');
INSERT INTO "Alignments" VALUES (3,'Lawful Evil');
INSERT INTO "Alignments" VALUES (4,'Neutral Good');
INSERT INTO "Alignments" VALUES (5,'True Neutral');
INSERT INTO "Alignments" VALUES (6,'Neutral Evil');
INSERT INTO "Alignments" VALUES (7,'Chaotic Good');
INSERT INTO "Alignments" VALUES (8,'Chaotic Neutral');
INSERT INTO "Alignments" VALUES (9,'Chaotic Evil');
INSERT INTO "Rarities" VALUES (1,'Poor','#9d9d9d');
INSERT INTO "Rarities" VALUES (2,'Common','#ffffff');
INSERT INTO "Rarities" VALUES (3,'Uncommon','#1eff00');
INSERT INTO "Rarities" VALUES (4,'Rare','#0070dd');
INSERT INTO "Rarities" VALUES (5,'Epic','#a335ee');
INSERT INTO "Rarities" VALUES (6,'Legendary','#ff8000');
INSERT INTO "Rarities" VALUES (7,'Artifact','#e6cc80');
INSERT INTO "Rarities" VALUES (8,'Heirloom','#00ccff');
INSERT INTO "Notification_Types" VALUES (1,'New User');
INSERT INTO "Notification_Types" VALUES (2,'New Item');
INSERT INTO "Notification_Types" VALUES (3,'Edit Item');
INSERT INTO "Security_Questions" VALUES (1,'What is your favorite number?');
INSERT INTO "Security_Questions" VALUES (2,'What is your favorite word?');
INSERT INTO "Security_Questions" VALUES (3,'What is your favorite book?');
INSERT INTO "Security_Questions" VALUES (4,'What is your favorite movie?');
INSERT INTO "Security_Questions" VALUES (5,'What is your favorite drink?');
INSERT INTO "Security_Questions" VALUES (6,'Who was your favorite teacher?');
INSERT INTO "Security_Questions" VALUES (7,'Who was or is your favorite president?');
INSERT INTO "Security_Questions" VALUES (8,'What did you do during lockdown?');
INSERT INTO "Security_Questions" VALUES (9,'Where were you on the new year of 2022?');
COMMIT;
