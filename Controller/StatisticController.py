from Model.csvParser import loadPledges

class StatisticController:
    def __init__(self):
        self.pledges = loadPledges()

    def getStatistics(self):
        success_count = sum(1 for p in self.pledges if p.get("status") == "Success")
        rejected_count = sum(1 for p in self.pledges if p.get("status") == "Rejected")
        return success_count, rejected_count