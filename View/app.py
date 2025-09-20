from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)

import sys

from Controller.StatisticController import StatisticController
from Controller.projectController import ProjectController
from View.ProjectListView import ProjectListView
from View.StatisticView import StatisticView

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create main menu window
        self.setWindowTitle("CS Camp Crowdfunding - Home")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Title label
        title = QLabel("Select a Menu Option:")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(title)

        # Project Button
        self.projectButton = QPushButton("Projects List")
        self.projectButton.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.projectButton.clicked.connect(self.openProjectListView)
        layout.addWidget(self.projectButton)

        # Project Button
        self.projectButton = QPushButton("View Statistics")
        self.projectButton.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.projectButton.clicked.connect(self.openStatistics)
        layout.addWidget(self.projectButton)

		# Statistics Button
        self.setLayout(layout)

    def openProjectListView(self):
        controller = ProjectController()
        self.projectWindow = ProjectListView(controller)
        self.projectWindow.show()

    def openStatistics(self):
        controller = StatisticController()
        self.statWindow = StatisticView(controller)
        self.statWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
