---

# Multiplayer Game Lobby Application

This application is a multiplayer lobby system built using Flask, Flask-SocketIO, and duckDB for database operations. It allows players to connect to different lobbies and interact in real-time.

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system
- pip package manager installed

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd multiplayer-lobby-app
   ```

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To run the application, follow these steps:

 Start the Flask application:
   ```bash
   python server.py
   ```
   or

use gunicorn and wsgi script to run server: 
'''bash
gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
'''



3. Access the application in your web browser at `http://localhost:5000`.

## Application Structure

The application consists of the following components:

- **app.py**: Main Flask application file containing routes, SocketIO event handlers, and database operations.
  
- **templates/**: Directory containing HTML templates for rendering different pages (`home.html`, `lobby.html`).

- **static/**: Directory for static assets like CSS stylesheets, JavaScript files, and images.

- **requirements.txt**: File listing all Python dependencies for the application.

## Features

- **Lobby Creation**: Players can create new lobbies with specified minimum and maximum sizes.
  
- **Player Management**: Adding and removing players from lobbies dynamically.

- **Real-time Communication**: SocketIO enables real-time communication between players in the same lobby.

- **Database Integration**: Uses duckDB for lightweight database operations to store lobby and player data.
- this database features 3 tables:
-  lobby: stores the id, curr players, min players, max players, and whether a game started or not
-  player: stores the id of each player (session ID number)
-  mappings: stores the keys of each lobbyid and playerid to show who is in each lobby

## Usage

- **Home Page**: Visit the home page (`/`) to view available lobbies and join or create new lobbies.

- **Lobby Page**: Navigate to a specific lobby (`/lobby/<lobbyId>`) to interact with other players in real-time.

## Dependencies

- Flask
- Flask-SocketIO
- Flask-Cors
- duckDB
- gunicorn

##NOTE:
* Although this application is not fully functional, there is a working front-end server functioning.
* In addition, the backend lightweight duckDB database works properly, and has a series of functions in server.py that interact with the database
* Although the functions are not called to work with the server, the logic and socket libraries needed for these functions are logically sound.
