from protorpc import messages
from google.appengine.ext import ndb
import random


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)


class Board:
    def __init__(self):
        width, height = 7, 6
        self.board = [[0 for x in range(width)] for y in range(height)]

    def update(self, row, col, player):
        # TODO: User can't specify a row, only a column: gravity does the rest!
        if self.board[row+1][col+1] is not 0:
            raise ValueError('This position has already been filled')
        else:
            self.board[row+1][col+1] = "R"


class Game(ndb.Model):
    """Game class"""
    player1 = ndb.KeyProperty(required=True, kind='User')
    player2 = ndb.KeyProperty(required=True, kind='User')
    whose_turn = ndb.KeyProperty(required=True, kind='User')
    created = ndb.DateTimeProperty(auto_now_add=True)
    # Board is 7x6 (width x height), so 42 holes/spaces
    board = ndb.PickleProperty(required=True)
    holes_remaining = ndb.IntegerProperty(required=True, default=42)
    game_over = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def new_game(cls, user1, user2):
        """Creates and returns a new game"""
        # Check if users exist
        player1 = User.query(User.name == user1).get()
        if not player1:
            raise ValueError('Player 1 does not exist')

        player2 = User.query(User.name == user2).get()
        if not player2:
            raise ValueError('Player 2 does not exist')

        # Randomly choose which player plays first
        if random.choice(range(1, 3)) == 1:
            whose_turn = player1.key
        else:
            whose_turn = player2.key

        # Create board, game and put in datastore
        game = Game(player1=player1.key,
                    player2=player2.key,
                    whose_turn=whose_turn,
                    board=Board())
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.player1 = self.player1.get().name
        form.player2 = self.player2.get().name
        form.whose_turn = self.whose_turn.get().name
        form.holes_remaining = self.holes_remaining
        form.game_over = self.game_over
        form.message = message
        form.board = str(self.board.board)
        return form


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    player1 = messages.StringField(2, required=True)
    player2 = messages.StringField(3, required=True)
    whose_turn = messages.StringField(4, required=True)
    holes_remaining = messages.IntegerField(5, required=True)
    game_over = messages.BooleanField(6, required=True)
    message = messages.StringField(7, required=True)
    board = messages.StringField(8, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    player1 = messages.StringField(1, required=True)
    player2 = messages.StringField(2, required=True)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    player = messages.StringField(1, required=True)
    position = messages.StringField(2, required=True)