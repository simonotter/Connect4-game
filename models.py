from protorpc import messages
from google.appengine.ext import ndb
import random
from datetime import date


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)


class Board:
    width, height = 7, 6

    def __init__(self):
        self.board = [['X' for x in range(self.width)]
                      for y in range(self.height)]

    def update(self, col, colour):
        for row in range(self.height):
            if self.board[row][col - 1] is 'X':
                self.board[row][col - 1] = colour
                return True  # Move has been successful
        """ TODO: Udacity Reviewer, is the above the best way to structure the
                conditional logic and returns. It works, but I don't feel it is easy
                to understand """
        return False  # Move has been unsuccessful

    def visual_board(self):
        """Returns a string rendered visual of the game board"""
        row_string = ''
        #for row in range(6, self.width-1):
        row_string += ''.join(self.board[self.height - 1]) + '|'
        row_string += ''.join(self.board[self.height - 2]) + '|'
        row_string += ''.join(self.board[self.height - 3]) + '|'
        row_string += ''.join(self.board[self.height - 4]) + '|'
        row_string += ''.join(self.board[self.height - 5]) + '|'
        row_string += ''.join(self.board[self.height - 6]) + '|'

        return row_string

    def is_won(self):
        # check for horizontal winning rows
        for row in range(self.height):
            row_string = ''.join(self.board[row])
            if row_string.find('RRRR') != -1 or row_string.find('YYYY') != -1:
                return True  # found winning horizontal row

        # check for vertical winning rows
        for col in range(self.width):
            column_string = ''
            for row in range(self.height):
                column_string += self.board[row][col]
            if column_string.find('RRRR') != -1 or column_string.find('YYYY') != -1:
                return True  # found winning vertical row

        # check for diagonal winning rows (bottom left to top right)
        # TODO: This can be done much more efficiently!
        diagonal_string = ''
        for col in range(3, 7):
            diagonal_string += self.board[col - 3][col]
        if diagonal_string.find('RRRR') != -1 or \
                diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        for col in range(2, 7):
            diagonal_string += self.board[col - 2][col]
        if diagonal_string.find('RRRR') != -1 or \
                diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        for col in range(1, 7):
            diagonal_string += self.board[col - 1][col]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        for col in range(0, 6):
            diagonal_string += self.board[col][col]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        for col in range(0, 5):
            diagonal_string += self.board[col + 1][col]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        for col in range(0, 4):
            diagonal_string += self.board[col + 2][col]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        # check for diagonal winning rows (top right to bottom left)
        # TODO: This can be done much more efficiently!
        diagonal_string = ''
        diagonal_string += self.board[3][0]
        diagonal_string += self.board[2][1]
        diagonal_string += self.board[1][2]
        diagonal_string += self.board[0][3]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        diagonal_string += self.board[4][0]
        diagonal_string += self.board[3][1]
        diagonal_string += self.board[2][2]
        diagonal_string += self.board[1][3]
        diagonal_string += self.board[0][4]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        diagonal_string += self.board[5][0]
        diagonal_string += self.board[4][1]
        diagonal_string += self.board[3][2]
        diagonal_string += self.board[2][3]
        diagonal_string += self.board[1][4]
        diagonal_string += self.board[0][5]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        diagonal_string += self.board[5][1]
        diagonal_string += self.board[4][2]
        diagonal_string += self.board[3][3]
        diagonal_string += self.board[2][4]
        diagonal_string += self.board[1][5]
        diagonal_string += self.board[0][6]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        diagonal_string += self.board[5][2]
        diagonal_string += self.board[4][3]
        diagonal_string += self.board[3][4]
        diagonal_string += self.board[2][5]
        diagonal_string += self.board[1][6]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row

        diagonal_string = ''
        diagonal_string += self.board[5][3]
        diagonal_string += self.board[4][4]
        diagonal_string += self.board[3][5]
        diagonal_string += self.board[2][6]
        if diagonal_string.find('RRRR') != -1 or \
                        diagonal_string.find('YYYY') != -1:
            return True  # found winning diagonal row


        return False


class Game(ndb.Model):
    """Game class"""
    player1 = ndb.KeyProperty(required=True, kind='User')
    player2 = ndb.KeyProperty(required=True, kind='User')
    player1Colour = ndb.StringProperty(required=True)
    player2Colour = ndb.StringProperty(required=True)
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

        # Randomly choose which player plays first and set token colours
        if random.choice(range(1, 3)) == 1:
            whose_turn = player1.key
            player1_colour = 'R'
            player2_colour = "Y"
        else:
            whose_turn = player2.key
            player1_colour = 'Y'
            player2_colour = "R"

        # Create board, game and put in datastore
        game = Game(player1=player1.key,
                    player2=player2.key,
                    player1Colour=player1_colour,
                    player2Colour=player2_colour,
                    whose_turn=whose_turn,
                    board=Board())
        game.put()
        return game

    def switch_turn(self):
        """Swaps who's turn it is in the game"""
        if self.whose_turn == self.player1:
            self.whose_turn = self.player2
        else:
            self.whose_turn = self.player1

    def is_won(self):
        """Checks if the game has been won"""
        return self.board.is_won()

    def end_game(self, won):
        self.game_over = True
        if won:

            # get the loser (Winner is in whose_turn)
            if self.player1 == self.whose_turn:
                loser = self.player2
            else:
                loser = self.player1

            # Add the game to the score 'board'
            score = Score(winning_user=self.whose_turn,
                          losing_user=loser,
                          date=date.today(),
                          holes_remaining=self.holes_remaining)
            score.put()

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.player1 = self.player1.get().name
        form.player2 = self.player2.get().name
        # TODO: return player colours
        form.whose_turn = self.whose_turn.get().name
        form.holes_remaining = self.holes_remaining
        form.game_over = self.game_over
        form.message = message
        form.board = str(self.board.board)
        form.visual_board = self.board.visual_board()
        return form


class Score(ndb.Model):
    """Score object"""
    winning_user = ndb.KeyProperty(required=True, kind='User')
    losing_user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    holes_remaining = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(winning_user=self.winning_user.get().name,
                         losing_user=self.losing_user.get().name,
                         date=str(self.date),
                         holes_remaining=self.holes_remaining)


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
    visual_board = messages.StringField(9, required=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    player1 = messages.StringField(1, required=True)
    player2 = messages.StringField(2, required=True)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    player = messages.StringField(1, required=True)
    column = messages.StringField(2, required=True)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    winning_user = messages.StringField(1, required=True)
    losing_user = messages.StringField(2, required=True)
    date = messages.StringField(3, required=True)
    holes_remaining = messages.IntegerField(4, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)