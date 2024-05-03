# In control mode
# 0 means keyboard
# 1 means mouse

import mysql.connector

#insert the information of a new user into database
def insert_account(username, password):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )
        cursor = conn.cursor()
        query = "INSERT INTO User (username, password,highest_score,music,volume,Cust1,Cust2,Cust3,Cust4,Curren_Cust,balance,e_volume, control_mode) VALUES (%s,%s,0,0,0.5,1,0,0,0,0,0,0.5,0)"
        data = (username, password)
        cursor.execute(query, data)

        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False


#update the highest score in the database
def update_score(username,update_value):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        
        query = "UPDATE User SET highest_score = %s WHERE username = %s"
        data = (update_value,username)
        cursor.execute(query, data)

        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
#may be useless
def add_balance(username,update_value):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )
        cursor = conn.cursor()

        query = "UPDATE User SET balance += %s WHERE username = %s"
        data = (update_value,username)
        cursor.execute(query, data)

        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
#may be useless
def reduce_balance(username,update_value):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
    
        query = "UPDATE User SET balance -= %s WHERE username = %s"
        data = (update_value,username)
        cursor.execute(query, data)

        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False

#test whether the information of a user is in databse
def match_user_information(username,password):
        

    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()

        query = "SELECT COUNT(*) AS count FROM User WHERE username = %s AND password = %s"
        data = (username,password)
        cursor.execute(query, data)
        
        result = cursor.fetchone()[0]

       

        cursor.close()
        conn.close()
        if result > 0:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        


#get the username, highest_score and ranking from the database
def get_ranking():
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()

        query = "SELECT username, highest_score, ROW_NUMBER() OVER (ORDER BY highest_score DESC) AS Ranking FROM User ORDER BY highest_score DESC"
            
        cursor.execute(query)
            
        results = cursor.fetchall()
    
       

        cursor.close()
        conn.close()
           # print("username\thighest_score\tranking")
        
        return results
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False

#may be useless
def get_customization(username,custn):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        custn = int(custn)
        if custn == 1:
            query = "SELECT COUNT(*) AS count FROM User WHERE Cust1 = 1 AND username = %s"
        if custn == 2:
            query = "SELECT COUNT(*) AS count FROM User WHERE Cust2 = 1 AND username = %s"
        if custn == 3:
            query = "SELECT COUNT(*) AS count FROM User WHERE Cust3 = 1 AND username = %s"
        if custn == 4:
            query = "SELECT COUNT(*) AS count FROM User WHERE Cust4 = 1 AND username = %s"
        data = (update_value,username)
        cursor.execute(query, data)

        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False



#may be useless
def if_has_customization(username,custn):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        custn = int(custn)
    
        if custn == 1:
            query = "UPDATE User SET Cust1 = 1 WHERE username = %s"
        if custn == 2:
            query = "UPDATE User SET Cust2 = 1 WHERE username = %s"
        if custn == 3:
            query = "UPDATE User SET Cust3 = 1 WHERE username = %s"
        if custn == 4:
            query = "UPDATE User SET Cust4 = 1 WHERE username = %s"
        
        data = (username,)
        cursor.execute(query, data)

        result = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        if result>0 :
            # print("having the customization")
            return True
        else:
            # print("not having")
            return False
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        
#change the customization of a user in database(in the shop)
def change_cust(username, custn):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        custn = int(custn)  # change cust to int
        query = "UPDATE User SET Curren_Cust = %s WHERE username = %s"
        data = (custn, username)
        cursor.execute(query, data)
        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False




#chang the music in the database(in the setting)
def change_music(username, music):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()

        music = int(music)
        query = "UPDATE User SET music = %s WHERE username = %s"
        data = (music,username)
        cursor.execute(query, data)

        conn.commit()

        cursor.close()
        conn.close()
        
        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
#change the music volume in database(in the setting)
def change_volume(username, change_volume):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        
        
        query = "UPDATE User SET volume = %s WHERE username = %s"
        data = (change_volume,username)
        cursor.execute(query, data)
        
        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
#change the effect volume in database(in the setting)
def change_evolume(username, change_volume):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        
        
        query = "UPDATE User SET e_volume = %s WHERE username = %s"
        data = (change_volume,username)
        cursor.execute(query, data)
        
        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
        


#get all information of a user in database
def current_state(username):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM User WHERE username = %s"
        data =(username,)
            
        cursor.execute(query,data)
            
        result = cursor.fetchone()
    
       

        cursor.close()
        conn.close()
          
        return result
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
#change the control mode in database
def change_cmode(username, control):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        
        
        query = "UPDATE User SET control_mode = %s WHERE username = %s"
        data = (control,username)
        cursor.execute(query, data)
        
        conn.commit()

        cursor.close()
        conn.close()

        print("Successfully!")
        return True
    except mysql.connector.Error as error:
        print("Failed to connect the database", error)
        return False
        

#for test below

#change_evolume('user1',0.5)
#v= get_ranking()
#print("user\thighest_score\tranking")
#for _ in v:
   # print(_[0],"\t",_[1],"\t\t",_[2])
#print(v)

#update_score('user1',10)
#print(current_state('user1'))
#print(get_ranking())


#change_music('user1',0)
