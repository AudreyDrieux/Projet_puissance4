"""
Minimax agent with alpha-beta pruning
"""

import time
import numpy as np
import random
#from loguru import logger


class MinimaxAgent:
    """
    Agent using minimax algorithm with alpha-beta pruning
    """
    def __init__(self, env, player_name=None):
        """
        Initialize minimax agent

        Parameters:
            env: PettingZoo environment
            depth: How many moves to look ahead
            player_name: Optional name
        """
        self.env = env
        self.depth = 4
        self.player_name = player_name or f"Minimax(d={self.depth})"
        self.POSITION_WEIGHTS = np.array([
            [10, 10 , 10 , 10 , 10 , 10 , 10],
            [10, 50 , 50 , 50 , 50 , 50 , 10],
            [10, 50 , 100, 200, 100, 50 , 10],
            [25, 50 , 100, 300, 100, 50 , 25],
            [50, 100, 200, 300, 200, 100, 50],
            [75, 100, 200, 300, 200, 100, 75],
        ])
        self.transposition = {}
        self.time_limit = 2.0
        self._deadline = None

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose action using minimax algorithm
        """
        start = time.perf_counter()
        self._deadline = start + self.time_limit

        self.transposition.clear()
        valid_actions = self._get_valid_moves(observation)
        
        # Rule 1: Win immediately
        winning_move = self._find_winning_move(observation, channel=0)
        if winning_move is not None and winning_move in valid_actions:
            return winning_move

        # Rule 2: Block opponent
        blocking_move = self._find_winning_move(observation, channel=1)
        if blocking_move is not None and blocking_move in valid_actions:
            return blocking_move
        
        # Rule 3: Block double threat
        block_double_threat = self._find_block_double_two_spot(observation, channel=0)
        if block_double_threat is not None and block_double_threat in valid_actions:
            #logger.info(f"{self.player_name}: BLOCK DOUBLE-TWO THREAT -> column {block_double_threat}")
            return block_double_threat
        
        # Rule 4: Avoid suicidal moves
        safe_actions = []
        for a in valid_actions:
            if not self._find_suicidal_move(observation, a):
                safe_actions.append(a)
        candidate_actions = safe_actions if safe_actions else valid_actions

        # Rule 5: create forced-win-in-two
        empty = np.sum((observation[:, :, 0] == 0) & (observation[:, :, 1] == 0))
        if empty <= 15 and time.perf_counter() < self._deadline:
            for a in candidate_actions:
                if time.perf_counter() > self._deadline:
                    break
                if self._is_forced_win_in_two(observation, a, channel=0):
                    #logger.debug(f"[FW2] {a}")
                    return a

        # Rule 6: Create double threat
        for a in candidate_actions:
            if self._creates_double_threat(observation, a, channel=0):
                #logger.info(f"{self.player_name}: DOUBLE THREAT -> column {a}")
                return a

        # Rule 7: Minimax
        best_action = None
        best_value = float('-inf')

        # Try each valid action
        for action in candidate_actions:
            if self._deadline is not None and time.perf_counter() > self._deadline:
                break
            # Simulate the move
            new_board = self._simulate_move(observation, action, channel=0)

            # Evaluate using minimax (opponent's turn, so minimizing)
            effective_depth = self._adaptive_depth(new_board)
            value = self._minimax(new_board, effective_depth, float('-inf'), float('inf'), False)
            #logger.debug(f"{self.player_name}: Action {action} -> minimax score {value}")

            if value > best_value:
                best_value = value
                best_action = action

        if best_action is None:
            return candidate_actions[0] if candidate_actions else valid_actions[0]
        
        return best_action if best_action is not None else random.choice(valid_actions)

    def _minimax(self, board, depth, alpha, beta, maximizing):
        """
        Minimax algorithm with alpha-beta pruning

        Parameters:
            board: Current board state
            depth: Remaining depth to search
            alpha: Best value for maximizer
            beta: Best value for minimizer
            maximizing: True if maximizing player's turn

        Returns:
            float: evaluation score
        """
        # TODO: Implement minimax
        # Base cases:
        #   - depth == 0: return evaluate(board)
        #   - game over: return win/loss score

        # Recursive case:
        #   - Try all valid moves
        #   - Recursively evaluate
        #   - Update alpha/beta
        #   - Prune if possible
        if self._deadline is not None and time.perf_counter() > self._deadline:
            return 0.0 
        
        key = (board.tobytes(), maximizing)

        if key in self.transposition:
            return self.transposition[key]
        
        if self._check_win(board, 0):
            val = 100000
            self.transposition[key] = val
            return val
        if self._check_win(board, 1):
            val = -100000
            self.transposition[key] = val
            return val
        if depth == 0:
            val = self._evaluate(board)
            self.transposition[key] = val
            return val
        
        valid_moves = self._get_valid_moves(board)
        if not valid_moves:
            val = self._evaluate(board)
            self.transposition[key] = val
            return val
        
        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                #new_board = self._simulate_move(board, col, channel=0)
                #eval = self._minimax(new_board, depth - 1, alpha, beta, False)
                row = self._make_move_inplace(board, col, channel=0)
                if row is None:
                    continue
                eval = self._minimax(board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                self._undo_move_inplace(board, col, row, channel=0)
                if beta <= alpha:
                    break
            self.transposition[key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                #new_board = self._simulate_move(board, col, channel=1)
                #eval = self._minimax(new_board, depth - 1, alpha, beta, True)
                row = self._make_move_inplace(board, col, channel=1)
                if row is None: 
                    continue
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                self._undo_move_inplace(board, col, row, channel=1)
                if beta <= alpha:
                    break
            self.transposition[key] = min_eval
            return min_eval
        
    def _get_next_row(self, board, col): 
        """
        Find which row a piece would land in if dropped in column col

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)

        Returns:
            row index (0-5) if space available, None if column full
        """
        # TODO: Implement this
        # Hint: Start from bottom row (5) and go up
        # A position is empty if board[row, col, 0] == 0 and board[row, col, 1] == 0
        for row in range(5, -1, -1): 
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row 
        return None 

    def _simulate_move(self, board, col, channel):
        """
        Simulate placing a piece without modifying original board

        Parameters:
            board: Current board (6, 7, 2)
            col: Column to play
            channel: 0 for current player, 1 for opponent

        Returns:
            new_board: Copy of board with move applied
        """
        # TODO: Implement
        # 1. Copy board
        # 2. Find next available row in column
        # 3. Place piece
        # 4. Return new board
        board1 = board.copy()
        row = self._get_next_row(board1,col)
        if row is None:
            return board1
        board1[row,col,channel] = 1
        return board1

    def _get_valid_moves(self, board):
        """
        Get list of valid column indices

        Returns:
            list of valid columns
        """
        # TODO: Check which columns aren't full
        order = [3, 2, 4, 1, 5, 0, 6]
        return [c for c in order if board[0, c, 0] == 0 and board[0, c, 1] == 0]
    
    def _find_suicidal_move(self, board, col):
        """
        Check whether playing in column `col` allows the opponent to win immediately.
        Such a move is considered suicidal.

        Returns:
            bool: True if the move leads to an immediate opponent win, otherwise False.
        """
        board_after_my_move = self._simulate_move(board, col, channel=0)
        return self._find_winning_move(board_after_my_move, channel=1) is not None

    def _count_three_in_row(self, board, channel):
        """
        Calculate the number of three-in-a-row combinations,
        and there must be at least one empty space either at the beginning or at the end of the "three-in-a-row" sequence
        
        Returns:
            int : the number of three-in-a-row
        """
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(6):
            for col in range(7):
                if board[row, col, channel] != 1: 
                    continue
                for dr, dc in directions:
                    boundary = True
                    for k in range(3): 
                        r = row + dr * k
                        c = col + dc * k
                        if not (0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1):
                            boundary = False
                            break
                    if not boundary:
                        continue
                    r_prev = row - dr
                    c_prev = col - dc
                    r_next = row + dr * 3
                    c_next = col + dc * 3
                    has_space_before = (
                        0 <= r_prev < 6 and 0 <= c_prev < 7 and
                        board[r_prev, c_prev, 0] == 0 and
                        board[r_prev, c_prev, 1] == 0
                    )
                    has_space_after = (
                        0 <= r_next < 6 and 0 <= c_next < 7 and
                        board[r_next, c_next, 0] == 0 and
                        board[r_next, c_next, 1] == 0
                    )
                    if has_space_before or has_space_after:
                        count += 1
        return count

    def _count_two_in_row(self, board, channel):
        """
        Calculate the number of two-in-a-row combinations

        Returns:
            int : the number of two-in-a-row
        """
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(6):
            for col in range(7):
                if board[row, col, channel] != 1:
                    continue
                for dr, dc in directions:
                    boundary = True
                    for k in range(2): 
                        r = row + dr * k
                        c = col + dc * k
                        if not (0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1):
                            boundary = False
                            break
                    if boundary:
                        count += 1
        return count

    def _count_pieces_in_column(self, board, channel, col):
        """
        Count how many pieces the player has in a given column.

        Returns:
            int: number of pieces belonging to the player in the given column
        """
        count = 0
        for row in range(6):
            if board[row, col, channel] == 1:
                count += 1
        return count

    def _evaluate(self, board):
        """
        Evaluate board position

        Scoring components:
          - Win / loss: +100000 / -100000
          - Opponent can win next move: -5000
          - 3-in-a-row: ours +200 each, opponent -50 each
          - 2-in-a-row: ours +20 each, opponent -10 each
          - Positional weights: add/subtract predefined cell values
          - Create double threat: +2000 (once)

        Returns:
            float: score (positive = good for us)
        """
        # TODO: Implement evaluation function
        # Consider: wins, threats, position, etc.
        score = 0
        # Check for wins
        if self._check_win(board, 0):
            return 100000

        if self._check_win(board, 1):
            return -100000
        
        # Check for loses
        if self._opponent_can_win_next(board, my_channel=0):
            score -= 5000

        # Count 3-in-a-row patterns (without the 4th piece blocked)
        my_three = self._count_three_in_row(board, 0)
        opp_three = self._count_three_in_row(board, 1)
        score += my_three * 200 - opp_three * 50

        # Count 2-in-a-row patterns
        my_two = self._count_two_in_row(board, 0)
        opp_two = self._count_two_in_row(board, 1)
        score += my_two * 20 - opp_two * 10

        my_plane = board[:, :, 0]
        opp_plane = board[:, :, 1]

        if np.any(my_plane):
            rows, cols = np.where(my_plane == 1)
            score += self.POSITION_WEIGHTS[rows, cols].sum()

        if np.any(opp_plane):
            rows, cols = np.where(opp_plane == 1)
            score -= self.POSITION_WEIGHTS[rows, cols].sum()

        return float(score)

    def _check_win(self, board, channel):
        """
        Check if player has won

        Returns:
            bool: True if won
        """
        # TODO: Check all positions for 4 in a row
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for row in range(6):
            for col in range(7):
                if board[row, col, channel] != 1:
                    continue
                for dr, dc in directions:
                    boundary = True
                    for k in range(4): 
                        r = row + dr * k
                        c = col + dc * k
                        if not (0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1):
                            boundary = False
                            break
                    if boundary:
                        return True
        return False
    
    def _find_winning_move(self, board, channel):
        """
        Find the "definitive winning move" for the current player.

        Returns:
            If a four-in-a-row pattern is formed immediately after placing a piece 
            in a certain column, return the column number; otherwise, return None.
        """
        valid_moves = self._get_valid_moves(board)
        for col in valid_moves:
            #new_board = self._simulate_move(board, col, channel=channel)
            row = self._get_next_row(board, col)
            board[row, col, channel] = 1
            
            if self._check_win(board, channel):
                board[row, col, channel] = 0
                return col
            board[row, col, channel] = 0
        return None
    
    def _opponent_can_win_next(self, board, my_channel=0):
        """
        Check whether the opponent has a winning move on their next turn.

        Returns:
            bool: True if the opponent can win immediately, otherwise False.
        """
        opp = 1 - my_channel
        return self._find_winning_move(board, opp) is not None

    def _creates_double_threat(self, board, col, channel):
        """
        Check if playing column col creates two separate winning threats

        A double threat is unbeatable because opponent can only block one.

        Returns:
            True if move creates double threat, False otherwise
        """
        row=self._get_next_row(board, col)
        if row is None:
            return False
        board1 = board.copy()
        board1[row,col,channel] = 1
        if self._check_win(board1, channel):
            return False
        count = 0
        for c in range(7):
            row2=self._get_next_row(board1, c)
            if row2 is None:
                continue
            board2 = board1.copy()
            board2[row2,c,channel] = 1
            if self._check_win(board2,channel) == True:
                count += 1
                if count >= 2:
                    return True
        return False
    
    def _is_forced_win_in_two(self, board, a, channel):
        """
        Check whether playing move `a` guarantees a win in two moves.
        
        Returns:
            bool: True if move `a` guarantees a forced win in two moves; False otherwise.
        """
        if self._deadline is not None and time.perf_counter() > self._deadline:
            return False
        board1 = self._simulate_move(board, a, channel)
        opp = 1 - channel

        for b in self._get_valid_moves(board1):
            if self._deadline is not None and time.perf_counter() > self._deadline:
                return False
            board2 = self._simulate_move(board1, b, opp)
            if self._find_winning_move(board2, channel) is None:
                return False
        return True

    def _adaptive_depth(self, board):
        """
        Adjust the search depth based on how many empty cells remain.
        Deeper search in late-game, shallower in early-game.

        Returns:
            int: The adapted search depth.
        """
        empty = np.sum((board[:, :, 0] == 0) & (board[:, :, 1] == 0))
        if empty <= 8:
            return self.depth
        elif empty <= 14:
            return self.depth - 1
        else:
            return self.depth - 1

    def _is_double_two_spot(self, board, row, col, channel):
        """
        Check whether placing a piece of `channel` at (row, col) 
        creates threats in at least two different directions,
        each forming a chain of length ≥ 2.

        Returns:
            bool: True if (row, col) is a double two-spot.
        """
        rows, cols, _ = board.shape
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        good_dirs = 0

        for dr, dc in directions:
            count = 1

            r, c = row + dr, col + dc
            while 0 <= r < rows and 0 <= c < cols and board[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc

            r, c = row - dr, col - dc
            while 0 <= r < rows and 0 <= c < cols and board[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc

            if count >= 3:
                good_dirs += 1

        return good_dirs >= 2
    
    def _find_block_double_two_spot(self, board, channel):
        """
        Find a column where the opponent would create a double two-spot
        if they play there. Used to decide blocking moves.

        Returns:
            int or None: Column index to block, or None if no threat exists.
        """
        rows, cols, _ = board.shape
        opp_channel = 1 - channel

        for col in range(cols):
            row = self._get_next_row(board, col)
            if row is None:
                continue 

            if self._is_double_two_spot(board, row, col, opp_channel):
                return col
        return None

    def _make_move_inplace(self, board, col, channel):
        """
        Place a piece for the given channel in column `col` (in-place) and return the row.
        If the column is full, return None.

        Returns:
            int or None: The row where the piece is placed, or None if the column is full.
        """
        row = self._get_next_row(board, col)
        if row is None:
            return None
        board[row, col, channel] = 1
        return row

    def _undo_move_inplace(self, board, col, row, channel):
        """
        Undo a piece placed at (row, col, channel) (in-place).

        Returns:
            None
        """
        board[row, col, channel] = 0
