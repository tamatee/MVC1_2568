import csv
import os

# load data from CSV files as 'dict'
def loadProjects():
    projects = []
    file_path = r'Data/Projects.csv'

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            projects.append({
                "project_id": row["project_id"],
                "project_name": row["project_name"],
                "category": row["category"],
                "funding_goal": float(row["funding_goal"]),
                "deadline": row["deadline"],
                "current_funding": float(row["current_funding"])
            })
    return projects

def loadPledges():
    pledges = []
    file_path = r'Data/Pledges.csv'

    if not os.path.exists(file_path):
        return pledges

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pledges.append({
                "pledge_id": row.get("pledge_id", ""),
                "user_id": row.get("user_id", ""),
                "project_id": row.get("project_id", ""),
                "amount": float(row.get("amount", 0)),
                "reward_id": row.get("reward_id", ""),
                "status": row.get("status", "")
            })

    return pledges