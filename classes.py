import utils

class Referral:
    def __init__(self, identifier, referral, amount, percent):
        self.identifier = utils.escape_markdown(identifier)
        self.referral = referral
        self.amount = amount
        self.percent = percent