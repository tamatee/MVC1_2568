from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton, 
    QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, QTextEdit
)
from datetime import datetime
from Model.BusinessRules import BusinessRules
import csv
import os

class AddPledgeView(QWidget):
    def __init__(self, statistic_controller):
        super().__init__()
        self.statistic_controller = statistic_controller
        self.setWindowTitle("Add New Pledge")
        self.setGeometry(300, 300, 400, 300)

        self.setupUI()

    def setupUI(self):
        mainLayout = QVBoxLayout()
        formLayout = QFormLayout()

        # Title
        title = QLabel("Add New Pledge")
        title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        mainLayout.addWidget(title)

        # User ID
        self.userIdEdit = QLineEdit()
        self.userIdEdit.setPlaceholderText("Enter user ID (1-10)")
        formLayout.addRow("User ID:", self.userIdEdit)

        # Project ID
        self.projectIdEdit = QLineEdit()
        self.projectIdEdit.setPlaceholderText("Enter project ID (e.g., 10000001)")
        formLayout.addRow("Project ID:", self.projectIdEdit)

        # Amount
        self.amountEdit = QLineEdit()
        self.amountEdit.setPlaceholderText("Enter pledge amount")
        formLayout.addRow("Amount:", self.amountEdit)

        # Reward ID
        self.rewardIdEdit = QLineEdit()
        self.rewardIdEdit.setPlaceholderText("Enter reward ID")
        formLayout.addRow("Reward ID:", self.rewardIdEdit)

        # Status (อัตโนมัติจากการตรวจสอบ)
        self.statusLabel = QLabel("Status will be determined automatically")
        self.statusLabel.setStyleSheet("color: #666; font-style: italic;")
        formLayout.addRow("Status:", self.statusLabel)

        # แสดงข้อมูลเพิ่มเติม
        self.infoText = QTextEdit()
        self.infoText.setMaximumHeight(100)
        self.infoText.setReadOnly(True)
        self.infoText.setPlaceholderText("Validation info will appear here...")
        formLayout.addRow("Info:", self.infoText)

        mainLayout.addLayout(formLayout)

        # Buttons
        buttonLayout = QHBoxLayout()

        self.saveButton = QPushButton("Save Pledge")
        self.saveButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.saveButton.clicked.connect(self.savePledge)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        self.cancelButton.clicked.connect(self.close)

        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def savePledge(self):
        # Validate inputs
        try:
            user_id = int(self.userIdEdit.text())
            if user_id < 1 or user_id > 10:
                raise ValueError("User ID must be between 1-10")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid User ID (1-10)!")
            return

        if not self.projectIdEdit.text().strip():
            QMessageBox.warning(self, "Error", "Please enter Project ID!")
            return

        try:
            amount = float(self.amountEdit.text())
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount!")
            return

        if not self.rewardIdEdit.text().strip():
            QMessageBox.warning(self, "Error", "Please enter Reward ID!")
            return

        # ใช้ BusinessRules ในการประมวลผล pledge
        status, message = BusinessRules.processPledge(
            user_id, 
            self.projectIdEdit.text().strip(), 
            amount, 
            self.rewardIdEdit.text().strip()
        )

        # แสดงข้อมูลการตรวจสอบ
        self.infoText.setText(f"Status: {status}\nMessage: {message}")

        # ถ้าเป็น Rejected แสดงจำนวนครั้งที่ถูกปฏิเสธ
        if status == "Rejected":
            rejection_count = BusinessRules.getRejectionCount(user_id)
            self.infoText.append(f"\nUser rejection count: {rejection_count + 1}")

        # Generate new pledge ID
        new_pledge_id = self.generateNewPledgeId()

        # Current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare new pledge data
        new_pledge = {
            "pledge_id": str(new_pledge_id),
            "user_id": str(user_id),
            "project_id": self.projectIdEdit.text().strip(),
            "pledge_time": current_time,
            "amount": amount,
            "reward_id": self.rewardIdEdit.text().strip(),
            "status": status
        }

        # Save to CSV
        if self.saveToCSV(new_pledge):
            if status == "Success":
                QMessageBox.information(self, "Success", f"Pledge processed successfully!\n{message}")
            else:
                QMessageBox.warning(self, "Pledge Rejected", f"Pledge was rejected:\n{message}")

            # Update controller's data immediately
            from Model.csvParser import loadPledges
            self.statistic_controller.pledges = loadPledges()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to save pledge!")

    def generateNewPledgeId(self):
        # Get highest existing pledge ID and add 1
        pledges = self.statistic_controller.pledges
        if not pledges:
            return 1

        max_id = max(int(p["pledge_id"]) for p in pledges if p["pledge_id"].isdigit())
        return max_id + 1

    def saveToCSV(self, new_pledge):
        try:
            file_path = r'Model/data/Pledges.csv'

            # Read existing data
            existing_data = []
            if os.path.exists(file_path):
                with open(file_path, 'r', newline="", encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile)
                    existing_data = list(reader)

            # Add new pledge
            existing_data.append({
                "pledge_id": new_pledge["pledge_id"],
                "user_id": new_pledge["user_id"],
                "project_id": new_pledge["project_id"],
                "pledge_time": new_pledge["pledge_time"],
                "amount": new_pledge["amount"],
                "reward_id": new_pledge["reward_id"],
                "status": new_pledge["status"]
            })

            # Write back to CSV
            with open(file_path, 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ["pledge_id", "user_id", "project_id", "pledge_time", "amount", "reward_id", "status"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_data)

            # Update controller's data
            from Model.csvParser import loadPledges
            self.statistic_controller.pledges = loadPledges()

            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False