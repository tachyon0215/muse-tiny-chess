# muse-tiny-chess

A chess engine in 4 KB of Python, entered in make.fun tiny-chess-01.

## Design

Three designs were compared against the competition's scoring (8 games per
trial against a fixed gauntlet, 10 seconds per move, deterministic replay):

1. A bitboard engine: fast per node in C, but in pure Python the move
   generator is long and slow to write correctly in the byte budget.
2. A mailbox engine with material-only evaluation: short, but too weak.
3. A mailbox engine with piece-square tables, alpha-beta search,
   quiescence over captures, a transposition table, null-move pruning and
   late-move reductions, packed with LZMA (chosen): the strongest design
   that fits 4,096 bytes, using the packing the rules expressly allow.

The readable source is `src.py`; `main.py` is what
`makefun compress src.py` makes of it. The engine searches to a fixed
node budget (never a clock), so replays play the same moves.

## Play

The engine talks to the env at `MAKEFUN_ENV_URL`: it asks for the game
in play with POST /game and answers each position with POST /move.
If its chosen move is ever refused, it falls back to the first legal
move the env lists, so a game is never lost to a protocol error.
