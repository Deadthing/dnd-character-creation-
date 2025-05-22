# -------------------------------------------------------------------------------------------------------------------------------
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
                        FORIEGN KEY (user_id) REFERENCES users (id)
                    )
                    """) 
    # Now create Stats Table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS statistics (
                       character_id INTEGER PRIMARY KEY,
                       strength INTEGER NOT NULL, 
                       desterity INTEGER NOT NULL,
                       constitution INTEGER NOT NULL,
                       intelligence INTEGER NOT NULL,
                       wisdom INTEGER NOT NULL,
                       charisma INTEGER NOT NULL,
                       FOREIGN KEY (character_id) REFERENCES characters (id)         
                   )
                   """)   
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    startup_db()
    print("Database setup complete.")
    # The database is now set up and ready to use.
    # You can add more functions here to interact with the database, such as adding users, creating characters, etc.
    # For example:
    # add_user("username", "password")
    # create_character(user_id, "character_name              

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
    Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################