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

def ShowLogin(Root, Create_Popup):
    Popup1 = Create_Popup("Popup1")
    Popup1.Show()
    Root.Disable()
    
    def LoginOrRegister(event = None):
        username = Popup1.usernamefield.Get().strip()
        password = Popup1.passwordfield.Get().strip()
        
        if not username:
            Popup1.loginlabel.Set("Username cannot be empty.")
            return

        try:
            conn = sqlite3.connect("characterCreate.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                UserID, CurrentPass = result
                if CurrentPass:
                    if password == CurrentPass:
                        #user defined a password and it matched
                        Root.CurrentUserID = UserID
                        Popup1.Hide()
                        Root.Enable()
                        Root.Show()
                    else:
                        # Password mismatch
                        Popup1.loginlabel.Set("Incorrect password.")
                else:
                    # No password set
                    Root.CurrentUserID = UserID
                    Popup1.Hide()
                    Root.Enable()
                    Root.Show()
            else:
                # User does not exist, create new user
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                UserID = cursor.lastrowid
                Root.CurrentUserID = UserID
                Popup1.Hide()
                Root.Enable()
                Root.Show()
            conn.close()
        except sqlite3.Error as e:
            Popup1.loginlabel.Set(f"Database error: {e}")
    Popup1.loginbutton.Bind(On_Click=LoginOrRegister)
    Popup1.Bind(On_Key_Press=LoginOrRegister, Key="Return")   #Auto suggested by Copilot, seemed like a good idea cause honestly I didnt even think of it

# -------------------------------------------------------------------------------------------------------------------------------
# Developer Programming End
# -------------------------------------------------------------------------------------------------------------------------------
#################################################################################################################################
#################################################################################################################################
   # Root.Start() ###!REQUIRED ------- Any Script After This Will Not Execute
#################################################################################################################################