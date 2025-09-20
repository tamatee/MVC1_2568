from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtCore import QDate
from Model.BusinessRules import BusinessRules
import csv
import os

class EditProjectView(QWidget):
    def __init__(self, controller, project):
        super().__init__()
        self.controller = controller
        self.project = project
        self.setWindowTitle(f"Edit Project - {project['project_name']}")
        self.setGeometry(300, 300, 400, 350)

        self.setupUI()
        self.loadProjectData()

    def setupUI(self):
        mainLayout = QVBoxLayout()
        formLayout = QFormLayout()

        # Title
        title = QLabel(f"Edit Project ID: {self.project['project_id']}")
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
        formLayout.addRow("Funding Goal:", self.fundingGoalEdit)

        # Current Funding (read-only display)
        self.currentFundingLabel = QLabel()
        formLayout.addRow("Current Funding:", self.currentFundingLabel)

        # Deadline
        self.deadlineEdit = QDateEdit()
        self.deadlineEdit.setCalendarPopup(True)
        formLayout.addRow("Deadline:", self.deadlineEdit)

        mainLayout.addLayout(formLayout)

        # Buttons
        buttonLayout = QHBoxLayout()

        self.saveButton = QPushButton("Save Changes")
        self.saveButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.saveButton.clicked.connect(self.saveChanges)

        self.deleteButton = QPushButton("Delete Project")
        self.deleteButton.setStyleSheet("background-color: #ff9800; color: white; padding: 8px;")
        self.deleteButton.clicked.connect(self.deleteProject)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.cancelButton.clicked.connect(self.close)

        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.cancelButton)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def loadProjectData(self):
        # Load existing project data into form
        self.projectNameEdit.setText(self.project['project_name'])

        # Set category
        category_index = self.categoryCombo.findText(self.project['category'])
        if category_index >= 0:
            self.categoryCombo.setCurrentIndex(category_index)

        self.fundingGoalEdit.setText(str(self.project['funding_goal']))
        self.currentFundingLabel.setText(f"${self.project['current_funding']:,.2f}")

        # Set deadline
        deadline_date = QDate.fromString(self.project['deadline'], "yyyy-MM-dd")
        self.deadlineEdit.setDate(deadline_date)

    def saveChanges(self):
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

        # ตรวจสอบวันหมดเขต
        deadline_str = self.deadlineEdit.date().toString("yyyy-MM-dd")
        if not BusinessRules.validateProjectDeadline(deadline_str):
            QMessageBox.warning(self, "Error", "Project deadline must be in the future!")
            return

        # Prepare updated project data
        updated_project = {
            "project_id": self.project["project_id"],
            "project_name": self.projectNameEdit.text().strip(),
            "category": self.categoryCombo.currentText(),
            "funding_goal": funding_goal,
            "deadline": self.deadlineEdit.date().toString("yyyy-MM-dd"),
            "current_funding": self.project["current_funding"]  # Keep existing funding
        }

        # Save to CSV
        if self.updateCSV(updated_project):
            QMessageBox.information(self, "Success", "Project updated successfully!")
            # Update controller's data immediately
            if hasattr(self.controller, 'projects'):
                from Model.csvParser import loadProjects
                self.controller.projects = loadProjects()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to update project!")

    def deleteProject(self):
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete project '{self.project['project_name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.deleteFromCSV():
                QMessageBox.information(self, "Success", "Project deleted successfully!")
                # Update controller's data immediately
                if hasattr(self.controller, 'projects'):
                    from Model.csvParser import loadProjects
                    self.controller.projects = loadProjects()
                self.close()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete project!")

    def updateCSV(self, updated_project):
        try:
            file_path = r'Model/data/Projects.csv'

            # Read existing data
            existing_data = []
            with open(file_path, 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                existing_data = list(reader)

            # Update the project
            for i, project in enumerate(existing_data):
                if project["project_id"] == updated_project["project_id"]:
                    existing_data[i] = updated_project
                    break

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
            print(f"Error updating CSV: {e}")
            return False

    def deleteFromCSV(self):
        try:
            file_path = r'Model/data/Projects.csv'

            # Read existing data
            existing_data = []
            with open(file_path, 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                existing_data = list(reader)

            # Remove the project
            existing_data = [p for p in existing_data if p["project_id"] != self.project["project_id"]]

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
            print(f"Error deleting from CSV: {e}")
            return False