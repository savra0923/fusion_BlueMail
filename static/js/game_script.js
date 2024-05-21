const socket = io();
  
const cells = document.querySelectorAll('.cell');
const resultDiv = document.getElementById('result');
const restartButton = document.getElementById('restartButton');
const playerXScoreSpan = document.getElementById('playerXScore');
const playerOScoreSpan = document.getElementById('playerOScore');
const drawScoreSpan = document.getElementById('drawScore');
  
let playerXScore = 0;
let playerOScore = 0;
let drawScore = 0;

cells.forEach((cell) => {
  cell.addEventListener('click', () => {
    const row = cell.dataset.row;
    const col = cell.dataset.col;
    if (cell.textContent === '') {
      socket.emit('make_move', { row: parseInt(row), col: parseInt(col) });
    }
  });
});
  
socket.on('move_made', (data) => {
  const cell = document.querySelector(`.cell[data-row="${data.row}"][data-col="${data.col}"]`);
  cell.textContent = data.player;
});
  
socket.on('game_won', (data) => {
  resultDiv.textContent = `Player ${data.winner} wins!`;
  if (data.winner === 'X') {
    playerXScore++;
    playerXScoreSpan.textContent = playerXScore;
  } else {
    playerOScore++;
    playerOScoreSpan.textContent = playerOScore;
  }
});
  
socket.on('game_drawn', () => {
  resultDiv.textContent = "It's a draw!";
  drawScore++;
  drawScoreSpan.textContent = drawScore;
});
  
restartButton.addEventListener('click', () => {
  socket.emit('restart_game');
});
  
socket.on('game_restarted', () => {
  resultDiv.textContent = '';
  cells.forEach((cell) => {
    cell.textContent = '';
  });
});