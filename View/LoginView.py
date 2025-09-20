from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
import csv

class LoginView(QWidget):
    # Signal เมื่อล็อกอินสำเร็จ
    login_successful = pyqtSignal(dict)  # ส่งข้อมูล user ที่ล็อกอิน

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - CS Camp Crowdfunding")
        self.setGeometry(400, 400, 350, 250)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)

        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(20)
        mainLayout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("CS Camp Crowdfunding")
        title.setStyleSheet("""
            font-weight: bold; 
            font-size: 20px; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(title)

        subtitle = QLabel("Please login to continue")
        subtitle.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 20px;")
        subtitle.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(subtitle)

        # Login Form
        formLayout = QFormLayout()
        formLayout.setSpacing(15)

        # Username
        self.usernameEdit = QLineEdit()
        self.usernameEdit.setPlaceholderText("Enter your username")
        self.usernameEdit.setStyleSheet("""
            padding: 8px; 
            border: 2px solid #bdc3c7; 
            border-radius: 5px;
            font-size: 14px;
        """)
        self.usernameEdit.returnPressed.connect(self.login)
        formLayout.addRow("Username:", self.usernameEdit)

        # Password
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("Enter 4-digit password")
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setMaxLength(4)
        self.passwordEdit.setStyleSheet("""
            padding: 8px; 
            border: 2px solid #bdc3c7; 
            border-radius: 5px;
            font-size: 14px;
        """)
        self.passwordEdit.returnPressed.connect(self.login)
        formLayout.addRow("Password:", self.passwordEdit)

        mainLayout.addLayout(formLayout)

        # Login Button
        self.loginButton = QPushButton("Login")
        self.loginButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.loginButton.clicked.connect(self.login)
        mainLayout.addWidget(self.loginButton)

        # Demo Info
        demoLabel = QLabel("Demo Users: alice (1111), bob (2222), charlie (3333)")
        demoLabel.setStyleSheet("""
            font-size: 11px; 
            color: #95a5a6; 
            margin-top: 15px;
            padding: 8px;
            background-color: #ecf0f1;
            border-radius: 3px;
        """)
        demoLabel.setAlignment(Qt.AlignCenter)
        demoLabel.setWordWrap(True)
        mainLayout.addWidget(demoLabel)

        self.setLayout(mainLayout)

        # Focus on username field
        self.usernameEdit.setFocus()

    def login(self):
        username = self.usernameEdit.text().strip().lower()
        password = self.passwordEdit.text().strip()

        # Validate input
        if not username:
            QMessageBox.warning(self, "Error", "Please enter username!")
            self.usernameEdit.setFocus()
            return

        if not password:
            QMessageBox.warning(self, "Error", "Please enter password!")
            self.passwordEdit.setFocus()
            return

        if len(password) != 4 or not password.isdigit():
            QMessageBox.warning(self, "Error", "Password must be exactly 4 digits!")
            self.passwordEdit.clear()
            self.passwordEdit.setFocus()
            return

        # Check credentials
        user_info = self.authenticate(username, password)

        if user_info:
            QMessageBox.information(self, "Success", f"Welcome, {user_info['username']}!")
            self.login_successful.emit(user_info)
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password!")
            self.passwordEdit.clear()
            self.usernameEdit.setFocus()

    def authenticate(self, username, password):
        """
        ตรวจสอบ username และ password
        ในการใช้งานจริงควรใช้ฐานข้อมูลและเข้ารหัสรหัสผ่าน
        """
        # สำหรับ demo - password คือ user_id ซ้ำ 4 ครั้ง (เช่น user_id 1 = password 1111)
        demo_users = {
            'alice': {'user_id': '1', 'password': '1111'},
            'bob': {'user_id': '2', 'password': '2222'},
            'charlie': {'user_id': '3', 'password': '3333'},
            'diana': {'user_id': '4', 'password': '4444'},
            'edward': {'user_id': '5', 'password': '5555'},
            'fiona': {'user_id': '6', 'password': '6666'},
            'george': {'user_id': '7', 'password': '7777'},
            'helen': {'user_id': '8', 'password': '8888'},
            'ian': {'user_id': '9', 'password': '9999'},
            'jane': {'user_id': '10', 'password': '1010'}
        }

        # ตรวจสอบใน demo users ก่อน
        if username in demo_users:
            demo_user = demo_users[username]
            if password == demo_user['password']:
                return {
                    'user_id': demo_user['user_id'],
                    'username': username.capitalize(),
                    'email': f"{username}@example.com"
                }

        # ตรวจสอบในไฟล์ CSV (สำหรับกรณีที่มีผู้ใช้เพิ่มเติม)
        try:
            with open(r'Data/User.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['username'].lower() == username:
                        # ใช้ user_id ซ้ำ 4 ครั้งเป็น password (เช่น user_id 11 = password 1111)
                        expected_password = row['user_id'] * 4
                        if len(expected_password) > 4:
                            expected_password = row['user_id'].zfill(2) * 2  # เช่น 01 -> 0101

                        if password == expected_password:
                            return {
                                'user_id': row['user_id'],
                                'username': row['username'],
                                'email': row['email']
                            }
        except Exception as e:
            print(f"Error reading user file: {e}")

        return None