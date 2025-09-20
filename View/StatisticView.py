from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class StatisticView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.pledgeList = controller.pledges

        self.setWindowTitle("Pledge Statistics")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        success_count = sum(1 for p in self.pledgeList if p.get("status") == "Success")
        rejected_count = sum(1 for p in self.pledgeList if p.get("status") == "Rejected")

        lblTitle = QLabel("Pledge Statistics")
        lblTitle.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(lblTitle)

        lblSuccess = QLabel(f"Successful Pledges: {success_count}")
        lblRejected = QLabel(f"Rejected Pledges: {rejected_count}")
        layout.addWidget(lblSuccess)
        layout.addWidget(lblRejected)

        self.setLayout(layout)
