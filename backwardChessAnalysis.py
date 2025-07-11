############################################################
# Explore alternatives to apparent "best answer" provided
#  by Stockfish
############################################################
import chess.pgn

from modelBackward import *

# Dynamically set memory -- first find out how much we have
with open('/proc/meminfo') as f:
    meminfo = f.read()
matched = re.search(r'^MemTotal:\s+(\d+)', meminfo)
if matched:
    mem_total_kB = int(matched.groups()[0])
    print("Total memory kb:", mem_total_kB)

calcTime = 55000

# Another interesting position Short v. Khalifman -- e5!!!
# inputFen = '2q1r1k1/pp2ppbp/3pbnp1/6B1/4P1PR/1NP2P2/P1PQ4/2K4R w - - 0 22'
# inputFen = '5bk1/1rq2p1p/p2pb1p1/1r2p1P1/N1p1Pn1P/P1N1BP2/KPP2Q2/1R5R b - - 8 27'
inputFen = 'r2qkb1r/pp3ppp/2n1p1n1/5b2/2BP1B2/2N2N2/PP3PPP/R2QK2R w KQkq - 1 10'

# first two best ideas
board1 = chess.Board(inputFen)
board2 = chess.Board(inputFen)
# Next level analysis
board11 = chess.Board(inputFen)
board12 = chess.Board(inputFen)
board13 = chess.Board(inputFen)
board21 = chess.Board(inputFen)
board22 = chess.Board(inputFen)
board23 = chess.Board(inputFen)

print(board1)
# white = (game.ply() % 2) == 0
print('input FEN: ', inputFen)

stockfish = Stockfish(path="/home/hugh/Downloads/Stockfish/src/stockfish")
stockfish.set_fen_position(board1.fen())
stockfish.set_hash(int(mem_total_kB * 0.00072075))
answers = stockfish.get_best_move_time(calcTime)
print(answers['stats'])
ans = board1.variation_san([chess.Move.from_uci(m) for m in answers['PV']])
print(answers['best'])
altMove = stockfish.get_top_moves(num_top_moves=5)
print("======================Alternatives=================================")
print(altMove[0])
print(altMove[1])
print(altMove[2])
print(altMove[3])
print(altMove[4])

board1.push_san(answers['best'][1])
board11.push_san(answers['best'][1])
board12.push_san(answers['best'][1])
board13.push_san(answers['best'][1])

# It's possible the first listed alternative doesn't equal
#    the actual best move calculated above, so we check
if altMove[0]['Move'] == answers['best'][1]:
    bmove2 = altMove[1]['Move']
    board2.push_san(altMove[1]['Move'])
    board21.push_san(altMove[1]['Move'])
    board22.push_san(altMove[1]['Move'])
    board23.push_san(altMove[1]['Move'])
else:
    bmove2 = altMove[0]['Move']
    board2.push_san(altMove[0]['Move'])
    board21.push_san(altMove[0]['Move'])
    board22.push_san(altMove[0]['Move'])
    board23.push_san(altMove[0]['Move'])

print(board1.fen())
print(board2.fen())

# Explore branch 1
print("=======================================================")
print("Examine responses to ", answers['best'][1])
stockfish.set_fen_position(board1.fen())
altMove2 = stockfish.get_top_moves(num_top_moves=3)

board11.push_san(altMove2[0]['Move'])
stockfish.set_fen_position(board11.fen())
answers11 = stockfish.get_best_move_time(calcTime)
print("investigating response ", altMove2[0]['Move'])
print(answers11['stats'])

board12.push_san(altMove2[1]['Move'])
stockfish.set_fen_position(board12.fen())
answers12 = stockfish.get_best_move_time(calcTime)
print("investigating response ", altMove2[1]['Move'])
print(answers12['stats'])

if len(altMove2) > 2:
    board13.push_san(altMove2[2]['Move'])
    stockfish.set_fen_position(board13.fen())
    answers13 = stockfish.get_best_move_time(calcTime)
    print("investigating response ", altMove2[2]['Move'])
    print(answers13['stats'])

# Explore branch 2
print("=======================================================")
print("Examine responses to ", bmove2)
stockfish.set_fen_position(board2.fen())
altMove3 = stockfish.get_top_moves(num_top_moves=3)

board21.push_san(altMove3[0]['Move'])
stockfish.set_fen_position(board21.fen())
answers21 = stockfish.get_best_move_time(calcTime)
print("investigating response ", altMove3[0]['Move'])
print(answers21['stats'])

board22.push_san(altMove3[1]['Move'])
stockfish.set_fen_position(board22.fen())
answers22 = stockfish.get_best_move_time(calcTime)
print("investigating response ", altMove3[1]['Move'])
print(answers22['stats'])

if len(altMove3) > 2:
    board23.push_san(altMove3[2]['Move'])
    stockfish.set_fen_position(board23.fen())
    answers23 = stockfish.get_best_move_time(calcTime)
    print("investigating response ", altMove3[2]['Move'])
    print(answers23['stats'])

stockfish.send_quit_command()
