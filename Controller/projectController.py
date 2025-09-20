from Model.csvParser import loadProjects
from datetime import datetime


class ProjectController:
    def __init__(self):
        self.projects = loadProjects()

    def getAllProjects(self):
        return self.projects

    def getCategories(self):
        return sorted(set([p["category"] for p in self.projects]))

    def filterProjects(self, keyword="", category="All", sortBy="Newest"):
        filtered = self.projects

        if keyword:
            keyword_lower = keyword.lower()
            filtered = [
                p for p in filtered
                if keyword_lower in str(p["project_id"]).lower()
                or keyword_lower in p["project_name"].lower()
            ]

        if category != "All":
            filtered = [p for p in filtered if p["category"] == category]

        if sortBy == "Newest":
            filtered = sorted(filtered, key=lambda p: p["project_id"], reverse=True)
        elif sortBy == "Deadline Soon":
            filtered = sorted(
                filtered,
                key=lambda p: datetime.strptime(p["deadline"], "%Y-%m-%d")
            )
        elif sortBy == "Most Funded":
            filtered = sorted(
                filtered,
                key=lambda p: float(p["current_funding"]),
                reverse=True
            )

        return filtered
