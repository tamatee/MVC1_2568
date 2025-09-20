from datetime import datetime
import csv
import os

class BusinessRules:
    def __init__(self):
        pass

    @staticmethod
    def validateProjectDeadline(deadline_str):
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            today = datetime.now()
            return deadline.date() > today.date()
        except ValueError:
            return False

    @staticmethod
    def getRewardInfo(reward_id):
        try:
            with open(r'Data/RewardTier.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["reward_id"] == str(reward_id):
                        return {
                            "reward_id": row["reward_id"],
                            "project_id": row["project_id"],
                            "reward_name": row["reward_name"],
                            "min_amount": float(row["min_amount"]),
                            "quota": int(row["quota"])
                        }
        except Exception as e:
            print(f"Error reading reward info: {e}")
        return None

    @staticmethod
    def getProjectInfo(project_id):
        try:
            with open(r'Data/Projects.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["project_id"] == str(project_id):
                        return {
                            "project_id": row["project_id"],
                            "project_name": row["project_name"],
                            "category": row["category"],
                            "funding_goal": float(row["funding_goal"]),
                            "deadline": row["deadline"],
                            "current_funding": float(row["current_funding"])
                        }
        except Exception as e:
            print(f"Error reading project info: {e}")
        return None

    @staticmethod
    def validatePledgeAmount(amount, reward_id):
        reward_info = BusinessRules.getRewardInfo(reward_id)
        if not reward_info:
            return False, "Reward not found"

        if amount < reward_info["min_amount"]:
            return False, f"Minimum amount for this reward is ${reward_info['min_amount']:,.2f}"

        return True, "Amount is valid"

    @staticmethod
    def checkRewardQuota(reward_id):
        reward_info = BusinessRules.getRewardInfo(reward_id)
        if not reward_info:
            return False, "Reward not found"

        # นับจำนวน pledge ที่ successful สำหรับรางวัลนี้
        successful_count = 0
        try:
            with open(r'Data/Pledges.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["reward_id"] == str(reward_id) and row["status"] == "Success":
                        successful_count += 1
        except Exception:
            pass

        remaining_quota = reward_info["quota"] - successful_count
        if remaining_quota <= 0:
            return False, "Reward quota is full"

        return True, f"Remaining quota: {remaining_quota}"

    @staticmethod
    def checkProjectDeadline(project_id):
        project_info = BusinessRules.getProjectInfo(project_id)
        if not project_info:
            return False, "Project not found"

        if not BusinessRules.validateProjectDeadline(project_info["deadline"]):
            return False, f"Project deadline ({project_info['deadline']}) has passed"

        return True, "Project is still active"

    @staticmethod
    def validatePledge(user_id, project_id, amount, reward_id):
        errors = []

        # 1. ตรวจสอบว่าโครงการยังไม่หมดเขต
        is_valid, message = BusinessRules.checkProjectDeadline(project_id)
        if not is_valid:
            errors.append(message)

        # 2. ตรวจสอบจำนวนเงินขั้นต่ำ
        is_valid, message = BusinessRules.validatePledgeAmount(amount, reward_id)
        if not is_valid:
            errors.append(message)

        # 3. ตรวจสอบโควตารางวัล
        is_valid, message = BusinessRules.checkRewardQuota(reward_id)
        if not is_valid:
            errors.append(message)

        # 4. ตรวจสอบว่ารางวัลเป็นของโครงการนี้
        reward_info = BusinessRules.getRewardInfo(reward_id)
        if reward_info and reward_info["project_id"] != str(project_id):
            errors.append("Reward does not belong to this project")

        return len(errors) == 0, errors

    @staticmethod
    def updateProjectFunding(project_id, amount):
        try:
            # อ่านข้อมูลปัจจุบัน
            projects = []
            with open(r'Data/Projects.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                projects = list(reader)

            # อัปเดตยอดเงิน
            for project in projects:
                if project["project_id"] == str(project_id):
                    current_funding = float(project["current_funding"])
                    project["current_funding"] = str(current_funding + amount)
                    break

            # เขียนกลับไฟล์
            with open(r'Data/Projects.csv', 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ["project_id", "project_name", "category", "funding_goal", "deadline", "current_funding"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(projects)

            return True
        except Exception as e:
            print(f"Error updating project funding: {e}")
            return False

    @staticmethod
    def updateRewardQuota(reward_id):
        try:
            # อ่านข้อมูลปัจจุบัน
            rewards = []
            with open(r'Data/RewardTier.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                rewards = list(reader)

            # ลดโควตา
            for reward in rewards:
                if reward["reward_id"] == str(reward_id):
                    current_quota = int(reward["quota"])
                    reward["quota"] = str(max(0, current_quota - 1))
                    break

            # เขียนกลับไฟล์
            with open(r'Data/RewardTier.csv', 'w', newline="", encoding="utf-8") as csvfile:
                fieldnames = ["reward_id", "project_id", "reward_name", "min_amount", "quota"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rewards)

            return True
        except Exception as e:
            print(f"Error updating reward quota: {e}")
            return False

    @staticmethod
    def processPledge(user_id, project_id, amount, reward_id):
        # ตรวจสอบความถูกต้อง
        is_valid, errors = BusinessRules.validatePledge(user_id, project_id, amount, reward_id)

        if is_valid:
            # สำเร็จ - อัปเดตยอดเงินและโควตา
            if BusinessRules.updateProjectFunding(project_id, amount):
                if BusinessRules.updateRewardQuota(reward_id):
                    return "Success", "Pledge processed successfully"
                else:
                    return "Rejected", "Failed to update reward quota"
            else:
                return "Rejected", "Failed to update project funding"
        else:
            # ปฏิเสธ - ส่งคืนเหตุผล
            return "Rejected", "; ".join(errors)

    @staticmethod
    def getRejectionCount(user_id):
        count = 0
        try:
            with open(r'Data/Pledges.csv', 'r', newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["user_id"] == str(user_id) and row["status"] == "Rejected":
                        count += 1
        except Exception:
            pass
        return count