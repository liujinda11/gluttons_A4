import mysql.connector


class DatabaseConnection:
    HOST = "10.13.79.93"
    USER = "CSCI3100"
    PASSWORD = "CSCI3100"
    DATABASE = "CSCI3100"

    @staticmethod
    def connect():
        try:
            return mysql.connector.connect(
                host=DatabaseConnection.HOST,
                user=DatabaseConnection.USER,
                password=DatabaseConnection.PASSWORD,
                database=DatabaseConnection.DATABASE
            )
        except mysql.connector.Error as error:
            print("Database connection failed:", error)
            return None


class Account:
    def __init__(self, username):
        self.username = username

    def execute_query(self, query, data, fetch=False):
        conn = DatabaseConnection.connect()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(query, data)
                if fetch:
                    result = cursor.fetchall()
                    return result
                else:
                    conn.commit()
                    return True
            except mysql.connector.Error as error:
                print("Query execution failed:", error)
                return False
            finally:
                cursor.close()
                conn.close()
        return False

    def insert_account(self, password):
        query = """INSERT INTO User (username, password, highest_score, music, volume, Cust1, Cust2, Cust3, Cust4,
                   Current_Cust, balance, e_volume, control_mode) VALUES (%s, %s, 0, 0, 0.5, 1, 0, 0, 0, 1, 0, 0.5, 0)"""
        return self.execute_query(query, (self.username, password))

    def update_score(self, score):
        query = "UPDATE User SET highest_score = %s WHERE username = %s"
        return self.execute_query(query, (score, self.username))

    def adjust_balance(self, amount, operation='add'):
        if operation == 'add':
            query = "UPDATE User SET balance = balance + %s WHERE username = %s"
        else:  # assume 'reduce'
            query = "UPDATE User SET balance = balance - %s WHERE username = %s"
        return self.execute_query(query, (amount, self.username))

    def authenticate_user(self, password):
        query = "SELECT COUNT(*) FROM User WHERE username = %s AND password = %s"
        result = self.execute_query(query, (self.username, password), fetch=True)
        if result:
            return result[0][0] > 0
        return False

    def get_ranking(self):
        query = """SELECT username, highest_score, ROW_NUMBER() OVER (ORDER BY highest_score DESC) AS ranking
                   FROM User ORDER BY highest_score DESC"""
        results = self.execute_query(query, (), fetch=True)
        if results:
            # 如果需要在外部处理数据，可以返回整个结果集
            return results
        return False

    def check_customization(self, customization):
        query = f"SELECT COUNT(*) FROM User WHERE {customization} = 1 AND username = %s"
        result = self.execute_query(query, (self.username,), fetch=True)
        if result:
            return result[0][0] > 0
        return False

    def activate_customization(self, customization):
        query = f"UPDATE User SET {customization} = 1 WHERE username = %s"
        return self.execute_query(query, (self.username,))

    def update_current_customization(self, customization_id):
        query = "UPDATE User SET Current_Cust = %s WHERE username = %s"
        return self.execute_query(query, (customization_id, self.username))

    def update_music(self, music_setting):
        query = "UPDATE User SET music = %s WHERE username = %s"
        return self.execute_query(query, (music_setting, self.username))

    def update_volume(self, volume_level):
        query = "UPDATE User SET volume = %s WHERE username = %s"
        return self.execute_query(query, (volume_level, self.username))

    def get_current_state(self):
        query = "SELECT * FROM User WHERE username = %s"
        result = self.execute_query(query, (self.username,), fetch=True)
        if result:
            return result[0]
        return False

    def change_control_mode(self, control_mode):
        query = "UPDATE User SET control_mode = %s WHERE username = %s"
        return self.execute_query(query, (control_mode, self.username))
