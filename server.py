import duckdb
import uuid
from flask import Flask, render_template, Response, request, Blueprint
from flask_socketio import join_room, leave_room, SocketIO
from flask_cors import CORS, cross_origin


app = Flask(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
# define your bluprint
blueprint = Blueprint('blueprint', __name__)

# put this sippet ahead of all your bluprints
# blueprint can also be app~~
print("FJFJFHFHJFH")
@blueprint.after_request 
def after_request(response):
    print("INITIED")

    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    # Other headers can be added here if needed
    print("THTH")
    return response

socket = SocketIO(app, logger=True, async_handlers= True, async_mode= 'threading', cors_allowed_origins="http://localhost:5000")

#class to represent lobby detail
class LobbyDetails:
    def __init__(self, curr_size, min_size, max_size, game_start):
        self.min_size = min_size
        self.max_size = max_size
        self.curr_size= curr_size
        self.game_start= "No"

#class to set the type of lobby, can be expanded upon to get more different lobbies (e.g. 2 player, 3 player)
class FourPlayer:
    def __init__(self):
        self.min_size=8
        self.max_size=64

#check for connection in 
@socket.on('connect')
def connect(auth):
    session_id = request.args.get('clientId')  # Get the custom clientId from query parameters
    if session_id:
        print("Client connected:", session_id)
        connected_clients= fetch_game_info()[1]
        if session_id not in connected_clients:
            print("New client connected!")
            connected_clients.append(session_id)  # Add the session identifier to the set of connected clients
            print(connected_clients)
            # Your existing logic for handling the new connection goes here
            playerId = session_id
            insert_player_db(playerId)
            fourplayer = FourPlayer()
            lob_det = LobbyDetails(curr_size=0, min_size=fourplayer.min_size, max_size=fourplayer.max_size, game_start="No")
            createLobby(playerId, lob_det)
            print("TRYING")
            socket.emit('my response', {'data': 'Connected'})
    else:
        print("Invalid session_id received")

def create_database():
    #CREATE duckDB database
    con= duckdb.connect("game.db")
    print("DATABASE MAKING")
    #check for tables before loading data
    try:
        con.sql("CREATE TABLE Lobby (LOBBYID VARCHAR, CURRSIZE INT, MINSIZE INT, MAXSIZE INT, GAME_START VARCHAR, PRIMARY KEY (LOBBYID))")
    except Exception as e:
        print("Error:", e)

    try:
        con.sql("CREATE TABLE Player (PLAYERID VARCHAR, PRIMARY KEY(PLAYERID))")
    except Exception as e:
        print("Error:", e)
    
    try:
        con.sql("CREATE TABLE Mappings (LOBBYID VARCHAR REFERENCES LOBBY(LOBBYID), PLAYERID VARCHAR REFERENCES PLAYER(PLAYERID), PRIMARY KEY (LOBBYID, PLAYERID))")
    except Exception as e:
        print("Error:", e)
    print("database created")
    con.close()

#routines to add, delete, and access items in database
def insert_lobby_db(lobbyId, lobbyDetails):
    con= duckdb.connect("game.db")
    con.execute(f"INSERT INTO Lobby VALUES ('{lobbyId}', {lobbyDetails.curr_size}, {lobbyDetails.min_size}, {lobbyDetails.max_size}, '{lobbyDetails.game_start}')")
    con.close()

def remove_lobby_db(lobbyId):
    con = duckdb.connect("game.db")
    con.execute(f"DELETE FROM Lobby WHERE LOBBYID = '{lobbyId}'")
    con.close()

def insert_player_db(playerId):
    con= duckdb.connect("game.db")
    con.execute(f"INSERT INTO Player VALUES ('{playerId}')")
    con.close()

def remove_player_db(playerId):
    con = duckdb.connect("game.db")
    con.execute(f"DELETE FROM Player WHERE PLAYERID = '{playerId}'")
    con.close()

def insert_player_lobby_db(playerId, lobbyId):
    con= duckdb.connect("game.db")
    con.execute(f"INSERT INTO Mappings VALUES ('{lobbyId}', '{playerId}')")
    con.close()

def remove_player_lobby_db(playerId, lobbyId):
    con = duckdb.connect("game.db")
    con.execute(f"DELETE FROM Mappings WHERE LOBBYID = '{lobbyId}' AND PLAYERID = '{playerId}'")
    con.close()

def fetch_game_info():
    con=duckdb.connect("game.db")
    con.table("Lobby").show()
    con.table("Player").show()
    con.table("Mappings").show()

    # Fetch lobby information
    lobby_result = con.execute("SELECT * FROM Lobby")
    lobby_info = []
    for row in lobby_result.fetchall():
        lobby_info.append(row)
    
    # Fetch player information
    player_result = con.execute("SELECT * FROM Player")
    player_info = []
    for row in player_result.fetchall():
        player_info.append(row)

    #Fetch player/lobby mappings
    mapping_result = con.execute("SELECT * FROM Mappings")
    mapping_info = []
    for row in mapping_result.fetchall():
        player_info.append(row)

    # Close the connection
    con.close()
    return lobby_info, player_info, mapping_info

def createLobby(playerId, lobbyDetails):
    lobbies={}
    #create empty lobby, add player to lobby
    lobbyId= str(uuid.uuid4())
    lobbies[lobbyId]= lobbyDetails
    insert_lobby_db(lobbyId, lobbies[lobbyId])
    print("INSERTED????")
    insert_player_lobby_db(playerId, lobbyId)

@socket.on('join')
def joinLobby(playerId, lobbyId):
    join_room(lobbyId)
    insert_player_lobby_db(playerId, lobbyId)
    send(playerId + 'has entered the lobby.', to=lobbyId)    
    print(f"Client connected with player ID: {playerId}")
    socket.emit('player_id', playerId)

@socket.on('leave')
def leaveLobby(playerId, lobbyId):
    leave_room(lobbyId)
    remove_player_lobby_db(playerId, lobbyId)
    send(player_id + ' has left the room.', to=lobbyId)
    print(f"Client left with player ID: {playerId}")
    socket.emit('player_id', playerId)

def startGame(lobbyId):
    for lobby in fetch_game_info():
        if lobby[0]==lobbyId:
            curr_lobby_size= lobby[1]
            max_lobby_size= lobby[3]
            remove_lobby_db(lobbyId)
            lob_det = LobbyDetails(curr_size=curr_lobby_size, min_size=fourplayer.min_size, max_size=fourplayer.max_size, game_start="Yes")
            insert_lobby_db(lobbyId, lob_det)
            if curr_lobby_size == max_lobby_size:
                remove_lobby_db(lobbyId)

def notifyPlayers(lobbyId, message):
    socket.emit('message', {'text': message}, room=lobbyId)


@app.route('/')
def home():
    print("HOME")
    # Redirect to the home page or render it with updated data
    # return redirect(url_for('home'))
    # Fetch lobby information
    lobby_info=fetch_game_info()[0]
    for lobby in lobby_info:
        if lobby_info[i][0]==0:
            remove_lobby_db(lobbyId)
    print(lobby_info, "LINFOOO")
    #send lobby info to template
    return render_template('home.html', data=lobby_info)   

#Lobby Details: object with lobby min size, lobby max size

@app.route('/lobby/<lobbyId>', methods=['GET', 'POST'])
def lobby(lobbyId=None):  
    lobby_info = fetch_game_info()[0]
    return render_template('lobby.html', lobbyId= lobbyId, lobby_info=lobby_info)


if __name__ == '__main__':
    print("LAUNCH")
    create_database()