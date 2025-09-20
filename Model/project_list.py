class project_list:
    def __init__(self, suitId):
        self.suitId = suitId

    def isValidId(self):
        return len(self.suitId) == 6 and not self.suitId.startswith('0')

    def checkSuitHealth(self):

        if not self.isValidId():
            return False, "Invalid Suit ID format"

        return True, "The Suit is in good condition"