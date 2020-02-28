BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Admin_Notifications";
CREATE TABLE IF NOT EXISTS "Admin_Notifications" (
	"Note_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"User_ID"	INTEGER NOT NULL,
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
	"Character_Image"	TEXT NOT NULL DEFAULT 'no_image.png'
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
	"Item_Damage_Num_Of_Dice_Sides"	INTEGER NOT NULL DEFAULT 0
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
	"Skill_Name"	TEXT NOT NULL,
	"Skill_Base_Value"	INTEGER NOT NULL DEFAULT 0,
	"Skill_Type"	TEXT NOT NULL
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
DROP TABLE IF EXISTS "Character_Skills";
CREATE TABLE IF NOT EXISTS "Character_Skills" (
	"Character_ID"	INTEGER NOT NULL,
	"Skill_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Character_ID")
);
DROP TABLE IF EXISTS "Character_Abilites";
CREATE TABLE IF NOT EXISTS "Character_Abilites" (
	"Character_ID"	INTEGER NOT NULL,
	"Ability_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Character_ID")
);
DROP TABLE IF EXISTS "Abilities";
CREATE TABLE IF NOT EXISTS "Abilities" (
	"Ability_ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"Ability_Type"	INTEGER NOT NULL DEFAULT 0,
	"Ability_Name"	TEXT NOT NULL,
	"Ability_Description"	TEXT NOT NULL
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
INSERT INTO "Skills" VALUES (1,'Athletics',0,'Strength');
INSERT INTO "Skills" VALUES (2,'Acrobatics',0,'Dexterity');
INSERT INTO "Skills" VALUES (3,'Sleight of Hand',0,'Dexterity');
INSERT INTO "Skills" VALUES (4,'Stealth',0,'Dexterity');
INSERT INTO "Skills" VALUES (5,'Arcana',0,'Intelligence');
INSERT INTO "Skills" VALUES (6,'History',0,'Intelligence');
INSERT INTO "Skills" VALUES (7,'Investigation',0,'Intelligence');
INSERT INTO "Skills" VALUES (8,'Nature',0,'Intelligence');
INSERT INTO "Skills" VALUES (9,'Religion',0,'Intelligence');
INSERT INTO "Skills" VALUES (10,'Animal Handling',0,'Wisdom');
INSERT INTO "Skills" VALUES (11,'Insight',0,'Wisdom');
INSERT INTO "Skills" VALUES (12,'Medicine',0,'Wisdom');
INSERT INTO "Skills" VALUES (13,'Perception',0,'Wisdom');
INSERT INTO "Skills" VALUES (14,'Survival',0,'Wisdom');
INSERT INTO "Skills" VALUES (15,'Deception',0,'Charisma');
INSERT INTO "Skills" VALUES (16,'Intimidation',0,'Charisma');
INSERT INTO "Skills" VALUES (17,'Performance',0,'Charisma');
INSERT INTO "Skills" VALUES (18,'Persuasion',0,'Charisma');
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
COMMIT;
