
class Card():
    """Contains a given word's info as listed in the NYT 'card' entries.
       Named for how each word is presented in the game, i.e. on cards.
    """
    def __init__(self, content : str, position : int):
        self.content = content
        self.position = position

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


class Category():
    def __init__(self):
        pass


