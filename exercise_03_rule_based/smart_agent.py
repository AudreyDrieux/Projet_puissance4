"""
My Smart Agent for Connect Four

This agent uses rule-based heuristics to play strategically.
"""

import random


class SmartAgent:
    """
    A rule-based agent that plays strategically
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the smart agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "SmartAgent"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose an action using rule-based strategy

        Strategy priority:
        1. Win if possible
        2. Block opponent from winning
        3. Avoid a column that would give 
           a chance for the opponent to win
        4. Create double threat
        5. Block double threat from opponent
        6. Prefer center columns if available
        7. Random valid move
        """
        # Get valid actions
        valid_actions = self._get_valid_actions(action_mask)

        # Rule 1: Try to win
        winning_move = self._find_winning_move(observation, valid_actions, channel=0)
        if winning_move is not None:
            return winning_move

        # Rule 2: Block opponent
        blocking_move = self._find_winning_move(observation, valid_actions, channel=1)
        if blocking_move is not None:
            return blocking_move
        
        # Rule 3: avoid a column that would give a chance for the opponent to win
        blocking_threat = self._find_threat(observation, valid_actions, channel=1)
        if blocking_threat is not None:
            col_to_pick = []
            for forbidden_col in blocking_threat:
                for col in valid_actions:
                    if col != forbidden_col:
                        col_to_pick.append(col)
            return random.choice(col_to_pick) 
        
        # Rule 4: Create double threat
        create_double_threat = self._find_double_threat(observation, valid_actions, channel=0)
        if create_double_threat is not None:
            return random.choice(create_double_threat)
        
        # Rule 5: Block double threat from opponent
        blocking_double_threat = self._find_double_threat(observation, valid_actions, channel=1)
        if blocking_double_threat is not None:
            return random.choice(blocking_double_threat) 
        
        # Rule 6: Prefer center columns
        center_preference = [3, 2, 4, 1, 5]
        for col in center_preference:
            if col in valid_actions:
                return col

        # Rule 7: Random fallback
        return random.choice(valid_actions)

    def _get_valid_actions(self, action_mask):
        """
        Get list of valid column indices

        Parameters:
            action_mask: numpy array (7,) with 1 for valid, 0 for invalid

        Returns:
            list of valid column indices
        """
        # TODO: Implement this
        valid_actions = [] 
        nb_column = 7

        for i in range(nb_column):
            if action_mask[i]:
                valid_actions.append(i)

        return valid_actions
        pass

    def _find_winning_move(self, observation, valid_actions, channel):
        """
        Find a move that creates 4 in a row for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if winning move found, None otherwise
        """
        # TODO: For each valid action, check if it would create 4 in a row
        # Hint: Simulate placing the piece, then check for wins
        for col in valid_actions:
            row = self._get_next_row(observation, col)
            win_from_position = self._check_win_from_position(observation,row,col,channel)
            if win_from_position:
                return col
            
        return None
        pass

    def _find_double_threat(self, observation, valid_actions, channel):
        """
        Find a move that creates a double threat for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            list of column indices if several double threat moves found, None otherwise 

        """

        col_double_threat = []
        for col in valid_actions:
            double_threat = self._creates_double_threat(observation, col, channel)
            if double_threat:
                col_double_threat.append(col)

        nb_col_double_threat = len(col_double_threat)
        if nb_col_double_threat != 0:
            return col_double_threat
        
        else:
            return None
    
    def _find_threat(self, observation, valid_actions, channel):
        """
        Find a move that would create a threat for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            list of column indices if several threat moves found, None otherwise

        """

        col_threat = []
        for col in valid_actions:
            threat = self._check_threat_from_position(observation,col,channel)
            if threat:
                col_threat.append(col)
        
        nb_col_threat = len(col_threat)
        if nb_col_threat != 0:
            return col_threat
        
        else:
            return None

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
        for row in range(5,-1,-1):
            if board[row,col,0] == 0 and board[row,col,1] == 0:
                return row
        return None
        pass

    def _check_win_from_position(self, board, row, col, channel):
        """
        Check if placing a piece at (row, col) would create 4 in a row

        Parameters:
            board: numpy array (6, 7, 2)
            row: row index (0-5)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if this position creates 4 in a row/col/diag, False otherwise
        """
        # TODO: Check all 4 directions: horizontal, vertical, diagonal /, diagonal \
        # Hint: Count consecutive pieces in both directions from (row, col)
        row_temp = row
        col_temp = col

        # Vérifier si en plaçant un jeton à la position (row,col) cela crée un alignement vertical de 4 mêmes jetons
        if 0 <= row and row <= 2 and board[row+1,col,channel] and board[row+2,col,channel] and board[row+3,col,channel]:
            return True
        
        # Vérifier si en plaçant un jeton à la position (row,col) cela crée un alignement horizontal de 4 mêmes jetons
        count_tokens_alignhoriz_on_right = 0 # nombre de jetons alignés horizontalement sur la droite
        while col_temp+1 <= 6 and board[row,col_temp+1,channel]:
            count_tokens_alignhoriz_on_right = count_tokens_alignhoriz_on_right + 1
            col_temp = col_temp + 1

        if count_tokens_alignhoriz_on_right >= 3:
            return True
        
        col_temp = col
        count_tokens_alignhoriz_on_left = 0 # nombre de jetons alignés horizontalement sur la gauche 
        while col_temp-1 >= 0 and board[row,col_temp-1,channel]:
            count_tokens_alignhoriz_on_left = count_tokens_alignhoriz_on_left + 1
            col_temp = col_temp - 1

        if count_tokens_alignhoriz_on_left >= 3:
            return True
        
        if count_tokens_alignhoriz_on_right != 0 and count_tokens_alignhoriz_on_left != 0:
            count_tokens_align_horiz = count_tokens_alignhoriz_on_right + count_tokens_alignhoriz_on_left # nombre de jetons alignés horizontalement
            if count_tokens_align_horiz >= 3:
                return True

        # Vérifier si en plaçant un jeton à la position (row,col) cela crée un alignement diagonal de pente positive (/) de 4 mêmes jetons     
        col_temp = col
        count_tokens_align_diagpos_on_right = 0 # nombre de jetons alignés diagonalement sur la droite 
        while row_temp-1 >= 0 and col_temp+1 <= 6 and board[row_temp-1,col_temp+1,channel]:
            count_tokens_align_diagpos_on_right = count_tokens_align_diagpos_on_right + 1
            row_temp = row_temp - 1
            col_temp = col_temp + 1
        
        if count_tokens_align_diagpos_on_right >= 3:
            return True
        
        row_temp = row
        col_temp = col
        count_tokens_align_diagpos_on_left = 0 # nombre de jetons alignés diagonalement sur la gauche
        while row_temp+1 <= 5 and col_temp-1 >= 0 and board[row_temp+1,col_temp-1,channel]:
            count_tokens_align_diagpos_on_left = count_tokens_align_diagpos_on_left + 1
            row_temp = row_temp + 1
            col_temp = col_temp - 1

        if count_tokens_align_diagpos_on_left >= 3:
            return True
        
        if count_tokens_align_diagpos_on_right != 0 and count_tokens_align_diagpos_on_left != 0:
            count_tokens_align_diagpos = count_tokens_align_diagpos_on_right + count_tokens_align_diagpos_on_left # nombre de jetons alignés diagonalement
            if count_tokens_align_diagpos >=3:
                return True
        
        # Vérifier si en plaçant un jeton à la position (row,col) cela crée un alignement diagonal de pente négative (\) de 4 mêmes jetons
        row_temp = row
        col_temp = col
        count_tokens_align_diagneg_on_right = 0 # nombre de jetons alignés diagonalement sur la droite
        while row_temp+1 <= 5 and col_temp+1 <= 6 and board[row_temp+1,col_temp+1,channel]:
            count_tokens_align_diagneg_on_right = count_tokens_align_diagneg_on_right + 1
            row_temp = row_temp + 1
            col_temp = col_temp + 1

        if count_tokens_align_diagneg_on_right >= 3:
            return True

        row_temp = row
        col_temp = col
        count_tokens_align_diagneg_on_left = 0 # nombre de jetons alignés diagonalement sur la gauche 
        while row_temp-1 >= 0 and col_temp-1 >= 0 and board[row_temp-1,col_temp-1,channel]:
            count_tokens_align_diagneg_on_left = count_tokens_align_diagneg_on_left + 1
            row_temp = row_temp - 1
            col_temp = col_temp - 1

        if count_tokens_align_diagneg_on_left >= 3:
            return True

        if count_tokens_align_diagneg_on_right != 0 and count_tokens_align_diagneg_on_left != 0:
            count_tokens_align_diagneg = count_tokens_align_diagneg_on_right + count_tokens_align_diagneg_on_left # nombre de jetons alignés diagonalement
            if count_tokens_align_diagneg >= 3:
                return True

        return False 
        
        pass

    def print_board(self, observation):
        """
        Affiche l'état du plateau du Puissance 4

        Arguments:
            observation : tableau de taille (6,7,2)
            observation[:,:,0] : tableau de taille 6x7 qui indique à l'agent dont 
                                 c'est le tour de jouer où sont ses pièces
            observation[:,:,1] : tableau de taille 6x7 qui indique à l'agent dont
                                 c'est le tour de jouer où sont les pièces de l'adversaire
        """

        nb_row = 6
        nb_column = 7

        for r in range(nb_row):
            for c in range(nb_column):
                if observation[r,c,0] != 0:
                    print('X', end = " ")
                
                elif observation[r,c,1] != 0:
                    print('O', end = " ")

                else:
                    print('.', end = " ")

            print("\n")

        pass

    def _creates_double_threat(self, board, col, channel):
        """
        Check if playing column col creates two separate winning threats

        A double threat is unbeatable because opponent can only block one.

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if move creates double threat, False otherwise
        """
        # TODO: This is advanced - implement if you have time
        # Hint: After placing piece, count how many ways you can win next turn

        col_temp = col
        row = self._get_next_row(board, col)

        # Check if playing column col creates two separate winning threats horizontally
        count_tokens_alignhoriz_on_right = 0 # nombre de jetons alignés horizontalement sur la droite
        while col_temp+1 <= 6 and board[row,col_temp+1,channel]:
            count_tokens_alignhoriz_on_right = count_tokens_alignhoriz_on_right + 1
            col_temp = col_temp + 1

        if count_tokens_alignhoriz_on_right == 2 and 1 <= col and col <= 3:
            if board[row,col-1,0] == 0 and board[row,col-1,1] == 0 and board[row,col+3,0] == 0 and board[row,col+3,1] == 0:
                if row == 5:
                    return True
                elif (board[row+1,col-1,0] or board[row+1,col-1,1]) and (board[row+1,col+3,0] or board[row+1,col+3,1]):
                    return True
            
        col_temp = col
        count_tokens_alignhoriz_on_left = 0 # nombre de jetons alignés horizontalement sur la gauche
        while col_temp-1 >= 0 and board[row,col_temp-1,channel]:
            count_tokens_alignhoriz_on_left = count_tokens_alignhoriz_on_left + 1
            col_temp = col_temp - 1
        
        if count_tokens_alignhoriz_on_left == 2 and 3 <= col and col <= 5:
            if board[row,col-3,0] == 0 and board[row,col-3,1] == 0 and board[row,col+1,0] == 0 and board[row,col+1,1] == 0:
                if row == 5:
                    return True
                elif (board[row+1,col-3,0] or board[row+1,col-3,1]) and (board[row+1,col+1,0] or board[row+1,col+1,1]):
                    return True
            
        if count_tokens_alignhoriz_on_right == 1 and count_tokens_alignhoriz_on_left == 1 and 2 <= col and col <= 4:
              if board[row,col-2,0] == 0 and board[row,col-2,1] == 0 and board[row,col+2,0] == 0 and board[row,col+2,1] == 0:
                  if row == 5:
                      return True
                  elif (board[row+1,col-2,0] or board[row+1,col-2,1]) and (board[row+1,col+2,0] or board[row+1,col+2,1]):
                      return True

        # Check if playing column col creates two separate winning threats diagonally /            
        col_temp = col
        row_temp = row
        count_tokens_align_diagpos_on_right = 0 # nombre de jetons alignés diagonalement sur la droite
        while row_temp-1 >= 0 and col_temp+1 <= 6 and board[row_temp-1,col_temp+1,channel]:
            count_tokens_align_diagpos_on_right = count_tokens_align_diagpos_on_right + 1
            row_temp = row_temp - 1
            col_temp = col_temp + 1

        if count_tokens_align_diagpos_on_right == 2 and 3 <= row and row <= 4 and 1 <= col and col <= 3:
              if board[row+1,col-1,0] == 0 and board[row+1,col-1,1] == 0 and board[row-3,col+3,0] == 0 and board[row-3,col+3,1] == 0:
                  if row == 4 and (board[2,col+3,0] or board[2,col+3,1]):
                      return True
                  elif (board[5,col-1,0] or board[5,col-1,1]) and (board[1,col+3,0] or board[1,col+3,1]):
                      return True
              
        col_temp = col
        row_temp = row
        count_tokens_align_diagpos_on_left = 0 # nombre de jetons alignés diagonalement sur la gauche 
        while row_temp+1 <= 5 and col_temp-1 >= 0 and board[row_temp+1,col_temp-1,channel]:
            count_tokens_align_diagpos_on_left = count_tokens_align_diagpos_on_left + 1
            row_temp = row_temp + 1
            col_temp = col_temp - 1

        if count_tokens_align_diagpos_on_left == 2 and 1 <= row and row <= 2 and 3 <= col and col <= 5:
              if board[row+3,col-3,0] == 0 and board[row+3,col-3,1] == 0 and board[row-1,col+1,0] == 0 and board[row-1,col+1,1] == 0:
                  if row == 2 and (board[2,col+1,0] or board[2,col+1,1]):
                      return True
                  elif (board[5,col-3,0] or board[5,col-3,1]) and (board[1,col+1,0] or board[1,col+1,1]):
                      return True
              
        if count_tokens_align_diagpos_on_right == 1 and count_tokens_align_diagpos_on_left == 1 and 2 <= row and row <= 3 and 2 <= col and col <= 4:
              if board[row-2,col+2,0] == 0 and board[row-2,col+2,1] == 0 and board[row+2,col-2,0] == 0 and board[row+2,col-2,1] == 0:
                  if row == 3 and (board[2,col+2,0] or board[2,col+2,1]):
                      return True
                  elif (board[5,col-2,0] or board[5,col-2,1]) and (board[1,col+2,0] or board[1,col+2,1]):
                      return True

        # Check if playing column col creates two separate winning threats diagonally \
        col_temp = col
        row_temp = row
        count_tokens_align_diagneg_on_right = 0 # nombre de jetons alignés diagonalement sur la droite 
        while row_temp+1 <= 5 and col_temp+1 <= 6 and board[row_temp+1,col_temp+1,channel]:
            count_tokens_align_diagneg_on_right = count_tokens_align_diagneg_on_right + 1
            row_temp = row_temp + 1
            col_temp = col_temp + 1

        if count_tokens_align_diagneg_on_right == 2 and 1 <= row and row <= 2 and 1 <= col and col <= 3:
              if board[row-1,col-1,0] == 0 and board[row-1,col-1,1] == 0 and board[row+3,col+3,0] == 0 and board[row+3,col+3,1] == 0:
                  if row == 2 and (board[2,col-1,0] or board[2,col-1,1]):
                      return True
                  elif (board[1,col-1,0] or board[1,col-1,1]) and (board[5,col+3,0] or board[5,col+3,1]):
                      return True

        col_temp = col 
        row_temp = row
        count_tokens_align_diagneg_on_left = 0 # nombre de jetons alignés diagonalement sur la gauche
        while row_temp-1 >= 0 and col_temp-1 >=0 and board[row_temp-1,col_temp-1,channel]:
            count_tokens_align_diagneg_on_left = count_tokens_align_diagneg_on_left + 1
            row_temp = row_temp - 1
            col_temp = col_temp - 1

        if count_tokens_align_diagneg_on_left == 2 and 3 <= row and row <= 4 and 3 <= col and col <= 5:
             if board[row+1,col+1,0] == 0 and board[row+1,col+1,1] == 0 and board[row-3,col-3,0] == 0 and board[row-3,col-3,1] == 0:
                 if row == 4 and (board[2,col-3,0] or board[2,col-3,1]):
                     return True
                 elif (board[5,col+1,0] or board[5,col+1,1]) and (board[1,col-3,0] or board[1,col-3,1]):
                     return True
             
        if count_tokens_align_diagneg_on_right == 1 and count_tokens_align_diagneg_on_left == 1 and 2 <= row and row <= 3 and 2 <= col and col <= 4:
             if board[row-2,col-2,0] == 0 and board[row-2,col-2,1] == 0 and board[row+2,col+2,0] == 0 and board[row+2,col+2,1] == 0:
                 if row == 3 and (board[2,col-2,0] or board[2,col-2,1]):
                     return True
                 elif (board[1,col-2,0] or board[1,col-2,1]) and (board[5,col+2,0] or board[5,col+2,1]):
                     return True
                 
        return False
    
    pass

    def _check_threat_from_position(self, board, col, channel):
        """
        Check if playing column col creates a winning threat

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if move creates a threat, False otherwise
        """

        row = self._get_next_row(board, col)
        col_temp = col

        # Vérifier si en plaçant un jeton à la position (row,col) cela donne la possibilité à l'adversaire de créer
        # un alignement horizontale de 4 jetons à son prochain tour
        count_tokens_alignhoriz_on_right = 0 # nombre de jetons alignés horizontalement sur la droite 
        while col_temp+1 <= 6 and board[row-1,col_temp+1,channel]:
            count_tokens_alignhoriz_on_right = count_tokens_alignhoriz_on_right + 1
            col_temp = col_temp + 1

        if count_tokens_alignhoriz_on_right >= 3:
            return True
        
        col_temp = col
        count_tokens_alignhoriz_on_left = 0 # nombre de jetons alignés horizontalement sur la gauche 
        while col_temp-1 >= 0 and board[row-1,col_temp-1,channel]:
            count_tokens_alignhoriz_on_left = count_tokens_alignhoriz_on_left + 1
            col_temp = col_temp - 1

        if count_tokens_alignhoriz_on_left >= 3:
            return True
        
        if count_tokens_alignhoriz_on_right != 0 and count_tokens_alignhoriz_on_left != 0:
            count_tokens_align_horiz = count_tokens_alignhoriz_on_right + count_tokens_alignhoriz_on_left # nombre de jetons alignés horizontalement 
            if count_tokens_align_horiz >= 3:
                return True

        # Vérifier si en plaçant un jeton à la position (row,col) cela donne la possibilité à l'adversaire de créer 
        # un alignement diagonale à pente positive de 4 jetons à son prochain tour   
        row_temp = row-1
        col_temp = col
        count_tokens_align_diagpos_on_right = 0 # nombre de jetons alignés diagonalement sur la droite 
        while row_temp-1 >= 0 and col_temp+1 <= 6 and board[row_temp-1,col_temp+1,channel]:
            count_tokens_align_diagpos_on_right = count_tokens_align_diagpos_on_right + 1
            row_temp = row_temp - 1
            col_temp = col_temp + 1

        if count_tokens_align_diagpos_on_right >= 3:
            return True
        
        row_temp = row-1
        col_temp = col
        count_tokens_align_diagpos_on_left = 0 # nombre de jetons alignés diagonalement sur la gauche 
        while row_temp+1 <= 5 and col_temp-1 >= 0 and board[row_temp+1,col_temp-1,channel]:
            count_tokens_align_diagpos_on_left = count_tokens_align_diagpos_on_left + 1
            row_temp = row_temp + 1
            col_temp = col_temp - 1

        if count_tokens_align_diagpos_on_left >= 3:
            return True
        
        if count_tokens_align_diagpos_on_right != 0 and count_tokens_align_diagpos_on_left != 0:
            count_tokens_align_diagpos = count_tokens_align_diagpos_on_right + count_tokens_align_diagpos_on_left # nombre de jetons alignés diagonalement 
            if count_tokens_align_diagpos >= 3:
                return True

        # Vérifier si en plaçant un jeton à la position (row,col) cela donne la possibilité à l'adversaire de créer
        # un alignement diagonale à pente négative de 4 jetons à son prochain tour    
        row_temp = row-1
        col_temp = col
        count_tokens_align_diagneg_on_right = 0 # nombre de jetons alignés diagonalement sur la droite 
        while row_temp+1 <= 5 and col_temp+1 <= 6 and board[row_temp+1,col_temp+1,channel]:
            count_tokens_align_diagneg_on_right = count_tokens_align_diagneg_on_right + 1
            row_temp = row_temp + 1
            col_temp = col_temp + 1

        if count_tokens_align_diagneg_on_right >= 3:
            return True
        
        row_temp = row-1
        col_temp = col
        count_tokens_align_diagneg_on_left = 0 # nombre de jetons alignés diagonalement sur la gauche 
        while row_temp-1 >= 0 and col_temp-1 >= 0 and board[row_temp-1,col_temp-1,channel]:
            count_tokens_align_diagneg_on_left = count_tokens_align_diagneg_on_left + 1
            row_temp = row_temp - 1
            col_temp = col_temp - 1

        if count_tokens_align_diagneg_on_left >= 3:
            return True
        
        if count_tokens_align_diagneg_on_right != 0 and count_tokens_align_diagneg_on_left != 0:
            count_tokens_align_diagneg = count_tokens_align_diagneg_on_right + count_tokens_align_diagneg_on_left # nombre de jetons alignés diagonalement 
            if count_tokens_align_diagneg >= 3:
                return True
            
        return False
    

    

        
            

