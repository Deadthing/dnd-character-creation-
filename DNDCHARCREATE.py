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
def add_stats(character_id, strength, dexterity, constitution, intelligence, wisdom, charisma):
    conn = sqlite3.connect('characterCreate.db')
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO statistics (character_id, strength, dexterity, constitution, intelligence, wisdom, charisma)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (character_id, strength, dexterity, constitution, intelligence, wisdom, charisma))
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
    if not users:
        print("No users found.")
        conn.close()
        return
    print("======CHARACTER CREATION TABLES======")
    
    # 
    conn.close()
    
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

#Testing the database functions
print_tables()

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################