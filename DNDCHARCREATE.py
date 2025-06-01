# -------------------------------------------------------------------------------------------------------------------------------
# Database Initialization
# -------------------------------------------------------------------------------------------------------------------------------
# This script initializes a SQLite database for a character creation application.
# It creates tables for users, characters, and character statistics.
# The database is named 'characterCreate.db'.
# -------------------------------------------------------------------------------------------------------------------------------
import sqlite3

def startup_db():
    # Establish or connect to the app database.
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    # Create the table if it doesn't exist.
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL UNIQUE,
                       password TEXT NOT NULL
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
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS statistics (
                       character_id INTEGER PRIMARY KEY,
                       strength INTEGER NOT NULL, 
                       dexterity INTEGER NOT NULL,
                       constitution INTEGER NOT NULL,
                       intelligence INTEGER NOT NULL,
                       wisdom INTEGER NOT NULL,
                       charisma INTEGER NOT NULL,
                       FOREIGN KEY (character_id) REFERENCES characters (id)         
                   )
                   """)
    # Races Table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS races (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL UNIQUE,
                   description TEXT
                   )
                   """)
    cursor.executemany("INSERT OR IGNORE INTO races (name, description) VALUES (?, ?)", [
        ("Dragonborn", "Dragon Ancestors"),
        ("Dwarf", "Hardy"),
        ("Elf", "Graceful"),
        ("Gnome", "Genius and Madness"),
        ("Goliath", "Big"),
        ("Halfling", "Lucky"),
        ("Human", "Versatile"),
        ("Orc", "Violent and Misunderstood"),
        ("Tiefling", "Infernal Bloodline, Objectively the coolest"),
    ])
    # Classes Table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS classes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE,
                       description TEXT
                   )
                   """)
    cursor.executemany("INSERT OR IGNORE INTO classes (name, description) VALUES (?, ?)", [
        ("Barbarian", "Fighter, but angrier"),
        ("Bard", "They're not all horny, but a lot of them are horny"),
        ("Cleric", "Wizards, but their magic comes from a diety"),
        ("Druid", "Clerics, but feral"),
        ("Fighter", "Like it says on the tin"),
        ("Monk", "Fighter but fists"),
        ("Paladin", "Fighter and Cleric had a baby, and the child has issues"),
        ("Ranger", "Cooler than Fighters, but about the same"),
        ("Rogue", "Fighter, but sneaky, with a tragic backstory"),
        ("Sorcerer", "Jock Wizards"),
        ("Warlock", "Made a deal, now you have powers"),
        ("Wizard", "Magic nerds"),
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







conn.close()
# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################