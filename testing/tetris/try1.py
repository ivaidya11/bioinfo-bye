#this is an actual tetris game
import tetris
game = tetris.BaseGame(board_size=(4, 4), seed=128)
game.queue
for _ in range(4): game.hard_drop()

game.playing
print(game)
