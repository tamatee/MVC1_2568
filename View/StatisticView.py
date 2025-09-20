from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from View.AddPledgeView import AddPledgeView

class StatisticView(QWidget):
    def __init__(self, controller, user_info=None):
        super().__init__()
        self.controller = controller
        self.pledgeList = controller.pledges

        self.setWindowTitle("Pledge Statistics")
        self.setGeometry(300, 300, 700, 500)

        layout = QVBoxLayout()

        # Title
        lblTitle = QLabel("Pledge Statistics")
        lblTitle.setStyleSheet("font-weight: bold; font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(lblTitle)

        # Statistics Summary
        statsLayout = QHBoxLayout()

        success_count = sum(1 for p in self.pledgeList if p.get("status") == "Success")
        rejected_count = sum(1 for p in self.pledgeList if p.get("status") == "Rejected")
        total_amount = sum(float(p.get("amount", 0)) for p in self.pledgeList if p.get("status") == "Success")

        # Success Stats
        successFrame = QWidget()
        successFrame.setStyleSheet("background-color: #e8f5e8; border: 2px solid #4CAF50; border-radius: 10px; padding: 15px;")
        successLayout = QVBoxLayout()
        successTitle = QLabel("Successful Pledges")
        successTitle.setStyleSheet("font-weight: bold; font-size: 14px; color: #4CAF50;")
        successCount = QLabel(f"{success_count}")
        successCount.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        successLayout.addWidget(successTitle)
        successLayout.addWidget(successCount)
        successFrame.setLayout(successLayout)

        # Rejected Stats
        rejectedFrame = QWidget()
        rejectedFrame.setStyleSheet("background-color: #fde8e8; border: 2px solid #f44336; border-radius: 10px; padding: 15px;")
        rejectedLayout = QVBoxLayout()
        rejectedTitle = QLabel("Rejected Pledges")
        rejectedTitle.setStyleSheet("font-weight: bold; font-size: 14px; color: #f44336;")
        rejectedCount = QLabel(f"{rejected_count}")
        rejectedCount.setStyleSheet("font-size: 24px; font-weight: bold; color: #f44336;")
        rejectedLayout.addWidget(rejectedTitle)
        rejectedLayout.addWidget(rejectedCount)
        rejectedFrame.setLayout(rejectedLayout)

        # Total Amount Stats
        totalFrame = QWidget()
        totalFrame.setStyleSheet("background-color: #e3f2fd; border: 2px solid #2196F3; border-radius: 10px; padding: 15px;")
        totalLayout = QVBoxLayout()
        totalTitle = QLabel("Total Amount (Success)")
        totalTitle.setStyleSheet("font-weight: bold; font-size: 14px; color: #2196F3;")
        totalAmount = QLabel(f"${total_amount:,.2f}")
        totalAmount.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3;")
        totalLayout.addWidget(totalTitle)
        totalLayout.addWidget(totalAmount)
        totalFrame.setLayout(totalLayout)

        statsLayout.addWidget(successFrame)
        statsLayout.addWidget(rejectedFrame)
        statsLayout.addWidget(totalFrame)
        layout.addLayout(statsLayout)

        # Pledge Table
        tableLabel = QLabel("All Pledges:")
        tableLabel.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
        layout.addWidget(tableLabel)

        self.pledgeTable = QTableWidget()
        self.pledgeTable.setColumnCount(6)
        self.pledgeTable.setHorizontalHeaderLabels(["Pledge ID", "User ID", "Project ID", "Amount", "Reward ID", "Status"])
        self.loadPledgeTable()
        layout.addWidget(self.pledgeTable)

        # Buttons
        buttonLayout = QHBoxLayout()

        self.addPledgeButton = QPushButton("Add New Pledge")
        self.addPledgeButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        self.addPledgeButton.clicked.connect(self.openAddPledge)

        self.refreshButton = QPushButton("Refresh Data")
        self.refreshButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 10px; font-weight: bold;")
        self.refreshButton.clicked.connect(self.refreshData)

        buttonLayout.addWidget(self.addPledgeButton)
        buttonLayout.addWidget(self.refreshButton)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def loadPledgeTable(self):
        """Load pledge data into table"""
        self.pledgeTable.setRowCount(len(self.pledgeList))
        for row, pledge in enumerate(self.pledgeList):
            self.pledgeTable.setItem(row, 0, QTableWidgetItem(str(pledge.get("pledge_id", ""))))
            self.pledgeTable.setItem(row, 1, QTableWidgetItem(str(pledge.get("user_id", ""))))
            self.pledgeTable.setItem(row, 2, QTableWidgetItem(str(pledge.get("project_id", ""))))
            self.pledgeTable.setItem(row, 3, QTableWidgetItem(f"${float(pledge.get('amount', 0)):,.2f}"))
            self.pledgeTable.setItem(row, 4, QTableWidgetItem(str(pledge.get("reward_id", ""))))

            # Color code status
            status_item = QTableWidgetItem(str(pledge.get("status", "")))
            if pledge.get("status") == "Success":
                status_item.setForeground(QColor(0, 128, 0))  # Green color
                font = QFont()
                font.setBold(True)
                status_item.setFont(font)
            elif pledge.get("status") == "Rejected":
                status_item.setForeground(QColor(255, 0, 0))  # Red color
                font = QFont()
                font.setBold(True)
                status_item.setFont(font)
            self.pledgeTable.setItem(row, 5, status_item)

        self.pledgeTable.resizeColumnsToContents()

    def openAddPledge(self):
        """Open Add Pledge window"""
        self.addPledgeWindow = AddPledgeView(self.controller)
        self.addPledgeWindow.show()

    def refreshData(self):
        """Refresh pledge data and update display"""
        # Reload data from CSV
        from Model.csvParser import loadPledges
        self.controller.pledges = loadPledges()
        self.pledgeList = self.controller.pledges

        # Update statistics display
        success_count = sum(1 for p in self.pledgeList if p.get("status") == "Success")
        rejected_count = sum(1 for p in self.pledgeList if p.get("status") == "Rejected")
        total_amount = sum(float(p.get("amount", 0)) for p in self.pledgeList if p.get("status") == "Success")

        # Reload table
        self.loadPledgeTable()