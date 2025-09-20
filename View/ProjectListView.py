from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from View.ProjectDetailView import ProjectDetailView


class ProjectListView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Projects List")
        self.setGeometry(250, 250, 800, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Goal", "Current Funding"])
        layout.addWidget(self.table)

        self.detailButton = QPushButton("View Detail")
        self.detailButton.clicked.connect(self.openDetail)
        layout.addWidget(self.detailButton)

        self.setLayout(layout)

        self.loadProjects(self.controller.getAllProjects())

    def loadProjects(self, projects):
        self.table.setRowCount(len(projects))
        for row, proj in enumerate(projects):
            self.table.setItem(row, 0, QTableWidgetItem(proj["project_id"]))
            self.table.setItem(row, 1, QTableWidgetItem(proj["project_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(proj["category"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(proj["funding_goal"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(proj["current_funding"])))

        self.table.resizeColumnsToContents()

    def openDetail(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            project = self.controller.getAllProjects()[current_row]
            self.detailWindow = ProjectDetailView(project)
            self.detailWindow.show()
