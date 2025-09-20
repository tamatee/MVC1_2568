import csv
import os

class UserManager:
    @staticmethod
    def getAllUsers():
        users = []
        try:
            with open(r'Model/data/UsersWithPassword.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    users.append({
                        'user_id': row['user_id'],
                        'username': row['username'],
                        'email': row['email'],
                        'password': row['password']  # ในการใช้งานจริงไม่ควรส่ง password ออกมา
                    })
        except Exception as e:
            print(f"Error loading users: {e}")
        return users

    @staticmethod
    def getUserById(user_id):
        try:
            with open(r'Model/data/UsersWithPassword.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['user_id'] == str(user_id):
                        return {
                            'user_id': row['user_id'],
                            'username': row['username'],
                            'email': row['email']
                        }
        except Exception as e:
            print(f"Error finding user: {e}")
        return None

    @staticmethod
    def getUserByUsername(username):
        try:
            with open(r'Model/data/UsersWithPassword.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['username'].lower() == username.lower():
                        return {
                            'user_id': row['user_id'],
                            'username': row['username'],
                            'email': row['email']
                        }
        except Exception as e:
            print(f"Error finding user: {e}")
        return None

    @staticmethod
    def addUser(username, email, password):
        try:
            # หา user_id ใหม่
            existing_users = UserManager.getAllUsers()
            if existing_users:
                max_id = max(int(user['user_id']) for user in existing_users)
                new_id = max_id + 1
            else:
                new_id = 1

            # อ่านข้อมูลเก่า
            existing_data = []
            if os.path.exists(r'Model/data/UsersWithPassword.csv'):
                with open(r'Model/data/UsersWithPassword.csv', 'r', newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    existing_data = list(reader)

            # เพิ่มข้อมูลใหม่
            existing_data.append({
                'user_id': str(new_id),
                'username': username,
                'email': email,
                'password': password
            })

            # เขียนกลับไฟล์
            with open(r'Model/data/UsersWithPassword.csv', 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ['user_id', 'username', 'email', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_data)

            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    @staticmethod
    def updateUser(user_id, username=None, email=None, password=None):
        try:
            # อ่านข้อมูลเก่า
            existing_data = []
            with open(r'Model/data/UsersWithPassword.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                existing_data = list(reader)

            # อัปเดตข้อมูล
            for user in existing_data:
                if user['user_id'] == str(user_id):
                    if username:
                        user['username'] = username
                    if email:
                        user['email'] = email
                    if password:
                        user['password'] = password
                    break

            # เขียนกลับไฟล์
            with open(r'Model/data/UsersWithPassword.csv', 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ['user_id', 'username', 'email', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_data)

            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def deleteUser(user_id):
        """ลบ user"""
        try:
            # อ่านข้อมูลเก่า
            existing_data = []
            with open(r'Model/data/UsersWithPassword.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                existing_data = list(reader)

            # ลบ user
            existing_data = [user for user in existing_data if user['user_id'] != str(user_id)]

            # เขียนกลับไฟล์
            with open(r'Model/data/UsersWithPassword.csv', 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ['user_id', 'username', 'email', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_data)

            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    @staticmethod
    def isAdmin(user_info):
        if not user_info:
            return False
        return user_info.get('username', '').lower() == 'admin'