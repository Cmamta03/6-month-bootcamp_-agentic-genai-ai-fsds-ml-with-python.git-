import streamlit as st
import copy

# === Board Colors ===
LIGHT_SQUARE = '#f0f0f0'   # White
DARK_SQUARE = '#4caf50'    # Green
SELECTED_SQUARE = '#f7ec6f'  # Yellow highlight
LEGAL_MOVE_SQUARE = '#7fffd4' # Aqua highlight

# Unicode chess pieces
PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    '.': ' '
}

# Initial board setup
START_BOARD = [
    list('rnbqkbnr'),
    list('pppppppp'),
    list('........'),
    list('........'),
    list('........'),
    list('........'),
    list('PPPPPPPP'),
    list('RNBQKBNR'),
]

# Helper functions for chess logic

def is_white(piece):
    return piece.isupper()

def is_black(piece):
    return piece.islower()

def get_piece(board, pos):
    row, col = pos
    return board[row][col]

def set_piece(board, pos, piece):
    row, col = pos
    board[row][col] = piece

def in_bounds(pos):
    row, col = pos
    return 0 <= row < 8 and 0 <= col < 8

def get_moves(board, pos):
    # Returns a list of legal moves for the piece at pos
    piece = get_piece(board, pos)
    moves = []
    if piece == '.':
        return moves
    directions = []
    row, col = pos
    if piece.lower() == 'p':
        # Pawn moves
        dir = -1 if is_white(piece) else 1
        start_row = 6 if is_white(piece) else 1
        # Forward
        next_row = row + dir
        if in_bounds((next_row, col)) and get_piece(board, (next_row, col)) == '.':
            moves.append((next_row, col))
            # Double move from start
            if row == start_row:
                next_row2 = row + 2*dir
                if in_bounds((next_row2, col)) and get_piece(board, (next_row2, col)) == '.':
                    moves.append((next_row2, col))
        # Captures
        for dc in [-1, 1]:
            next_col = col + dc
            if in_bounds((next_row, next_col)):
                target = get_piece(board, (next_row, next_col))
                if target != '.' and is_white(piece) != is_white(target):
                    moves.append((next_row, next_col))
    elif piece.lower() == 'n':
        # Knight moves
        for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
            nr, nc = row+dr, col+dc
            if in_bounds((nr, nc)):
                target = get_piece(board, (nr, nc))
                if target == '.' or is_white(piece) != is_white(target):
                    moves.append((nr, nc))
    elif piece.lower() == 'b':
        # Bishop moves
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            for i in range(1,8):
                nr, nc = row+dr*i, col+dc*i
                if not in_bounds((nr, nc)):
                    break
                target = get_piece(board, (nr, nc))
                if target == '.':
                    moves.append((nr, nc))
                elif is_white(piece) != is_white(target):
                    moves.append((nr, nc))
                    break
                else:
                    break
    elif piece.lower() == 'r':
        # Rook moves
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            for i in range(1,8):
                nr, nc = row+dr*i, col+dc*i
                if not in_bounds((nr, nc)):
                    break
                target = get_piece(board, (nr, nc))
                if target == '.':
                    moves.append((nr, nc))
                elif is_white(piece) != is_white(target):
                    moves.append((nr, nc))
                    break
                else:
                    break
    elif piece.lower() == 'q':
        # Queen moves
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)]:
            for i in range(1,8):
                nr, nc = row+dr*i, col+dc*i
                if not in_bounds((nr, nc)):
                    break
                target = get_piece(board, (nr, nc))
                if target == '.':
                    moves.append((nr, nc))
                elif is_white(piece) != is_white(target):
                    moves.append((nr, nc))
                    break
                else:
                    break
    elif piece.lower() == 'k':
        # King moves
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row+dr, col+dc
                if in_bounds((nr, nc)):
                    target = get_piece(board, (nr, nc))
                    if target == '.' or is_white(piece) != is_white(target):
                        moves.append((nr, nc))
    return moves

# Streamlit UI

def main():
    st.set_page_config(page_title="Chess Board Game", page_icon="♟️", layout="centered")
    st.title("♟️ Chess Board Game")
    st.markdown("---")

    if 'board' not in st.session_state:
        st.session_state.board = copy.deepcopy(START_BOARD)
        st.session_state.selected = None
        st.session_state.turn_white = True
        st.session_state.legal_moves = []
        st.session_state.move_history = []

    board = st.session_state.board
    selected = st.session_state.selected
    turn_white = st.session_state.turn_white
    legal_moves = st.session_state.legal_moves

    def square_color(row, col):
        base = LIGHT_SQUARE if (row+col)%2==0 else DARK_SQUARE
        if selected == (row, col):
            return SELECTED_SQUARE
        elif (row, col) in legal_moves:
            return LEGAL_MOVE_SQUARE
        else:
            return base

    st.write(f"Turn: {'White' if turn_white else 'Black'}")

    # Chess board grid
    for row in range(8):
        cols = st.columns(8)
        for col in range(8):
            piece = board[row][col]
            btn_label = PIECES.get(piece, '?')
            btn_color = square_color(row, col)
            if cols[col].button(btn_label, key=f"{row}-{col}", help=f"{row},{col}", use_container_width=True, 
                                args=None, kwargs=None, type="secondary", disabled=False, 
                                ):  # type and disabled for future customizability
                if selected is None:
                    # Select a piece
                    if piece != '.' and ((turn_white and is_white(piece)) or (not turn_white and is_black(piece))):
                        st.session_state.selected = (row, col)
                        st.session_state.legal_moves = get_moves(board, (row, col))
                else:
                    # Try to move
                    if (row, col) in legal_moves:
                        # Move piece
                        from_row, from_col = selected
                        to_row, to_col = row, col
                        moving_piece = board[from_row][from_col]
                        captured = board[to_row][to_col]
                        board[to_row][to_col] = moving_piece
                        board[from_row][from_col] = '.'
                        st.session_state.move_history.append(((from_row, from_col), (to_row, to_col), moving_piece, captured))
                        st.session_state.turn_white = not turn_white
                    st.session_state.selected = None
                    st.session_state.legal_moves = []

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset Game"):
            st.session_state.board = copy.deepcopy(START_BOARD)
            st.session_state.selected = None
            st.session_state.turn_white = True
            st.session_state.legal_moves = []
            st.session_state.move_history = []
    with col2:
        if st.button("Undo Move") and st.session_state.move_history:
            last = st.session_state.move_history.pop()
            (from_row, from_col), (to_row, to_col), moving_piece, captured = last
            board[from_row][from_col] = moving_piece
            board[to_row][to_col] = captured
            st.session_state.turn_white = not st.session_state.turn_white
            st.session_state.selected = None
            st.session_state.legal_moves = []

    st.write("**How to play:** Click a piece to select, then click a highlighted square to move. Undo and reset are available. No check/checkmate logic yet.")

if __name__ == "__main__":
    main()