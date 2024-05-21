import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

board = [[None, None, None],
         [None, None, None],
         [None, None, None]]

current_player = 'X'

def check_win(board, player):
    # Check rows
    for row in board:
        if row.count(player) == 3:
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    if all(cell is not None for row in board for cell in row):
        return 'draw'
    return False

def reset_game():
    global board, current_player
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    current_player = 'X'
    
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('make_move')
def handle_move(data):
    global board, current_player
    row, col = data['row'], data['col']
    if board[row][col] is None:
        board[row][col] = current_player
        emit('move_made', {'row': row, 'col': col, 'player': current_player}, broadcast=True)

        result = check_win(board, current_player)
        if result == True:
            emit('game_won', {'winner': current_player}, broadcast=True)
        elif result == 'draw':
            emit('game_drawn', {}, broadcast=True)
        else:
            current_player = 'O' if current_player == 'X' else 'X'

@socketio.on('restart_game')
def restart_game():
    reset_game()
    emit('game_restarted', {}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)