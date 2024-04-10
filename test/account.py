# 在control mode里面
# 0 代表是keyboard
# 1 代表是mouse

import mysql.connector

#新建用户
def insert_account(username, password):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )
        cursor = conn.cursor()
        query = "INSERT INTO User (username, password,highest_score,music,volume,Cust1,Cust2,Cust3,Cust4,Curren_Cust,balance,e_volume, control_mode) VALUES (%s,%s,0,0,0.5,1,0,0,0,1,0,0.5,0)"
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


#更新最高分
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
#应该没用
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
#应该没用
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

#查找是否存在改用户
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
        


#输出排名表
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

#应该没用
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




#应该没用
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
        
#换数据库里的装
def change_cust(username, custn):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()
        custn = int(custn)  # 将 custn 转换为整数
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




#换数据库里的音乐
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
#换数据库里的音乐音量
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
#换数据库里的effect音量
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
        


#输出现有的用户条
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
#改数据库里的control mode
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
        

import mysql.connector

def export_user_data(username):
    try:
        conn = mysql.connector.connect(
            host="10.13.79.93",
            user="CSCI3100",
            password="CSCI3100",
            database="CSCI3100"
        )

        cursor = conn.cursor()

        query = "SELECT * FROM User WHERE username = %s"
        data = (username,)
        cursor.execute(query, data)

        result = cursor.fetchone()

        if result:
            # 将结果存储到一个字典中
            user_data = {
                "username": result[0],
                "password": result[1],
                "highest_score": result[2],
                "music": result[3],
                "volume": result[4],
                "Cust1": result[5],
                "Cust2": result[6],
                "Cust3": result[7],
                "Cust4": result[8],
                "Curren_Cust": result[9],
                "balance": result[10],
                "e_volume": result[11],
                "control_mode": result[12]
            }

            # 将用户数据写入文件
            with open(f"{username}_data.txt", "w") as file:
                for key, value in user_data.items():
                    file.write(f"{key}: {value}\n")

            print(f"User data for {username} has been exported successfully.")
        else:
            print(f"No user found with username {username}.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as error:
        print("Failed to connect to the database", error)

# 调用函数,导出用户名为 "111" 的数据
export_user_data("111")

        

export_user_data("111")
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


