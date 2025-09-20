from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt


class ProjectDetailView(QWidget):
    def __init__(self, project):
        super().__init__()
        self.project = project

        self.setWindowTitle(f"Project Detail - {project['project_name']}")
        self.setGeometry(300, 300, 500, 350)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(15)

        # Title
        title = QLabel(f"[{project['project_id']}] {project['project_name']}")
        title.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        mainLayout.addWidget(title, alignment=Qt.AlignCenter)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(line)

        # Project Info
        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(10)

        # Category
        category = QLabel(f"Category: {project['category']}")
        category.setStyleSheet("font-size: 14px;")
        infoLayout.addWidget(category)

        # Goal
        goal = QLabel(f"Goal: {project['funding_goal']}")
        goal.setStyleSheet("font-size: 14px;")
        infoLayout.addWidget(goal)

        # Current funding
        current = QLabel(f"Current Funding: {project['current_funding']}")
        current.setStyleSheet("font-size: 14px; color: green;")
        infoLayout.addWidget(current)

        # Deadline
        deadline = QLabel(f"Deadline: {project['deadline']}")
        deadline.setStyleSheet("font-size: 14px; color: red;")
        infoLayout.addWidget(deadline)

        mainLayout.addLayout(infoLayout)

        #Progress Bar
        progressLabel = QLabel("Progress:")
        progressLabel.setStyleSheet("font-weight: bold; font-size: 14px;")
        mainLayout.addWidget(progressLabel)

        progressBar = QProgressBar()
        progressBar.setAlignment(Qt.AlignCenter)
        progressBar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bbb;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 20px;
            }
        """)

        try:
            goal_value = float(project["funding_goal"])
            current_value = float(project["current_funding"])
            percent = int((current_value / goal_value) * 100) if goal_value > 0 else 0
        except Exception:
            percent = 0

        progressBar.setValue(percent)
        mainLayout.addWidget(progressBar)

        self.setLayout(mainLayout)
