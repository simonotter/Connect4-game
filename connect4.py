import endpoints
from protorpc import remote, messages
from models import User
from models import StringMessage

API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
EMAIL_SCOPE = endpoints.EMAIL_SCOPE

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))


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


# registers API
api = endpoints.api_server([ConnectFourApi])