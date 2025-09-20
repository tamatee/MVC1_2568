from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)

import sys

from Controller.StatisticController import StatisticController
from Controller.projectController import ProjectController
from View.ProjectListView import ProjectListView
from View.StatisticView import StatisticView

class MainWindow(QWidget):
    def __init__(self, user_info=None):
        super().__init__()
        self.user_info = user_info  # ข้อมูลผู้ใช้ที่ล็อกอิน

        # Create main menu window
        self.setWindowTitle("CS Camp Crowdfunding - Home")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # User info display (ถ้ามี)
        if self.user_info:
            userLabel = QLabel(f"Welcome, {self.user_info['username']} (Admin)")
            userLabel.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50; margin-bottom: 15px;")
            layout.addWidget(userLabel)

        # Title label
        title = QLabel("Select a Menu Option:")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(title)

        # Project Button
        self.projectButton = QPushButton("Projects List")
        self.projectButton.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.projectButton.clicked.connect(self.openProjectListView)
        layout.addWidget(self.projectButton)

        # Statistics Button
        self.statisticsButton = QPushButton("View Statistics")
        self.statisticsButton.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.statisticsButton.clicked.connect(self.openStatistics)
        layout.addWidget(self.statisticsButton)

        # Logout Button (ถ้ามี user ล็อกอิน)
        if self.user_info:
            self.logoutButton = QPushButton("Logout")
            self.logoutButton.setStyleSheet("background-color: #e74c3c; color: white; font-size: 14px; padding: 10px;")
            self.logoutButton.clicked.connect(self.logout)
            layout.addWidget(self.logoutButton)

        self.setLayout(layout)

    def openProjectListView(self):
        controller = ProjectController()
        self.projectWindow = ProjectListView(controller, self.user_info)
        self.projectWindow.show()

    def openStatistics(self):
        controller = StatisticController()
        self.statWindow = StatisticView(controller, self.user_info)
        self.statWindow.show()

    def logout(self):
        """ออกจากระบบ"""
        reply = QMessageBox.question(
            self, 
            "Logout", 
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()
            # เรียกหน้า login ใหม่
            from View.LoginView import LoginView
            self.login_window = LoginView()
            self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())