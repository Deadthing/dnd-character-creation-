# -------------------------------------------------------------------------------------------------------------------------------
# Database Initialization
# -------------------------------------------------------------------------------------------------------------------------------
# This script initializes a SQLite database for a character creation application.
# It creates tables for users, characters, and character statistics.
# The database is named 'characterCreate.db'.
# -------------------------------------------------------------------------------------------------------------------------------
import sqlite3

# -------------------------------------------------------------------------------------------------------------------------------
# Function to initialize the database and create necessary tables
def startup_db():
    # Establish or connect to the app database.
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    # Create the table if it doesn't exist.
    cursor.execute(""" DROP TABLE IF EXISTS users """) # Testing purposes, drop the table if it exists to ensure a clean slate
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL UNIQUE,
                       password TEXT 
                    )
                     """)
    # Now create characters table
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS characters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        race TEXT NOT NULL,
                        class TEXT NOT NULL,
                        level INTEGER DEFAULT 1,
                        background TEXT,
                        alignment TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                    """) 
    # Now create Stats Table
    #cursor.execute(""" DROP TABLE IF EXISTS statistics """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS statistics (
                       character_id INTEGER PRIMARY KEY,
                       strength INTEGER, 
                       dexterity INTEGER,
                       constitution INTEGER,
                       intelligence INTEGER,
                       wisdom INTEGER,
                       charisma INTEGER,
                       FOREIGN KEY (character_id) REFERENCES characters (id)         
                   )
                   """)
    # Races Table
    #cursor.execute(""" DROP TABLE IF EXISTS races """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS races (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE,
                   size TEXT,
                   speed INTEGER,
                   description TEXT
                   )
                   """)
    cursor.executemany("INSERT OR IGNORE INTO races (name, size, speed, description) VALUES (?, ?, ?, ?)", [
        ("Dragonborn","Medium", 30, "Dragon Ancestors"),
        ("Dwarf","Medium", 25, "Hardy"),
        ("Elf","Medium", 30, "Graceful"),
        ("Gnome", 'Small', 25, "Genius and Madness"),
        ("Goliath","Medium", 35, "Big"),
        ("Halfling", 'Small', 25, "Lucky"),
        ("Human","Medium", 30, "Versatile"),
        ("Orc","Medium", 30, "Violent and Misunderstood"),
        ("Tiefling","Medium", 30, "Infernal Bloodline, Objectively the coolest"),
    ])
    # Classes Table
    #cursor.execute(""" DROP TABLE IF EXISTS classes """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS classes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE,
                       primarystat TEXT,
                       hitdice TEXT,
                       spellcasting BOOLEAN,
                       description TEXT
                   )
                   """)
    cursor.executemany("INSERT OR IGNORE INTO classes (name, primarystat, hitdice, spellcasting, description) VALUES (?, ?, ?, ?, ?)", [
        ("Barbarian", 'Strength', 'd12', 0, "Fighter, but angrier"),
        ("Bard", 'Charisma', 'd8', 1, "They're not all horny, but a lot of them are horny"),
        ("Cleric", 'Wisdom', 'd8', 1, "Wizards, but their magic comes from a diety"),
        ("Druid", 'Wisdom', 'd8', 1, "Clerics, but feral"),
        ("Fighter", 'Strength or Dexterity', 'd10', 0, "Like it says on the tin"),
        ("Monk", 'Dexterity and Wisdom', 'd8', 0, "Fighter but fists"),
        ("Paladin", 'Strength and Charisma', 'd10', 1, "Fighter and Cleric had a baby, and the child has issues"),
        ("Ranger", 'Dexterity and Wisdom', 'd10', 1, "Cooler than Fighters, but about the same"),
        ("Rogue", 'Dexterity', 'd8', 0, "Fighter, but sneaky, with a tragic backstory"),
        ("Sorcerer", 'Charisma', 'd6', 1, "Jock Wizards"),
        ("Warlock", 'Charisma', 'd8', 1, "Made a deal, now you have powers"),
        ("Wizard", 'Intelligence', 'd6', 1, "Magic nerds"),
    ])
    # Backgrounds Table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS backgrounds (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE,
                       description TEXT
                   )
                   """)
    cursor.executemany("INSERT OR IGNORE INTO backgrounds (name, description) VALUES (?, ?)", [
        ("Acolyte", "Raised in the church"),
        ("Criminal", "Like it says on the tin"),
        ("Sage", "You love to learn"),
        ("Soldier", "Professional Fighter"),
    ])
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS alignments (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE,
                       description TEXT
                       )
                       """)
    cursor.executemany("INSERT OR IGNORE INTO alignments (name, description) VALUES (?, ?)", [
        ("Lawful Good", "Moral absolutist"),
        ("Neutral Good", "Good is more important than law or chaos"),
        ("Chaotic Good", "Generally good, but follows conscience over law"),
        ("Lawful Neutral", "Rules over all"),
        ("True Neutral", "Balance in all things"),
        ("Chaotic Neutral", "It insists upon itself"),
        ("Lawful Evil", "Evil, but with a code"),
        ("Neutral Evil", "Evil, plain and simple"),
        ("Chaotic Evil", "Evil, with crielty and malice"),
        
    ]) 
    # Create Levels Table                 
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS levels (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       level INTEGER NOT NULL UNIQUE,
                       experience INTEGER NOT NULL,
                       proficiency INTEGER NOT NULL
                   )   
                   """)
    # Insert levels, xp, and proficiency bonus
    cursor.executemany("INSERT OR IGNORE INTO levels (level, experience, proficiency) VALUES (?, ?, ?)", [
        (1, 0, 2),
        (2, 300, 2),
        (3, 900, 2),
        (4, 2700, 2),
        (5, 6500, 3),
        (6, 14000, 3),
        (7, 23000, 3),
        (8, 34000, 3),
        (9, 48000, 4),
        (10, 64000, 4),
        (11, 85000, 4),
        (12, 100000, 4),
        (13, 120000, 5),
        (14, 140000, 5),
        (15, 165000, 5),
        (16, 195000, 5),
        (17, 225000, 6),
        (18, 265000, 6),
        (19, 305000, 6),
        (20, 355000, 6)
    ])              
    conn.commit()
    conn.close()

