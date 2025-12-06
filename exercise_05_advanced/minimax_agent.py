"""
Minimax agent with alpha-beta pruning
"""

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
            [10, 10, 10, 10, 10, 10, 10],
            [10, 50, 50, 50, 50, 50, 10],
            [10, 50, 100, 200, 100, 50, 10],
            [50, 50, 100, 200, 100, 50, 50],
            [75, 100, 200, 200, 200, 100, 75],
            [100, 100, 200, 200, 200, 100, 100],
        ])

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose action using minimax algorithm
        """
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
        
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
        
        # Rule 5: Create double threat
        for a in candidate_actions:
            if self._creates_double_threat(observation, a, channel=0):
                #logger.info(f"{self.player_name}: DOUBLE THREAT -> column {a}")
                return a

        # Rule 6: Minimax
        best_action = None
        best_value = float('-inf')

        # Try each valid action
        for action in candidate_actions:
            # Simulate the move
            new_board = self._simulate_move(observation, action, channel=0)

            # Evaluate using minimax (opponent's turn, so minimizing)
            effective_depth = self._adaptive_depth(new_board)
            value = self._minimax(new_board, effective_depth, float('-inf'), float('inf'), False)
            #logger.debug(f"{self.player_name}: Action {action} -> minimax score {value}")

            if value > best_value:
                best_value = value
                best_action = action

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
        if self._check_win(board, 0):
            return 100000
        if self._check_win(board, 1):
            return -100000
        if depth == 0:
            return self._evaluate(board)
        
        valid_moves = self._get_valid_moves(board)
        if not valid_moves:
            return self._evaluate(board)
        if maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=0)
                eval = self._minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                new_board = self._simulate_move(board, col, channel=1)
                eval = self._minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
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
        Check whether playing column `col` (as player 0) is a suicidal move.

        A move is suicidal if, after we play it, the opponent has an immediate
        winning move on their next turn.

        Returns:
            bool: True if the move is suicidal, otherwise False.
        """
        board_after_my_move = self._simulate_move(board, col, channel=0)
        valid_moves = self._get_valid_moves(board_after_my_move)
        for opp_col in valid_moves:
            board_after_opp = self._simulate_move(board_after_my_move, opp_col, channel=1)
            if self._check_win(board_after_opp, 1):
                #logger.info(f"[Suicidal] Action {col} is suicidal! Opponent wins by {opp_col}")
                return True
        return False

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
          - Double threat: +2000 (once)

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
        s_three = my_three * 200 - opp_three * 50
        score += s_three

        # Count 2-in-a-row patterns
        my_two = self._count_two_in_row(board, 0)
        opp_two = self._count_two_in_row(board, 1)
        s_two = my_two * 20 - opp_two * 10
        score += s_two

        # Prefer center positions
        #score += self._count_pieces_in_column(board, 0, 3) * 30
        #score += self._count_pieces_in_column(board, 0, 2) * 20
        #score += self._count_pieces_in_column(board, 0, 4) * 20
        #score += self._count_pieces_in_column(board, 0, 0) * 10
        #score += self._count_pieces_in_column(board, 0, 1) * 10
        #score += self._count_pieces_in_column(board, 0, 5) * 10
        #score += self._count_pieces_in_column(board, 0, 6) * 10

        for r in range(6):
            for c in range(7):
                if board[r, c, 0] == 1:
                    score += self.POSITION_WEIGHTS[r, c]
                elif board[r, c, 1] == 1:
                    score -= self.POSITION_WEIGHTS[r, c]

        # Double threat
        for col in self._get_valid_moves(board):
            if self._creates_double_threat(board, col, channel=0):
                score += 2000
                break

        return score

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
            new_board = self._simulate_move(board, col, channel=channel)
            if self._check_win(new_board, channel):
                return col
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
    
    def _adaptive_depth(self, board):
        """
        Adjust the search depth based on how many empty cells remain.
        Deeper search in late-game, shallower in early-game.

        Returns:
            int: The adapted search depth.
        """
        empty = np.sum((board[:, :, 0] == 0) & (board[:, :, 1] == 0))
        if empty <= 8:
            return self.depth + 2
        elif empty <= 14:
            return self.depth + 1
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

