
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


class Puzzle():
    def __init__(self, nyjson):
        self.status = nyjson['status']
        self.id = nyjson['id']
        self.print_date = nyjson['print_date']
        self.editor = nyjson['editor']
        self.categories = {
            category['title']: [ Card(**card) for card in category['cards'] ]
            for category in nyjson['categories']
        }

    def __repr__(self):
        return (
            f"------- {self.print_date}-------\n" +
            '\n'.join(
                ' '.join(str(card) for card in cat)
                for cat in self.categories.values()
            )
        )

    @property
    def cards(self):
        return self._list_cards()

    def _list_cards(self):
        return sorted(
            [card for cards in self.categories.values() for card in cards],
            key = lambda card: card.position
        )

    # def store_puzzle(self):
    #     self.fetcher.throw_ball()

