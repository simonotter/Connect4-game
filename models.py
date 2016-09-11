from protorpc import messages
from google.appengine.ext import ndb
import random
from datetime import date


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)


class Board:
    BOARD_WIDTH, BOARD_HEIGHT = 7, 6
    EMPTY_SLOT = 'X'

    def __init__(self):
        # TODO: Udacity Reviewer, is there a better structure to avoid later
        # having to refer to game.board.board (e.g. board twice!)
        self.board = [[self.EMPTY_SLOT for x in range(self.BOARD_WIDTH)]
                      for y in range(self.BOARD_HEIGHT)]

    def update(self, col, player_token):
        col -= 1
        for row in range(self.BOARD_HEIGHT):
            if self.board[row][col] is self.EMPTY_SLOT:
                self.board[row][col] = player_token
                return True  # Move has been successful
        return False  # Move has been unsuccessful

    def visual_board(self):
        """Returns a string rendered visual of the game board"""
        row_string = ''
        row_string += ''.join(self.board[self.BOARD_HEIGHT - 1]) + '|'
        row_string += ''.join(self.board[self.BOARD_HEIGHT - 2]) + '|'
        row_string += ''.join(self.board[self.BOARD_HEIGHT - 3]) + '|'
        row_string += ''.join(self.board[self.BOARD_HEIGHT - 4]) + '|'
        row_string += ''.join(self.board[self.BOARD_HEIGHT - 5]) + '|'
        row_string += ''.join(self.board[self.BOARD_HEIGHT - 6]) + '|'

        return row_string

    def is_won(self):
        # check for horizontal winning rows
        for row in range(self.BOARD_HEIGHT):
            row_string = ''.join(self.board[row])
            if row_string.find('RRRR') != -1 or row_string.find('YYYY') != -1:
                return True  # found winning horizontal row

        # check for vertical winning rows
        for col in range(self.BOARD_WIDTH):
            column_string = ''
            for row in range(self.BOARD_HEIGHT):
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


class History(ndb.Model):
    move_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    user = ndb.KeyProperty(required=True, kind='User')
    column = ndb.IntegerProperty(required=True)
    board_state_after_move = ndb.PickleProperty(required=True)


class HistoryForm(messages.Message):
    """ScoreForm for outbound Score information"""
    move_date = messages.StringField(1, required=True)
    user_name = messages.StringField(2, required=True)
    column = messages.IntegerField(3, required=True)
    board_state = messages.StringField(4, required=True)


class HistoryForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(HistoryForm, 1, repeated=True)


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
    history = ndb.StructuredProperty(History, repeated=True)

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

            # Update winning user rank
            user_rank = UserRank.query(
                UserRank.user_name == self.whose_turn).get()
            if not user_rank:
                user_rank = UserRank()
                user_rank.user_name = self.whose_turn
                user_rank.games_played = 1
                user_rank.games_won = 1
            else:
                user_rank.games_played += 1
                user_rank.games_won += 1
            user_rank.win_ratio = user_rank.games_won / (user_rank.
                                                         games_played + 0.0)
            user_rank.put()

            # Update losing user rank
            user_rank = UserRank.query(
                UserRank.user_name == loser).get()
            if not user_rank:
                user_rank = UserRank()
                user_rank.user_name = loser
                user_rank.games_played = 1
                user_rank.games_won = 0
            else:
                user_rank.games_played += 1

            user_rank.win_ratio = user_rank.games_won / (user_rank.
                                                         games_played + 0.0)
            user_rank.put()

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

    def history_to_form(self):
        """Returns a series of History Forms"""
        forms = HistoryForms()
        for history in self.history:
            form = HistoryForm()
            form.move_date = str(history.move_date)
            form.user_name = history.user.get().name
            form.column = history.column
            print str(history.board_state_after_move)
            form.board_state = str(history.board_state_after_move)
            forms.items.append(form)
        return forms


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


class UserRank(ndb.Model):
    """User rank object"""
    user_name = ndb.KeyProperty(required=True, kind='User')
    games_played = ndb.IntegerProperty(required=True)
    games_won = ndb.IntegerProperty(required=True)
    win_ratio = ndb.FloatProperty(required=True)

    def to_form(self):
        return UserRankForm(user_name=self.user_name.get().name,
                            games_played=self.games_played,
                            games_won=self.games_won,
                            win_ratio=self.win_ratio)


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


class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)


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


class UserRankForm(messages.Message):
    """UserRankForm for outbound user rank information"""
    user_name = messages.StringField(1, required=True)
    games_played = messages.IntegerField(2, required=True)
    games_won = messages.IntegerField(3, required=True)
    win_ratio = messages.FloatField(4, required=True)


class UserRankForms(messages.Message):
    """Return multiple UserRankForms"""
    items = messages.MessageField(UserRankForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)