#Function to add a new user
def add_user(username, password):
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO users (username, password)
                   VALUES (?, ?)
                   """, (username, password))
    user_id = cursor.lastrowid #this was a copilot suggestion here, returning the uid, but I liked the the idea
    conn.commit()
    conn.close()
    return user_id


# Function to add a new character under an existing user
def add_character(user_id, name, race, char_class, level = 1, background = None, alignment = None):
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO characters (user_id, name, race, class, level, background, alignment)
                   VALUES (?, ?, ?, ?, ?, ?, ?) """, 
                   (user_id, name, race, char_class, level, background, alignment))
    
    char_id = cursor.lastrowid #this was a copilot suggestion here, returning the uid, but I liked the the idea
    conn.commit()
    conn.close()
    return char_id
      
                    
# Function to add statistics for a character
def add_stats(char_id, strength, dexterity, constitution, intelligence, wisdom, charisma):
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO statistics (character_id, strength, dexterity, constitution, intelligence, wisdom, charisma)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (char_id, strength, dexterity, constitution, intelligence, wisdom, charisma))
    conn.commit()
    conn.close()
    return True

# Clear Tables for testing purposes
def clear_tables():
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM characters")
    cursor.execute("DELETE FROM statistics")
    
    # sqlite tracks autoincrement seprately so: also clear the autoincrement counters
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='users'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='characters'")   
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='statistics'")   
    conn.commit()
    conn.close()
    
# Function to print the tables in a readable fasion

def print_tables():
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    
    # Print users
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    
    #Print message if no users
    if len(users) == 0:
        print("No users found.\n")
        conn.close()
        return
    
    print("======USERS TABLE======")
    # Print each user
    for user in users:
        user_id = user[0]
        username = user[1]
        print(f"User: {username} (ID: {user_id})")
        print("------")
    # Print characters
        print("======CHARACTER TABLES======")
    
        cursor.execute("""SELECT id, name, race, class, level, background, alignment 
                   FROM characters
                   WHERE user_id = ?""", (user_id,))
        characters = cursor.fetchall()
    
    #Print message if no characters
        if len(characters) == 0:
            print("No characters found for this user.\n")
            conn.close()
            return
        else:
        # Print each character
            for character in characters:
                char_id = character[0]
                name = character[1]
                race = character[2]
                char_class = character[3]
                level = character[4]
                background = character[5]
                alignment = character[6]
                
                print(f" Character: {name} (ID: {char_id})")
                print(f" Race: {race}")
                print(f" Class: {char_class}")
                print(f" Level: {level}")
                print(f" Background: {background}")
                print(f" Alignment: {alignment}")
                print("------")
            
                # Print statistics
                print("======STATISTICS TABLE======")
                        
                cursor.execute("""SELECT strength, dexterity, constitution, intelligence, wisdom, charisma
                                    FROM statistics
                                    WHERE character_id = ?""", (char_id,))
                stats = cursor.fetchone()
                if stats is None:
                    print("No statistics found for this character.\n")
                else:
                    strength = stats[0]
                    dexterity = stats[1]
                    constitution = stats[2]
                    intelligence = stats[3]
                    wisdom = stats[4]
                    charisma = stats[5]
                            
                    print(f" Stats:")
                    print(f" Strength: {strength}")
                    print(f" Dexterity: {dexterity}")
                    print(f" Constitution: {constitution}")
                    print(f" Intelligence: {intelligence}")
                    print(f" Wisdom: {wisdom}")
                    print(f" Charisma: {charisma}")
                    conn.close()
            print("====================================\n")

    
#################################################################################################################################
# Gluonix Runtime
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
if __name__=='__main__':
    from Nucleon.Runner import * ###!REQUIRED ------- Any Script Before This Won't Effect GUI Elements
