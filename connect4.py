import endpoints
from protorpc import remote, messages
from models import User, Game
from models import StringMessage, NewGameForm, GameForm

API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
EMAIL_SCOPE = endpoints.EMAIL_SCOPE

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)


@endpoints.api(name='connect4',
               version='v1',
               allowed_client_ids=[API_EXPLORER_CLIENT_ID],
               scopes=[EMAIL_SCOPE])
class ConnectFourApi(remote.Service):
    """Connect Four API v0.1"""

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
            request.user_name))

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates a new Game"""
        try:
            game = Game.new_game(request.player1, request.player2)
        except ValueError:
            raise endpoints.BadRequestException('Invalid player objects')

        return game.to_form("Good luck. It\'s %s\'s turn" % game.whose_turn.get().name)


# registers API
api = endpoints.api_server([ConnectFourApi])