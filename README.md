#Connect 4 Game
Example of the popular Connect4 game implemented as an API on the Google App Engine (GAE)

## Set-Up Instructions:
1.  Update the value of application in app.yaml to the app ID you have registered in the App Engine admin console and would like to use to host your instance of this sample.
1.  Run the app with the devserver using dev_appserver.py DIR, and ensure it's running by visiting the API Explorer - by default ocalhost:8080/_ah/api/explorer.
 
##Game Description:
Connect 4 is two player connection game in which the players first choose a color and then take turns dropping colored discs from the top into a seven-column, six-row vertically suspended grid.
The pieces fall straight down, occupying the next available space within the column. 
The objective of the game is to connect four of one's own discs of the same color next to each other vertically, horizontally, or diagonally before your opponent. Connect Four is a strongly solved game. 
The first player can always win by playing the right moves.

Each player makes their move via the `make_move` endpoint which will reply
with either: 'next player turn', 'you win', or 'game over' (if no more moves can be made).

Many different Guess a Number games can be played by many different 
Users at any given time. Each game can be retrieved or played by using 
the path parameter `urlsafe_game_key`.

##Files Included:
 - api.py: Contains endpoints and game playing logic.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for taskqueue handler.
 - models.py: Entity and message definitions including helper methods.
 - utils.py: Helper function for retrieving ndb.Models by urlsafe Key string.
 
 ##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: user_name, email
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. user_name provided must be unique. Will 
    raise a ConflictException if a User with that user_name already exists.
    
 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: player1_user_name, player2_user_name
    - Returns: GameForm with initial game state and which player will play first
    - Description: Creates a new Game. player1_ and player2_user_names provided 
    must correspond to an existing user - will raise a NotFoundException if not. 
    Randomises which player is to play first.
    

 