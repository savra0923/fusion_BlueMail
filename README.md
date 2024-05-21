# Fusion_BlueMail
repo for the home test interview from Fusion BlueMail
The test will be sent at 12:00 PM Israel time (21.5.2024) and I have 5 hours to complete it.
Test was received at 12:15 PM

# Instructions
To run the game: 
- Download or clone the repo.
- make sure you can run python and have flask and flask_socketio pip installed. (i.e. pip install flask flask-socketio).
- In terminal, go to the project directory.
- Run "python server.py"
- If that does not work, try "set FLASK_APP=server.py" and run again.
- Open two tab browsers of http://127.0.0.1:5000
- Enjoy the game.

# Explainations
## Game structure
HTML:
- The HTML file contains the structure of the game board, scoreboard, and restart button.
- It includes links to the CSS file for styling and the JavaScript file for game logic and socket communication.
CSS:
- The CSS file provides styles for the game board, cells, scoreboard, and buttons to make the game visually appealing.
JavaScript:
- The JavaScript file handles the game logic, user interactions, and communication with the server using Socket.IO.
Python:
- A Flask server is used to serve the HTML file and manage game state.
- The server uses Socket.IO to handle real-time communication between browsers.

## Entities used
Board:
- A 3x3 grid represented as a 2D list (array) in both the server and client-side code.
- Each cell in the grid can be None, 'X', or 'O'.
Players:
- Two players, 'X' and 'O'.
- The current player alternates between 'X' and 'O' after each valid move.
Scoreboard:
- Tracks the state of the game board, current player, and scores.
Restart Button:
- Resets the game board so a new game can be played.

## Basic flow
Game initialization:
The game starts by loading the HTML pages, which initializes the board and other UI elements.
The JavaScript code establishes a connection with the server via Socket.IO.

Making a move:
When a player clicks on a cell, the JavaScript code captures the click event and emits a make_move event to the server with the cell's coordinates.
The server receives the move, updates the game board, and checks for a win or draw conditions.

Updating the board:
If the move is valid, the server updates the game board and broadcasts the updated board state to all connected clients.
The clients update their local board display based on the server's broadcast.

Checking for win/draw conditions:
After each move, the server checks if the current player has won or if the game is a draw.
If a player wins, the server emits a game_won event with the winner's information.
If the game is a draw, the server emits a game_drawn event.

Restarting the game:
Players can restart the game by clicking the "Restart Game" button, which emits a restart_game event to the server.
The server resets the game state and broadcasts the reset state to all clients.

## How win condition is checked
After each make_move event is emited, the handle_move() function (in the python server side) updates the game board and calls the function check_win().
check_win() takes the state of the board and the curent player as arguments. Then it goes though a few loops and if statements to check the if there is a win or draw.
- It runs over each row on the board. It counts the number of the given player symbol. If there are 3 - meaning, we have a winning row - it returns true.
- It runs over each column on the board by setting the column number each time. It checks if all cells in the column are equal to each other and to the current player symbol. If they are all equal - meaning, we have a winning column - it returns true.
- It checks the diagonal of cells (0,0), (1,1), (2,2). If they equal each other and the current player's symbol - meaning, we have a winning diagonal - it returns true.
- It checks the diagonal of cells (0,2), (1,1), (2,0). If they equal each other and the current player's symbol - meaning, we have a winning diagonal - it returns true.
- If all of the cells in the board do not equal 'None', meaning the board is full and we didn't find a win. It returns 'draw'.

If the result handle_move() recieved from check_win() is True, it emits 'game_won' event.
If it recieved a 'draw', it emits 'game_drawn' event.
otherwise, it changes the current player to the next on.