#################################################################################################################################
#################################################################################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming Start
# -------------------------------------------------------------------------------------------------------------------------------
#Testing the database functions ===========================
# clear_tables()
# startup_db()
# creating a varible to store the user_id awkwardly because other way to fix this are getting ahead of myself
#user_id = add_user("Wizard", "itsboss")
# char_id = add_character(user_id, "Red", "Human", "Wizard", level = 1, background = "Sage", alignment = "Lawful Evil")
# add_stats(char_id, 10, 12, 14, 16, 18, 20)
# print(f" DEBUG About to fetch stats for character ID: {char_id}, type = {type(char_id)}")
# print_tables()
# Testing ============================================================
startup_db()

conn = sqlite3.connect('characterCreate.db')
cursor = conn.cursor()

# Populate Race Select Menu
cursor.execute("SELECT name FROM races")
for row in cursor.fetchall():
    Root.Frame1.RaceSelect.Add(row[0])
    
# Populate Class Select Menu
cursor.execute("SELECT name FROM classes")
for row in cursor.fetchall():
    Root.Frame1.ClassSelect.Add(row[0])

# Populate Background Select Menu

cursor.execute("SELECT name FROM backgrounds")
for row in cursor.fetchall():
    Root.Frame1.BackgroundSelect.Add(row[0])
    
# Populate Alignment Select Menu
cursor.execute("SELECT name FROM alignments")
for row in cursor.fetchall():
    Root.Frame1.AlignmentSelect.Add(row[0])
    
conn.close()

def SaveChar(event=None):
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    
    # Grab Username, print message if empty
    username = Root.Frame4.userentry.Get().strip()

    if not username:
        Root.Frame3.readout.Set("Username required to save character")
        return
    
    # Find or Create User
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    else:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user_id = cursor.lastrowid
    
    # Get Character Info from fields
    charname = Root.Frame1.NameEntry.Get().strip()
    charrace = Root.Frame1.RaceSelect.Get()
    charclass = Root.Frame1.ClassSelect.Get()
    charbackground = Root.Frame1.BackgroundSelect.Get()
    charalignment = Root.Frame1.AlignmentSelect.Get()
    
    #Check empty fields
    if not charname or not charrace or not charclass:
        Root.Frame3.readout.Set("Please enter at least a name, race, and class")
        return
    
    # Add Character to Database
    cursor.execute("""
                   INSERT INTO characters (user_id, name, race, class, background, alignment) VALUES (?, ?, ?, ?, ?, ?)""",
                   (user_id, charname, charrace, charclass, charbackground, charalignment
                ))
    conn.commit()
    character_id = cursor.lastrowid
    # Get stats if entered
    
    try:
        stats = (
            int(Root.Frame2.strentry.Get().strip()),
            int(Root.Frame2.dexentry.Get().strip()),
            int(Root.Frame2.conentry.Get().strip()),
            int(Root.Frame2.intentry.Get().strip()),
            int(Root.Frame2.wisentry.Get().strip()),
            int(Root.Frame2.chaentry.Get().strip())
        )
    except ValueError:
        Root.Frame3.readout.Set("Stats must be numbers")
        conn.close()    
        return
    # Add stats to database
    cursor.execute("""
                   INSERT INTO statistics (character_id, strength, dexterity, constitution, intelligence, wisdom, charisma)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (character_id, *stats))
    conn.commit()
    
    Root.Frame3.readout.Set("Character saved\n")
    conn.close()
    
    SavedReadout(character_id)  # Call to display the saved character readout

def SavedReadout(character_id):
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    
    # Fetch character info
    cursor.execute("""
                   SELECT name, race, class, level, background, alignment FROM characters WHERE id = ?
                   """, (character_id,))
    character = cursor.fetchone()
    
    if not character:
        Root.Frame3.readout.Set("Character not found")
        conn.close()
        return
    
    name, race, char_class, level, bacground, alignment = character
    
    # Fetch stats
    cursor.execute("""
                   SELECT strength, dexterity, constitution, intelligence, wisdom, charisma FROM statistics WHERE character_id = ?
                   """, (character_id,))
    stats = cursor.fetchone()
    
    conn.close()
    
    if stats:
        strength, dexterity, constitution, intelligence, wisdom, charisma = stats
        printout = (
            f"Character: {name}\n"
            f"Race: {race}\n"
            f"Class: {char_class}\n"
            f"Level: {level}\n"
            f"Background: {bacground}\n"
            f"Alignment: {alignment}\n"
            f"------Statistics------\n"
            f"Strength: {strength}  Dexterity: {dexterity}  Constitution: {constitution}\n"
            f"Intelligence: {intelligence}  Wisdom: {wisdom}  Charisma: {charisma}"
        )
    else:
        printout = (f"Character: {name} has no stats!")
    
    Root.Frame3.readout.Set(printout)
            


def testbutton(event=None):
    Root.Frame3.readout.Set("Test button clicked")  
    print("Test button clicked")
    

# Bind Save Button
Root.Frame4.save.Bind(On_Click=SaveChar)
    
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################
