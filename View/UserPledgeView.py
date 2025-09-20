from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import csv

class UserPledgeView(QWidget):
    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle(f"My Pledges - {user_info['username']}")
        self.setGeometry(300, 300, 900, 600)

        self.setupUI()
        self.loadUserPledges()

    def setupUI(self):
        mainLayout = QVBoxLayout()

        # Header
        headerLayout = QVBoxLayout()

        # Welcome message
        welcomeLabel = QLabel(f"Welcome, {self.user_info['username']}!")
        welcomeLabel.setStyleSheet("""
            font-weight: bold; 
            font-size: 20px; 
            color: #2c3e50;
            margin-bottom: 5px;
        """)
        headerLayout.addWidget(welcomeLabel)

        # User info
        userInfoLabel = QLabel(f"User ID: {self.user_info['user_id']} | Email: {self.user_info['email']}")
        userInfoLabel.setStyleSheet("font-size: 14px; color: #7f8c8d; margin-bottom: 20px;")
        headerLayout.addWidget(userInfoLabel)

        mainLayout.addLayout(headerLayout)

        # Statistics Cards
        self.createStatsCards(mainLayout)

        # Pledges Table
        tableLabel = QLabel("Your Pledges:")
        tableLabel.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 20px; margin-bottom: 10px;")
        mainLayout.addWidget(tableLabel)

        self.pledgeTable = QTableWidget()
        self.pledgeTable.setColumnCount(7)
        self.pledgeTable.setHorizontalHeaderLabels([
            "Pledge ID", "Project ID", "Project Name", "Amount", "Reward", "Status", "Date"
        ])
        mainLayout.addWidget(self.pledgeTable)

        # Buttons
        buttonLayout = QHBoxLayout()

        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refreshButton.clicked.connect(self.loadUserPledges)

        self.logoutButton = QPushButton("Logout")
        self.logoutButton.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.logoutButton.clicked.connect(self.logout)

        buttonLayout.addWidget(self.refreshButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.logoutButton)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def createStatsCards(self, mainLayout):
        """สร้างการ์ดแสดงสถิติ"""
        statsLayout = QHBoxLayout()

        # คำนวณสถิติ
        stats = self.calculateUserStats()

        # Successful Pledges Card
        successCard = self.createStatsCard(
            "Successful Pledges",
            str(stats['successful']),
            "#27ae60"
        )

        # Rejected Pledges Card
        rejectedCard = self.createStatsCard(
            "Rejected Pledges",
            str(stats['rejected']),
            "#e74c3c"
        )

        # Total Amount Card
        totalCard = self.createStatsCard(
            "Total Successful Amount",
            f"${stats['successful_amount']:,.2f}",
            "#3498db"
        )

        # Success Rate Card
        successRateCard = self.createStatsCard(
            "Success Rate",
            f"{stats['success_rate']:.1f}%",
            "#9b59b6"
        )

        statsLayout.addWidget(successCard)
        statsLayout.addWidget(rejectedCard)
        statsLayout.addWidget(totalCard)
        statsLayout.addWidget(successRateCard)

        mainLayout.addLayout(statsLayout)

    def createStatsCard(self, title, value, color):
        """สร้างการ์ดสถิติ"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)

        cardLayout = QVBoxLayout()

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet(f"font-weight: bold; font-size: 12px; color: {color};")
        titleLabel.setAlignment(Qt.AlignCenter)

        valueLabel = QLabel(value)
        valueLabel.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
        valueLabel.setAlignment(Qt.AlignCenter)

        cardLayout.addWidget(titleLabel)
        cardLayout.addWidget(valueLabel)
        card.setLayout(cardLayout)

        return card

    def calculateUserStats(self):
        """คำนวณสถิติของผู้ใช้"""
        stats = {
            'total': 0,
            'successful': 0,
            'rejected': 0,
            'successful_amount': 0.0,
            'success_rate': 0.0
        }

        try:
            with open(r'Model/data/Pledges.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['user_id'] == str(self.user_info['user_id']):
                        stats['total'] += 1
                        amount = float(row.get('amount', 0))

                        if row.get('status') == 'Success':
                            stats['successful'] += 1
                            stats['successful_amount'] += amount
                        elif row.get('status') == 'Rejected':
                            stats['rejected'] += 1
        except Exception as e:
            print(f"Error calculating stats: {e}")

        # คำนวณอัตราความสำเร็จ
        if stats['total'] > 0:
            stats['success_rate'] = (stats['successful'] / stats['total']) * 100

        return stats

    def loadUserPledges(self):
        """โหลด Pledge ของผู้ใช้"""
        pledges = []

        # ดึง Pledge ของผู้ใช้
        try:
            with open(r'Model/data/Pledges.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['user_id'] == str(self.user_info['user_id']):
                        pledges.append(row)
        except Exception as e:
            print(f"Error loading pledges: {e}")

        # ดึงข้อมูลโครงการและรางวัล
        projects = self.loadProjects()
        rewards = self.loadRewards()

        # แสดงในตาราง
        self.displayPledges(pledges, projects, rewards)

    def loadProjects(self):
        projects = {}
        try:
            with open(r'Model/data/Projects.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    projects[row['project_id']] = row
        except Exception as e:
            print(f"Error loading projects: {e}")
        return projects

    def loadRewards(self):
        rewards = {}
        try:
            with open(r'Model/data/RewardTier.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    rewards[row['reward_id']] = row
        except Exception as e:
            print(f"Error loading rewards: {e}")
        return rewards

    def displayPledges(self, pledges, projects, rewards):
        self.pledgeTable.setRowCount(len(pledges))

        for row, pledge in enumerate(pledges):
            # Pledge ID
            self.pledgeTable.setItem(row, 0, QTableWidgetItem(pledge.get('pledge_id', '')))

            # Project ID
            self.pledgeTable.setItem(row, 1, QTableWidgetItem(pledge.get('project_id', '')))

            # Project Name
            project_name = 'Unknown'
            if pledge.get('project_id') in projects:
                project_name = projects[pledge.get('project_id')]['project_name']
            self.pledgeTable.setItem(row, 2, QTableWidgetItem(project_name))

            # Amount
            amount = float(pledge.get('amount', 0))
            amount_item = QTableWidgetItem(f"${amount:,.2f}")
            amount_item.setForeground(QColor(0, 100, 0))
            self.pledgeTable.setItem(row, 3, amount_item)

            # Reward Name
            reward_name = 'Unknown'
            if pledge.get('reward_id') in rewards:
                reward_name = rewards[pledge.get('reward_id')]['reward_name']
            self.pledgeTable.setItem(row, 4, QTableWidgetItem(reward_name))

            # Status
            status_item = QTableWidgetItem(pledge.get('status', ''))
            if pledge.get('status') == 'Success':
                status_item.setForeground(QColor(0, 128, 0))
                font = QFont()
                font.setBold(True)
                status_item.setFont(font)
            elif pledge.get('status') == 'Rejected':
                status_item.setForeground(QColor(255, 0, 0))
                font = QFont()
                font.setBold(True)
                status_item.setFont(font)
            self.pledgeTable.setItem(row, 5, status_item)

            # Date
            pledge_time = pledge.get('pledge_time', '')
            if ' ' in pledge_time:
                date_part = pledge_time.split(' ')[0]
            else:
                date_part = pledge_time
            self.pledgeTable.setItem(row, 6, QTableWidgetItem(date_part))

        self.pledgeTable.resizeColumnsToContents()

        # อัปเดตสถิติ
        self.updateStatsCards()

    def updateStatsCards(self):
        """อัปเดตการ์ดสถิติ"""
        # สร้างการ์ดใหม่ (วิธีง่ายๆ)
        # ในการใช้งานจริงควร update แค่ค่าใน label
        pass

    def logout(self):
        """ออกจากระบบ"""
        self.close()