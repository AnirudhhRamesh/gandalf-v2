class Character:
    """
    Represents a character in the game.
    """

    def __init__(self, id, emoji, name, quote, description, message, bot_behaviour, bot_rules, secret, current_level):
        """
        Initialize a character object with the provided attributes.

        Args:
            id (str): Unique identifier for the character.
            emoji (str): Emoji representation of the character.
            name (str): Name of the character.
            quote (str): Character's famous quote.
            description (str): A brief description of the character's role in the game.
            message (str): Message from the character to the player.
            bot_behaviour (str): Behavior of the character as a chatbot.
            bot_rules (list): List of rules that define how the character responds in different levels.
            secret (list): List of secrets associated with the character's levels.
            current_level (int): The current level of the character.
        """
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
        """
        Return a string representation of the character's attributes.
        """
        return f"Character: {self.name}\n" \
               f"Emoji: {self.emoji}\n" \
               f"Quote: {self.quote}\n" \
               f"Description: {self.description}\n" \
               f"Message: {self.message}\n" \
               f"Current Level: {self.current_level}\n" \
               f"Total Levels: {self.total_levels}\n" \
               f"GPT Descriptions: {self.bot_rules}\n" \
               f"Secret: {self.secret}\n"

    def serialize(self):
        """
        Serialize the character object to a dictionary.

        Returns:
            dict: A dictionary representation of the character.
        """
        return {
            "id": self.id,
            "emoji": self.emoji,
            "name": self.name,
            "quote": self.quote,
            "description": self.description,
            "message": self.message,
            "bot_behaviour": self.bot_behaviour,
            "bot_rules": self.bot_rules,
            "secret": self.secret,
            "current_level": self.current_level,
            "total_levels": self.total_levels
        }

    @classmethod
    def deserialize(cls, data):
        """
        Deserialize a dictionary into a Character object.

        Args:
            data (dict): A dictionary representing a character.

        Returns:
            Character: A Character object.
        """
        return cls(
            id=data["id"],
            emoji=data["emoji"],
            name=data["name"],
            quote=data["quote"],
            description=data["description"],
            message=data["message"],
            bot_behaviour=data["bot_behaviour"],
            bot_rules=data["bot_rules"],
            secret=data["secret"],
            current_level=data["current_level"]
        )
