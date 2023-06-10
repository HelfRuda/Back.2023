class SpamCheck:
    SPAM_WORDS = [
    "быстро заработать",
    "легкие деньги",
    "спам",
    "виагра",
    "сиалис",
    "онлайн аптека",
    "Нигерийский принц",
    "лотерея",
    "наследство",
    "заработок на дому",
    "работа на дому",
    "похудение",
    "диетические таблетки",
    "знакомства"
]

    @classmethod
    def is_spam(cls, text):
        for word in cls.SPAM_WORDS:
            if word in text.lower():
                return True
        return False