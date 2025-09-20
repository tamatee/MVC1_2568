from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtCore import QDate
import csv
import os

class AddProjectView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Add New Project")
        self.setGeometry(300, 300, 400, 350)

        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout()
        formLayout = QFormLayout()

        # Title
        title = QLabel("Add New Project")
        title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        mainLayout.addWidget(title)

        # Project Name
        self.projectNameEdit = QLineEdit()
        formLayout.addRow("Project Name:", self.projectNameEdit)

        # Category
        self.categoryCombo = QComboBox()
        categories = ["Technology", "Art", "Community"]
        self.categoryCombo.addItems(categories)
        formLayout.addRow("Category:", self.categoryCombo)

        # Funding Goal
        self.fundingGoalEdit = QLineEdit()
        self.fundingGoalEdit.setPlaceholderText("Enter amount (e.g., 50000)")
        formLayout.addRow("Funding Goal:", self.fundingGoalEdit)

        # Deadline
        self.deadlineEdit = QDateEdit()
        self.deadlineEdit.setDate(QDate.currentDate().addDays(30))
        self.deadlineEdit.setCalendarPopup(True)
        formLayout.addRow("Deadline:", self.deadlineEdit)

        mainLayout.addLayout(formLayout)

        # Buttons
        buttonLayout = QHBoxLayout()

        self.saveButton = QPushButton("Save Project")
        self.saveButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.saveButton.clicked.connect(self.saveProject)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.cancelButton.clicked.connect(self.close)

        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def saveProject(self):
        # Validate inputs
        if not self.projectNameEdit.text().strip():
            QMessageBox.warning(self, "Error", "Please enter project name!")
            return

        try:
            funding_goal = float(self.fundingGoalEdit.text())
            if funding_goal <= 0:
                raise ValueError("Funding goal must be positive")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid funding goal!")
            return

        # Generate new project ID
        new_id = self.generateNewProjectId()

        # Prepare new project data
        new_project = {
            "project_id": str(new_id),
            "project_name": self.projectNameEdit.text().strip(),
            "category": self.categoryCombo.currentText(),
            "funding_goal": funding_goal,
            "deadline": self.deadlineEdit.date().toString("yyyy-MM-dd"),
            "current_funding": 0.0
        }

        # Save to CSV
        if self.saveToCSV(new_project):
            QMessageBox.information(self, "Success", "Project added successfully!")
            # Emit a custom signal or call parent refresh directly
            if hasattr(self.controller, 'projects'):
                from Model.csvParser import loadProjects
                self.controller.projects = loadProjects()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to save project!")

    def generateNewProjectId(self):
        # Get highest existing ID and add 1
        projects = self.controller.getAllProjects()
        if not projects:
            return 10000001

        max_id = max(int(p["project_id"]) for p in projects)
        return max_id + 1

    def saveToCSV(self, new_project):
        try:
            file_path = r'Model/data/Projects.csv'

            # Read existing data
            existing_data = []
            if os.path.exists(file_path):
                with open(file_path, 'r', newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    existing_data = list(reader)

            # Add new project
            existing_data.append({
                "project_id": new_project["project_id"],
                "project_name": new_project["project_name"],
                "category": new_project["category"],
                "funding_goal": new_project["funding_goal"],
                "deadline": new_project["deadline"],
                "current_funding": new_project["current_funding"]
            })

            # Write back to CSV
            with open(file_path, 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ["project_id", "project_name", "category", "funding_goal", "deadline", "current_funding"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_data)

            # Update controller's data
            self.controller.projects = self.controller.loadProjects()

            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False