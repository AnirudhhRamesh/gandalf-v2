class Character:
    def __init__(self, id, emoji, name, quote, description, message, bot_behaviour, bot_rules, secret, current_level):
        self.id = id
        self.emoji = emoji
        self.name = name
        self.quote = quote
        self.description = description
        self.message = message
        self.bot_behaviour = bot_behaviour
        self.bot_rules = bot_rules
        self.secret = secret
        self.current_level = current_level
        self.total_levels = len(bot_rules)

    def __str__(self):
        return f"Character: {self.name}\n" \
               f"Emoji: {self.emoji}\n" \
               f"Quote: {self.quote}\n" \
               f"Description: {self.description}\n" \
               f"Message: {self.message}\n" \
               f"Current Level: {self.current_level}\n" \
               f"Total Levels: {self.total_levels}\n" \
               f"GPT Descriptions: {self.bot_rules}\n" \
               f"Secret: {self.secret}\n"
