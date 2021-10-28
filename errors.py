"""
These are custon errors
meant for this game
"""

#### Imports ####


class ObjNameError(Exception):
    def __init__(self, name, message):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name}: {self.message}"