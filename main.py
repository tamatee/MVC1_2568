from PyQt5.QtWidgets import QApplication
from View.LoginView import LoginView
from View.AdminConsole import MainWindow
from View.UserPledgeView import UserPledgeView
from Model.UserManager import UserManager
import sys

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_user = None
        self.main_window = None
        self.login_window = None
        self.user_pledge_window = None

        # เริ่มต้นด้วยหน้า login
        self.showLogin()

    def showLogin(self):
        """แสดงหน้า login"""
        self.login_window = LoginView()
        self.login_window.login_successful.connect(self.onLoginSuccess)
        self.login_window.show()

    def onLoginSuccess(self, user_info):
        """เมื่อ login สำเร็จ"""
        self.current_user = user_info

        # ปิดหน้า login
        if self.login_window:
            self.login_window.close()

        # แสดงหน้าที่เหมาะสมตาม user type
        if UserManager.isAdmin(user_info):
            # Admin เห็นหน้า main menu ปกติ
            self.showMainWindow()
        else:
            # User ทั่วไป เห็นแค่ pledge ของตัวเอง
            self.showUserPledgeView()

    def showMainWindow(self):
        """แสดงหน้า main menu (สำหรับ admin)"""
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()

    def showUserPledgeView(self):
        """แสดงหน้า pledge ของ user"""
        self.user_pledge_window = UserPledgeView(self.current_user)
        self.user_pledge_window.show()

    def run(self):
        """เรียกใช้ application"""
        return self.app.exec_()

def main():
    controller = AppController()
    sys.exit(controller.run())

if __name__ == "__main__":
    main()