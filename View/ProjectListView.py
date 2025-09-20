from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLabel
from View.ProjectDetailView import ProjectDetailView
from View.AddProjectView import AddProjectView
from View.EditProjectView import EditProjectView
from Model.UserManager import UserManager


class ProjectListView(QWidget):
    def __init__(self, controller, user_info=None):
        super().__init__()
        self.controller = controller
        self.user_info = user_info  # ข้อมูลผู้ใช้ที่ล็อกอิน
        self.setWindowTitle("Projects List")
        self.setGeometry(250, 250, 900, 500)

        layout = QVBoxLayout()

        # User info (ถ้ามี)
        if self.user_info:
            if UserManager.isAdmin(self.user_info):
                userLabel = QLabel(f"Logged in as: {self.user_info['username']} (Admin)")
            else:
                userLabel = QLabel(f"Logged in as: {self.user_info['username']} (User)")
            userLabel.setStyleSheet("font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
            layout.addWidget(userLabel)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Goal", "Current Funding", "Deadline"])
        layout.addWidget(self.table)

        # Buttons Layout
        buttonLayout = QHBoxLayout()

        # Add Project Button (เฉพาะ admin)
        if UserManager.isAdmin(self.user_info):
            self.addButton = QPushButton("Add New Project")
            self.addButton.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
            self.addButton.clicked.connect(self.openAddProject)
            buttonLayout.addWidget(self.addButton)

            # Edit Project Button (เฉพาะ admin)
            self.editButton = QPushButton("Edit Project")
            self.editButton.setStyleSheet("background-color: #ff9800; color: white; padding: 8px; font-weight: bold;")
            self.editButton.clicked.connect(self.openEditProject)
            buttonLayout.addWidget(self.editButton)

        # View Detail Button
        self.detailButton = QPushButton("View Detail")
        self.detailButton.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; font-weight: bold;")
        self.detailButton.clicked.connect(self.openDetail)
        buttonLayout.addWidget(self.detailButton)

        # Refresh Button
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px; font-weight: bold;")
        self.refreshButton.clicked.connect(self.refreshData)
        buttonLayout.addWidget(self.refreshButton)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.loadProjects(self.controller.getAllProjects())

        self.loadProjects(self.controller.getAllProjects())

    def loadProjects(self, projects):
        self.current_projects = projects  # Store current projects for reference
        self.table.setRowCount(len(projects))
        for row, proj in enumerate(projects):
            self.table.setItem(row, 0, QTableWidgetItem(proj["project_id"]))
            self.table.setItem(row, 1, QTableWidgetItem(proj["project_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(proj["category"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"${proj['funding_goal']:,.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"${proj['current_funding']:,.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(proj["deadline"]))

        self.table.resizeColumnsToContents()

    def openDetail(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            project = self.current_projects[current_row]
            self.detailWindow = ProjectDetailView(project)
            self.detailWindow.show()
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Warning", "Please select a project to view details!")

    def openAddProject(self):
        if UserManager.isAdmin(self.user_info):
            self.addWindow = AddProjectView(self.controller)
            self.addWindow.show()
        else:
            QMessageBox.warning(self, "Access Denied", "Only administrators can add projects!")

    def openEditProject(self):
        if UserManager.isAdmin(self.user_info):
            current_row = self.table.currentRow()
            if current_row >= 0:
                project = self.current_projects[current_row]
                self.editWindow = EditProjectView(self.controller, project)
                self.editWindow.show()
            else:
                QMessageBox.warning(self, "Warning", "Please select a project to edit!")
        else:
            QMessageBox.warning(self, "Access Denied", "Only administrators can edit projects!")

    def refreshData(self):
        """Refresh the project list from controller"""
        # Reload data from CSV
        from Model.csvParser import loadProjects
        self.controller.projects = loadProjects()
        # Reload the table
        self.loadProjects(self.controller.getAllProjects())